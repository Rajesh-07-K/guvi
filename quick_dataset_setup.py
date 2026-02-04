"""
Quick Dataset Setup Helper
Helps you quickly organize your training data
"""

import os


def setup_folders():
    """Create training data folder structure."""
    
    print("=" * 70)
    print("Setting up training folders")
    print("=" * 70)
    
    folders = [
        "training_data",
        "training_data/human",
        "training_data/ai"
    ]
    
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Created: {folder}")
        else:
            print(f"Exists: {folder}")
    
    print("\nFolder structure ready!")


def count_files():
    """Count files in each folder."""
    
    human_path = "training_data/human"
    ai_path = "training_data/ai"
    
    human_files = len([f for f in os.listdir(human_path) if f.endswith('.mp3')]) if os.path.exists(human_path) else 0
    ai_files = len([f for f in os.listdir(ai_path) if f.endswith('.mp3')]) if os.path.exists(ai_path) else 0
    
    print("\n" + "=" * 70)
    print("Current Dataset Status")
    print("=" * 70)
    print(f"Human voices: {human_files} MP3 files")
    print(f"AI voices: {ai_files} MP3 files")
    print(f"Total: {human_files + ai_files} files")
    
    if human_files == 0 and ai_files == 0:
        print("\nNo training data yet!")
        print("\nNext steps:")
        print("   1. Add human voice MP3s to: training_data/human/")
        print("   2. Add AI voice MP3s to: training_data/ai/")
        print("   3. Run: python train_model.py")
    elif human_files < 20 or ai_files < 20:
        print("\nDataset is too small!")
        print(f"   Need: At least 20-50 files per category")
        print(f"   Current: {human_files} human, {ai_files} AI")
        print("\nAdd more files and try again")
    else:
        print("\nDataset looks good!")
        print("Ready to train! Run: python train_model.py")
    
    return human_files, ai_files


def show_instructions():
    """Show detailed instructions."""
    
    print("\n" + "=" * 70)
    print("How to Collect Training Data")
    print("=" * 70)
    
    print("\nHUMAN VOICES (training_data/human/):")
    print("   1. Record yourself and friends/family")
    print("      - Windows: Use 'Voice Recorder' app")
    print("      - Record 10-30 second clips")
    print("   ")
    print("   2. Download from LibriVox (free audiobooks)")
    print("      - Visit: https://librivox.org/")
    print("      - Download MP3 files")
    print("      - Cut into 30-second clips if needed")
    print("   ")
    print("   3. Or use Common Voice dataset")
    print("      - Visit: https://commonvoice.mozilla.org/")
    
    print("\nAI VOICES (training_data/ai/):")
    print("   1. TTSMaker (Easiest!)")
    print("      - Visit: https://ttsmaker.com/")
    print("      - Type different texts")
    print("      - Try different voices")
    print("      - Download as MP3")
    print("   ")
    print("   2. NaturalReaders")
    print("      - Visit: https://www.naturalreaders.com/online/")
    print("      - Generate voices")
    print("   ")
    print("   3. Google Cloud TTS")
    print("      - Visit: https://cloud.google.com/text-to-speech")
    print("   ")
    print("   4. Use MULTIPLE TTS systems for better results!")
    
    print("\nRECOMMENDED:")
    print("   - Minimum: 50 human + 50 AI voices")
    print("   - Good: 100 human + 100 AI voices")
    print("   - Best: 200+ human + 200+ AI voices")
    
    print("\nFile Requirements:")
    print("   - Format: MP3 only")
    print("   - Length: 5-30 seconds ideal")
    print("   - Quality: Clear audio, no noise")
    print("   - Diversity: Different speakers, languages, TTS systems")


def main():
    """Main setup function."""
    
    print("\n")
    print("=" * 70)
    print(" Quick Dataset Setup - Voice Classifier Training")
    print("=" * 70)
    
    # Setup folders
    setup_folders()
    
    # Count current files
    human_count, ai_count = count_files()
    
    # Show instructions
    show_instructions()
    
    # Final message
    print("\n" + "=" * 70)
    print("Next Steps")
    print("=" * 70)
    
    if human_count >= 20 and ai_count >= 20:
        print("\nYou have enough data to start training!")
        print("\n   Run: python train_model.py")
    else:
        print("\nCollect more audio files:")
        print("   1. Add MP3 files to training_data/human/ and training_data/ai/")
        print("   2. Run this script again to check: python quick_dataset_setup.py")
        print("   3. When ready, train: python train_model.py")
    
    print("\nTIP: For quick testing, even 10 files per category helps!")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
