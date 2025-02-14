from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    
    CORS(app, resources={r"/filter": {"origins": "*"}})

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app