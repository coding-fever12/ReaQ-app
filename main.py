import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from backend.src.main import create_app as create_disaster_app
from backend.flask_app.app import app as ml_prediction_app
from backend.ml_backend.api import app as social_media_app

# Load environment variables
load_dotenv()

def create_integrated_app():
    # Create the main Flask application
    app = Flask(__name__)
    CORS(app)

    # Register the disaster management blueprint
    disaster_app = create_disaster_app()
    app.register_blueprint(disaster_app, url_prefix='/disaster')

    # Register the ML prediction blueprint
    app.register_blueprint(ml_prediction_app, url_prefix='/ml')

    # Register the social media analysis blueprint
    app.register_blueprint(social_media_app, url_prefix='/social')

    @app.route('/')
    def home():
        return {
            'status': 'ok',
            'message': 'Disaster Management System API',
            'endpoints': {
                'disaster_management': '/disaster',
                'ml_predictions': '/ml',
                'social_media_analysis': '/social'
            }
        }

    return app

if __name__ == '__main__':
    app = create_integrated_app()
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug) 