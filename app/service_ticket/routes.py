from flask import request, jsonify
from sqlalchemy import select
from app.db import SessionLocal
from app.models import Ticket, Mechanic, Inventory
from . import service_ticket_bp
from .schemas import TicketSchema

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)

 
@service_ticket_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.get_json()
    with SessionLocal() as session:
        ticket = ticket_schema.load(data, session=session)
        session.add(ticket)
        session.commit()
        return jsonify(ticket_schema.dump(ticket)), 201
 
@service_ticket_bp.route('/', methods=['GET'])
def get_tickets():
    with SessionLocal() as session:
        tickets = session.execute(select(Ticket)).scalars().all()
        return jsonify(tickets_schema.dump(tickets)), 200
 
@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    with SessionLocal() as session:
        ticket = session.get(Ticket, ticket_id)
        mechanic = session.get(Mechanic, mechanic_id)

        if not ticket or not mechanic:
            return jsonify({'error': 'Ticket or Mechanic not found'}), 404

        if mechanic not in ticket.mechanics:
            ticket.mechanics.append(mechanic)
            session.commit()

        return jsonify(ticket_schema.dump(ticket)), 200
 
@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    with SessionLocal() as session:
        ticket = session.get(Ticket, ticket_id)
        mechanic = session.get(Mechanic, mechanic_id)

        if not ticket or not mechanic:
            return jsonify({'error': 'Ticket or Mechanic not found'}), 404

        if mechanic in ticket.mechanics:
            ticket.mechanics.remove(mechanic)
            session.commit()

        return jsonify(ticket_schema.dump(ticket)), 200

@service_ticket_bp.route('/<int:ticket_id>/add-part/<int:part_id>', methods=['POST'])
def add_part_to_ticket(ticket_id, part_id):
    with SessionLocal() as session:
        ticket = session.get(Ticket, ticket_id)
        part = session.get(Inventory, part_id)

        if not ticket or not part:
            return jsonify({'error': 'Ticket or part not found'}), 404

        if part not in ticket.parts:
            ticket.parts.append(part)
            session.commit()

        return jsonify({'message': f'Part {part.name} added to ticket {ticket.id}'})