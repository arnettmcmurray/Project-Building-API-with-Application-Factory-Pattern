from app import create_app
from app.extensions import db
from app.models import Customer, Mechanic, Inventory, ServiceTicket, ServiceTicketInventory
from config import ProductionConfig   #  force Production

app = create_app(ProductionConfig)    #  point seeder at Render Postgres

with app.app_context():
    # === Customers ===
    if Customer.query.count() == 0:
        c1 = Customer(name="John Doe", email="john@example.com", phone="555-1111", car="Honda Civic")
        c2 = Customer(name="Jane Smith", email="jane@example.com", phone="555-2222", car="Toyota Corolla")
        db.session.add_all([c1, c2])

    # === Mechanics ===
    if Mechanic.query.count() == 0:
        m1 = Mechanic(name="Mike Wrench", email="mike@example.com", specialty="Engine")
        m1.set_password("password1")
        m2 = Mechanic(name="Sara Bolt", email="sara@example.com", specialty="Brakes")
        m2.set_password("password2")
        db.session.add_all([m1, m2])

    # === Inventory ===
    if Inventory.query.count() == 0:
        p1 = Inventory(name="Brake Pads", price=59.99)
        p2 = Inventory(name="Oil Filter", price=14.99)
        db.session.add_all([p1, p2])

    db.session.commit()

    # === Service Tickets ===
    if ServiceTicket.query.count() == 0:
        t1 = ServiceTicket(customer_id=1, description="Oil change", status="Open")
        t2 = ServiceTicket(customer_id=2, description="Brake replacement", status="Open")
        db.session.add_all([t1, t2])
        db.session.commit()

        # Link mechanics to tickets
        t1.mechanics.append(Mechanic.query.get(1))  # John → Mike
        t2.mechanics.append(Mechanic.query.get(2))  # Jane → Sara

        # Link inventory
        link1 = ServiceTicketInventory(ticket=t1, part=Inventory.query.get(2), quantity=1)
        link2 = ServiceTicketInventory(ticket=t2, part=Inventory.query.get(1), quantity=4)
        db.session.add_all([link1, link2])

    db.session.commit()

print(" Database seeded into Production (Render Postgres).")
