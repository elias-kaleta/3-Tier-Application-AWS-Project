# Theme Templates Guide

Quick reference for creating your own theme or using existing ones.

---

## Available Themes

### ✅ Complete: Ticket Booking System
**Location**: `themes/ticket-booking/`

**Files**:
- ✅ index.html (Complete with animations, modal, search)
- ✅ app.py (Full Flask backend with 8 endpoints)
- ✅ README.md (Deployment guide)
- ✅ requirements.txt

**Features**:
- Browse 8 sample events
- Real-time search
- Booking modal with form validation
- Automatic ticket inventory management
- Beautiful gradient design
- Fully responsive

**Use this as your base template!**

---

### 🚧 Templates: Other Themes

The following themes are **template ideas** for interns to build:

#### Gaming Platform
- Game library management
- Genre filtering
- Playtime tracking
- User ratings

#### Veterinary Clinic
- Pet appointment booking
- Vet selection
- Pet profiles
- Service types (checkup, surgery, grooming)

#### Hospital Booking
- Doctor appointments
- Department selection
- Patient information
- Appointment scheduling

#### Restaurant Reservation
- Table booking
- Time slot selection
- Party size
- Special requests

---

## How to Create a New Theme

### Method 1: Adapt Ticket Booking (Recommended)

1. **Copy the ticket-booking folder**:
```bash
cp -r themes/ticket-booking themes/your-theme
```

2. **Update the database schema** in `app.py`:
```python
# Change "events" to your entity (games, appointments, tables)
# Change "bookings" to your action (purchases, appointments, reservations)
```

3. **Update the frontend** in `index.html`:
- Change colors (search for `#667eea` and `#764ba2`)
- Change text ("TicketHub" → "Your Name")
- Change icons (🎫 → your icon)
- Update form fields

4. **Update sample data**:
- Replace the 8 sample events with your data
- Adjust fields to match your theme

**Time**: 3-5 hours

---

### Method 2: Build From Scratch

1. **Create database schema**:
```sql
CREATE TABLE items (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    -- your fields here
);

CREATE TABLE transactions (
    id INT PRIMARY KEY,
    item_id INT,
    -- your fields here
);
```

2. **Create Flask backend**:
```python
@app.route('/api/items')
def get_items():
    # your code

@app.route('/api/transactions', methods=['POST'])
def create_transaction():
    # your code
```

3. **Create HTML frontend**:
- Grid layout for items
- Modal for actions
- Search/filter functionality

**Time**: 6-10 hours

---

## Theme Conversion Guide

### Ticket Booking → Gaming Platform

#### Database Changes
```sql
-- events → games
ALTER TABLE events RENAME TO games;

-- Update columns
ALTER TABLE games 
  CHANGE name title VARCHAR(255),
  CHANGE event_date release_date DATE,
  CHANGE location platform VARCHAR(50);

-- bookings → purchases  
ALTER TABLE bookings RENAME TO purchases;
```

#### Frontend Changes
```javascript
// Replace event terms
events → games
event_date → release_date
location → platform
available_tickets → copies_available
```

#### Visual Changes
```css
/* Change color scheme */
background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); /* Gaming pink */

/* Change icons */
🎫 → 🎮
```

---

### Ticket Booking → Veterinary Clinic

#### Database Changes
```sql
-- events → services
-- columns: name, type (checkup, surgery, grooming), duration, price

-- bookings → appointments
-- columns: service_id, pet_name, pet_type, owner_name, owner_email, appointment_date
```

#### Frontend Changes
```javascript
events → services
Book Tickets → Schedule Appointment
Quantity → Select Service
```

#### Visual Changes
```css
background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%); /* Soft pastels */
Icons: 🐾 🐶 🐱 🐰
```

---

### Ticket Booking → Hospital Booking

#### Database Changes
```sql
-- events → doctors
-- columns: name, specialization, available_slots, hospital_location

-- bookings → appointments
-- columns: doctor_id, patient_name, patient_age, symptoms, appointment_date
```

#### Frontend Changes
```javascript
events → doctors
event_date → available_date
category → specialization (cardiology, pediatrics, etc.)
```

#### Visual Changes
```css
background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); /* Medical blue */
Icons: 🏥 👨‍⚕️ 💊 🩺
```

---

### Ticket Booking → Restaurant Reservation

#### Database Changes
```sql
-- events → time_slots
-- columns: date, time, available_tables, max_party_size

-- bookings → reservations
-- columns: slot_id, guest_name, guest_email, party_size, special_requests
```

#### Frontend Changes
```javascript
events → time_slots
Tickets → Tables
Book Now → Reserve Table
```

#### Visual Changes
```css
background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); /* Warm food colors */
Icons: 🍽️ 👨‍🍳 🥘 🍷
```

---

## Common Components (Reusable)

All themes share these components:

### 1. Card Grid Layout
```css
.items-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 25px;
}
```

### 2. Search Box
```html
<input type="text" id="searchInput" placeholder="Search...">
```
```javascript
function filterItems() {
    const searchTerm = input.value.toLowerCase();
    const filtered = items.filter(item => 
        item.name.toLowerCase().includes(searchTerm)
    );
}
```

### 3. Modal Dialog
```html
<div id="modal" class="modal">
    <div class="modal-content">
        <form id="actionForm">...</form>
    </div>
</div>
```

### 4. API Client
```javascript
async function fetchItems() {
    const response = await fetch('/api/items');
    const data = await response.json();
    return data;
}
```

### 5. Health Check
```python
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200
```

---

## Database Patterns

### Pattern 1: Inventory System
- Main table: Items (events, games, products)
- Action table: Transactions (bookings, purchases, orders)
- Tracks: Available quantity

**Use for**: Ticket booking, e-commerce, library management

### Pattern 2: Scheduling System
- Main table: Resources (doctors, rooms, time slots)
- Action table: Appointments (reservations, bookings)
- Tracks: Time availability

**Use for**: Appointments, reservations, scheduling

### Pattern 3: Catalog System
- Main table: Items (games, movies, books)
- Action table: User Library (collection, favorites)
- Tracks: User ownership

**Use for**: Digital libraries, collections, catalogs

---

## Quick Customization Checklist

### Colors (5 minutes)
- [ ] Update gradient backgrounds
- [ ] Update button colors
- [ ] Update accent colors

### Text (10 minutes)
- [ ] Update page title
- [ ] Update headings
- [ ] Update button labels
- [ ] Update placeholder text

### Icons (5 minutes)
- [ ] Update emoji icons
- [ ] Update category icons

### Database (30 minutes)
- [ ] Rename tables
- [ ] Update column names
- [ ] Update sample data

### API (30 minutes)
- [ ] Update endpoint names
- [ ] Update field names
- [ ] Update validation logic

### Testing (30 minutes)
- [ ] Test health check
- [ ] Test GET endpoints
- [ ] Test POST endpoints
- [ ] Test frontend integration

**Total**: ~2 hours for basic customization

---

## Deployment Checklist

- [ ] Replace `DB_HOST` with your RDS endpoint
- [ ] Replace `DB_PASS` with your database password
- [ ] Test locally first (optional)
- [ ] Upload to EC2 instances
- [ ] Set environment variables
- [ ] Start the application
- [ ] Test via Load Balancer URL
- [ ] Test via CloudFront URL

---

## Tips for Success

### Do's ✅
- Start with ticket-booking theme (it's complete)
- Test locally before deploying to AWS
- Make small changes incrementally
- Keep the same database structure initially
- Use the same API patterns

### Don'ts ❌
- Don't change too many things at once
- Don't skip testing between changes
- Don't hardcode database credentials
- Don't forget to update environment variables
- Don't remove error handling

---

## Getting Help

### If Frontend Breaks
1. Check browser console (F12 → Console tab)
2. Look for JavaScript errors
3. Verify API endpoints are correct
4. Check network tab for failed requests

### If Backend Breaks
1. Check application logs
2. Test database connection
3. Verify environment variables
4. Test API endpoints with curl

### If Database Breaks
1. Check RDS security groups
2. Verify database credentials
3. Check if tables exist
4. Test connection from EC2

---

## Next Steps

1. **Week 4 Day 1-2**: Choose and deploy ticket-booking theme
2. **Week 4 Day 2-3**: Customize colors, text, and icons
3. **Week 4 Day 3**: Add one unique feature
4. **Week 4 Day 4**: Polish and prepare presentation
5. **Week 4 Day 5**: Present!

Or build a completely new theme using ticket-booking as template!

---

## Summary

✅ **Complete theme available**: Ticket Booking System  
✅ **Template patterns**: Gaming, Veterinary, Hospital, Restaurant  
✅ **Conversion guides**: How to adapt ticket-booking to other themes  
✅ **Common components**: Reusable code snippets  
✅ **Deployment ready**: Works with AWS 3-tier setup  

The ticket-booking theme is production-ready and can be deployed immediately or customized to match any use case! 🚀
