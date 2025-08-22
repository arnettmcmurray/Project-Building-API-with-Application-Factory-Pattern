from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# association table: ServiceTicket
ticket_mechanics = db.Table(
    "ticket_mechanics",
    db.Column("ticket_id", db.Integer, db.ForeignKey("service_ticket.id"), primary_key=True),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanic.id"), primary_key=True),
)

class Mechanic(db.Model):
    __tablename__ = "mechanic"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
   
    password = db.Column(db.String(255), nullable=False)

    tickets = db.relationship(
        "ServiceTicket",
        secondary=ticket_mechanics,
        back_populates="mechanics",
    )

    # password
    def set_password(self, raw_password: str) -> None:
        self.password = generate_password_hash(raw_password)

    def check_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password, raw_password)


class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="open")

    mechanics = db.relationship(
        "Mechanic",
        secondary=ticket_mechanics,
        back_populates="tickets",
    )
from app.extensions import db

class Customer(db.Model):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    car = db.Column(db.String(100))
