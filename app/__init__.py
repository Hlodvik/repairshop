from flask import Flask
from .db import engine
from .models import Base
from .mechanic import mechanic_bp
from .service_ticket import service_ticket_bp
from .customer import customer_bp
from app.inventory import inventory_bp
from app.extensions import ma, limiter, cache

def create_app():
    app = Flask(__name__)
    ma.init_app(app) 
    limiter.init_app(app)
    cache.init_app(app)
    # Register blueprints
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")
    # Create tables
    Base.metadata.create_all(bind=engine)

    return app