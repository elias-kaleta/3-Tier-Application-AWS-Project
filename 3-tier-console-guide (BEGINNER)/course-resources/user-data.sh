#!/bin/bash
set -euxo pipefail

ASSET_BUCKET="<YOUR_ASSET_BUCKET>"
MASTER_SECRET_ARN="<YOUR_RDS_MASTER_SECRET_ARN>"
RUNTIME_SECRET_ARN="<YOUR_RUNTIME_SECRET_ARN>"
AWS_REGION="<YOUR_REGION_CODE>"

exec > >(tee /var/log/user-data.log | logger -t user-data -s 2>/dev/console) 2>&1

dnf update -y
dnf install -y python3 python3-pip amazon-cloudwatch-agent

id tickethub >/dev/null 2>&1 || useradd --system --home /opt/tickethub --shell /sbin/nologin tickethub
mkdir -p /opt/tickethub
aws s3 cp "s3://${ASSET_BUCKET}/ticket-booking/app.py" /opt/tickethub/app.py
aws s3 cp "s3://${ASSET_BUCKET}/ticket-booking/index.html" /opt/tickethub/index.html
aws s3 cp "s3://${ASSET_BUCKET}/ticket-booking/requirements.txt" /opt/tickethub/requirements.txt
curl --fail --silent --show-error \
  https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem \
  --output /opt/tickethub/global-bundle.pem

python3 -m venv /opt/tickethub/venv
/opt/tickethub/venv/bin/pip install --no-cache-dir -r /opt/tickethub/requirements.txt

cat > /opt/tickethub/bootstrap.py <<'PYTHON'
import json
import os
import sys

import boto3
import pymysql

region = os.environ["AWS_REGION"]
runtime_arn = os.environ["RUNTIME_SECRET_ARN"]
master_arn = os.environ["MASTER_SECRET_ARN"]
ca_bundle = "/opt/tickethub/global-bundle.pem"
client = boto3.client("secretsmanager", region_name=region)


def read_secret(secret_arn):
    value = client.get_secret_value(SecretId=secret_arn)
    return json.loads(value["SecretString"])


def connect(credentials, database="appdb"):
    return pymysql.connect(
        host=credentials["host"],
        port=int(credentials.get("port", 3306)),
        user=credentials["username"],
        password=credentials["password"],
        database=database,
        ssl={"ca": ca_bundle, "check_hostname": True},
        connect_timeout=5,
    )


runtime = read_secret(runtime_arn)
if runtime["username"] != "tickethub_app":
    raise ValueError("Runtime secret username must be tickethub_app")

try:
    connection = connect(runtime)
except pymysql.err.OperationalError as error:
    if not error.args or error.args[0] != 1045:
        raise
    print("MySQL denied runtime user authentication; performing one-time bootstrap")
else:
    connection.close()
    print("Runtime database user already exists")
    sys.exit(0)

master = read_secret(master_arn)
connection = connect(master, database="mysql")
try:
    with connection.cursor() as cursor:
        cursor.execute(
            "CREATE USER IF NOT EXISTS 'tickethub_app'@'10.%' IDENTIFIED BY %s",
            (runtime["password"],),
        )
        cursor.execute(
            "ALTER USER 'tickethub_app'@'10.%' IDENTIFIED BY %s",
            (runtime["password"],),
        )
        cursor.execute(
            "GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, ALTER, INDEX, "
            "REFERENCES ON appdb.* TO 'tickethub_app'@'10.%'"
        )
    connection.commit()
finally:
    connection.close()
print("Runtime database user created with appdb-scoped permissions")
PYTHON

cat > /opt/tickethub/run.py <<'PYTHON'
import json
import os

import boto3

secret = boto3.client(
    "secretsmanager",
    region_name=os.environ["AWS_REGION"],
).get_secret_value(SecretId=os.environ["RUNTIME_SECRET_ARN"])
credentials = json.loads(secret["SecretString"])
os.environ["DB_HOST"] = credentials["host"]
os.environ["DB_PORT"] = str(credentials.get("port", 3306))
os.environ["DB_USER"] = credentials["username"]
os.environ["DB_PASS"] = credentials["password"]
os.environ["DB_NAME"] = credentials.get("dbname", "appdb")
os.environ["RDS_CA_BUNDLE"] = "/opt/tickethub/global-bundle.pem"

os.execv(
    "/opt/tickethub/venv/bin/gunicorn",
    [
        "gunicorn",
        "--bind", "0.0.0.0:5000",
        "--workers", "1",
        "--threads", "4",
        "--access-logfile", "-",
        "--error-logfile", "-",
        "app:app",
    ],
)
PYTHON

export MASTER_SECRET_ARN RUNTIME_SECRET_ARN AWS_REGION
/opt/tickethub/venv/bin/python /opt/tickethub/bootstrap.py

chown -R tickethub:tickethub /opt/tickethub
chmod 750 /opt/tickethub
chmod 640 /opt/tickethub/global-bundle.pem

cat > /etc/systemd/system/tickethub.service <<EOF
[Unit]
Description=TicketHub application
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=tickethub
Group=tickethub
WorkingDirectory=/opt/tickethub
Environment=AWS_REGION=${AWS_REGION}
Environment=RUNTIME_SECRET_ARN=${RUNTIME_SECRET_ARN}
ExecStart=/opt/tickethub/venv/bin/python /opt/tickethub/run.py
Restart=always
RestartSec=5
StandardOutput=append:/var/log/tickethub.log
StandardError=append:/var/log/tickethub.log

[Install]
WantedBy=multi-user.target
EOF

cat > /opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json <<EOF
{
  "agent": {"metrics_collection_interval": 60},
  "logs": {
    "logs_collected": {
      "files": {
        "collect_list": [
          {
            "file_path": "/var/log/tickethub.log",
            "log_group_name": "/3tier-app/application",
            "log_stream_name": "{instance_id}",
            "retention_in_days": 7
          },
          {
            "file_path": "/var/log/user-data.log",
            "log_group_name": "/3tier-app/user-data",
            "log_stream_name": "{instance_id}",
            "retention_in_days": 7
          }
        ]
      }
    }
  }
}
EOF

systemctl daemon-reload
systemctl enable --now tickethub
/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
  -a fetch-config -m ec2 \
  -c file:/opt/aws/amazon-cloudwatch-agent/etc/amazon-cloudwatch-agent.json -s
