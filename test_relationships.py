from app import create_app, db
from app.models import Mechanic, ServiceTicket

app = create_app()

with app.app_context():
    # Reset tables
    db.drop_all()
    db.create_all()

    # Create mechanics
    mech1 = Mechanic(first_name="Tony", last_name="Stark", email="tony@shop.com", salary=90000)
    mech2 = Mechanic(first_name="Bruce", last_name="Wayne", email="bruce@shop.com", salary=85000)

    # Create tickets
    ticket1 = ServiceTicket(service_desc="Oil Change", price=49.99, vin="123VIN", service_date="2025-08-18")
    ticket2 = ServiceTicket(service_desc="Brake Repair", price=299.99, vin="456VIN", service_date="2025-08-18")

    # Assign relationships
    ticket1.mechanics.append(mech1)   # Tony assigned
    ticket1.mechanics.append(mech2)   # Bruce also assigned
    ticket2.mechanics.append(mech1)   # Tony assigned to another ticket

    db.session.add_all([mech1, mech2, ticket1, ticket2])
    db.session.commit()

    # Query test
    print("Mechanics for Ticket1:", [m.first_name for m in ticket1.mechanics])
    print("Tickets for Tony:", [t.service_desc for t in mech1.tickets])
