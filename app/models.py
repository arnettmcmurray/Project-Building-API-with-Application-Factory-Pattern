from app.extensions import db
from sqlalchemy import ForeignKey, String, Float, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

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

# === Mechanic model ===
class Mechanic(db.Model):
    __tablename__ = "mechanic"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    specialty: Mapped[str] = mapped_column(String(100), nullable=True)

    tickets = relationship("ServiceTicket", secondary=ticket_mechanics, back_populates="mechanics")

    # helpers for password 
    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


# === Customer model ===
class Customer(db.Model):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    car: Mapped[str] = mapped_column(String(100), nullable=True)

    # 🔧 changed backref -> back_populates for consistency
    tickets = relationship("ServiceTicket", back_populates="customer", cascade="all, delete-orphan")


# === ServiceTicket model ===
class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customer.id", name="fk_service_ticket_customer_id"),
        nullable=False
    )

    # 🔧 aligned relationship with Customer
    customer = relationship("Customer", back_populates="tickets")
    mechanics = relationship("Mechanic", secondary=ticket_mechanics, back_populates="tickets")
    parts = relationship("ServiceTicketInventory", back_populates="ticket")


# === Inventory model ===
class Inventory(db.Model):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    tickets = relationship("ServiceTicketInventory", back_populates="part")


# === Junction model with quantity ===
class ServiceTicketInventory(db.Model):
    __tablename__ = "service_ticket_inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_ticket_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("service_ticket.id", name="fk_service_ticket_inventory_ticket_id")
    )
    inventory_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("inventory.id", name="fk_service_ticket_inventory_inventory_id")
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    ticket = relationship("ServiceTicket", back_populates="parts")
    part = relationship("Inventory", back_populates="tickets")
