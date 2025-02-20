from flask import Flask
from flask_cors import CORS
from os import getenv
from dotenv import load_dotenv


def create_app() -> Flask:
    
    load_dotenv()
    if not isinstance(getenv('SECRET_KEY'), str) or not isinstance(getenv('API_KEY'), str):
        raise ValueError("Environment variables SECRET_KEY or API_KEY are not set properly.")    
    
    app: Flask = Flask(__name__)
    CORS(app)
    
    #Updates the config
    app.config.from_mapping(
        SECRET_KEY=str(getenv('SECRET_KEY'))
    )

    #Register Blueprints on the application
    from .routes import analyzer, estimate, generate
    
    app.register_blueprint(analyzer.bp)
    app.register_blueprint(estimate.bp)
    app.register_blueprint(generate.bp)   
    
    return app
