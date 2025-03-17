from typing import Dict, Any
from .spam_detection.spam_detector import SpamDetector
from backend.ml_backend.model import DisasterClassifier  # Import your existing disaster classifier

class DisasterPredictionPipeline:
    def __init__(self):
        self.spam_detector = SpamDetector()
        self.disaster_classifier = DisasterClassifier()
    
    def process_post(self, text: str) -> Dict[str, Any]:
        """
        Process a social media post through spam detection and disaster classification.
        
        Args:
            text (str): The text content of the social media post
            
        Returns:
            Dict containing:
            - is_spam (bool): Whether the post is spam
            - spam_confidence (float): Confidence score for spam detection
            - is_verified (bool): Whether the news is verified
            - verification_info (dict): Information about news verification
            - disaster_prediction (dict): Disaster classification results (if not spam)
        """
        # First check for spam and verify news
        is_spam, spam_confidence, verification_info = self.spam_detector.is_spam(text)
        
        result = {
            'is_spam': is_spam,
            'spam_confidence': spam_confidence,
            'is_verified': verification_info.get('news_confidence', 0) > 0.5,
            'verification_info': verification_info
        }
        
        # Only perform disaster classification if not spam and news is verified
        if not is_spam and result['is_verified']:
            disaster_prediction = self.disaster_classifier.predict(text)
            result['disaster_prediction'] = disaster_prediction
        else:
            result['disaster_prediction'] = None
            
        return result
    
    def train_spam_detector(self, training_data):
        """Train the spam detection model with new data."""
        self.spam_detector.train(training_data)
    
    def train_disaster_classifier(self, training_data):
        """Train the disaster classification model with new data."""
        self.disaster_classifier.train(training_data) 