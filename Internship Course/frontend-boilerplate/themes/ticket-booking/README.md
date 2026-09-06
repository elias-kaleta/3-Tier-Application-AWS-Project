# Ticket Booking System Theme

A complete event ticket booking system for concerts, sports, theater, and more!

---

## Features

✅ Browse events by category  
✅ Search events by name/location  
✅ Real-time ticket availability  
✅ Simple booking process  
✅ Responsive design  
✅ Database-backed inventory  

---

## Database Schema

### Events Table
```sql
- id (Primary Key)
- name (Event name)
- category (concert, sports, theater, comedy, conference)
- event_date (Date and time)
- location (Venue)
- price (Ticket price)
- available_tickets (Current availability)
- total_tickets (Total capacity)
- description (Event details)
```

### Bookings Table
```sql
- id (Primary Key)
- event_id (Foreign Key to events)
- customer_name
- customer_email
- quantity (Number of tickets)
- total_price
- booking_date
```

---

## API Endpoints

```
GET  /                     # Homepage
GET  /health               # Health check
GET  /api/events           # List all events
GET  /api/events/<id>      # Get single event
POST /api/bookings         # Create booking
GET  /api/bookings/<id>    # Get booking details
GET  /api/stats            # System statistics
```

---

## Sample Data Included

8 sample events:
- Summer Music Festival (Concert)
- Tech Conference 2026
- Comedy Night Live
- Soccer Championship (Sports)
- Broadway Musical (Theater)
- Jazz Evening
- Basketball Finals
- Classical Orchestra

---

## Customization Ideas

### Easy Changes
1. **Change event types**: Edit `category` field
   - concerts → festivals
   - sports → esports
   - theater → cinema

2. **Update colors**: Modify CSS gradient
   ```css
   background: linear-gradient(135deg, #YOUR_COLOR 0%, #YOUR_COLOR 100%);
   ```

3. **Change icons**: Update `getEventIcon()` function
   ```javascript
   const icons = {
       'your_category': '🎸'
   };
   ```

### Medium Changes
1. **Add seat selection**: Include seat numbers
2. **Add event images**: Upload to S3, add image URLs
3. **Add payment integration**: Stripe/PayPal API
4. **Add user accounts**: Login/registration system

### Advanced Changes
1. **Add QR code tickets**: Generate unique codes
2. **Add email notifications**: AWS SES integration
3. **Add refund system**: Cancel bookings
4. **Add admin panel**: Manage events

---

## Local Development

### Prerequisites
- Python 3.8+
- MySQL 8.0+
- pip

### Setup

1. **Install dependencies**:
```bash
pip install flask pymysql
```

2. **Set up MySQL database**:
```bash
mysql -u root -p
CREATE DATABASE appdb;
```

3. **Set environment variables**:
```bash
export DB_HOST=localhost
export DB_USER=root
export DB_PASS=your_password
export DB_NAME=appdb
export PORT=5000
```

4. **Run the application**:
```bash
python app.py
```

5. **Open browser**:
```
http://localhost:5000
```

---

## AWS Deployment

### Method 1: Via EC2 User Data

When creating EC2 instances in Guide 03, use this user data script:

```bash
#!/bin/bash
yum update -y
yum install -y python3 python3-pip git

# Install dependencies
pip3 install flask pymysql boto3

# Create app directory
mkdir -p /opt/tickethub
cd /opt/tickethub

# Download application files
# (Upload index.html and app.py to S3 first)
aws s3 cp s3://your-bucket/ticket-booking/index.html .
aws s3 cp s3://your-bucket/ticket-booking/app.py .

# Set environment variables (replace with your RDS endpoint)
cat > /etc/environment << EOF
DB_HOST=your-rds-endpoint.rds.amazonaws.com
DB_USER=admin
DB_PASS=your-password
DB_NAME=appdb
PORT=80
EOF

# Start application
source /etc/environment
nohup python3 app.py > /var/log/app.log 2>&1 &
```

### Method 2: Manual Upload

1. **SSH to EC2** (via Session Manager):
```bash
sudo su
cd /opt
```

2. **Upload files**:
```bash
# Create directory
mkdir tickethub
cd tickethub

# Copy files (use SCP or paste content)
nano index.html  # Paste HTML content
nano app.py      # Paste Python content
```

3. **Install and run**:
```bash
yum install -y python3-pip
pip3 install flask pymysql boto3

export DB_HOST=your-rds-endpoint.rds.amazonaws.com
export DB_USER=admin
export DB_PASS=your_password
export DB_NAME=appdb

python3 app.py
```

---

## Environment Variables

Set these before running:

```bash
DB_HOST      # RDS endpoint (from Guide 02)
DB_USER      # Database username (default: admin)
DB_PASS      # Database password (from Guide 02)
DB_NAME      # Database name (default: appdb)
PORT         # Application port (80 for production, 5000 for local)
```

---

## Testing

### 1. Health Check
```bash
curl http://localhost:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2026-09-02T..."
}
```

### 2. Get Events
```bash
curl http://localhost:5000/api/events
```

### 3. Create Booking
```bash
curl -X POST http://localhost:5000/api/bookings \
  -H "Content-Type: application/json" \
  -d '{
    "event_id": 1,
    "customer_name": "John Doe",
    "customer_email": "john@example.com",
    "quantity": 2
  }'
```

### 4. Get Statistics
```bash
curl http://localhost:5000/api/stats
```

---

## Troubleshooting

### Can't Connect to Database
- ✅ Check RDS security group allows port 3306 from EC2
- ✅ Verify RDS endpoint is correct
- ✅ Check database username/password
- ✅ Ensure database `appdb` exists

### Application Won't Start
- ✅ Check Python is installed: `python3 --version`
- ✅ Check dependencies: `pip3 list | grep flask`
- ✅ Check port 80 is available: `sudo netstat -tlnp | grep :80`
- ✅ Check logs: `tail -f /var/log/app.log`

### No Events Showing
- ✅ Check browser console for errors (F12)
- ✅ Verify `/api/events` endpoint works
- ✅ Check database has sample data
- ✅ Look for CORS issues

### Bookings Not Working
- ✅ Check form validation (all fields filled)
- ✅ Verify enough tickets available
- ✅ Check browser console for errors
- ✅ Test API directly with curl

---

## Production Enhancements

### Security
- [ ] Add HTTPS (CloudFront handles this)
- [ ] Add rate limiting
- [ ] Add input sanitization
- [ ] Add CSRF protection
- [ ] Add user authentication

### Features
- [ ] Email confirmations (AWS SES)
- [ ] PDF ticket generation
- [ ] QR code scanning
- [ ] Admin dashboard
- [ ] Reviews and ratings
- [ ] Seat map selection
- [ ] Multiple ticket types (VIP, standard)

### Performance
- [ ] Add caching (ElastiCache)
- [ ] Optimize database queries
- [ ] Add CDN for static assets
- [ ] Enable connection pooling
- [ ] Add database indexes

---

## Cost Estimate

Running this theme:
- **EC2**: Covered in main guide (~$15/month)
- **RDS**: Covered in main guide (~$30/month)
- **Additional**: $0 (no extra services)

Total: Same as base 3-tier architecture

---

## Support

For issues specific to this theme:
1. Check the troubleshooting section above
2. Review Flask documentation: https://flask.palletsprojects.com/
3. Check MySQL documentation: https://dev.mysql.com/doc/
4. Ask your instructor during lab sessions

---

## Next Steps

1. ✅ Deploy the base infrastructure (Guides 01-02)
2. ✅ Upload these files to your EC2 instances
3. ✅ Test locally first (optional)
4. ✅ Customize the design (colors, text, images)
5. ✅ Add your own features
6. ✅ Present your project!

Good luck with your ticket booking system! 🎫
