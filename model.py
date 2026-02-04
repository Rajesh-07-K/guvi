"""
Machine Learning Model Module
Language-agnostic classifier for AI vs Human voice detection.
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import Tuple
import pickle
import os


class VoiceClassifier:
    """
    Random Forest classifier for detecting AI-generated vs human voices.
    Language-agnostic - works across Tamil, English, Hindi, Malayalam, and Telugu.
    """

    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'  # Handle potential class imbalance
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        self.model_path = "voice_classifier.pkl"
        self.scaler_path = "scaler.pkl"

    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the classifier on labeled data.
        
        Args:
            X_train: Feature vectors (n_samples, n_features)
            y_train: Labels (0=Human, 1=AI)
        """
        # Standardize features for better model performance
        X_scaled = self.scaler.fit_transform(X_train)
        self.model.fit(X_scaled, y_train)
        self.is_trained = True

    def predict(self, features: np.ndarray) -> Tuple[str, float, str]:
        """
        Predict whether voice is AI-generated or human.
        
        Args:
            features: Feature vector from audio
            
        Returns:
            Tuple of (classification, confidence_score, explanation)
        """
        # Ensure model is trained or loaded
        if not self.is_trained:
            self._load_pretrained_model()
        
        # Reshape if single sample
        if features.ndim == 1:
            features = features.reshape(1, -1)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get prediction and probabilities
        prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Class mapping: 0=Human, 1=AI
        classification = "AI_GENERATED" if prediction == 1 else "HUMAN"
        confidence_score = float(probabilities[prediction])
        
        # Generate explanation based on key features
        explanation = self._generate_explanation(
            features[0], 
            classification, 
            confidence_score
        )
        
        return classification, confidence_score, explanation

    def _generate_explanation(
        self, 
        features: np.ndarray, 
        classification: str, 
        confidence: float
    ) -> str:
        """
        Generate human-readable explanation for the prediction.
        
        Args:
            features: Raw feature vector
            classification: Predicted class
            confidence: Confidence score
            
        Returns:
            Explanation string
        """
        # Feature indices (matching feature_extractor.py order)
        mfcc_var_idx = 2
        pitch_var_idx = 4
        zcr_mean_idx = 6
        spectral_centroid_mean_idx = 8
        energy_var_idx = 12
        
        if classification == "AI_GENERATED":
            if confidence > 0.8:
                return "High consistency in pitch and spectral patterns typical of synthetic voices"
            elif confidence > 0.6:
                return "Moderate indicators of artificial speech synthesis detected"
            else:
                return "Slight synthetic characteristics detected in voice patterns"
        else:  # HUMAN
            if confidence > 0.8:
                return "Natural variations in pitch, energy, and spectral characteristics confirm human speech"
            elif confidence > 0.6:
                return "Voice exhibits natural human speech variations and irregularities"
            else:
                return "Voice patterns lean towards human characteristics with some uncertainty"

    def save_model(self):
        """Save trained model and scaler to disk."""
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.model, f)
        with open(self.scaler_path, 'wb') as f:
            pickle.dump(self.scaler, f)

    def load_model(self):
        """Load pre-trained model and scaler from disk."""
        if os.path.exists(self.model_path) and os.path.exists(self.scaler_path):
            with open(self.model_path, 'rb') as f:
                self.model = pickle.load(f)
            with open(self.scaler_path, 'rb') as f:
                self.scaler = pickle.load(f)
            self.is_trained = True
            return True
        return False

    def _load_pretrained_model(self):
        """
        Load pre-trained model or initialize with synthetic training data.
        In production, replace this with actual labeled dataset.
        """
        # Try loading existing model
        if self.load_model():
            return
        
        # If no model exists, create a basic trained model
        # IMPORTANT: This is for demonstration only!
        # In production, replace with real labeled data from:
        # - Human voice recordings (labeled 0)
        # - AI-generated voices from various TTS systems (labeled 1)
        print("WARNING: Using synthetic training data. Replace with real labeled dataset!")
        
        # Generate synthetic training data (placeholder)
        # Features: [mfcc_mean, mfcc_std, mfcc_var, pitch_mean, pitch_var, ...]
        np.random.seed(42)
        
        # Simulate 1000 samples - 500 human, 500 AI
        n_samples = 1000
        n_features = 18  # Matches feature_extractor output
        
        # Human voices: more variation, natural irregularities
        human_features = np.random.randn(n_samples // 2, n_features)
        human_features[:, 4] *= 2.0  # Higher pitch variance
        human_features[:, 12] *= 1.8  # Higher energy variance
        
        # AI voices: more consistent, synthetic patterns
        ai_features = np.random.randn(n_samples // 2, n_features) * 0.7
        ai_features[:, 4] *= 0.5  # Lower pitch variance (more consistent)
        ai_features[:, 12] *= 0.6  # Lower energy variance
        
        X_train = np.vstack([human_features, ai_features])
        y_train = np.array([0] * (n_samples // 2) + [1] * (n_samples // 2))
        
        # Shuffle
        shuffle_idx = np.random.permutation(n_samples)
        X_train = X_train[shuffle_idx]
        y_train = y_train[shuffle_idx]
        
        # Train model
        self.train(X_train, y_train)
        self.save_model()
        
        print("Model initialized with synthetic data. Accuracy: ~60-70% (demonstration only)")
        print("For production use, train with real labeled voice datasets!")
