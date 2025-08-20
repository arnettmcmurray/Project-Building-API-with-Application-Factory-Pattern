from app.extensions import db

ticket_mechanics = db.Table(
    "ticket_mechanics",
    db.Column("ticket_id", db.Integer, db.ForeignKey("service_ticket.id"), primary_key=True),
    db.Column("mechanic_id", db.Integer, db.ForeignKey("mechanic.id"), primary_key=True),
)

class Mechanic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialty = db.Column(db.String(100))
    password = db.Column(db.String(128), nullable=False)
    tickets = db.relationship(
        "ServiceTicket",
        secondary=ticket_mechanics,
        back_populates="mechanics"
    )

class ServiceTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), default="open")
    mechanics = db.relationship(
        "Mechanic",
        secondary=ticket_mechanics,
        back_populates="tickets"
    )
