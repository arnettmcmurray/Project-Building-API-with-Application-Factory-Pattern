from app.extensions import db
from app import create_app
from app.models import Mechanic, Customer, ServiceTicket, Inventory, ServiceTicketInventory

app = create_app()

with app.app_context():
    # Reset db content fresh
    db.drop_all()
    db.create_all()

    # --- Mechanics ---
    admin = Mechanic(
        name="Admin User",
        email="admin@example.com",
        specialty="Manager"
    )
    admin.set_password("password123")

    mike = Mechanic(
        name="Mike Wrench",
        email="mike.wrench@example.com",
        specialty="Engine Repair"
    )
    mike.set_password("mike123")

    sarah = Mechanic(
        name="Sarah Bolt",
        email="sarah.bolt@example.com",
        specialty="Transmission"
    )
    sarah.set_password("sarah123")

    db.session.add_all([admin, mike, sarah])

    # --- Customers (with email +phone + car) ---
    cust1 = Customer(
        name="John Driver",
        email="john.driver@example.com",
        phone="555-123-4567",
        car="Toyota Camry"
    )
    cust2 = Customer(
        name="Emily Rider",
        email="emily.rider@example.com",
        phone="555-987-6543",
        car="Honda Accord"
    )
    cust3 = Customer(
        name="Carlos Speed",
        email="carlos.speed@example.com",
        phone="555-222-3333",
        car="Ford Mustang"
    )

    db.session.add_all([cust1, cust2, cust3])
    db.session.add_all([cust1, cust2, cust3])

    # --- Inventory parts ---
    parts = [
        Inventory(name="Brake Pads", price=79.99),
        Inventory(name="Oil Filter", price=15.49),
        Inventory(name="Air Filter", price=18.99),
        Inventory(name="Alternator", price=229.99),
        Inventory(name="Battery", price=139.99),
        Inventory(name="Spark Plugs", price=49.99),
        Inventory(name="Timing Belt", price=199.99),
        Inventory(name="Radiator", price=299.99),
        Inventory(name="Fuel Pump", price=189.99),
        Inventory(name="Headlights", price=99.99),
    ]
    db.session.add_all(parts)

    db.session.commit()
    print("Database seeded with mechanics, customers, and inventory parts")
