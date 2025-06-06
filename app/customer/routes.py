from flask import request, jsonify
from sqlalchemy import select
from ..db import SessionLocal
from ..models import Customer
from .schemas import CustomerSchema
from . import customer_bp

customer_schema = CustomerSchema()
customer_list_schema = CustomerSchema(many=True)
 
@customer_bp.route('/', methods=['GET'])
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

 
@customer_bp.route('/', methods=['POST'])
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

 
@customer_bp.route('/<int:customer_id>', methods=['PUT'])
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
 
@customer_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    with SessionLocal() as session:
        customer = session.get(Customer, customer_id)
        if customer is None:
            return jsonify({'error': 'Customer not found'}), 404

        session.delete(customer)
        session.commit()
        return jsonify({'message': 'Customer deleted'}), 200
