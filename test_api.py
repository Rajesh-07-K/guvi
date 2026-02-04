"""
Test script for AI Voice Detection API
Demonstrates how to call the API with a sample audio file.
"""

import requests
import base64
import json


def test_voice_detection_api():
    """
    Test the voice detection API with a sample MP3 file.
    
    Note: You need to provide your own MP3 file for testing.
    """
    
    # API configuration
    API_URL = "http://localhost:8000/api/voice-detection"
    API_KEY = "YOUR_SECRET_API_KEY"
    
    # Read and encode MP3 file
    # Replace 'sample.mp3' with your actual audio file path
    mp3_file_path = "sample.mp3"
    
    try:
        with open(mp3_file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: File '{mp3_file_path}' not found.")
        print("Please create a sample MP3 file or update the file path.")
        return
    
    # Prepare request
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "language": "English",
        "audioFormat": "mp3",
        "audioBase64": audio_base64
    }
    
    # Send request
    print("Sending request to API...")
    print(f"Audio size: {len(audio_bytes)} bytes")
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        # Print response
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response:\n{json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"\n✅ Classification: {result['classification']}")
            print(f"✅ Confidence: {result['confidenceScore']:.2%}")
            print(f"✅ Explanation: {result['explanation']}")
        else:
            print(f"\n❌ Error: {response.json()['message']}")
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server.")
        print("Make sure the server is running: python app.py")
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")


def test_health_check():
    """Test the health check endpoint."""
    try:
        response = requests.get("http://localhost:8000/health")
        print("Health Check:")
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Health check failed: {str(e)}")


if __name__ == "__main__":
    print("=" * 60)
    print("AI Voice Detection API - Test Script")
    print("=" * 60)
    
    # Test health endpoint
    print("\n1. Testing health endpoint...")
    test_health_check()
    
    # Test voice detection
    print("\n2. Testing voice detection endpoint...")
    test_voice_detection_api()
