from flask import request, jsonify
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Mechanic
from . import mechanic_bp
from .schemas import MechanicSchema
from app.extensions import limiter, cache

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
 # limit to avoid spamming new mechanic creations
@mechanic_bp.route('/', methods=['POST']) 
def create_mechanic():
    data = request.get_json()
    with SessionLocal() as session:
        mechanic = mechanic_schema.load(data, session=session)
        session.add(mechanic)
        session.commit()
        return jsonify(mechanic_schema.dump(mechanic)), 201

 
#caches, paginates, and uses ilike
@mechanic_bp.route('/', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def get_mechanics():
    name_query = request.args.get('name')
    specialty_query = request.args.get('specialty')

    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    offset = (page - 1) * per_page

    with SessionLocal() as session:
        stmt = select(Mechanic)

        if name_query:
            stmt = stmt.where(Mechanic.name.ilike(f"%{name_query}%"))
        if specialty_query:
            stmt = stmt.where(Mechanic.specialty.ilike(f"%{specialty_query}%"))

        stmt = stmt.offset(offset).limit(per_page)

        mechanics = session.execute(stmt).scalars().all()
        return jsonify(mechanics_schema.dump(mechanics)), 200
    

#get by mechanic by id
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

@mechanic_bp.route('/most-active', methods=['GET'])
def most_active_mechanics():
    with SessionLocal() as session:
        mechanics = session.query(Mechanic).all()
        mechanics.sort(key=lambda m: len(m.tickets), reverse=True)
        return jsonify(mechanic_schema.dump(mechanics, many=True)), 200