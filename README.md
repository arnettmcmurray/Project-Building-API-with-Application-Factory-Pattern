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

## API Endpoints

### Mechanics
- **POST /mechanics/** → Create a new mechanic  
- **GET /mechanics/** → Retrieve all mechanics  
- **PUT /mechanics/<id>** → Update mechanic by ID  
- **DELETE /mechanics/<id>** → Delete mechanic by ID  

### Service Tickets
- **POST /tickets/** → Create a new service ticket  
- **GET /tickets/** → Retrieve all tickets  
- **PUT /tickets/<id>** → Update ticket by ID  
- **DELETE /tickets/<id>** → Delete ticket by ID  
- **POST /tickets/<id>/assign/<mechanic_id>** → Assign a mechanic to a ticket  
- **DELETE /tickets/<id>/remove/<mechanic_id>** → Remove a mechanic from a ticket  

---

## Postman Usage

- Import the provided collection file: `Mechanic_API_New.postman_collection.json`  
- (Optional) Import the environment file: `Mechanic_API_New.postman_environment.json`  

---

## Notes

- Input validation is handled using Marshmallow schemas.  
- SQLAlchemy is used for database ORM and migrations.  
