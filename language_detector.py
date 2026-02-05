"""
Language Detection Module
Detects the language of audio from acoustic features.
Supports: English, Tamil, Malayalam, Hindi, Telugu
"""

import librosa
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os
import io
from typing import Tuple, Optional


class LanguageDetector:
    """
    Detects the language of audio using acoustic features.
    Trained to distinguish between English, Tamil, Malayalam, Hindi, and Telugu.
    """
    
    # Language mapping
    LANGUAGES = ["English", "Tamil", "Malayalam", "Hindi", "Telugu"]
    LANGUAGE_TO_IDX = {lang: idx for idx, lang in enumerate(LANGUAGES)}
    IDX_TO_LANGUAGE = {idx: lang for idx, lang in enumerate(LANGUAGES)}
    
    def __init__(self):
        self.classifier = None
        self.scaler = None
        self.is_trained = False
        
    def extract_language_features(self, audio_bytes: bytes) -> np.ndarray:
        """
        Extract language-specific acoustic features from audio.
        
        Features include:
        - Spectral features (centroid, rolloff, bandwidth)
        - MFCC statistics (different languages have distinct phonetic patterns)
        - Pitch characteristics (tonal languages have different pitch patterns)
        - Rhythm features (zero-crossing rate, tempo)
        - Formant-related features
        
        Args:
            audio_bytes: Raw audio file bytes
            
        Returns:
            Feature vector for language classification
        """
        # Load audio
        y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None, mono=True)
        
        features = []
        
        # 1. MFCC Statistics (13 coefficients)
        # Different languages have distinct phonetic patterns
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features.extend([
            np.mean(mfcc),
            np.std(mfcc),
            np.median(mfcc),
            np.max(mfcc),
            np.min(mfcc)
        ])
        
        # Individual MFCC coefficient statistics (first 5 coefficients)
        for i in range(5):
            features.extend([
                np.mean(mfcc[i]),
                np.std(mfcc[i])
            ])
        
        # 2. Spectral Features
        # Spectral Centroid (brightness of sound)
        spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        features.extend([
            np.mean(spectral_centroid),
            np.std(spectral_centroid),
            np.median(spectral_centroid)
        ])
        
        # Spectral Rolloff
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        features.extend([
            np.mean(spectral_rolloff),
            np.std(spectral_rolloff)
        ])
        
        # Spectral Bandwidth
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        features.extend([
            np.mean(spectral_bandwidth),
            np.std(spectral_bandwidth)
        ])
        
        # Spectral Contrast (spectral valley/peak differences)
        spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        features.extend([
            np.mean(spectral_contrast),
            np.std(spectral_contrast)
        ])
        
        # 3. Pitch/Fundamental Frequency Features
        # Important for tonal languages like Tamil, Telugu, Malayalam
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:
                pitch_values.append(pitch)
        
        if len(pitch_values) > 0:
            features.extend([
                np.mean(pitch_values),
                np.std(pitch_values),
                np.median(pitch_values),
                np.max(pitch_values),
                np.min(pitch_values),
                np.percentile(pitch_values, 75) - np.percentile(pitch_values, 25)  # IQR
            ])
        else:
            features.extend([0.0] * 6)
        
        # 4. Zero-Crossing Rate (rhythm/tempo related)
        zcr = librosa.feature.zero_crossing_rate(y)[0]
        features.extend([
            np.mean(zcr),
            np.std(zcr)
        ])
        
        # 5. Chroma Features (harmonic content)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        features.extend([
            np.mean(chroma),
            np.std(chroma)
        ])
        
        # 6. Mel Spectrogram Features
        mel_spec = librosa.feature.melspectrogram(y=y, sr=sr)
        features.extend([
            np.mean(mel_spec),
            np.std(mel_spec)
        ])
        
        # 7. Tonnetz (tonal centroid features)
        # Useful for distinguishing tonal vs non-tonal languages
        tonnetz = librosa.feature.tonnetz(y=y, sr=sr)
        features.extend([
            np.mean(tonnetz),
            np.std(tonnetz)
        ])
        
        # 8. Tempo (speaking rate can differ across languages)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        features.append(tempo)
        
        return np.array(features)
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray):
        """
        Train the language classifier.
        
        Args:
            X_train: Feature vectors (n_samples, n_features)
            y_train: Language labels (0=English, 1=Tamil, 2=Malayalam, 3=Hindi, 4=Telugu)
        """
        # Initialize scaler
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train Random Forest classifier
        self.classifier = RandomForestClassifier(
            n_estimators=100,
            max_depth=20,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.classifier.fit(X_scaled, y_train)
        self.is_trained = True
        
        print(f"✅ Language classifier trained on {len(X_train)} samples")
    
    def predict(self, audio_bytes: bytes) -> Tuple[str, float]:
        """
        Predict the language of the audio.
        
        Args:
            audio_bytes: Raw audio file bytes
            
        Returns:
            Tuple of (language_name, confidence_score)
        """
        if not self.is_trained:
            raise RuntimeError("Language classifier not trained. Call train() or load_model() first.")
        
        # Extract features
        features = self.extract_language_features(audio_bytes)
        features_scaled = self.scaler.transform(features.reshape(1, -1))
        
        # Predict
        prediction = self.classifier.predict(features_scaled)[0]
        probabilities = self.classifier.predict_proba(features_scaled)[0]
        confidence = float(probabilities[prediction])
        
        language = self.IDX_TO_LANGUAGE[prediction]
        
        return language, confidence
    
    def save_model(self):
        """Save trained model and scaler to disk."""
        with open('language_classifier.pkl', 'wb') as f:
            pickle.dump(self.classifier, f)
        with open('language_scaler.pkl', 'wb') as f:
            pickle.dump(self.scaler, f)
        print("✅ Language model saved to language_classifier.pkl and language_scaler.pkl")
    
    def load_model(self) -> bool:
        """
        Load pre-trained model and scaler from disk.
        
        Returns:
            True if models loaded successfully, False otherwise
        """
        try:
            if os.path.exists('language_classifier.pkl') and os.path.exists('language_scaler.pkl'):
                with open('language_classifier.pkl', 'rb') as f:
                    self.classifier = pickle.load(f)
                with open('language_scaler.pkl', 'rb') as f:
                    self.scaler = pickle.load(f)
                self.is_trained = True
                print("[SUCCESS] Language model loaded from disk")
                return True
            return False
        except Exception as e:
            print(f"[WARNING] Failed to load language model: {str(e)}")
            return False

    def initialize_with_synthetic_data(self):
        """Initialize classifier with synthetic training data."""
        print("[WARNING] No pre-trained language model found. Initializing with synthetic data...")
        print("[INFO] For production use, train with real labeled audio data!")
        
        X_train, y_train = self._create_synthetic_training_data()
        self.train(X_train, y_train)
        self.save_model()
