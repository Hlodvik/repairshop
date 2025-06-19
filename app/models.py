from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column


 
class Base(DeclarativeBase):
    pass
 
ticket_mechanic = Table(
    "ticket_mechanic",
    Base.metadata,
    Column("ticket_id", Integer, ForeignKey("tickets.id"), primary_key=True),
    Column("mechanic_id", Integer, ForeignKey("mechanics.id"), primary_key=True)
)
ticket_inventory = Table(
    "ticket_inventory",
    Base.metadata,
    Column("ticket_id", ForeignKey("tickets.id"), primary_key=True),
    Column("inventory_id", ForeignKey("inventory.id"), primary_key=True)
)
class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(360), nullable=False, unique=True)
    address: Mapped[str] = mapped_column(String(255), nullable=False)

class Mechanic(Base):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    tickets: Mapped[list["Ticket"]] = relationship(
        secondary=ticket_mechanic, back_populates="mechanics"
    )

class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)

    mechanics: Mapped[list["Mechanic"]] = relationship(
        secondary=ticket_mechanic, back_populates="tickets"
    )
    parts: Mapped[list["Inventory"]] = relationship(
        secondary=ticket_inventory,
        back_populates="tickets"
    )

class Inventory(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)

    tickets: Mapped[list["Ticket"]] = relationship(
        secondary=ticket_inventory,
        back_populates="parts"
    )
