import os
from flask import Flask, jsonify
from app.errors.handlers import APIError
from app.core.logging import configure_logging
from app.api.v1.users.route import users_bp
from app.api.v1.auth.route import auth_bp
from app.core.config import config_map
from .extensions import db, migrate, jwt, cors, limiter, talisman


env = os.getenv("FLASK_ENV", "development")

def create_app():
    app = Flask(__name__)
    app.config.from_object(config_map[env])

    @app.errorhandler(APIError)
    def handle_api_errors(error):
        return jsonify(error.to_json()), error.status_code

    # Configure logging
    configure_logging()
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, origins=app.config['CORS_ORIGINS'], supports_credentials=app.config['CORS_SUPPORTS_CREDENTIALS'])
    limiter.init_app(app)
    
    # Initialize Talisman (security headers)
    if app.config.get('TALISMAN_FORCE_HTTPS'):
        talisman.init_app(
            app,
            force_https=app.config['TALISMAN_FORCE_HTTPS'],
            strict_transport_security=app.config['TALISMAN_STRICT_TRANSPORT_SECURITY'],
            content_security_policy=app.config['TALISMAN_CONTENT_SECURITY_POLICY']
        )
    
    # Import models
    from app.modules.users import model

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)

    return app