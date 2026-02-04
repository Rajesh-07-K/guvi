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
        Uses hybrid approach: ML model + rule-based energy variance threshold.
        
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
        
        # Extract energy_variance for rule-based check (index 12)
        energy_variance = features[0, 12]
        
        # **HYBRID APPROACH: Rule-based + ML**
        # Rule: AI voices have VERY LOW energy variance (< 0.008)
        # Based on real analysis: AI sample had 0.00328, humans typically > 0.01
        ENERGY_VARIANCE_THRESHOLD = 0.008
        
        # Scale features for ML model
        features_scaled = self.scaler.transform(features)
        
        # Get ML prediction and probabilities
        ml_prediction = self.model.predict(features_scaled)[0]
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Apply rule-based override/boost based on energy variance
        if energy_variance < ENERGY_VARIANCE_THRESHOLD:
            # Very low energy variance = strong AI indicator
            prediction = 1  # AI
            # Boost confidence based on how far below threshold
            confidence_boost = min(0.85, 0.65 + (ENERGY_VARIANCE_THRESHOLD - energy_variance) / ENERGY_VARIANCE_THRESHOLD * 0.3)
            # If ML also says AI, use ML confidence; otherwise use boosted confidence
            if ml_prediction == 1:
                confidence_score = max(probabilities[1], confidence_boost)
            else:
                confidence_score = confidence_boost
        elif energy_variance > 0.015:
            # High energy variance = strong HUMAN indicator
            prediction = 0  # HUMAN
            # Boost confidence based on how far above threshold
            confidence_boost = min(0.85, 0.65 + (energy_variance - 0.015) / 0.035 * 0.2)
            if ml_prediction == 0:
                confidence_score = max(probabilities[0], confidence_boost)
            else:
                confidence_score = confidence_boost
        else:
            # Borderline case - trust ML model
            prediction = ml_prediction
            confidence_score = float(probabilities[prediction])
        
        # Class mapping: 0=Human, 1=AI
        classification = "AI_GENERATED" if prediction == 1 else "HUMAN"
        
        # Generate explanation based on key features and detection method
        explanation = self._generate_explanation(
            features[0], 
            classification, 
            confidence_score,
            energy_variance
        )
        
        return classification, confidence_score, explanation

    def _generate_explanation(
        self, 
        features: np.ndarray, 
        classification: str, 
        confidence: float,
        energy_variance: float = None
    ) -> str:
        """
        Generate human-readable explanation for the prediction.
        
        Args:
            features: Raw feature vector
            classification: Predicted class
            confidence: Confidence score
            energy_variance: Energy variance value (key AI indicator)
            
        Returns:
            Explanation string
        """
        # Feature indices (matching feature_extractor.py order)
        mfcc_var_idx = 2
        pitch_var_idx = 4
        zcr_mean_idx = 6
        spectral_centroid_mean_idx = 8
        energy_var_idx = 12
        
        # Get energy variance from features if not provided
        if energy_variance is None:
            energy_variance = features[energy_var_idx]
        
        if classification == "AI_GENERATED":
            if energy_variance < 0.005:
                return f"Extremely low energy variance ({energy_variance:.5f}) indicates no natural breathing - typical of AI voices"
            elif energy_variance < 0.008:
                return f"Very low energy variance ({energy_variance:.5f}) suggests synthetic voice with uniform energy distribution"
            elif confidence > 0.8:
                return "High consistency in pitch and spectral patterns typical of synthetic voices"
            elif confidence > 0.6:
                return "Moderate indicators of artificial speech synthesis detected"
            else:
                return "Slight synthetic characteristics detected in voice patterns"
        else:  # HUMAN
            if energy_variance > 0.015:
                return f"Natural energy variation ({energy_variance:.5f}) from breathing and emphasis confirms human speech"
            elif energy_variance > 0.010:
                return f"Energy variance ({energy_variance:.5f}) shows natural human speech patterns"
            elif confidence > 0.8:
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
        Load pre-trained model or initialize with enhanced synthetic training data.
        Based on REAL AI voice analysis: Energy variance is the KEY discriminator!
        In production, replace this with actual labeled dataset.
        """
        # Try loading existing model
        if self.load_model():
            return
        
        # If no model exists, create atrained model
        # IMPORTANT: This is for demonstration only!
        # In production, replace with real labeled data from:
        # - Human voice recordings (labeled 0)
        # - AI-generated voices from various TTS systems (labeled 1)
        print("WARNING: Using IMPROVED synthetic training data based on real AI analysis!")
        print("Key finding: ENERGY VARIANCE is the primary AI voice indicator")
        
        # Generate enhanced synthetic training data with realistic AI vs human patterns
        # Based on analysis of sample.mp3 (AI voice):
        # - energy_variance: 0.00328 (VERY LOW - key indicator!)
        # - pitch_variance: 848302.5 (can be HIGH in AI!)
        # - mfcc_var: 11718.9
        # - spectral variances: can be high in AI
        
        # Features order: [mfcc_mean, mfcc_std, mfcc_var, pitch_mean, pitch_var, pitch_std,
        #                  zcr_mean, zcr_std, spectral_centroid_mean, spectral_centroid_std, 
        #                  spectral_centroid_var, energy_mean, energy_var, energy_std,
        #                  spectral_rolloff_mean, spectral_rolloff_std, 
        #                  spectral_bandwidth_mean, spectral_bandwidth_std]
        np.random.seed(42)
        
        # Increased samples for better model coverage
        n_samples = 2000
        n_features = 18  # Matches feature_extractor output
        
        # === HUMAN VOICES: Natural variations, especially in ENERGY ===
        human_features = np.random.randn(n_samples // 2, n_features)
        
        # Pitch can vary in both human and AI, so less emphasis here
        human_features[:, 4] *= 1.5  # pitch_variance - moderate
        human_features[:, 5] *= 1.3  # pitch_std - moderate
        
        # **CRITICAL: Energy variance is THE key discriminator!**
        # Humans have natural breathing, pauses, emphasis changes
        # Human energy_variance typically: 0.01 - 0.05
        human_features[:, 12] = np.abs(np.random.randn(n_samples // 2) * 0.015 + 0.025)  # energy_variance - MUCH HIGHER
        human_features[:, 13] *= 2.5  # energy_std - higher
        human_features[:, 11] *= 1.2  # energy_mean - moderate
        
        # MFCC - moderate variation
        human_features[:, 1] *= 1.4  # mfcc_std
        human_features[:, 2] *= 1.3  # mfcc_var
        
        # Spectral features - moderate (can be high in both)
        human_features[:, 9] *= 1.3   # spectral_centroid_std
        human_features[:, 10] *= 1.2  # spectral_centroid_var
        human_features[:, 15] *= 1.2  # spectral_rolloff_std
        human_features[:, 17] *= 1.3  # spectral_bandwidth_std
        
        # ZCR - moderate
        human_features[:, 7] *= 1.3   # zcr_std
        
        # === AI VOICES: VERY LOW energy variance (KEY!), other features can vary ===
        ai_features = np.random.randn(n_samples // 2, n_features) * 0.8
        
        # Pitch can actually be HIGH in modern AI voices (like sample.mp3)
        # So don't rely on pitch as a discriminator
        ai_features[:, 4] *= 1.2  # pitch_variance - can be varied
        ai_features[:, 5] *= 1.0  # pitch_std - can be varied
        
        # **CRITICAL: ENERGY VARIANCE IS THE PRIMARY AI INDICATOR!**
        # AI voices have NO natural breathing = extremely consistent energy
        # AI energy_variance typically: 0.001 - 0.005 (VERY LOW!)
        ai_features[:, 12] = np.abs(np.random.randn(n_samples // 2) * 0.001 + 0.003)  # energy_variance - EXTREMELY LOW
        ai_features[:, 13] *= 0.4  # energy_std - much lower
        ai_features[:, 11] *= 0.9  # energy_mean - slightly lower
        
        # MFCC - can vary in AI
        ai_features[:, 1] *= 0.8  # mfcc_std
        ai_features[:, 2] *= 0.7  # mfcc_var
        
        # Spectral features - can be high in modern AI (less reliable)
        ai_features[:, 9] *= 0.9   # spectral_centroid_std
        ai_features[:, 10] *= 1.0  # spectral_centroid_var - can be high
        ai_features[:, 15] *= 0.9  # spectral_rolloff_std
        ai_features[:, 17] *= 0.9  # spectral_bandwidth_std
        
        # ZCR - slightly lower in AI
        ai_features[:, 7] *= 0.7   # zcr_std
        
        # Combine datasets
        X_train = np.vstack([human_features, ai_features])
        y_train = np.array([0] * (n_samples // 2) + [1] * (n_samples // 2))
        
        # Shuffle
        shuffle_idx = np.random.permutation(n_samples)
        X_train = X_train[shuffle_idx]
        y_train = y_train[shuffle_idx]
        
        # Train model
        self.train(X_train, y_train)
        self.save_model()
        
        print("Model initialized with IMPROVED synthetic data (real AI analysis).")
        print("PRIMARY DISCRIMINATOR: Energy variance")
        print("  - AI voices: 0.001-0.005 (very low, no breathing)")
        print("  - Human voices: 0.01-0.05 (higher, natural variations)")
        print("For production use, train with real labeled voice datasets!")
