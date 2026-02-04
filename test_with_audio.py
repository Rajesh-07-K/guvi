"""
Easy Audio Tester - Test the API with your MP3 files
Usage: python test_with_audio.py [language] [audio_file.mp3]
       python test_with_audio.py [audio_file.mp3]  (auto-detect language)
"""

import requests
import base64
import sys
import os


def test_with_audio(audio_file="sample.mp3", language=None):
    """
    Test the API with an audio file.
    
    Args:
        audio_file: Path to MP3 file (default: sample.mp3)
        language: Language of audio (Tamil, English, Hindi, Malayalam, Telugu) - Optional, will be auto-detected
    """
    
    # API configuration
    API_URL = "http://localhost:8000/api/voice-detection"
    API_KEY = "YOUR_SECRET_API_KEY"
    
    # Validate language if provided
    if language is not None:
        language = language.capitalize()
        valid_languages = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
        
        if language not in valid_languages:
            print(f"❌ Error: Invalid language '{language}'")
            print(f"✅ Valid languages: {', '.join(valid_languages)}")
            return
    
    # Check if file exists
    if not os.path.exists(audio_file):
        print(f"❌ Error: File '{audio_file}' not found!")
        print(f"\n💡 Please make sure:")
        print(f"   1. The file exists in the current directory")
        print(f"   2. The file is in MP3 format")
        print(f"   3. The filename is correct")
        print(f"\n📁 Current directory: {os.getcwd()}")
        return
    
    print("=" * 60)
    print("🎤 AI Voice Detection - Audio Test")
    print("=" * 60)
    print(f"📁 Audio file: {audio_file}")
    print(f"🗣️  Language: {language if language else 'Auto-detect'}")
    
    try:
        # Read and encode audio file
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
        
        file_size_kb = len(audio_bytes) / 1024
        print(f"📊 File size: {file_size_kb:.2f} KB")
        
        # Prepare request
        headers = {
            "x-api-key": API_KEY,
            "Content-Type": "application/json"
        }
        
        payload = {
            "audioFormat": "mp3",
            "audioBase64": audio_base64
        }
        
        # Add language only if provided
        if language is not None:
            payload["language"] = language
        
        print(f"\n🚀 Sending request to API...")
        
        # Send request
        response = requests.post(API_URL, headers=headers, json=payload)
        
        print(f"📡 Status Code: {response.status_code}")
        
        # Handle response
        if response.status_code == 200:
            result = response.json()
            
            print("\n" + "=" * 60)
            print("✅ RESULT")
            print("=" * 60)
            print(f"🌐 Detected Language: {result['language']}")
            print(f"🎯 Classification: {result['classification']}")
            print(f"📊 Confidence: {result['confidenceScore']*100:.2f}%")
            print(f"💬 Explanation: {result['explanation']}")
            print("=" * 60)
            
            # Visual indicator
            if result['classification'] == 'AI_GENERATED':
                print("🤖 This voice appears to be AI-generated")
            else:
                print("👤 This voice appears to be human")
            
            # Confidence level interpretation
            confidence = result['confidenceScore']
            if confidence >= 0.9:
                print("💪 Very high confidence")
            elif confidence >= 0.7:
                print("👍 High confidence")
            elif confidence >= 0.5:
                print("🤔 Moderate confidence")
            else:
                print("⚠️  Low confidence - result uncertain")
                
        elif response.status_code == 401:
            print("\n❌ Authentication Error!")
            print("💡 Check that the API key is correct")
            
        elif response.status_code == 400:
            error_detail = response.json().get('detail', 'Unknown error')
            print(f"\n❌ Bad Request Error!")
            print(f"💡 Details: {error_detail}")
            print("\n🔍 Common causes:")
            print("   - Audio file is not a valid MP3")
            print("   - Audio file is corrupted")
            print("   - Audio file is too small/empty")
            
        else:
            print(f"\n❌ Error: {response.json()}")
    
    except FileNotFoundError:
        print(f"\n❌ Error: Cannot find file '{audio_file}'")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server")
        print("💡 Make sure the server is running:")
        print("   python app.py")
    
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
    
    print("\n" + "=" * 60)


def show_help():
    """Show usage instructions."""
    print("""
╔══════════════════════════════════════════════════════════╗
║         AI Voice Detection - Audio Tester                ║
╚══════════════════════════════════════════════════════════╝

USAGE:
    python test_with_audio.py [language] [audio_file.mp3]
    python test_with_audio.py [audio_file.mp3]  (auto-detect language)

EXAMPLES:
    # Test with default file (sample.mp3) - auto-detect language
    python test_with_audio.py
    
    # Test with custom file - auto-detect language
    python test_with_audio.py my_voice.mp3
    
    # Test with custom file in Tamil (manual)
    python test_with_audio.py tamil my_voice.mp3
    
    # Test with custom file in Hindi (manual)
    python test_with_audio.py hindi recording.mp3

SUPPORTED LANGUAGES (Auto-Detection):
    - Tamil
    - English
    - Hindi
    - Malayalam
    - Telugu

REQUIREMENTS:
    1. Server must be running: python app.py
    2. Audio file must be in MP3 format
    3. Audio file must exist in current directory

STEPS:
    1. Start the server in one terminal: python app.py
    2. Put your MP3 file in this folder
    3. Run this script: python test_with_audio.py
    
TIP: To record voice on Windows, use "Voice Recorder" app
    """)


if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) == 1:
        # No arguments - use defaults
        test_with_audio()
    
    elif len(sys.argv) == 2:
        arg = sys.argv[1].lower()
        if arg in ['help', '-h', '--help']:
            show_help()
        else:
            # Assume it's a language
            test_with_audio(language=sys.argv[1])
    
    elif len(sys.argv) == 3:
        # Both language and file provided
        language = sys.argv[1]
        audio_file = sys.argv[2]
        test_with_audio(audio_file, language)
    
    else:
        print("❌ Too many arguments!")
        show_help()
