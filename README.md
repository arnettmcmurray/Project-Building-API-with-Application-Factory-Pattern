# Mechanics API

## Features

- Customer CRUD
- Mechanic CRUD + login + ticket assignment
- Parts and Part Descriptions
- Service Tickets (with relationships to Customers, Mechanics, and Parts)
- JWT-based authentication
- Role-based access control
- Swagger API Documentation

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- Marshmallow-SQLAlchemy
- Flask-Migrate
- Flask-Limiter
- Flask-Caching
- Flask-Swagger-UI
- python-jose (for JWT)
- Gunicorn (for production server)

## Setup (Local Development)

1. Clone the repo.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   Set environment variables in a .env file:
   ```

ini
Copy code
SQLALCHEMY_DATABASE_URI=mysql+mysqlconnector://username:password@localhost/mechanics_api
SECRET_KEY=your_secret_key
Initialize the database:

bash
Copy code
flask db init
flask db migrate
flask db upgrade
Run the app:

bash
Copy code
flask run
Postman Workflow
Use Postman to test:

/customers (CRUD)

/mechanics (CRUD, login, my-tickets)

/parts (CRUD)

/tickets (CRUD, mechanic + part assignments)

Authentication:

Login via /mechanics/login to receive JWT token.

Use token as Bearer Auth in subsequent requests.

Entity-Relationship Diagram (ERD)
(Include image of ERD here)

Notes
JWT tokens expire after 30 minutes.

Role-based access control is in place for certain endpoints.

Swagger documentation available at /api/docs.

Deployment (Render + GitHub Actions)
This API is live at:
👉 https://mechanics-api.onrender.com

Setup on Render
Create a new Web Service on Render.

Connect this repo.

Set the Start Command:

nginx
Copy code
gunicorn flask_app:app
Add Environment Variables:

SQLALCHEMY_DATABASE_URI = External DB URL from Render Postgres

SECRET_KEY = secret key for JWT

Continuous Deployment
Each push to main triggers GitHub Actions CI.

On success, Render redeploys automatically.

Swagger Docs
Swagger UI available at:
👉 https://mechanics-api.onrender.com/api/docs

pgsql
Copy code

---

### Commit (clean checkpoint):

```bash
git add README.md
git commit -m "Update README with Render deployment instructions"
git push origin main
```
