from app.extensions import db
from sqlalchemy import ForeignKey, String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

# === ServiceTicket model  ===
class ServiceTicket(db.Model):
    __tablename__ = "service_ticket"
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(String(200), nullable=False)
    date: Mapped[str] = mapped_column(String(50), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customer.id"))
    parts = relationship("ServiceTicketInventory", back_populates="ticket")
mechanics = relationship("Mechanic", secondary="service_mechanic", back_populates="tickets")


# === Inventory model ===
class Inventory(db.Model):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    tickets = relationship("ServiceTicketInventory", back_populates="part")


# === Junction model ===
class ServiceTicketInventory(db.Model):
    __tablename__ = "service_ticket_inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    service_ticket_id: Mapped[int] = mapped_column(ForeignKey("service_ticket.id"))
    inventory_id: Mapped[int] = mapped_column(ForeignKey("inventory.id"))
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    ticket = relationship("ServiceTicket", back_populates="parts")
    part = relationship("Inventory", back_populates="tickets")
