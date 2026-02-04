"""
Debug script to analyze the actual features extracted from sample.mp3
"""
import base64
from feature_extractor import AudioFeatureExtractor
import numpy as np

# Read the sample audio
with open("sample.mp3", "rb") as f:
    audio_bytes = f.read()

# Extract features
extractor = AudioFeatureExtractor()
features = extractor.extract_features(audio_bytes)
feature_vector = extractor.get_feature_vector(audio_bytes)

print("=" * 70)
print("ACTUAL FEATURES FROM sample.mp3 (AI-GENERATED VOICE)")
print("=" * 70)
print("\n🔍 Raw Feature Values:")
print("-" * 70)

# Feature names in order
feature_names = [
    'mfcc_mean', 'mfcc_std', 'mfcc_var',
    'pitch_mean', 'pitch_variance', 'pitch_std',
    'zcr_mean', 'zcr_std',
    'spectral_centroid_mean',  'spectral_centroid_std', 'spectral_centroid_var',
    'energy_mean', 'energy_variance', 'energy_std',
    'spectral_rolloff_mean', 'spectral_rolloff_std',
    'spectral_bandwidth_mean', 'spectral_bandwidth_std'
]

for name, value in zip(feature_names, feature_vector):
    print(f"{name:30s}: {value:15.6f}")

print("\n=" * 70)
print("KEY AI INDICATORS (from real AI voices):")
print("=" * 70)
print("✅ LOW pitch_variance      → AI voice characteristic")
print("✅ LOW energy_variance      → AI voice characteristic")
print("✅ LOW mfcc_var            → AI voice characteristic")
print("✅ LOW spectral variances  → AI voice characteristic")

print("\n=" * 70)
print("ANALYSIS OF sample.mp3:")
print("=" * 70)
print(f"pitch_variance:        {features['pitch_variance']:.6f}")
print(f"energy_variance:       {features['energy_variance']:.6f}")
print(f"mfcc_var:             {features['mfcc_var']:.6f}")
print(f"spectral_centroid_var: {features['spectral_centroid_var']:.6f}")
