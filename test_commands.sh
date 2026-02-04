#!/bin/bash
# Sample API Test Commands
# Replace <BASE64_STRING> with actual Base64-encoded MP3

# ===============================================
# 1. Health Check
# ===============================================
echo "Testing health endpoint..."
curl http://localhost:8000/health

echo -e "\n\n"

# ===============================================
# 2. API Info
# ===============================================
echo "Getting API info..."
curl http://localhost:8000/

echo -e "\n\n"

# ===============================================
# 3. Voice Detection - Valid Request (Tamil)
# ===============================================
echo "Testing voice detection (Tamil)..."
curl -X POST http://localhost:8000/api/voice-detection \
  -H "x-api-key: YOUR_SECRET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": "<BASE64_STRING>"
  }'

echo -e "\n\n"

# ===============================================
# 4. Voice Detection - Valid Request (English)
# ===============================================
echo "Testing voice detection (English)..."
curl -X POST http://localhost:8000/api/voice-detection \
  -H "x-api-key: YOUR_SECRET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "<BASE64_STRING>"
  }'

echo -e "\n\n"

# ===============================================
# 5. Error Test - Invalid API Key
# ===============================================
echo "Testing invalid API key..."
curl -X POST http://localhost:8000/api/voice-detection \
  -H "x-api-key: WRONG_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "<BASE64_STRING>"
  }'

echo -e "\n\n"

# ===============================================
# 6. Error Test - Invalid Language
# ===============================================
echo "Testing invalid language..."
curl -X POST http://localhost:8000/api/voice-detection \
  -H "x-api-key: YOUR_SECRET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "French",
    "audioFormat": "mp3",
    "audioBase64": "<BASE64_STRING>"
  }'

echo -e "\n\n"

# ===============================================
# 7. Error Test - Missing API Key
# ===============================================
echo "Testing missing API key..."
curl -X POST http://localhost:8000/api/voice-detection \
  -H "Content-Type: application/json" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "<BASE64_STRING>"
  }'

echo -e "\n\n"

# ===============================================
# 8. Error Test - Invalid Base64
# ===============================================
echo "Testing invalid Base64..."
curl -X POST http://localhost:8000/api/voice-detection \
  -H "x-api-key: YOUR_SECRET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "invalid_base64_string!!!"
  }'

echo -e "\n\nAll tests completed!"
