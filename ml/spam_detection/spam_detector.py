import re
import requests
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from textblob import TextBlob
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
import joblib
import os

class SpamDetector:
    def __init__(self):
        # Download required NLTK data
        nltk.download('punkt')
        nltk.download('stopwords')
        nltk.download('averaged_perceptron_tagger')
        
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(max_features=5000)
        self.classifier = RandomForestClassifier(n_estimators=100)
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.model_path = os.path.join('ml', 'spam_detection', 'models')
        
        # Load pre-trained model if exists
        if os.path.exists(os.path.join(self.model_path, 'spam_classifier.joblib')):
            self.load_model()
    
    def preprocess_text(self, text: str) -> str:
        """Preprocess the text by removing special characters, links, etc."""
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'http\S+|www\S+|https\S+', '', text, flags=re.MULTILINE)
        
        # Remove special characters and numbers
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\d+', '', text)
        
        # Tokenize and remove stop words
        tokens = word_tokenize(text)
        tokens = [t for t in tokens if t not in self.stop_words]
        
        return ' '.join(tokens)
    
    def extract_features(self, text: str) -> Dict:
        """Extract features from the text for spam detection."""
        # Basic text features
        processed_text = self.preprocess_text(text)
        blob = TextBlob(processed_text)
        
        features = {
            'text_length': len(text),
            'word_count': len(text.split()),
            'avg_word_length': sum(len(word) for word in text.split()) / len(text.split()) if text else 0,
            'contains_url': 1 if re.search(r'http\S+|www\S+|https\S+', text) else 0,
            'sentiment_polarity': blob.sentiment.polarity,
            'sentiment_subjectivity': blob.sentiment.subjectivity,
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'capital_ratio': sum(1 for c in text if c.isupper()) / len(text) if text else 0
        }
        
        return features
    
    def verify_news(self, text: str) -> Tuple[bool, float, List[Dict]]:
        """Verify if the disaster news is true by checking against news APIs."""
        try:
            # Extract potential location and disaster type
            blob = TextBlob(text)
            locations = [word for (word, tag) in blob.tags if tag in ['NNP', 'GPE']]
            
            # Common disaster keywords
            disaster_keywords = ['earthquake', 'flood', 'hurricane', 'tornado', 'wildfire', 
                               'tsunami', 'landslide', 'storm', 'cyclone']
            
            # Find disaster keywords in text
            found_disasters = [word for word in disaster_keywords if word in text.lower()]
            
            if not found_disasters or not locations:
                return False, 0.0, []
            
            # Construct search query
            query = f"{' '.join(locations)} {' '.join(found_disasters)}"
            
            # Search news from the last 24 hours
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': query,
                'apiKey': self.news_api_key,
                'from': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'),
                'sortBy': 'relevancy',
                'language': 'en'
            }
            
            response = requests.get(url, params=params)
            news_data = response.json()
            
            if news_data.get('status') == 'ok':
                articles = news_data.get('articles', [])
                if articles:
                    # Calculate confidence based on number and relevancy of news articles
                    confidence = min(len(articles) / 5.0, 1.0)  # Cap at 1.0
                    return True, confidence, articles[:5]  # Return top 5 related articles
            
            return False, 0.0, []
            
        except Exception as e:
            print(f"Error verifying news: {str(e)}")
            return False, 0.0, []
    
    def is_spam(self, text: str) -> Tuple[bool, float, Dict]:
        """
        Check if the text is spam and verify the news.
        Returns: (is_spam, confidence, verification_info)
        """
        # First verify if it's real news
        is_real_news, news_confidence, related_articles = self.verify_news(text)
        
        if not is_real_news:
            return True, 0.9, {
                'reason': 'No verification from reliable news sources',
                'news_confidence': news_confidence,
                'related_articles': related_articles
            }
        
        # Extract features for spam detection
        features = self.extract_features(text)
        
        # Convert features to DataFrame
        features_df = pd.DataFrame([features])
        
        # Make prediction
        try:
            spam_probability = self.classifier.predict_proba(features_df)[0][1]
            is_spam = spam_probability > 0.5
            
            return is_spam, spam_probability, {
                'reason': 'Spam detection model classification',
                'news_confidence': news_confidence,
                'related_articles': related_articles,
                'feature_importance': dict(zip(features.keys(), 
                                            self.classifier.feature_importances_))
            }
        except:
            # If model not trained yet, use rule-based approach
            spam_indicators = {
                'excessive_punctuation': features['exclamation_count'] > 3,
                'all_caps_ratio': features['capital_ratio'] > 0.5,
                'extreme_sentiment': abs(features['sentiment_polarity']) > 0.8,
                'high_subjectivity': features['sentiment_subjectivity'] > 0.8
            }
            
            spam_score = sum(spam_indicators.values()) / len(spam_indicators)
            is_spam = spam_score > 0.5
            
            return is_spam, spam_score, {
                'reason': 'Rule-based classification (model not trained)',
                'news_confidence': news_confidence,
                'related_articles': related_articles,
                'spam_indicators': spam_indicators
            }
    
    def train(self, training_data: List[Tuple[str, bool]]):
        """Train the spam detection model."""
        texts, labels = zip(*training_data)
        
        # Extract features for all texts
        features_list = [self.extract_features(text) for text in texts]
        features_df = pd.DataFrame(features_list)
        
        # Train the classifier
        self.classifier.fit(features_df, labels)
        
        # Save the model
        os.makedirs(self.model_path, exist_ok=True)
        joblib.dump(self.classifier, os.path.join(self.model_path, 'spam_classifier.joblib'))
    
    def load_model(self):
        """Load the pre-trained model."""
        model_file = os.path.join(self.model_path, 'spam_classifier.joblib')
        if os.path.exists(model_file):
            self.classifier = joblib.load(model_file)
        else:
            print("No pre-trained model found. Will use rule-based classification until trained.") 