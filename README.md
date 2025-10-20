# Mechanic Workshop API

Flask backend for the **Mechanic Workshop** system — full CRUD web service with JWT authentication, Swagger documentation, and persistent seeding.  
Manages **mechanics, customers, inventory, and service tickets**, and connects to a separate React frontend.

---

## 🚀 Features

- Flask + SQLAlchemy + Marshmallow + JWT
- Auto-seeding for local dev (no more empty DB)
- Swagger UI documentation (`/api/docs`)
- Token-based auth for protected routes
- Render deployment ready (PostgreSQL in production)
- Compatible with `react-mechanic-api` frontend

---

## ⚙️ Quickstart (Local Dev)

```bash
# 1. Clone repo
git clone https://github.com/arnettmcmurray/mechanic-api.git
cd mechanic-api

# 2. Create and activate venv
python -m venv venv
source venv/bin/activate   # Mac / Linux
# venv\Scripts\activate     # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. (Optional) set environment
export FLASK_ENV=development

# 5. Run Flask
flask --app app run
Then open:
👉 http://127.0.0.1:5000/api/docs

🔑 Default Logins (Auto-Seeded)
Role	Email	Password
Admin	admin@shop.com	admin123
Mechanic	alex@shop.com	password123

Use either to log in via /mechanics/login and get a JWT token for protected routes.

🗄️ Database

Local: SQLite (instance/mechanic_shop.db)

Production: PostgreSQL (Render)

Auto-seed runs automatically for SQLite on first boot.
Manual reseed (if needed):

python -m app.dev.seed

🌍 Deployment (Render)

Backend: https://mechanics-api.onrender.com

Swagger Docs: https://mechanics-api.onrender.com/api/docs

Render redeploys automatically on each push to main.

⚛️ Frontend Link

Frontend repo: https://github.com/arnettmcmurray/react-mechanic-api

Set the React .env:

VITE_API_URL=https://mechanics-api.onrender.com


Then run the React app and verify CRUD sync through your API.
```
