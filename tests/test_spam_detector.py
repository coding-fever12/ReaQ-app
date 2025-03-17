import pytest
from ..ml.spam_detection.spam_detector import SpamDetector
import os

@pytest.fixture
def spam_detector():
    return SpamDetector()

def test_preprocess_text(spam_detector):
    text = "CHECK THIS OUT!!! http://spam.com Buy now! #disaster"
    processed = spam_detector.preprocess_text(text)
    assert 'http' not in processed.lower()
    assert 'buy' in processed.lower()
    assert '!!!' not in processed

def test_extract_features(spam_detector):
    text = "URGENT! Massive earthquake hits California! Click here: http://news.com"
    features = spam_detector.extract_features(text)
    
    assert 'text_length' in features
    assert 'word_count' in features
    assert 'contains_url' in features
    assert features['exclamation_count'] == 2
    assert features['contains_url'] == 1

def test_verify_news(spam_detector):
    # Test with fake news
    fake_text = "Massive alien invasion in New York! Buy protection now!"
    is_real, confidence, articles = spam_detector.verify_news(fake_text)
    assert not is_real
    assert confidence == 0.0
    assert len(articles) == 0
    
    # Test with potential real news (note: this might need to be updated based on current events)
    real_text = "Earthquake reported in California today"
    is_real, confidence, articles = spam_detector.verify_news(real_text)
    # We don't assert the result as it depends on current news

def test_spam_detection(spam_detector):
    # Test obvious spam
    spam_text = "CLICK HERE!!! WIN $1000000 FREE!!! disaster alert!!!"
    is_spam, confidence, info = spam_detector.is_spam(spam_text)
    assert is_spam
    assert confidence > 0.5
    
    # Test potential legitimate news
    news_text = "A magnitude 6.2 earthquake has been reported in California. Local authorities are responding."
    is_spam, confidence, info = spam_detector.is_spam(news_text)
    # We don't assert the result as it depends on the model and current news

def test_model_training(spam_detector):
    # Test training with a small dataset
    training_data = [
        ("URGENT! Win prizes! Disaster strikes!!!", True),
        ("A 7.1 magnitude earthquake has been reported in Japan. Officials are assessing damage.", False),
        ("FREE MONEY! Natural disaster insurance! Act now!!!", True),
        ("Hurricane warning issued for Florida coast. Residents advised to evacuate.", False)
    ]
    
    # Train the model
    spam_detector.train(training_data)
    
    # Test prediction on new data
    test_text = "URGENT! Win free disaster relief! Click now!!!"
    is_spam, confidence, info = spam_detector.is_spam(test_text)
    assert is_spam
    assert confidence > 0.5

def test_model_persistence(spam_detector):
    # Test if model file is created after training
    training_data = [
        ("Spam disaster alert!!!", True),
        ("Real earthquake news", False)
    ]
    spam_detector.train(training_data)
    
    model_path = os.path.join('ml', 'spam_detection', 'models', 'spam_classifier.joblib')
    assert os.path.exists(model_path) 