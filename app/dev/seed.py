# app/dev/seed.py
# clean standalone seeder — runs without touching create_app()

from flask import Flask
from config import DevelopmentConfig  # config.py is at project root
from app.extensions import db
from app.models import Mechanic, Customer, Inventory, ServiceTicket

# --- setup app + db manually ---
app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    print("Dropping + recreating local DB ...")
    db.drop_all()
    db.create_all()

    # Mechanics
    m1 = Mechanic(name="Alex Rivera", email="alex@shop.com", specialty="Brakes")
    m1.set_password("password123")
    m2 = Mechanic(name="Jamie Lee", email="jamie@shop.com", specialty="Engine")
    m2.set_password("password123")
    m3 = Mechanic(name="Taylor Admin", email="admin@shop.com", specialty="ADMIN")
    m3.set_password("admin123")
    db.session.add_all([m1, m2, m3])
    db.session.flush()

    # Customers
    c1 = Customer(name="John Doe", email="john@example.com", phone="312-555-1111", car="Honda Civic")
    c2 = Customer(name="Jane Smith", email="jane@example.com", phone="312-555-2222", car="Toyota Corolla")
    db.session.add_all([c1, c2])
    db.session.flush()

    # Inventory
    i1 = Inventory(name="Brake Pads", price=49.99, quantity=20)
    i2 = Inventory(name="Oil Filter", price=9.99, quantity=50)
    db.session.add_all([i1, i2])
    db.session.flush()

    # Service Tickets
    t1 = ServiceTicket(description="Brake pad replacement", status="open", customer_id=c1.id)
    t2 = ServiceTicket(description="Oil change", status="closed", customer_id=c2.id)
    db.session.add_all([t1, t2])
    db.session.flush()

    # Relationships
    t1.mechanics.append(m1)
    t1.parts.append(i1)
    t2.mechanics.append(m2)
    t2.parts.append(i2)

    db.session.commit()
    print("✅ Local dev DB reseeded successfully.")
