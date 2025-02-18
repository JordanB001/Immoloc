from flask import Flask
from os import getenv
from dotenv import load_dotenv


def create_app():
    
    load_dotenv()
    try:
        isinstance(getenv('SECRET_KEY'), str)
        isinstance(getenv('API_KEY'), str)
    except Exception as e:
        raise Exception("Environment variables SECRET_KEY or API_KEY are not set properly.")
    
    app = Flask(__name__)

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
