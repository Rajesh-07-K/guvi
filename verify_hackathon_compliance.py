
import sys
import os
import base64
import json
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from app import app, API_KEY

# Initialize TestClient
client = TestClient(app)

def test_hackathon_compliance():
    print("[START] Starting Hackathon Compliance Verification...")
    
    # Mock efficient audio data (silence)
    # 1 second of silence MP3 base64 (approx)
    SILENCE_MP3_B64 = "SUQzBAAAAAAAI1RTU0UAAAAPAAADTGF2ZjU4LjI5LjEwMAAAAAAAAAAAAAAA//OEAAAAAAAAAAAAAAAAAAAAAAAASW5mbwAAAA8AAAAEAAABIADAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDATGF2YzU4LjU0AAAAAAAAAAAAAAAAJAAAAAAAAAAAASAAAAAAA//OEAAAAAAA"
    
    # 1. Test Feature: Dual Authentication
    print("\n[TEST] Testing Dual Authentication...")
    
    # Case 1A: x-api-key (Old method)
    response = client.post(
        "/api/voice-detection",
        json={"audioFormat": "mp3", "audioBase64": SILENCE_MP3_B64},
        headers={"x-api-key": API_KEY}
    )
    if response.status_code == 200:
        print("[PASS] x-api-key Authentication: SUCCESS")
    else:
        print(f"[FAIL] x-api-key Authentication: FAILED ({response.status_code})")
        print(response.json())

    # Case 1B: Authorization: Bearer (New method)
    response = client.post(
        "/api/voice-detection",
        json={"audioFormat": "mp3", "audioBase64": SILENCE_MP3_B64},
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    if response.status_code == 200:
        print("[PASS] Bearer Token Authentication: SUCCESS")
    else:
        print(f"[FAIL] Bearer Token Authentication: FAILED ({response.status_code})")
        print(response.json())

    # 2. Test Feature: Dual Input (Base64 vs URL)
    print("\n[TEST] Testing Dual Input Modes...")
    
    # MOCK feature extraction for valid inputs to verify API flow
    # We don't care about actual audio processing here, just the API contract
    with patch('app.feature_extractor.get_feature_vector') as mock_features:
        # valid feature vector (random)
        import numpy as np
        mock_features.return_value = np.zeros(18) # 18 features expected

        # Case 2A: audioBase64 (Standard)
        response = client.post(
            "/api/voice-detection",
            json={"audioFormat": "mp3", "audioBase64": SILENCE_MP3_B64},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        if response.status_code == 200:
            print("[PASS] audioBase64 Input: SUCCESS")
        else:
            print(f"[FAIL] audioBase64 Input: FAILED ({response.status_code})")
            print(response.json())

        # Case 2B: audioUrl (New requirement)
        with patch('app.requests.get') as mock_get:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = base64.b64decode(SILENCE_MP3_B64)
            mock_get.return_value = mock_response
            
            response = client.post(
                "/api/voice-detection",
                json={
                    "audioFormat": "mp3", 
                    "audioUrl": "http://example.com/test.mp3"
                },
                headers={"Authorization": f"Bearer {API_KEY}"}
            )
            
            if response.status_code == 200:
                print("[PASS] audioUrl Input (Mocked): SUCCESS")
            else:
                print(f"[FAIL] audioUrl Input: FAILED ({response.status_code})")
                print(response.json())
                
    # Re-run Auth tests with mocked features to get green 200s
    print("\n[TEST] Retesting Auth with valid flow...")
    with patch('app.feature_extractor.get_feature_vector') as mock_features:
        mock_features.return_value = np.zeros(18)
        
        # Case 1A: x-api-key
        response = client.post(
            "/api/voice-detection",
            json={"audioFormat": "mp3", "audioBase64": SILENCE_MP3_B64},
            headers={"x-api-key": API_KEY}
        )
        if response.status_code == 200:
            print("[PASS] x-api-key Authentication: SUCCESS")
        else:
             print(f"[FAIL] x-api-key Authentication: FAILED ({response.status_code})")

        # Case 1B: Bearer
        response = client.post(
            "/api/voice-detection",
            json={"audioFormat": "mp3", "audioBase64": SILENCE_MP3_B64},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        if response.status_code == 200:
            print("[PASS] Bearer Token Authentication: SUCCESS")
        else:
             print(f"[FAIL] Bearer Token Authentication: FAILED ({response.status_code})")

    # 3. Test Feature: Robust Error Handling (No 500 crashes)
    print("\n[TEST] Testing Error Handling...")
    
    # Case 3A: Invalid Base64 (Should return 400, not crash)
    response = client.post(
        "/api/voice-detection",
        json={"audioFormat": "mp3", "audioBase64": "NOT_A_BASE64_STRING"},
        headers={"Authorization": f"Bearer {API_KEY}"}
    )
    if response.status_code == 400:
        print("[PASS] Invalid Base64 Handling: SUCCESS (Returns 400)")
    else:
        print(f"[FAIL] Invalid Base64 Handling: FAILED (Got {response.status_code})")
        
    # Case 3B: Server Error Simulation (Mocking internal failure)
    with patch('app.feature_extractor.get_feature_vector') as mock_extract:
        mock_extract.side_effect = Exception("Simulated Critical Failure")
        
        response = client.post(
            "/api/voice-detection",
            json={"audioFormat": "mp3", "audioBase64": SILENCE_MP3_B64},
            headers={"Authorization": f"Bearer {API_KEY}"}
        )
        
        # Should return 500 but as a structured JSON, NOT a raw server crash trace
        if response.status_code == 500:
            data = response.json()
            if "detail" in data and "Simulated Critical Failure" in data["detail"]:
                 print("[PASS] Global Exception Handler: SUCCESS (Caught crash & returned JSON)")
            else:
                 print(f"[WARN] Global Exception Handler: Partial Success (Got 500 but unexpected body: {data})")
        else:
            print(f"[FAIL] Global Exception Handler: FAILED (Got {response.status_code})")

if __name__ == "__main__":
    try:
        # Check if httpx is installed, if not install it
        try:
            import httpx
        except ImportError:
            print("[WARN] 'httpx' module missing. Installing for TestClient...")
            os.system("pip install httpx")
            import httpx
            
        test_hackathon_compliance()
    except Exception as e:
        print(f"[FAIL] FATAL TEST ERROR: {str(e)}")
