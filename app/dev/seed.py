# dev/seed.py — simple working reseed
from flask import Flask
from config import DevelopmentConfig
from app.extensions import db
from app.models import Mechanic, Customer, Inventory, ServiceTicket

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
db.init_app(app)

with app.app_context():
    print("Dropping + recreating local DB ...")
    db.drop_all()
    db.create_all()

    admin = Mechanic(name="Admin User", email="admin@shop.com", specialty="Admin")
    admin.set_password("admin123")

    alex = Mechanic(name="Alex Rivera", email="alex@shop.com", specialty="Brakes")
    alex.set_password("password123")

    db.session.add_all([admin, alex])
    db.session.commit()

    john = Customer(name="John Doe", email="john@example.com", phone="312-555-1111", car="Honda Civic")
    jane = Customer(name="Jane Smith", email="jane@example.com", phone="312-555-2222", car="Toyota Corolla")
    db.session.add_all([john, jane])
    db.session.commit()

    brake = Inventory(name="Brake Pads", price=49.99, quantity=20)
    oil = Inventory(name="Oil Filter", price=9.99, quantity=50)
    db.session.add_all([brake, oil])
    db.session.commit()

    ticket1 = ServiceTicket(description="Brake pad replacement", status="Open", customer_id=john.id)
    ticket2 = ServiceTicket(description="Oil change", status="Closed", customer_id=jane.id)
    db.session.add_all([ticket1, ticket2])
    db.session.commit()

    print("✅ Seed complete — test logins:")
    print("- admin@shop.com / admin123")
    print("- alex@shop.com / password123")
