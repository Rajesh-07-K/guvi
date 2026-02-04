"""
Quick test to verify language detector initialization
"""

from language_detector import LanguageDetector
import os

print("=" * 60)
print("🧪 Testing Language Detector")
print("=" * 60)

# Initialize detector
detector = LanguageDetector()

# Try to load existing model
print("\n📂 Checking for existing model...")
if detector.load_model():
    print("✅ Loaded existing language model")
else:
    print("⚠️  No existing model found")
    print("📚 Creating synthetic training data...")
    detector.initialize_with_synthetic_data()

print("\n" + "=" * 60)
print("✅ Language Detector Ready!")
print("=" * 60)
print(f"Supported languages: {', '.join(detector.LANGUAGES)}")

# Check if model files exist
print("\n📁 Model files:")
for filename in ['language_classifier.pkl', 'language_scaler.pkl']:
    if os.path.exists(filename):
        size_kb = os.path.getsize(filename) / 1024
        print(f"   ✅ {filename} ({size_kb:.1f} KB)")
    else:
        print(f"   ❌ {filename} (not found)")

print("\n" + "=" * 60)
