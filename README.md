# Mechanic Shop API

A Flask-based REST API for managing mechanics and service tickets.

---

## Setup

1. Clone the repository and open it in VS Code (or your preferred editor).
2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   pip install -r requirements.txt
   ```
3. Run the development server:
   ```bash
   flask run
   ```

---

API Endpoints
👨 Mechanics

POST /mechanics → Create a new mechanic

POST /mechanics/login → Login and receive JWT

GET /mechanics → Retrieve all mechanics

PUT /mechanics/<id> → Update mechanic by ID

DELETE /mechanics/<id> → Delete mechanic by ID

👥 Customers

POST /customers → Create a new customer

GET /customers → Retrieve all customers

PUT /customers/<id> → Update customer by ID

DELETE /customers/<id> → Delete customer by ID

📝 Service Tickets

POST /service_tickets → Create a new service ticket

GET /service_tickets → Retrieve all tickets

GET /service_tickets/paginated?page=1&per_page=5 → Paginated tickets

PUT /service_tickets/<id> → Update ticket by ID

DELETE /service_tickets/<id> → Delete ticket by ID

POST /service_tickets/<ticket_id>/assign/<mechanic_id> → Assign a mechanic to a ticket

POST /service_tickets/<ticket_id>/remove/<mechanic_id> → Remove a mechanic from a ticket

POST /service_tickets/<ticket_id>/parts → Add one or multiple parts to a ticket
Example request body:

{
"parts": [
{ "part_id": 1, "quantity": 2 },
{ "part_id": 3, "quantity": 1 },
{ "part_id": 5, "quantity": 4 }
]
}

🛠️ Inventory

POST /parts → Add a new part

GET /parts → Retrieve all parts

GET /parts/<id> → Retrieve part by ID

PUT /parts/<id> → Update part

DELETE /parts/<id> → Delete part

🗂️ Postman Usage

Import the provided collection:
Mechanic_API_New.postman_collection.json

(Optional) Import environment file:
Mechanic_API_New.postman_environment.json

Use JWT token from /mechanics/login for protected routes.

📊 Database

Entity Relationship Diagram (ERD):

📝 Notes

Input validation handled with Marshmallow schemas.

SQLAlchemy ORM + Flask-Migrate for database schema and migrations.

Flask-Limiter used to prevent spam requests.

Flask-Caching available for optimization.
