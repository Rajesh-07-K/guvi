"""
Voice Classifier Training Script
Trains the model with REAL voice samples (human and AI-generated)
"""

import os
import numpy as np
from feature_extractor import AudioFeatureExtractor
from model import VoiceClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import json


class VoiceDatasetTrainer:
    """Train the voice classifier with real audio samples."""
    
    def __init__(self):
        self.feature_extractor = AudioFeatureExtractor()
        self.classifier = VoiceClassifier()
        self.dataset = {
            'features': [],
            'labels': [],
            'filenames': []
        }
    
    def load_dataset_from_folders(self, dataset_path="training_data"):
        """
        Load audio files from organized folders.
        
        Expected structure:
        training_data/
        ├── human/
        │   ├── voice1.mp3
        │   ├── voice2.mp3
        │   └── ...
        └── ai/
            ├── ai_voice1.mp3
            ├── ai_voice2.mp3
            └── ...
        """
        print("=" * 70)
        print("🎓 Voice Classifier Training")
        print("=" * 70)
        
        human_path = os.path.join(dataset_path, "Human")
        ai_path = os.path.join(dataset_path, "AI_Generated")
        
        # Check if folders exist
        if not os.path.exists(human_path):
            print(f"❌ Error: Folder '{human_path}' not found!")
            print(f"💡 Create it and add human voice MP3 files")
            return False
        
        if not os.path.exists(ai_path):
            print(f"❌ Error: Folder '{ai_path}' not found!")
            print(f"💡 Create it and add AI-generated voice MP3 files")
            return False
        
        # Load human voices (label = 0)
        print(f"\n📂 Loading HUMAN voices from: {human_path}")
        human_count = self._load_from_folder(human_path, label=0, voice_type="HUMAN")
        
        # Load AI voices (label = 1)
        print(f"\n📂 Loading AI voices from: {ai_path}")
        ai_count = self._load_from_folder(ai_path, label=1, voice_type="AI")
        
        total = human_count + ai_count
        
        if total == 0:
            print("\n❌ No audio files found!")
            print("💡 Add MP3 files to the folders and try again")
            return False
        
        print("\n" + "=" * 70)
        print("📊 Dataset Summary")
        print("=" * 70)
        print(f"👤 Human voices: {human_count}")
        print(f"🤖 AI voices: {ai_count}")
        print(f"📦 Total samples: {total}")
        
        if human_count < 10 or ai_count < 10:
            print("\n⚠️  WARNING: Very small dataset!")
            print("💡 Recommended: At least 50+ samples per class for good accuracy")
            print("   Current: Human={}, AI={}".format(human_count, ai_count))
        
        return True
    
    def _load_from_folder(self, folder_path, label, voice_type):
        """Load all MP3 files from a folder and its subfolders."""
        count = 0
        
        # Walk through the folder and subfolders
        mp3_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.mp3'):
                    mp3_files.append(os.path.join(root, file))
        
        if len(mp3_files) == 0:
            print(f"   ⚠️  No MP3 files found in {folder_path}")
            return 0
        
        print(f"   Found {len(mp3_files)} MP3 files")
        
        for filepath in mp3_files:
            filename = os.path.basename(filepath)
            try:
                # Read audio file
                with open(filepath, 'rb') as f:
                    audio_bytes = f.read()
                
                # Extract features
                features = self.feature_extractor.get_feature_vector(audio_bytes)
                
                # Store
                self.dataset['features'].append(features)
                self.dataset['labels'].append(label)
                self.dataset['filenames'].append(filename)
                
                count += 1
                print(f"   ✅ {count}. {filename[:40]}")
                
            except Exception as e:
                print(f"   ❌ Failed: {filename} - {str(e)}")
        
        return count
    
    def train(self, test_size=0.2):
        """Train the classifier with loaded data."""
        
        if len(self.dataset['features']) == 0:
            print("❌ No data loaded! Load dataset first.")
            return
        
        print("\n" + "=" * 70)
        print("🧠 Training the Model")
        print("=" * 70)
        
        # Convert to numpy arrays
        X = np.array(self.dataset['features'])
        y = np.array(self.dataset['labels'])
        
        # Split into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=42, stratify=y
        )
        
        print(f"\n📊 Data Split:")
        print(f"   Training samples: {len(X_train)}")
        print(f"   Test samples: {len(X_test)}")
        
        # Train the model
        print(f"\n⏳ Training Random Forest classifier...")
        self.classifier.train(X_train, y_train)
        
        # Evaluate on training set
        train_predictions = []
        for features in X_train:
            pred, _, _ = self.classifier.predict(features)
            train_predictions.append(1 if pred == "AI_GENERATED" else 0)
        
        train_accuracy = accuracy_score(y_train, train_predictions)
        
        # Evaluate on test set
        test_predictions = []
        test_confidences = []
        for features in X_test:
            pred, confidence, _ = self.classifier.predict(features)
            test_predictions.append(1 if pred == "AI_GENERATED" else 0)
            test_confidences.append(confidence)
        
        test_accuracy = accuracy_score(y_test, test_predictions)
        
        # Print results
        print("\n" + "=" * 70)
        print("✅ Training Complete!")
        print("=" * 70)
        print(f"🎯 Training Accuracy: {train_accuracy*100:.2f}%")
        print(f"🎯 Test Accuracy: {test_accuracy*100:.2f}%")
        
        # Detailed classification report
        print("\n📊 Detailed Performance Report:")
        print("=" * 70)
        target_names = ['HUMAN', 'AI_GENERATED']
        print(classification_report(y_test, test_predictions, target_names=target_names))
        
        # Confusion matrix
        cm = confusion_matrix(y_test, test_predictions)
        print("🔍 Confusion Matrix:")
        print(f"                Predicted HUMAN  Predicted AI")
        print(f"Actual HUMAN    {cm[0][0]:15}  {cm[0][1]:13}")
        print(f"Actual AI       {cm[1][0]:15}  {cm[1][1]:13}")
        
        # Average confidence
        avg_confidence = np.mean(test_confidences)
        print(f"\n💪 Average Confidence: {avg_confidence*100:.2f}%")
        
        # Save the model
        print("\n💾 Saving trained model...")
        self.classifier.save_model()
        print("✅ Model saved successfully!")
        
        # Save training statistics
        stats = {
            'train_accuracy': float(train_accuracy),
            'test_accuracy': float(test_accuracy),
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'human_samples': int(np.sum(y == 0)),
            'ai_samples': int(np.sum(y == 1)),
            'avg_confidence': float(avg_confidence)
        }
        
        with open('training_stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        
        print("📊 Training statistics saved to: training_stats.json")
        
        if test_accuracy < 0.7:
            print("\n⚠️  WARNING: Accuracy is below 70%")
            print("💡 Suggestions to improve:")
            print("   1. Add more diverse training samples")
            print("   2. Ensure good audio quality")
            print("   3. Balance human and AI samples")
            print("   4. Use multiple AI voice generators (Google TTS, ElevenLabs, etc.)")
        elif test_accuracy >= 0.85:
            print("\n🎉 Excellent! Model is performing well!")
            print("✅ Ready for production use")
        
        return test_accuracy


def main():
    """Main training function."""
    
    trainer = VoiceDatasetTrainer()
    
    # Load dataset
    if trainer.load_dataset_from_folders("training_data"):
        # Train
        accuracy = trainer.train(test_size=0.2)
        
        if accuracy is not None:
            print("\n" + "=" * 70)
            print("🎓 Training Complete!")
            print("=" * 70)
            print("\n💡 Next steps:")
            print("   1. Restart the API server: python app.py")
            print("   2. Test with your audio: python test_with_audio.py")
            print("   3. The model should now be more accurate!")
    else:
        print("\n" + "=" * 70)
        print("📚 How to Prepare Training Data")
        print("=" * 70)
        print("\n1. Create folders:")
        print("   training_data/")
        print("   ├── human/    ← Put human voice MP3s here")
        print("   └── ai/       ← Put AI voice MP3s here")
        print("\n2. Collect at least 50+ MP3 files for each category")
        print("\n3. Run this script again: python train_model.py")


if __name__ == "__main__":
    main()
