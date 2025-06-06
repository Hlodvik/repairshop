from flask import request, jsonify
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Mechanic
from . import mechanic_bp
from .schemas import MechanicSchema

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    with SessionLocal() as session:
        mechanic = mechanic_schema.load(data, session=session)
        session.add(mechanic)
        session.commit()
        return jsonify(mechanic_schema.dump(mechanic)), 201

@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    with SessionLocal() as session:
        mechanics = session.execute(select(Mechanic)).scalars().all()
        return jsonify(mechanics_schema.dump(mechanics)), 200

@mechanic_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    with SessionLocal() as session:
        mechanic = session.get(Mechanic, id)
        if not mechanic:
            return jsonify({'error': 'Mechanic not found'}), 404
        return jsonify(mechanic_schema.dump(mechanic)), 200

@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    data = request.get_json()
    with SessionLocal() as session:
        mechanic = session.get(Mechanic, id)
        if not mechanic:
            return jsonify({'error': 'Mechanic not found'}), 404

        for key, value in data.items():
            setattr(mechanic, key, value)

        session.commit()
        return jsonify(mechanic_schema.dump(mechanic)), 200

@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    with SessionLocal() as session:
        mechanic = session.get(Mechanic, id)
        if not mechanic:
            return jsonify({'error': 'Mechanic not found'}), 404

        session.delete(mechanic)
        session.commit()
        return jsonify({'message': 'Mechanic deleted'}), 200
