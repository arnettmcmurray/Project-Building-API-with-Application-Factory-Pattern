# === seed.py ===
# Safe seed script: only inserts if tables are empty.

from app import create_app, db
from app.models import Customer, Mechanic, Part, ServiceTicket

app = create_app()

with app.app_context():
    # --- Customers ---
    if Customer.query.count() == 0:
        c1 = Customer(name="John Doe", email="john@example.com", phone="555-1111", car="Honda Civic")
        c2 = Customer(name="Jane Smith", email="jane@example.com", phone="555-2222", car="Toyota Corolla")
        db.session.add_all([c1, c2])

    # --- Mechanics ---
    if Mechanic.query.count() == 0:
        m1 = Mechanic(name="Mike Wrench", email="mike@example.com", password_hash="hashed_pw1", specialty="Engine")
        m2 = Mechanic(name="Sara Bolt", email="sara@example.com", password_hash="hashed_pw2", specialty="Brakes")
        db.session.add_all([m1, m2])

    # --- Parts ---
    if Part.query.count() == 0:
        p1 = Part(name="Brake Pads", description="Front brake pads set", quantity=10)
        p2 = Part(name="Oil Filter", description="Standard oil filter", quantity=25)
        db.session.add_all([p1, p2])

    # --- Service Tickets ---
    if ServiceTicket.query.count() == 0:
        t1 = ServiceTicket(customer_id=1, mechanic_id=1, description="Oil change", status="open")
        t2 = ServiceTicket(customer_id=2, mechanic_id=2, description="Brake replacement", status="open")
        db.session.add_all([t1, t2])

    db.session.commit()
    print("Database seeded (skipped if already populated).")
