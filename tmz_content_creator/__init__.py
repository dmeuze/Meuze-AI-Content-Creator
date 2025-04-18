from flask import Flask
from .config.config import Config
from .services.content_service import ContentService

def create_app(test_config=None):
    app = Flask(__name__, 
                instance_relative_config=True,
                static_folder='static',
                template_folder='templates')
    
    if test_config is None:
        app.config.from_object(Config)
    else:
        app.config.from_mapping(test_config)
    
    # Initialize services
    app.content_service = ContentService()
    
    # Register blueprints
    from .routes import main
    app.register_blueprint(main.bp)
    
    return app 