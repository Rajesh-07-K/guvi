# 🧪 Hackathon Verification Commands

Here are the exact commands you need to run to verify your API locally and for the hackathon submission.

## ✅ STEP 1: Verify API Key Configuration

Your API is already configured with the correct key for the hackathon:

**File:** `app.py`
```python
# API Key for Hackathon (Bearer token format)
API_KEY = "hackathon-ai-voice-12345"
```

## ✅ STEP 2: Run Your API Locally

Open a terminal and run:

```bash
python app.py
```
*Your API will start at `http://0.0.0.0:8000`*

## ✅ STEP 3: Test with cURL (As requested)

Open a **new terminal** (keep the API running in the first one) and run these commands.

### Option A: Using Git Bash (Recommended for Windows)

```bash
curl -X POST "http://127.0.0.1:8000/api/voice-detection" \
-H "Authorization: Bearer hackathon-ai-voice-12345" \
-H "Content-Type: application/json" \
-d '{
  "audioFormat": "mp3", 
  "audioBase64": "'$(base64 -w 0 sample.mp3)'"
}'
```

### Option B: Using Windows PowerShell

```powershell
$audioBase64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("sample.mp3"))

curl -Uri "http://127.0.0.1:8000/api/voice-detection" `
  -Method Post `
  -Headers @{
    "Authorization" = "Bearer hackathon-ai-voice-12345";
    "Content-Type"  = "application/json"
  } `
  -Body (@{
    audioFormat = "mp3";
    audioBase64 = $audioBase64
  } | ConvertTo-Json)
```

## ✅ STEP 4: Submission Details for Endpoint Tester

When using the **India AI Impact Buildathon** endpoint tester, enter these details:

| Field | Value |
|-------|-------|
| **API Endpoint URL** | `https://your-app.onrender.com/api/voice-detection` (After deployment) |
| **Authorization Header** | `Bearer hackathon-ai-voice-12345` |
| **Test Message** | `Final Hackathon Submission` |

> **Note:** The hackathon instructions mention `audio_url`. 
> - If the tester specifically asks for `audio_url`, it means they might support URL-based fetching too. 
> - However, your problem statement explicitly asked for **Base64 MP3 input**.
> - Your API currently accepts **Base64** (`audioBase64`). 
> - If you need to support `audio_url` as well, let me know! But sticking to your core requirement (Base64) is usually safer for the "API Endpoint Tester" phase unless stated otherwise in the *specific* problem statement.

---
**Status:** Your API is fully updated to support the `Authorization: Bearer` header format! 🚀
