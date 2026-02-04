# 🚀 Deployment Guide - GUVI Hackathon AI Voice Detection API

## 📋 Current Status

✅ **Your API is READY and WORKING locally!**
- API Endpoint: `http://localhost:8000/api/voice-detection`
- Current API Key: `YOUR_SECRET_API_KEY`
- Status: Running and tested ✅

---



### Current Setup
Your API key is defined in `app.py` line 31:
```python
API_KEY = "hackathon-ai-voice-12345"
```

### Option A: Keep the Default Key (Easiest)
✅ **For the hackathon, you can keep using: `hackathon-ai-voice-12345`**

This is already set and working!

### Option B: Create a Custom API Key (Recommended for Production)

1. Open `app.py`
2. Find line 31: `API_KEY = "YOUR_SECRET_API_KEY"`
3. Change it to your custom key:

```python
# Example custom keys:
API_KEY = "sk_guvi_hackathon_2026_ai_voice_detection"
# OR
API_KEY = "guvi_ai_voice_api_secure_key_12345"
# OR create a random secure key
API_KEY = "sk_prod_a1b2c3d4e5f6g7h8i9j0"
```

**Important:** Whatever API key you set here, you'll use it in the hackathon endpoint tester!

---

## 📝 Step 2: What You Already Have (No Action Needed)

✅ Your API is already complete with:
- FastAPI REST API
- `/api/voice-detection` endpoint
- API key authentication (x-api-key header)
- Base64 MP3 input support
- 5 language support (Tamil, English, Hindi, Malayalam, Telugu)
- Auto-language detection
- ML classification (AI vs Human)
- JSON responses
- Error handling

**You're 100% ready for local testing!**

---

## 🧪 Step 3: Test Your API Locally (Before Deployment)

### Test with the Test Script:
```bash
python test_with_audio.py sample.mp3
```

### Test with cURL (if you want to simulate the hackathon tester):
```powershell
# Windows PowerShell
$apiKey = "YOUR_SECRET_API_KEY"  # Use YOUR configured API key
$audioBase64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes("sample.mp3"))

$headers = @{
    "x-api-key" = $apiKey
    "Content-Type" = "application/json"
}

$body = @{
    audioFormat = "mp3"
    audioBase64 = $audioBase64
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/voice-detection" -Method Post -Headers $headers -Body $body
```

### Test with Python:
```python
import requests, base64

# Your API key (must match app.py)
API_KEY = "YOUR_SECRET_API_KEY"

# Read and encode audio
with open("sample.mp3", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

# Send request
response = requests.post(
    "http://localhost:8000/api/voice-detection",
    headers={
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    },
    json={
        "audioFormat": "mp3",
        "audioBase64": audio_b64
    }
)

print(response.json())
```

---

## 🌐 Step 4: What the Hackathon Endpoint Tester Needs

The hackathon endpoint tester requires:

1. **Deployed API URL** (public, accessible from internet)
   - Example: `https://your-api.onrender.com/api/voice-detection`
   - Example: `https://your-api.railway.app/api/voice-detection`
   - Example: `https://your-api.vercel.app/api/voice-detection`

2. **Your API Key** (x-api-key header)
   - Whatever you configured in app.py
   - Example: `YOUR_SECRET_API_KEY`

3. **Audio File URL** (publicly accessible MP3)
   - They will provide this
   - OR you provide a sample URL

**❌ Problem:** You can't use `http://localhost:8000` because the hackathon tester can't access your local machine!

**✅ Solution:** You need to deploy your API to a public server!

---

## 🚀 Step 5: Deployment Options (REQUIRED for Hackathon Testing)

Since the hackathon endpoint tester needs to access your API from the internet, you MUST deploy it. Here are your options:

### Option 1: Render.com (Recommended - FREE & Easy)

**Pros:**
- ✅ Free tier available
- ✅ Easy deployment from GitHub
- ✅ Supports Python/FastAPI
- ✅ Auto HTTPS
- ✅ Good for hackathons

**What you'll get:**
- URL like: `https://your-app-name.onrender.com`

**Steps:**
1. Push your code to GitHub (you already did this! ✅)
2. Sign up at render.com
3. Create new "Web Service"
4. Connect your GitHub repo
5. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`
6. Deploy!

### Option 2: Railway.app (Also Great - FREE)

**Pros:**
- ✅ Free tier available
- ✅ Super easy deployment
- ✅ GitHub integration
- ✅ Fast setup

**What you'll get:**
- URL like: `https://your-app.railway.app`

**Steps:**
1. Sign up at railway.app
2. Create new project from GitHub
3. Select your repo
4. Railway auto-detects Python and deploys!

### Option 3: PythonAnywhere (Simple - FREE)

**Pros:**
- ✅ Free tier
- ✅ Python-focused
- ✅ Simple interface

**What you'll get:**
- URL like: `https://yourusername.pythonanywhere.com`

### Option 4: Hugging Face Spaces (AI-Focused - FREE)

**Pros:**
- ✅ Free for public apps
- ✅ AI/ML focused
- ✅ Good community

**What you'll get:**
- URL like: `https://huggingface.co/spaces/username/app-name`

---

## 📋 Files You Need for Deployment (You Already Have These!)

✅ All required files are ready:

```
guvi/
├── app.py                      ✅ Main API
├── feature_extractor.py        ✅ Feature extraction
├── model.py                    ✅ ML model
├── language_detector.py        ✅ Language detection
├── requirements.txt            ✅ Dependencies
├── voice_classifier.pkl        ✅ Trained model
├── language_classifier.pkl     ✅ Language model
├── scaler.pkl                  ✅ Scaler
└── language_scaler.pkl         ✅ Language scaler
```

---

## ⚙️ Step 6: Pre-Deployment Checklist

Before deploying, make these small changes:

### 1. Update `app.py` for Production

Change the start command section (lines 259-270):

**Current (Development):**
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # ← Remove this for production
        log_level="info"
    )
```

**Change to (Production):**
```python
if __name__ == "__main__":
    import uvicorn
    import os
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
```

### 2. Verify `requirements.txt`

Current content:
```
fastapi
uvicorn
librosa
scikit-learn
pydantic
numpy
```

✅ This is good! All dependencies are listed.

### 3. Create a `Procfile` (for some platforms)

Create a new file called `Procfile` (no extension):
```
web: uvicorn app:app --host 0.0.0.0 --port $PORT
```

---

## 🎯 Quick Deployment Guide (Render.com - Recommended)

### Step-by-Step:

1. **Go to render.com** and sign up (free)

2. **Click "New +" → "Web Service"**

3. **Connect GitHub:**
   - Authorize Render to access your repos
   - Select your repo: `Rajesh-07-K/guvi`

4. **Configure:**
   - Name: `guvi-ai-voice-detection`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app:app --host 0.0.0.0 --port $PORT`

5. **Click "Create Web Service"**

6. **Wait 5-10 minutes** for deployment

7. **Get your URL:** 
   - Example: `https://guvi-ai-voice-detection.onrender.com`

8. **Test your deployed API:**
   ```bash
   curl https://guvi-ai-voice-detection.onrender.com/health
   ```

---

## 🧪 Testing Your Deployed API

Once deployed, test with:

### Health Check:
```bash
curl https://YOUR-APP.onrender.com/health
```

### Voice Detection:
```python
import requests, base64

API_URL = "https://YOUR-APP.onrender.com/api/voice-detection"
API_KEY = "YOUR_SECRET_API_KEY"  # Same as in app.py

with open("sample.mp3", "rb") as f:
    audio_b64 = base64.b64encode(f.read()).decode()

response = requests.post(
    API_URL,
    headers={"x-api-key": API_KEY},
    json={"audioFormat": "mp3", "audioBase64": audio_b64}
)

print(response.json())
```

---

## 🏆 Using the Hackathon Endpoint Tester

Once deployed, fill in the tester:

1. **API Endpoint URL:**
   ```
   https://YOUR-APP.onrender.com/api/voice-detection
   ```

2. **Authorization Header:**
   - Header Name: `Authorization`
   - Header Value: `Bearer hackathon-ai-voice-12345` (or your custom key)

3. **Test Message:**
   ```
   Testing AI Voice Detection API for GUVI Hackathon
   ```

4. **Audio File URL:**
   - They might provide this
   - OR use a public MP3 URL you host

5. **Click "Test Endpoint"**

**Expected Response:**
```json
{
  "status": "success",
  "language": "Telugu",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.85,
  "explanation": "Extremely low energy variance indicates AI voice"
}
```

---

## 📝 Summary: What You Need to Do

### ✅ Already Done:
- [x] API code complete
- [x] Tested locally
- [x] API key configured
- [x] GitHub repository ready

### 🚀 Next Steps (Deployment Required):

1. **Choose a deployment platform** (Recommended: Render.com)
2. **Make small code adjustments** (production mode)
3. **Deploy to platform** (5-10 minutes)
4. **Get your public URL**
5. **Test deployed API**
6. **Submit to hackathon endpoint tester** with:
   - Your deployed URL
   - Your API key (Authorization: Bearer header)
   - Wait for validation ✅

---

## 🎯 Quick Answer to Your Questions

**Q1: How to create the API key?**
**A:** It's already created! In `app.py` line 31: `API_KEY = "YOUR_SECRET_API_KEY"`
- You can keep this OR change it to any string you want
- This is the key you'll use in the hackathon tester

**Q2: I have the AI, how to convert to API?**
**A:** ✅ Already done! Your code IS an API (FastAPI)
- You have the `/api/voice-detection` endpoint
- It accepts Base64 MP3
- It returns JSON classification

**Q3: What steps need deployment?**
**A:** You MUST deploy to use the hackathon endpoint tester because:
- Local `http://localhost:8000` is NOT accessible from internet
- Hackathon tester needs a public URL like `https://your-app.onrender.com`

**Q4: What are the next steps?**
**A:** 
1. Update app.py for production (small changes)
2. Deploy to Render.com (or Railway.app)
3. Get your public URL
4. Test it
5. Submit to hackathon endpoint tester

---

## 🆘 Need Help?

**I can help you with:**
1. ✅ Code adjustments for deployment (I'll do this now!)
2. ✅ Creating deployment files
3. ❌ Actually deploying (you need to do this on the platform)
4. ✅ Testing after deployment
5. ✅ Endpoint tester submission format

**You need to do:**
- Sign up on Render.com (or similar)
- Connect your GitHub repo
- Click deploy
- Get the URL

**Estimated time:** 15-20 minutes for first-time deployment!

---

**Status:** Your API is READY! Just needs deployment to go public! 🚀
