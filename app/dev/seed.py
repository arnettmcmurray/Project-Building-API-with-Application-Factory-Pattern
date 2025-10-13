# dev/seed.py
# optional seeding script, safe to run locally or in staging

from app import create_app
from app.extensions import db
from app.models import Mechanic, Customer, Inventory, ServiceTicket

app = create_app()
with app.app_context():  # your existing seeding logic (don’t wrap in another input())
        db.drop_all()
        db.create_all()

        m1 = Mechanic(name="Alex Rivera", email="alex@shop.com", specialty="Brakes"); m1.set_password("password123")
        m2 = Mechanic(name="Jamie Lee", email="jamie@shop.com", specialty="Engine"); m2.set_password("password123")
        m3 = Mechanic(name="Taylor Admin", email="admin@shop.com", specialty="ADMIN"); m3.set_password("admin123")
        db.session.add_all([m1, m2, m3])

        c1 = Customer(name="John Doe", email="john@example.com", phone="312-555-1111", car="Honda Civic")
        c2 = Customer(name="Jane Smith", email="jane@example.com", phone="312-555-2222", car="Toyota Corolla")
        db.session.add_all([c1, c2])

        i1 = Inventory(name="Brake Pads", price=49.99, quantity=20)
        i2 = Inventory(name="Oil Filter", price=9.99, quantity=50)
        db.session.add_all([i1, i2])

        t1 = ServiceTicket(description="Brake pad replacement", status="open", customer_id=c1.id)
        t1.mechanics.append(m1); t1.parts.append(i1)
        t2 = ServiceTicket(description="Oil change", status="closed", customer_id=c2.id)
        t2.mechanics.append(m2); t2.parts.append(i2)

        db.session.add_all([t1, t2])
        db.session.commit()

        print("Local dev DB reseeded successfully.")