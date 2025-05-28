# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
# from datetime import date
# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
# from marshmallow import fields

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@localhost:3306/repairshop'

# class Base(DeclarativeBase):
#     pass

# db = SQLAlchemy(model_class=Base)
# db.init_app(app)

# # --- MODELS ---

# class Customer(Base):
#     __tablename__ = 'customers'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(db.String(255), nullable=False)
#     email: Mapped[str] = mapped_column(db.String(360), nullable=False, unique=True)
#     DOB: Mapped[date]
#     password: Mapped[str] = mapped_column(db.String(255), nullable=False)


# class Mechanic(Base):
#     __tablename__ = 'mechanics'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     name: Mapped[str] = mapped_column(db.String(255), nullable=False)


# class Ticket(Base):
#     __tablename__ = 'tickets'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     customer_id: Mapped[int] = mapped_column(db.ForeignKey('customers.id'), nullable=False)
#     description: Mapped[str] = mapped_column(db.String(255), nullable=False)
#     status: Mapped[str] = mapped_column(db.String(50), nullable=False)
#     mechanic_id: Mapped[int] = mapped_column(db.ForeignKey('mechanics.id'), nullable=False)

# # --- SCHEMAS ---

# class CustomerSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Customer
#         load_instance = True

#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True)
#     email = fields.Email(required=True)
#     DOB = fields.Date(required=True)
#     password = fields.Str(required=True)

# class MechanicSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Mechanic
#         load_instance = True

#     id = fields.Int(dump_only=True)
#     name = fields.Str(required=True)

# class TicketSchema(SQLAlchemyAutoSchema):
#     class Meta:
#         model = Ticket
#         load_instance = True

#     id = fields.Int(dump_only=True)
#     customer_id = fields.Int(required=True)
#     description = fields.Str(required=True)
#     status = fields.Str(required=True)
#     mechanic_id = fields.Int(required=True)

# # --- INIT DB ---
# with app.app_context():
#     db.create_all()

# # --- RUN APP ---
# if __name__ == '__main__':
#     app.run(debug=True)