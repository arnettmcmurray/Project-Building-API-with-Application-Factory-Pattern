from app import db
from models import Customer, Mechanic, Inventory, ServiceTicket, ServiceTicketInventory
from werkzeug.security import generate_password_hash

def run_seed():
    # === Customers (Swagger expects Alice) ===
    c1 = Customer(name="Alice Johnson", email="alice@example.com", phone="555-1234", car="Ford Focus")
    c2 = Customer(name="Bob Smith", email="bob@example.com", phone="555-5678", car="Honda Accord")
    db.session.add_all([c1, c2])
    db.session.commit()

    # === Mechanics (Swagger expects Mike Wrench login) ===
    m1 = Mechanic(
        name="Mike Wrench",
        email="mike.wrench@example.com",
        password=generate_password_hash("password1"),
        specialty="Engine"
    )
    m2 = Mechanic(
        name="Sara Bolt",
        email="sara@example.com",
        password=generate_password_hash("password2"),
        specialty="Brakes"
    )
    db.session.add_all([m1, m2])
    db.session.commit()

    # === Inventory (Swagger expects Brake Pads) ===
    p1 = Inventory(name="Brake Pads", price=59.99)
    p2 = Inventory(name="Oil Filter", price=14.99)
    db.session.add_all([p1, p2])
    db.session.commit()

    # === Service Tickets (Swagger expects Oil change, status Open) ===
    t1 = ServiceTicket(customer_id=1, description="Oil change", status="Open")
    t2 = ServiceTicket(customer_id=2, description="Brake replacement", status="Open")
    db.session.add_all([t1, t2])
    db.session.commit()

    # Link mechanics to tickets
    t1.mechanics.append(m1)  # Alice → Mike
    t2.mechanics.append(m2)  # Bob → Sara

    # Link inventory to tickets
    link1 = ServiceTicketInventory(ticket=t1, part=p2, quantity=1)  # Oil change → Oil Filter
    link2 = ServiceTicketInventory(ticket=t2, part=p1, quantity=2)  # Brake replacement → Brake Pads
    db.session.add_all([link1, link2])
    db.session.commit()

    print("Database seeded with Swagger-aligned data")
