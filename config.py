import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017')
MONGODB_DB = os.getenv('MONGODB_DB', 'disaster_connect')

# API Configuration
API_VERSION = 'v1'
API_PREFIX = f'/api/{API_VERSION}'

# ML Model Configuration
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'ml', 'models')
DATASET_PATH = os.path.join(os.path.dirname(__file__), 'ml', 'dataset')

# Twitter API Configuration
TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

# Flask Configuration
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-here')
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Frontend Configuration
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:3000')

# Mobile App Configuration
MOBILE_APP_API_URL = os.getenv('MOBILE_APP_API_URL', 'http://localhost:5000')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.path.join(os.path.dirname(__file__), 'logs', 'app.log')

# Security Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-jwt-secret-key')
JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour

# Disaster Types
DISASTER_TYPES = [
    'earthquake',
    'flood',
    'hurricane',
    'tornado',
    'wildfire',
    'tsunami',
    'volcanic_eruption',
    'other'
]

# Resource Types
RESOURCE_TYPES = [
    'medical',
    'food',
    'water',
    'shelter',
    'rescue',
    'transportation',
    'other'
]

# Alert Levels
ALERT_LEVELS = [
    'low',
    'medium',
    'high',
    'critical'
]

# Create necessary directories
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
os.makedirs(MODEL_PATH, exist_ok=True)
os.makedirs(DATASET_PATH, exist_ok=True) 