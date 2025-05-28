from flask import request, jsonify
from . import mechanic_bp
from ..models import db, Mechanic
from .schemas import MechanicSchema

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)

@mechanic_bp.route('/', methods=['POST'])
def create_mechanic():
    data = request.get_json()
    mechanic = mechanic_schema.load(data, session=db.session)
    db.session.add(mechanic)
    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic)), 201

@mechanic_bp.route('/', methods=['GET'])
def get_mechanics():
    all_mechanics = Mechanic.query.all()
    return jsonify(mechanics_schema.dump(all_mechanics))

@mechanic_bp.route('/<int:id>', methods=['PUT'])
def update_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    data = request.get_json()
    for key, value in data.items():
        setattr(mechanic, key, value)
    db.session.commit()
    return jsonify(mechanic_schema.dump(mechanic))

@mechanic_bp.route('/<int:id>', methods=['DELETE'])
def delete_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    db.session.delete(mechanic)
    db.session.commit()
    return jsonify({'message': 'Mechanic deleted'})


@mechanic_bp.route('/<int:id>', methods=['GET'])
def get_mechanic(id):
    mechanic = Mechanic.query.get_or_404(id)
    return jsonify(mechanic_schema.dump(mechanic))