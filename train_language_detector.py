"""
Train Language Detector with Real Audio Samples

Directory structure needed:
training_data/
├── English/
│   ├── sample1.mp3
│   ├── sample2.mp3
│   └── ...
├── Tamil/
│   ├── sample1.mp3
│   └── ...
├── Malayalam/
│   ├── sample1.mp3
│   └── ...
├── Hindi/
│   ├── sample1.mp3
│   └── ...
└── Telugu/
    ├── sample1.mp3
    └── ...
"""

import os
import numpy as np
from language_detector import LanguageDetector
from pathlib import Path

def train_from_audio_files(training_data_dir: str = "training_data"):
    """
    Train language detector from real audio files.
    
    Args:
        training_data_dir: Directory containing language subdirectories with audio files
    """
    detector = LanguageDetector()
    
    # Check if training data directory exists
    if not os.path.exists(training_data_dir):
        print(f"❌ Training data directory '{training_data_dir}' not found!")
        print("\n📁 Please create the following directory structure:")
        print("training_data/")
        print("├── English/")
        print("├── Tamil/")
        print("├── Malayalam/")
        print("├── Hindi/")
        print("└── Telugu/")
        print("\nPut MP3 audio samples in each language folder.")
        return False
    
    X_train = []
    y_train = []
    
    print("🎵 Loading and extracting features from audio files...\n")
    
    # Process each language
    for lang_idx, lang_name in enumerate(detector.LANGUAGES):
        # We look into both AI_Generated and Human folders for language samples
        sources = [
            os.path.join(training_data_dir, "AI_Generated", lang_name),
            os.path.join(training_data_dir, "Human", lang_name)
        ]
        
        audio_files = []
        for src in sources:
            if os.path.exists(src):
                audio_files.extend(list(Path(src).glob("*.mp3")))
        
        if len(audio_files) == 0:
            print(f"⚠️  Warning: No MP3 files found for {lang_name} in AI_Generated or Human folders. Skipping...")
            continue
        
        print(f"📂 Processing {lang_name}: {len(audio_files)} files")
        
        # Extract features from each audio file
        for audio_file in audio_files:
            try:
                # Read audio file
                with open(audio_file, 'rb') as f:
                    audio_bytes = f.read()
                
                # Extract features
                features = detector.extract_language_features(audio_bytes)
                
                X_train.append(features)
                y_train.append(lang_idx)
                
                print(f"  ✓ {audio_file.name}")
                
            except Exception as e:
                print(f"  ✗ Failed to process {audio_file.name}: {str(e)}")
    
    # Check if we have enough data
    if len(X_train) == 0:
        print("\n❌ No training data found! Cannot train model.")
        return False
    
    print(f"\n📊 Total samples collected: {len(X_train)}")
    
    # Convert to numpy arrays
    X_train = np.array(X_train)
    y_train = np.array(y_train)
    
    # Train the model
    print("\n🚀 Training language detector...")
    detector.train(X_train, y_train)
    
    # Save the model
    detector.save_model()
    
    print("\n✅ Training complete!")
    print("🎯 Model saved to language_classifier.pkl and language_scaler.pkl")
    print("\n💡 Restart your API server to use the new model.")
    
    return True


if __name__ == "__main__":
    print("=" * 60)
    print("🎓 Language Detector Training Script")
    print("=" * 60)
    print()
    
    success = train_from_audio_files()
    
    if not success:
        print("\n" + "=" * 60)
        print("📝 Instructions:")
        print("=" * 60)
        print("1. Create a 'training_data' folder in this directory")
        print("2. Create subfolders: English, Tamil, Malayalam, Hindi, Telugu")
        print("3. Put MP3 audio samples in each folder (20-50 samples per language)")
        print("4. Run this script again: python train_language_detector.py")
        print("=" * 60)
