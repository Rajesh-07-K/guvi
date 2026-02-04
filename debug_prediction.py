"""
Debug script to test the hybrid prediction logic directly
"""
import base64
from feature_extractor import AudioFeatureExtractor
from model import VoiceClassifier

# Read the sample audio
with open("sample.mp3", "rb") as f:
    audio_bytes = f.read()

# Extract features
extractor = AudioFeatureExtractor()
features = extractor.get_feature_vector(audio_bytes)

print("=" * 70)
print("DEBUG: Testing hybrid prediction logic")
print("=" * 70)

print(f"\n🔍 Energy variance (index 12): {features[12]:.6f}")
print(f"📏 Threshold: 0.008")
print(f"📊 Should classify as: {'AI' if features[12] < 0.008 else 'HUMAN'}")

# Test prediction
classifier = VoiceClassifier()
if not classifier.load_model():
    classifier._load_pretrained_model()

classification, confidence, explanation = classifier.predict(features)

print(f"\n✅ ACTUAL RESULT:")
print(f"   Classification: {classification}")
print(f"   Confidence: {confidence:.4f} ({confidence*100:.2f}%)")
print(f"   Explanation: {explanation}")
