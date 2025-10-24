# === seed.py — unified seeder for local + Render ===
import os

# Force Flask to use development config BEFORE anything else
os.environ["FLASK_ENV"] = "development"

from flask import Flask
from dotenv import load_dotenv

# Load .env from project root (ensures DATABASE_URL is available)
load_dotenv()

from config import DevelopmentConfig, ProductionConfig
from app.extensions import db
from app.models import Mechanic, Customer, Inventory, ServiceTicket

# === Detect environment and choose config ===
env = os.getenv("FLASK_ENV", "production").lower()
config = DevelopmentConfig if env == "development" else ProductionConfig

# === App + DB setup ===
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

# === Seeding logic ===
with app.app_context():
    uri = app.config.get("SQLALCHEMY_DATABASE_URI", "")
    print(f"\nSeeding DB at: {uri}")

    # Local SQLite gets dropped/recreated, Render/Postgres stays intact
    if "sqlite" in uri:
        print("Dropping + recreating local DB ...")
        db.drop_all()
        db.create_all()
    else:
        print("Render/Postgres mode — skipping drop, will insert if empty.")

    # Only seed if mechanics table is empty
    if not Mechanic.query.first():
        # Mechanics
        admin = Mechanic(name="Admin User", email="admin@shop.com", specialty="Admin")
        admin.set_password("admin123")

        alex = Mechanic(name="Alex Rivera", email="alex@shop.com", specialty="Brakes")
        alex.set_password("password123")

        db.session.add_all([admin, alex])
        db.session.commit()

        # Customers
        john = Customer(name="John Doe", email="john@example.com", phone="312-555-1111", car="Honda Civic")
        jane = Customer(name="Jane Smith", email="jane@example.com", phone="312-555-2222", car="Toyota Corolla")
        db.session.add_all([john, jane])
        db.session.commit()

        # Inventory
        brake = Inventory(name="Brake Pads", price=49.99, quantity=20)
        oil = Inventory(name="Oil Filter", price=9.99, quantity=50)
        db.session.add_all([brake, oil])
        db.session.commit()

        # Service Tickets
        ticket1 = ServiceTicket(description="Brake pad replacement", status="Open", customer_id=john.id)
        ticket2 = ServiceTicket(description="Oil change", status="Closed", customer_id=jane.id)
        db.session.add_all([ticket1, ticket2])
        db.session.commit()

        print("\n✅ Seed complete — default accounts ready:")
        print("  - admin@shop.com / admin123")
        print("  - alex@shop.com / password123\n")
    else:
        print("Mechanics already exist — skipping seed.\n")
