#!/usr/bin/env python3
"""TicketHub teaching application for the AWS three-tier console course."""

import logging
import os
import re
from datetime import datetime

import pymysql
from flask import Flask, jsonify, request, send_from_directory

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder=".")

DB_CONFIG = {
    "host": os.environ["DB_HOST"],
    "user": os.environ["DB_USER"],
    "password": os.environ["DB_PASS"],
    "database": os.getenv("DB_NAME", "appdb"),
    "port": int(os.getenv("DB_PORT", "3306")),
    "cursorclass": pymysql.cursors.DictCursor,
    "connect_timeout": 5,
    "read_timeout": 10,
    "write_timeout": 10,
    "ssl": {
        "ca": os.environ["RDS_CA_BUNDLE"],
        "check_hostname": True,
    },
}


def get_db_connection():
    return pymysql.connect(**DB_CONFIG)


def init_database():
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    category VARCHAR(50) NOT NULL,
                    event_date DATETIME NOT NULL,
                    location VARCHAR(255) NOT NULL,
                    price DECIMAL(10,2) NOT NULL,
                    available_tickets INT NOT NULL,
                    total_tickets INT NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    event_id INT NOT NULL,
                    customer_name VARCHAR(120) NOT NULL,
                    customer_email VARCHAR(254) NOT NULL,
                    quantity INT NOT NULL,
                    total_price DECIMAL(10,2) NOT NULL,
                    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (event_id) REFERENCES events(id)
                )
                """
            )
            cursor.execute("SELECT COUNT(*) AS count FROM events")
            if cursor.fetchone()["count"] == 0:
                cursor.executemany(
                    """
                    INSERT INTO events
                        (name, category, event_date, location, price,
                         available_tickets, total_tickets, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    [
                        (
                            "Summer Music Festival",
                            "Concert",
                            "2026-07-15 19:00:00",
                            "Central Park Amphitheater",
                            79.99,
                            500,
                            500,
                            "Outdoor music festival featuring top artists",
                        ),
                        (
                            "Tech Conference 2026",
                            "Conference",
                            "2026-09-20 09:00:00",
                            "Convention Center",
                            199.99,
                            300,
                            300,
                            "Technology conference with industry speakers",
                        ),
                        (
                            "Soccer Championship",
                            "Sports",
                            "2026-08-05 18:00:00",
                            "National Stadium",
                            65.00,
                            1000,
                            1000,
                            "Championship match",
                        ),
                    ],
                )
        connection.commit()
        logger.info("Database schema is ready")
    except Exception:
        logger.exception("Database initialization failed")
        raise
    finally:
        if connection:
            connection.close()


init_database()


@app.get("/")
def index():
    return send_from_directory(".", "index.html")


@app.get("/health")
def health():
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        connection.close()
        return jsonify(
            status="healthy",
            database="connected",
            timestamp=datetime.now().isoformat(),
        )
    except Exception:
        logger.exception("Health check failed")
        return jsonify(status="unhealthy"), 500


@app.get("/api/events")
def get_events():
    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, name, category, event_date, location, price,
                       available_tickets, total_tickets, description
                FROM events
                WHERE available_tickets > 0
                ORDER BY event_date ASC
                """
            )
            events = cursor.fetchall()
        for event in events:
            if isinstance(event["event_date"], datetime):
                event["event_date"] = event["event_date"].isoformat()
        return jsonify(events)
    except Exception:
        logger.exception("Failed to list events")
        return jsonify(error="Unable to load events"), 500
    finally:
        if connection:
            connection.close()


@app.post("/api/bookings")
def create_booking():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify(error="Invalid request body"), 400

    required = ("event_id", "customer_name", "customer_email", "quantity")
    if any(field not in data for field in required):
        return jsonify(error="Missing a required booking field"), 400

    customer_name = str(data["customer_name"]).strip()
    customer_email = str(data["customer_email"]).strip().lower()
    if not customer_name or len(customer_name) > 120:
        return jsonify(error="Enter a valid name"), 400
    if len(customer_email) > 254 or not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", customer_email):
        return jsonify(error="Enter a valid email address"), 400

    try:
        event_id = int(data["event_id"])
        quantity = int(data["quantity"])
    except (TypeError, ValueError):
        return jsonify(error="Event and quantity must be numbers"), 400
    if quantity < 1 or quantity > 10:
        return jsonify(error="Quantity must be between 1 and 10"), 400

    connection = None
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT available_tickets, price, name
                FROM events
                WHERE id = %s
                FOR UPDATE
                """,
                (event_id,),
            )
            event = cursor.fetchone()
            if not event:
                connection.rollback()
                return jsonify(error="Event not found"), 404
            if event["available_tickets"] < quantity:
                connection.rollback()
                return jsonify(error="Not enough tickets are available"), 400

            total_price = float(event["price"]) * quantity
            cursor.execute(
                """
                INSERT INTO bookings
                    (event_id, customer_name, customer_email, quantity, total_price)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (event_id, customer_name, customer_email, quantity, total_price),
            )
            booking_id = cursor.lastrowid
            cursor.execute(
                """
                UPDATE events
                SET available_tickets = available_tickets - %s
                WHERE id = %s
                """,
                (quantity, event_id),
            )
        connection.commit()
        return (
            jsonify(
                message="Booking created successfully",
                booking_id=booking_id,
                event_name=event["name"],
                quantity=quantity,
                total_price=total_price,
            ),
            201,
        )
    except Exception:
        if connection:
            connection.rollback()
        logger.exception("Failed to create booking")
        return jsonify(error="Unable to create booking"), 500
    finally:
        if connection:
            connection.close()


@app.errorhandler(404)
def not_found(_error):
    return jsonify(error="Not found"), 404


@app.errorhandler(500)
def internal_error(_error):
    return jsonify(error="Internal server error"), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")), debug=False)
