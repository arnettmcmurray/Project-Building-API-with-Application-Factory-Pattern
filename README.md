# 🧰 Mechanic Workshop API

Flask-based backend for managing mechanics, customers, inventory (parts), and service tickets.  
Now fully flattened — every endpoint uses raw JSON bodies instead of URL parameters.

---

## 🚀 Live Deployment

**Render URL:**  
[https://mechanics-api.onrender.com](https://mechanics-api.onrender.com)

**Swagger Docs:**  
[https://mechanics-api.onrender.com/api/docs](https://mechanics-api.onrender.com/api/docs)

---

## 🔄 October 2025 Update

All API endpoints now accept **JSON input only**.  
No path parameters, no text boxes — Swagger and Postman behave the same.

### Example

**Old:**  
`PUT /service_tickets/1`

**New:**  
`PUT /service_tickets/update`

**Body Example:**

```json
{
  "ticket_id": 1,
  "status": "Closed",
  "description": "Updated brake and rotor replacement"
}
🧩 Features
Mechanics can register, login, update, and view tickets.

Customers can create, update, delete, and view profiles.

Inventory (Parts) can be added, updated, or removed.

Service tickets support create, update, assign mechanics, remove mechanics, and add parts.

JWT authentication protects all key routes.

Swagger UI for live JSON testing.

Deployed with Render (PostgreSQL + Gunicorn).

⚙️ Tech Stack
Backend: Flask 3.x
ORM: SQLAlchemy 2.x
Serialization: Marshmallow 4.x
Auth: JWT
Docs: Swagger UI
Rate Limiting: Flask-Limiter
Deployment: Render
Database: PostgreSQL

🧰 Local Setup
Clone repo

bash
Copy code
git clone https://github.com/arnettmcmurray/mechanic-api.git
cd mechanic-api
Create and activate virtual environment

bash
Copy code
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
Install dependencies

bash
Copy code
pip install -r requirements.txt
Set environment variables
Create a .env file:

ini
Copy code
FLASK_APP=app
FLASK_ENV=development
DATABASE_URL=postgresql://user:password@localhost:5432/mechanic_db
JWT_SECRET_KEY=supersecretkey
Run the app

bash
Copy code
flask run
Open Swagger Docs
Visit http://127.0.0.1:5000/api/docs

🧠 Example Workflows
Create Mechanic
POST /mechanics/create

json
Copy code
{
  "name": "Alex Rivera",
  "email": "alex@shop.com",
  "password": "password123",
  "specialty": "Brakes"
}
Assign Mechanic to Ticket
POST /service_tickets/assign

json
Copy code
{
  "ticket_id": 1,
  "mech_id": 2
}
Add Parts to Ticket
POST /service_tickets/add_parts

json
Copy code
{
  "ticket_id": 1,
  "parts": [
    { "part_id": 1 },
    { "part_id": 2 }
  ]
}
```

## Deployment Notes

Render Environment Variables:

- DATABASE_URL: postgresql://mechanic_db_hlrw_user:p9GXJpig6WrHW8j1NzQYfLilZt3LPRo8@dpg-d3ooheu3jp1c739kd210-a.oregon-postgres.render.com/mechanic_db_hlrw?sslmode=require
- FLASK_ENV: production
- JWT_SECRET_KEY: my-mechanics-secret-2025
- SECRET_KEY: my-mechanics-secret-2025
- RENDER_API_KEY: (GitHub secret)
- RENDER_SERVICE_ID: (GitHub secret)
