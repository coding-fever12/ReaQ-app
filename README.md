# DisasterConnect - Integrated Disaster Management System

This is an integrated disaster management system that combines social media analysis for disaster prediction with a comprehensive disaster management platform.

## Project Structure

```
integrated-project/
├── backend/           # Backend API and server code
├── frontend/         # Web application frontend
├── mobile-app/       # Mobile application
├── ml/              # Machine learning models and notebooks
├── utils/           # Shared utilities and helper functions
├── docs/            # Documentation
├── tests/           # Test suites
└── scripts/         # Utility scripts
```

## Features

1. **Disaster Prediction**
   - Social media analysis for disaster prediction
   - Machine learning models for disaster classification
   - Real-time monitoring and alerts

2. **Disaster Management**
   - Resource allocation and tracking
   - Emergency response coordination
   - Community engagement platform
   - Real-time updates and notifications

3. **Data Management**
   - MongoDB database integration
   - Data collection and processing
   - Analytics and reporting

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- MongoDB
- Android Studio (for mobile app development)

### Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd integrated-project
```

2. Set up the backend:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
```

4. Set up the mobile app:
```bash
cd mobile-app
npm install
```

5. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

### Running the Application

1. Start the backend server:
```bash
cd backend
python main.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Run the mobile app:
```bash
cd mobile-app
npm run android  # or npm run ios
```

## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Security

Please read [SECURITY.md](SECURITY.md) for details on our security policy and how to report security vulnerabilities. 