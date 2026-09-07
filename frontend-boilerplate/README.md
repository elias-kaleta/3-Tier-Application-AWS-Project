# Frontend Boilerplate for 3-Tier Application

A simple, customizable web application frontend that connects to your backend API. Choose from multiple themes or create your own!

---

## Available Themes

1. **Ticket Booking System** - Concert/Event tickets
2. **Gaming Platform** - Game library management
3. **Veterinary Clinic** - Pet appointment booking
4. **Hospital Booking** - Doctor appointment system
5. **Restaurant Reservation** - Table booking system

Each theme includes:
- HTML frontend with modern design
- Python Flask backend API
- MySQL database schema
- Sample data

---

## Project Structure

```
frontend-boilerplate/
├── README.md                    # This file
├── themes/
│   ├── ticket-booking/         # Concert/event tickets
│   ├── gaming-platform/        # Game library
│   ├── veterinary/             # Pet appointments
│   ├── hospital/               # Doctor appointments
│   └── restaurant/             # Table reservations
├── shared/
│   ├── app.py                  # Flask backend (common)
│   ├── database.sql            # Database schema
│   └── static/
│       ├── css/
│       │   └── shared.css      # Shared styles
│       └── js/
│           └── api.js          # API client
└── deployment/
    ├── user-data.sh            # EC2 startup script
    └── nginx.conf              # Web server config
```

---

## How to Use

### Step 1: Choose Your Theme

Pick one theme folder that matches your team's project idea:
- Event ticketing → `ticket-booking/`
- Game management → `gaming-platform/`
- Pet clinic → `veterinary/`
- Medical appointments → `hospital/`
- Restaurant booking → `restaurant/`

### Step 2: Customize

Each theme folder contains:
- `index.html` - Homepage
- `app.py` - Backend API
- `schema.sql` - Database tables
- `README.md` - Theme-specific guide

Modify the HTML/CSS to match your vision!

### Step 3: Deploy

Follow the deployment guide in each theme folder.

---

## Technology Stack

### Frontend
- HTML5
- CSS3 (modern, responsive)
- Vanilla JavaScript (no frameworks)
- Bootstrap 5 (optional)

### Backend
- Python 3
- Flask web framework
- PyMySQL (database connector)
- Boto3 (AWS SDK)

### Database
- MySQL 8.0
- Simple schema (1-3 tables)
- Sample data included

---

## Features (All Themes)

✅ Responsive design (mobile-friendly)  
✅ REST API backend  
✅ Database connection  
✅ CRUD operations (Create, Read, Update, Delete)  
✅ Health check endpoint  
✅ Error handling  
✅ AWS RDS integration  
✅ Load balancer ready  

---

## Quick Start

### Local Development (Optional)

```bash
# Install Python dependencies
pip install flask pymysql boto3

# Set environment variables
export DB_HOST=localhost
export DB_USER=root
export DB_PASS=yourpassword
export DB_NAME=appdb

# Run the app
python app.py

# Visit http://localhost:5000
```

### AWS Deployment

1. Copy your chosen theme files to EC2
2. Update database connection in `app.py`
3. Run deployment script
4. Access via Load Balancer URL

Detailed instructions in each theme's README.

---

## Customization Guide

### Easy Changes
- Colors and fonts (CSS)
- Text content (HTML)
- Logo/images
- Button labels

### Medium Changes
- Add new pages
- Modify database schema
- Add new API endpoints
- Change form fields

### Advanced Changes
- Add authentication
- Integrate payment API
- Add real-time features
- Multi-language support

---

## Database Connection

All themes connect to RDS MySQL:

```python
# In app.py
connection = pymysql.connect(
    host='your-rds-endpoint.rds.amazonaws.com',
    user='admin',
    password='your-password',
    database='appdb',
    cursorclass=pymysql.cursors.DictCursor
)
```

Update with your RDS details from Guide 02!

---

## API Endpoints (Standard)

All themes include these endpoints:

```
GET  /                    # Homepage
GET  /health              # Health check
GET  /api/items           # List all items
GET  /api/items/<id>      # Get single item
POST /api/items           # Create new item
PUT  /api/items/<id>      # Update item
DELETE /api/items/<id>    # Delete item
```

"Items" = tickets, games, appointments, etc. depending on theme.

---

## Theme Comparison

| Theme | Complexity | Tables | Best For |
|-------|-----------|--------|----------|
| Ticket Booking | Medium | 3 | Events, concerts |
| Gaming Platform | Easy | 2 | Game catalogs |
| Veterinary | Medium | 3 | Pet services |
| Hospital | Medium | 3 | Healthcare |
| Restaurant | Easy | 2 | Food service |

All are beginner-friendly!

---

## Security Notes

⚠️ **This is a learning project** - includes basic security:
- Input validation
- SQL injection protection (parameterized queries)
- HTTPS via CloudFront
- Security groups for network isolation

**For production**, add:
- User authentication
- Session management
- CSRF protection
- Rate limiting
- Input sanitization

---

## AWS Integration Points

### EC2 (Application Tier)
- Flask app runs on port 80
- Multiple instances via Auto Scaling
- User data script for deployment

### RDS (Database Tier)
- MySQL connection via endpoint
- Connection pooling
- Automatic failover (Multi-AZ)

### ALB (Load Balancer)
- Distributes traffic
- Health checks on `/health`
- Session stickiness (optional)

### CloudFront (CDN)
- HTTPS encryption
- Static asset caching
- DDoS protection

---

## Well-Architected Framework

Each theme demonstrates:

### Operational Excellence
- Health check endpoints
- CloudWatch logging
- Error handling

### Security
- No hardcoded credentials
- Parameterized SQL queries
- HTTPS only

### Reliability
- Multi-instance deployment
- Auto Scaling
- RDS Multi-AZ

### Performance Efficiency
- Efficient SQL queries
- CloudFront caching
- Lightweight frontend

### Cost Optimization
- Free tier eligible
- Minimal dependencies
- Auto Scaling saves cost

### Sustainability
- Efficient resource usage
- Minimal data transfer
- Scale down when idle

---

## Next Steps

1. Browse the `themes/` folder
2. Pick a theme that matches your project
3. Read that theme's README.md
4. Customize to your vision
5. Deploy to AWS!

---

## Support

- Review Flask documentation: https://flask.palletsprojects.com/
- Check MySQL syntax: https://dev.mysql.com/doc/
- AWS deployment help: See console guides

---

## Credits

Built for AWS Cloud Architecture Internship Course - Week 4 Project.

Happy building! 🚀
