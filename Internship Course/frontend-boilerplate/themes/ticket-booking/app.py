#!/usr/bin/env python3
"""
TicketHub Backend API
Flask application for event ticket booking system
"""

from flask import Flask, jsonify, request, send_from_directory
import pymysql
import os
from datetime import datetime
import json

app = Flask(__name__, static_folder='.')

# Database configuration from environment variables
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'admin'),
    'password': os.getenv('DB_PASS', ''),
    'database': os.getenv('DB_NAME', 'appdb'),
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    """Create database connection"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Exception as e:
        print(f"Database connection error: {e}")
        raise

def init_database():
    """Initialize database tables if they don't exist"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Create events table
            cursor.execute("""
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
            """)
            
            # Create bookings table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS bookings (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    event_id INT NOT NULL,
                    customer_name VARCHAR(255) NOT NULL,
                    customer_email VARCHAR(255) NOT NULL,
                    quantity INT NOT NULL,
                    total_price DECIMAL(10,2) NOT NULL,
                    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (event_id) REFERENCES events(id)
                )
            """)
            
            # Check if events table is empty
            cursor.execute("SELECT COUNT(*) as count FROM events")
            if cursor.fetchone()['count'] == 0:
                # Insert sample events
                sample_events = [
                    ('Summer Music Festival', 'Concert', '2026-07-15 19:00:00', 'Central Park Amphitheater', 79.99, 500, 500, 'Amazing outdoor music festival featuring top artists'),
                    ('Tech Conference 2026', 'Conference', '2026-09-20 09:00:00', 'Convention Center', 199.99, 300, 300, 'Annual technology conference with industry leaders'),
                    ('Comedy Night Live', 'Comedy', '2026-06-10 20:00:00', 'Comedy Club Downtown', 35.50, 150, 150, 'Hilarious stand-up comedy show'),
                    ('Soccer Championship', 'Sports', '2026-08-05 18:00:00', 'National Stadium', 65.00, 1000, 1000, 'Exciting championship match'),
                    ('Broadway Musical', 'Theater', '2026-10-12 19:30:00', 'Grand Theater', 120.00, 400, 400, 'Award-winning musical performance'),
                    ('Jazz Evening', 'Concert', '2026-07-22 20:00:00', 'Blue Note Jazz Club', 45.00, 100, 100, 'Smooth jazz evening with live band'),
                    ('Basketball Finals', 'Sports', '2026-11-15 19:00:00', 'Sports Arena', 95.00, 800, 800, 'Championship finals game'),
                    ('Classical Orchestra', 'Concert', '2026-09-30 19:00:00', 'Symphony Hall', 85.00, 600, 600, 'World-class orchestral performance')
                ]
                
                cursor.executemany("""
                    INSERT INTO events (name, category, event_date, location, price, available_tickets, total_tickets, description)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, sample_events)
            
            connection.commit()
            print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        if connection:
            connection.close()

# Initialize database on startup
init_database()

@app.route('/')
def index():
    """Serve the main HTML page"""
    return send_from_directory('.', 'index.html')

@app.route('/health')
def health():
    """Health check endpoint"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        connection.close()
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.now().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e)
        }), 500

@app.route('/api/events', methods=['GET'])
def get_events():
    """Get all events"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, category, event_date, location, price, 
                       available_tickets, total_tickets, description
                FROM events
                WHERE available_tickets > 0
                ORDER BY event_date ASC
            """)
            events = cursor.fetchall()
        connection.close()
        
        # Convert datetime objects to strings
        for event in events:
            if isinstance(event['event_date'], datetime):
                event['event_date'] = event['event_date'].isoformat()
        
        return jsonify(events), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    """Get single event by ID"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, name, category, event_date, location, price,
                       available_tickets, total_tickets, description
                FROM events
                WHERE id = %s
            """, (event_id,))
            event = cursor.fetchone()
        connection.close()
        
        if not event:
            return jsonify({'error': 'Event not found'}), 404
        
        if isinstance(event['event_date'], datetime):
            event['event_date'] = event['event_date'].isoformat()
        
        return jsonify(event), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings', methods=['POST'])
def create_booking():
    """Create a new booking"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['event_id', 'customer_name', 'customer_email', 'quantity']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        event_id = data['event_id']
        customer_name = data['customer_name']
        customer_email = data['customer_email']
        quantity = int(data['quantity'])
        
        if quantity <= 0:
            return jsonify({'error': 'Quantity must be greater than 0'}), 400
        
        connection = get_db_connection()
        
        try:
            with connection.cursor() as cursor:
                # Check event exists and has enough tickets
                cursor.execute("""
                    SELECT available_tickets, price, name
                    FROM events
                    WHERE id = %s
                    FOR UPDATE
                """, (event_id,))
                event = cursor.fetchone()
                
                if not event:
                    return jsonify({'error': 'Event not found'}), 404
                
                if event['available_tickets'] < quantity:
                    return jsonify({
                        'error': f'Not enough tickets available. Only {event["available_tickets"]} left.'
                    }), 400
                
                # Calculate total price
                total_price = float(event['price']) * quantity
                
                # Create booking
                cursor.execute("""
                    INSERT INTO bookings (event_id, customer_name, customer_email, quantity, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                """, (event_id, customer_name, customer_email, quantity, total_price))
                
                booking_id = cursor.lastrowid
                
                # Update available tickets
                cursor.execute("""
                    UPDATE events
                    SET available_tickets = available_tickets - %s
                    WHERE id = %s
                """, (quantity, event_id))
                
                connection.commit()
                
                return jsonify({
                    'message': 'Booking created successfully',
                    'booking_id': booking_id,
                    'event_name': event['name'],
                    'quantity': quantity,
                    'total_price': total_price
                }), 201
                
        except Exception as e:
            connection.rollback()
            raise
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/bookings/<int:booking_id>', methods=['GET'])
def get_booking(booking_id):
    """Get booking details"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT b.id, b.event_id, b.customer_name, b.customer_email,
                       b.quantity, b.total_price, b.booking_date,
                       e.name as event_name, e.event_date, e.location
                FROM bookings b
                JOIN events e ON b.event_id = e.id
                WHERE b.id = %s
            """, (booking_id,))
            booking = cursor.fetchone()
        connection.close()
        
        if not booking:
            return jsonify({'error': 'Booking not found'}), 404
        
        # Convert datetime objects
        if isinstance(booking['booking_date'], datetime):
            booking['booking_date'] = booking['booking_date'].isoformat()
        if isinstance(booking['event_date'], datetime):
            booking['event_date'] = booking['event_date'].isoformat()
        
        return jsonify(booking), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # Total events
            cursor.execute("SELECT COUNT(*) as count FROM events")
            total_events = cursor.fetchone()['count']
            
            # Total bookings
            cursor.execute("SELECT COUNT(*) as count, SUM(quantity) as tickets, SUM(total_price) as revenue FROM bookings")
            booking_stats = cursor.fetchone()
            
            # Available tickets
            cursor.execute("SELECT SUM(available_tickets) as count FROM events")
            available_tickets = cursor.fetchone()['count']
        
        connection.close()
        
        return jsonify({
            'total_events': total_events,
            'total_bookings': booking_stats['count'] or 0,
            'tickets_sold': int(booking_stats['tickets'] or 0),
            'total_revenue': float(booking_stats['revenue'] or 0),
            'available_tickets': int(available_tickets or 0)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Run on port 80 for production, 5000 for local development
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
