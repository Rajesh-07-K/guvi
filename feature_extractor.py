"""
Feature Extractor Module
Extracts audio features using librosa without modifying the original audio.
"""

import librosa
import numpy as np
from typing import Dict
import io


class AudioFeatureExtractor:
    """
    Extracts acoustic features from audio files for AI voice detection.
    Features include: MFCC, pitch variance, zero-crossing rate, spectral centroid, and energy variance.
    """

    def __init__(self):
        # No resampling - preserve original audio characteristics
        self.sr = None  # Sample rate will be auto-detected

    def extract_features(self, audio_bytes: bytes) -> Dict[str, float]:
        """
        Extract all required features from MP3 audio bytes.
        
        Args:
            audio_bytes: Raw audio file bytes (MP3 format)
            
        Returns:
            Dictionary containing extracted features
        """
        # Load audio from bytes WITHOUT resampling (sr=None keeps original sample rate)
        y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None, mono=True)
        
        # Extract all features
        features = {}
        
        # 1. MFCC (Mel-Frequency Cepstral Coefficients)
        # AI voices often have different spectral characteristics
        mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
        features['mfcc_mean'] = float(np.mean(mfcc))
        features['mfcc_std'] = float(np.std(mfcc))
        features['mfcc_var'] = float(np.var(mfcc))
        
        # 2. Pitch Variance
        # AI voices tend to have more consistent pitch patterns
        pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
        pitch_values = []
        for t in range(pitches.shape[1]):
            index = magnitudes[:, t].argmax()
            pitch = pitches[index, t]
            if pitch > 0:  # Only valid pitches
                pitch_values.append(pitch)
        
        if len(pitch_values) > 0:
            features['pitch_mean'] = float(np.mean(pitch_values))
            features['pitch_variance'] = float(np.var(pitch_values))
            features['pitch_std'] = float(np.std(pitch_values))
        else:
            features['pitch_mean'] = 0.0
            features['pitch_variance'] = 0.0
            features['pitch_std'] = 0.0
        
        # 3. Zero-Crossing Rate
        # Measures the rate of sign changes in the signal
        # AI voices may have different ZCR patterns
        zcr = librosa.feature.zero_crossing_rate(y)
        features['zcr_mean'] = float(np.mean(zcr))
        features['zcr_std'] = float(np.std(zcr))
        
        # 4. Spectral Centroid
        # Indicates where the "center of mass" of the spectrum is
        # AI voices often have distinct spectral centroids
        spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
        features['spectral_centroid_mean'] = float(np.mean(spectral_centroids))
        features['spectral_centroid_std'] = float(np.std(spectral_centroids))
        features['spectral_centroid_var'] = float(np.var(spectral_centroids))
        
        # 5. Energy Variance
        # RMS energy - AI voices may have more uniform energy distribution
        rms = librosa.feature.rms(y=y)[0]
        features['energy_mean'] = float(np.mean(rms))
        features['energy_variance'] = float(np.var(rms))
        features['energy_std'] = float(np.std(rms))
        
        # Additional discriminative features
        # Spectral Rolloff - frequency below which 85% of energy is contained
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
        features['spectral_rolloff_mean'] = float(np.mean(spectral_rolloff))
        features['spectral_rolloff_std'] = float(np.std(spectral_rolloff))
        
        # Spectral Bandwidth - width of the spectrum
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)[0]
        features['spectral_bandwidth_mean'] = float(np.mean(spectral_bandwidth))
        features['spectral_bandwidth_std'] = float(np.std(spectral_bandwidth))
        
        return features

    def get_feature_vector(self, audio_bytes: bytes) -> np.ndarray:
        """
        Extract features and return as numpy array for ML model.
        
        Args:
            audio_bytes: Raw audio file bytes
            
        Returns:
            1D numpy array of features in consistent order
        """
        features = self.extract_features(audio_bytes)
        
        # Maintain consistent feature order for model
        feature_order = [
            'mfcc_mean', 'mfcc_std', 'mfcc_var',
            'pitch_mean', 'pitch_variance', 'pitch_std',
            'zcr_mean', 'zcr_std',
            'spectral_centroid_mean', 'spectral_centroid_std', 'spectral_centroid_var',
            'energy_mean', 'energy_variance', 'energy_std',
            'spectral_rolloff_mean', 'spectral_rolloff_std',
            'spectral_bandwidth_mean', 'spectral_bandwidth_std'
        ]
        
        return np.array([features[key] for key in feature_order])
