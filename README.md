# Mechanic Shop API

A Flask + SQLAlchemy REST API for managing a mechanic shop.  
Supports mechanics, customers, inventory (parts), and service tickets.  
Built for Coding Temple assignments.

---

## 🚀 Features

- **Mechanics**
  - Create, login (JWT), update/delete self
  - View assigned tickets
  - Get mechanic with most tickets
- **Customers**
  - Create, search by email, update/delete
- **Service Tickets**
  - CRUD tickets
  - Assign/remove mechanics
  - Add parts to tickets
  - Paginated ticket view
- **Inventory**
  - CRUD parts

---

## 📦 Tech Stack

- Python 3.11+
- Flask
- SQLAlchemy 2.0
- Marshmallow
- Flask-Limiter (rate limiting)
- Flask-Caching
- python-jose (JWT)

---

## ⚙️ Setup

1. **Clone the repo**
   ```bash
   git clone <your-repo-url>
   cd mechanic-api
   Create and activate virtual environment
   ```

bash
Copy
Edit
python -m venv venv
source venv/bin/activate # Mac/Linux
venv\Scripts\activate # Windows
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Seed the database

bash
Copy
Edit
python seed.py
Run the server

bash
Copy
Edit
flask run
Server starts on: http://127.0.0.1:5000

🔑 Authentication
Login via /mechanics/login to receive a JWT.

Pass token in headers for protected routes:

makefile
Copy
Edit
Authorization: Bearer <your_token>
🧪 Testing with Postman
Import MechanicAPI_Assignment.postman_collection.json

Import MechanicAPI_env.postman_environment.json

Select MechanicAPI Environment in Postman.

Run Mechanics → Login Mechanic to get token.

Token auto-fills → test Customers, Tickets, Inventory endpoints.

🗂 ERD
The project includes an auto-generated ERD (erd.png) showing tables and relationships.

📌 Notes
Database resets each time you run seed.py

Default seeded accounts:

Admin User → admin@example.com / password123

Mike Wrench → mike.wrench@example.com / mike123

Sarah Bolt → sarah.bolt@example.com / sarah123
