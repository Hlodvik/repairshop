from flask import request, jsonify
from sqlalchemy import select
from ..db import SessionLocal
from ..models import Customer, Ticket
from .schemas import CustomerSchema, LoginSchema
from marshmallow import ValidationError
from . import customer_bp
from app.extensions import limiter, cache
from app.utils.auth import encode_token, token_required
from ..service_ticket.schemas import TicketSchema  

ticket_schema = TicketSchema(many=True)

customer_schema = CustomerSchema()
customer_list_schema = CustomerSchema(many=True)

login_schema = LoginSchema()  

@customer_bp.route("/login", methods=['POST'])
def login():
    try: # Using load() here to trigger ValidationError for login schema validation
        data = login_schema.load(request.json)
        email = data['email']
        password = data['password']
    except ValidationError as e:
            return jsonify({'message': e.messages}), 400

    with SessionLocal() as session:
        query = select(Customer).where(Customer.email == email)
        customer = session.execute(query).scalar_one_or_none()

        if customer and customer.password == password:
            token = encode_token(customer.id)

            return jsonify({
                "status": "success",
                "message": "Successfully Logged In",
                "auth_token": token
            }), 200
        else:
            return jsonify({'message': "Invalid email or password"}), 401

# cache customer list 
@customer_bp.route('/', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def get_customers():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    offset = (page - 1) * per_page

    with SessionLocal() as session:
        stmt = select(Customer).offset(offset).limit(per_page)
        customers = session.execute(stmt).scalars().all()
        return jsonify(customer_list_schema.dump(customers)), 200

@customer_bp.route('/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    with SessionLocal() as session:
        customer = session.get(Customer, customer_id)
        if customer is None:
            return jsonify({'error': 'Customer not found'}), 404
        return jsonify(customer_schema.dump(customer)), 200

# limit new customer creation
@customer_bp.route('/', methods=['POST'])
@limiter.limit("10 per hour")
def create_customer():
    data = request.get_json()
    errors = customer_schema.validate(data)
    if errors:
        return jsonify(errors), 400

    new_customer = Customer(**data)
    with SessionLocal() as session:
        session.add(new_customer)
        session.commit()
        return jsonify({'id': new_customer.id}), 201

# limit updates
@customer_bp.route('/<int:customer_id>', methods=['PUT'])
@limiter.limit("15 per hour")
def update_customer(customer_id):
    data = request.get_json()
    with SessionLocal() as session:
        customer = session.get(Customer, customer_id)
        if customer is None:
            return jsonify({'error': 'Customer not found'}), 404

        for field in ['name', 'email', 'address']:
            if field in data:
                setattr(customer, field, data[field])

        session.commit()
        return jsonify({'message': 'Customer updated'}), 200

# Limit delete  
@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
@limiter.limit("5 per hour")
@token_required
def delete_customer(customer_id):
    with SessionLocal() as session:
        customer = session.get(Customer, customer_id)
        if customer is None:
            return jsonify({'error': 'Customer not found'}), 404

        session.delete(customer)
        session.commit()
        return jsonify({'message': 'Customer deleted'}), 200


@customer_bp.route("/my-tickets", methods=["GET"])
@token_required
def get_my_tickets(customer_id):
    with SessionLocal() as session:
        stmt = select(Ticket).where(Ticket.customer_id == int(customer_id))
        tickets = session.execute(stmt).scalars().all()
        return jsonify(ticket_schema.dump(tickets)), 200