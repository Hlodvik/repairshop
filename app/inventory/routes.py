from flask import request, jsonify
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Inventory
from . import inventory_bp
from .schemas import InventorySchema

inventory_schema = InventorySchema()
inventory_list_schema = InventorySchema(many=True)

@inventory_bp.route('/', methods=['POST'])
def create_inventory():
    data = request.get_json()
    with SessionLocal() as session:
        item = inventory_schema.load(data, session=session)
        session.add(item)
        session.commit()
        return jsonify(inventory_schema.dump(item)), 201

@inventory_bp.route('/', methods=['GET'])
def get_inventory():
    with SessionLocal() as session:
        items = session.execute(select(Inventory)).scalars().all()
        return jsonify(inventory_list_schema.dump(items)), 200

@inventory_bp.route('/<int:id>', methods=['GET'])
def get_inventory_item(id):
    with SessionLocal() as session:
        item = session.get(Inventory, id)
        if not item:
            return jsonify({"error": "Part not found"}), 404
        return jsonify(inventory_schema.dump(item)), 200

@inventory_bp.route('/<int:id>', methods=['PUT'])
def update_inventory_item(id):
    data = request.get_json()
    with SessionLocal() as session:
        item = session.get(Inventory, id)
        if not item:
            return jsonify({"error": "Part not found"}), 404

        for field in ['name', 'price']:
            if field in data:
                setattr(item, field, data[field])
        session.commit()
        return jsonify(inventory_schema.dump(item)), 200

@inventory_bp.route('/<int:id>', methods=['DELETE'])
def delete_inventory_item(id):
    with SessionLocal() as session:
        item = session.get(Inventory, id)
        if not item:
            return jsonify({"error": "Part not found"}), 404
        session.delete(item)
        session.commit()
        return jsonify({"message": "Part deleted"}), 200