from app import create_app
from app.extensions import db
from app.models import Mechanic, Customer, Inventory, ServiceTicket, ServiceTicketInventory

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # === Mechanics ===
    admin = Mechanic(name="Admin User", email="admin@example.com", specialty="Manager")
    admin.set_password("password123")

    mike = Mechanic(name="Mike Wrench", email="mike.wrench@example.com", specialty="Engine Repair")
    mike.set_password("mike123")

    sarah = Mechanic(name="Sarah Bolt", email="sarah.bolt@example.com", specialty="Transmission")
    sarah.set_password("sarah123")

    tom = Mechanic(name="Tom Tires", email="tom.tires@example.com", specialty="Tires")
    tom.set_password("tom123")

    lily = Mechanic(name="Lily Lights", email="lily.lights@example.com", specialty="Electrical")
    lily.set_password("lily123")

    db.session.add_all([admin, mike, sarah, tom, lily])

    # === Customers ===
    john = Customer(name="John Driver", email="john.driver@example.com", phone="555-123-4567", car="Toyota Camry")
    emily = Customer(name="Emily Rider", email="emily.rider@example.com", phone="555-987-6543", car="Honda Accord")
    carlos = Customer(name="Carlos Speed", email="carlos.speed@example.com", phone="555-222-3333", car="Ford Mustang")
    sophie = Customer(name="Sophie Lane", email="sophie.lane@example.com", phone="555-333-1212", car="Mazda CX-5")
    dan = Customer(name="Dan Drift", email="dan.drift@example.com", phone="555-888-7777", car="Nissan 350Z")

    db.session.add_all([john, emily, carlos, sophie, dan])

    # === Inventory (10 parts) ===
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

    # === Service Tickets ===
    ticket1 = ServiceTicket(description="Brake replacement", customer=john, status="Open")
    ticket1.mechanics.append(mike)

    ticket2 = ServiceTicket(description="Oil change + filter replacement", customer=emily, status="Open")
    ticket2.mechanics.append(sarah)

    ticket3 = ServiceTicket(description="Radiator leak repair", customer=carlos, status="In Progress")
    ticket3.mechanics.extend([mike, lily])

    ticket4 = ServiceTicket(description="Battery replacement", customer=sophie, status="Completed")
    ticket4.mechanics.append(tom)

    db.session.add_all([ticket1, ticket2, ticket3, ticket4])
    db.session.commit()

    # === Add parts to tickets via junction table ===
    db.session.add_all([
        ServiceTicketInventory(service_ticket_id=ticket1.id, inventory_id=parts[0].id, quantity=1),  # Brake Pads
        ServiceTicketInventory(service_ticket_id=ticket2.id, inventory_id=parts[1].id, quantity=1),  # Oil Filter
        ServiceTicketInventory(service_ticket_id=ticket2.id, inventory_id=parts[2].id, quantity=1),  # Air Filter
        ServiceTicketInventory(service_ticket_id=ticket3.id, inventory_id=parts[7].id, quantity=1),  # Radiator
        ServiceTicketInventory(service_ticket_id=ticket4.id, inventory_id=parts[4].id, quantity=1),  # Battery
    ])

    db.session.commit()
    print("Database LOADED with mechanics, customers, inventory, and demo tickets (with links)")
