from flask import Flask
from flask_cors import CORS
from .config.config import Config
from .services.openai_service import OpenAIService
from .services.content_service import ContentService

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configure session
    app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key
    
    # Initialize services
    app.openai_service = OpenAIService()
    app.content_service = ContentService(app.openai_service)
    
    # Register blueprints
    from .routes.main import bp as main_bp
    app.register_blueprint(main_bp)
    
    CORS(app)
    return app 