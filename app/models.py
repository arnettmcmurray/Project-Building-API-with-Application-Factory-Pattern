from app.extensions import db
from sqlalchemy import ForeignKey, String, Float, Integer, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# === Junctions ===
ticket_mechanics = Table(
    "service_mechanic",
    db.Model.metadata,
    Column("service_ticket_id", Integer, ForeignKey("service_ticket.id")),
    Column("mechanic_id", Integer, ForeignKey("mechanic.id"))
)

ticket_parts = Table(
    "service_ticket_parts",
    db.Model.metadata,
    Column("service_ticket_id", Integer, ForeignKey("service_ticket.id")),
    Column("inventory_id", Integer, ForeignKey("inventory.id"))
)

# === Mechanic ===
class Mechanic(db.Model):
    __tablename__ = "mechanic"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    specialty: Mapped[str] = mapped_column(String(100))

    tickets = relationship("ServiceTicket", secondary=ticket_mechanics, back_populates="mechanics")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


# === Customer ===
class Customer(db.Model):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20))
    car: Mapped[str] = mapped_column(String(100))

    tickets = relationship("ServiceTicket", back_populates="customer", cascade="all, delete-orphan")


# === ServiceTicket ===
class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="Open")
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"), nullable=False)

    customer = relationship("Customer", back_populates="tickets")
    mechanics = relationship("Mechanic", secondary=ticket_mechanics, back_populates="tickets")
    parts = relationship("Inventory", secondary=ticket_parts, back_populates="tickets")


# === Inventory ===
class Inventory(db.Model):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    tickets = relationship("ServiceTicket", secondary=ticket_parts, back_populates="parts")
