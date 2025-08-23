from app.extensions import db
from sqlalchemy import ForeignKey, String, Float, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Junction table for mechanics <-> service tickets
ticket_mechanics = Table(
    "service_mechanic",
    db.Model.metadata,
    Column(
        "service_ticket_id",
        Integer,
        ForeignKey("service_ticket.id", name="fk_service_mechanic_ticket_id")
    ),
    Column(
        "mechanic_id",
        Integer,
        ForeignKey("mechanic.id", name="fk_service_mechanic_mechanic_id")
    )
)

# Mechanic model
class Mechanic(db.Model):
    __tablename__ = "mechanic"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    tickets = relationship("ServiceTicket", secondary=ticket_mechanics, back_populates="mechanics")

# Customer model
class Customer(db.Model):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    tickets = relationship("ServiceTicket", backref="customer", cascade="all, delete-orphan")

# ServiceTicket model
class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    date: Mapped[str] = mapped_column(String(50), nullable=False)
    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("customer.id", name="fk_service_ticket_customer_id")
    )

    mechanics = relationship(
        "Mechanic",
        secondary=ticket_mechanics,
        back_populates="tickets"
    )

    parts = relationship("ServiceTicketInventory", back_populates="ticket")

# Inventory model
class Inventory(db.Model):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    tickets = relationship("ServiceTicketInventory", back_populates="part")

# Junction model with quantity
class ServiceTicketInventory(db.Model):
    __tablename__ = "service_ticket_inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_ticket_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("service_ticket.id", name="fk_serviceticketinventory_ticket_id")
    )
    inventory_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("inventory.id", name="fk_serviceticketinventory_inventory_id")
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    ticket = relationship("ServiceTicket", back_populates="parts")
    part = relationship("Inventory", back_populates="tickets")
