from flask import request, jsonify
from . import service_ticket_bp
from app.models import db, Ticket, Mechanic
from .schemas import TicketSchema

ticket_schema = TicketSchema()
tickets_schema = TicketSchema(many=True)

@service_ticket_bp.route('/', methods=['POST'])
def create_ticket():
    data = request.get_json()
    ticket = ticket_schema.load(data, session=db.session)  # ✅ add session
    db.session.add(ticket)
    db.session.commit()
    return jsonify(ticket_schema.dump(ticket)), 201  # ✅ fix

@service_ticket_bp.route('/', methods=['GET'])
def get_tickets():
    tickets = Ticket.query.all()
    return jsonify(tickets_schema.dump(tickets))  # ✅ fix

@service_ticket_bp.route('/<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['PUT'])
def assign_mechanic(ticket_id, mechanic_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    if mechanic not in ticket.mechanics:
        ticket.mechanics.append(mechanic)
        db.session.commit()
    return jsonify(ticket_schema.dump(ticket))  # ✅ fix

@service_ticket_bp.route('/<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['PUT'])
def remove_mechanic(ticket_id, mechanic_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    mechanic = Mechanic.query.get_or_404(mechanic_id)
    if mechanic in ticket.mechanics:
        ticket.mechanics.remove(mechanic)
        db.session.commit()
    return jsonify(ticket_schema.dump(ticket))  # ✅ fix
