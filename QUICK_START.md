# 🚀 QUICK START - Deploy Your API in 20 Minutes

## ⚡ TL;DR - What You Need to Know

### ✅ Your API is READY!
- Already works locally ✅
- Code is production-ready ✅
- Just needs deployment ✅

### 🔑 Your API Key (Already Set!)
**Location:** `app.py` line 31
```python
API_KEY = "hackathon-ai-voice-12345"
```
**Use this in hackathon tester:** `hackathon-ai-voice-12345`

### 🎯 What You Need to Do
1. Deploy to Render.com (15 min)
2. Test your deployed API (3 min)
3. Submit to hackathon (2 min)

**Total Time:** 20 minutes

---

## 📱 Step-by-Step: Render.com Deployment

### Step 1: Sign Up (2 minutes)
1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub
4. Authorize Render

### Step 2: Create Web Service (3 minutes)
1. Click "New +" button (top right)
2. Select "Web Service"
3. Click "Connect GitHub"
4. Find and select: `Rajesh-07-K/guvi`
5. Click "Connect"

### Step 3: Configure (2 minutes)
Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | `guvi-ai-voice-detection` |
| **Region** | `Singapore` or closest to you |
| **Branch** | `master` |
| **Root Directory** | `guvi` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn app:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### Step 4: Deploy (10 minutes)
1. Click "Create Web Service"
2. Wait for deployment (watch the logs)
3. Status will change to "Live"

### Step 5: Get Your URL (1 minute)
Your URL will be:
```
https://guvi-ai-voice-detection.onrender.com
```
(Or similar - it will show at the top)

### Step 6: Test It (2 minutes)
```bash
# Test health endpoint
curl https://your-app.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "supported_languages": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
}
```

---

## 🏆 Submit to Hackathon Endpoint Tester

### Fill in the Form:

**1. API Endpoint URL:**
```
https://guvi-ai-voice-detection.onrender.com/api/voice-detection
```
(Use YOUR actual URL from Render)

**2. Authorization Header:**

**Header Name:**
```
Authorization
```

**Header Value:**
```
Bearer hackathon-ai-voice-12345
```

**3. Test Message:**
```
GUVI Hackathon - AI Voice Detection Final Submission
```

**4. Audio File URL:**
*(They will provide this OR you provide a public MP3 URL)*

**5. Click "Test Endpoint" →  Wait for Success! ✅**

---

## ✅ Expected Success Response

```json
{
  "status": "success",
  "language": "Tamil|English|Hindi|Malayalam|Telugu",
  "classification": "AI_GENERATED|HUMAN",
  "confidenceScore": 0.85,
  "explanation": "Detailed explanation of classification"
}
```

---

## 🔧 Alternative: Railway.app (Even Easier!)

If Render doesn't work, try Railway:

1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `Rajesh-07-K/guvi`
6. Railway auto-deploys!
7. Get URL from dashboard

---

## 🆘 Troubleshooting

### Deployment Failed?
- Check build logs in Render dashboard
- Verify root directory is set to `guvi`
- Ensure all files are in GitHub

### API Returns 500?
- Wait 1-2 minutes for models to load
- Check if deployment logs show "Model loaded"
- Restart service if needed

### Hackathon Tester Can't Connect?
- Make sure URL starts with `https://`
- Include full path: `/api/voice-detection`
- Verify service is "Live" on Render

### Authentication Failed?
- Header name: `x-api-key` (with dash!)
- Value: `YOUR_SECRET_API_KEY` (case-sensitive!)
- Check no extra spaces

---

## 📋 Deployment Checklist

- [ ] Signed up on Render.com
- [ ] Connected GitHub repository
- [ ] Configured web service
- [ ] Deployment completed (Status: Live)
- [ ] Tested /health endpoint
- [ ] Got deployment URL
- [ ] Submitted to hackathon tester
- [ ] Received success response

---

## 💡 Pro Tips

1. **Keep build logs open** - Shows what's happening
2. **First deploy takes longest** - 8-10 minutes is normal
3. **Test health first** - Ensures API is running
4. **Use exact header name** - `x-api-key` not `X-API-Key`
5. **Keep API key simple** - `YOUR_SECRET_API_KEY` works fine

---

## 🎯 Your Current Files (All Ready!)

```
✅ app.py              - API with production config
✅ Procfile            - Deployment command
✅ requirements.txt    - Dependencies
✅ render.yaml         - Render configuration
✅ voice_classifier    - Trained ML model
✅ language_classifier - Language detection model
✅ All supporting files
```

Everything you need is in your GitHub repo!

---

## ⏱️ Timeline

| Task | Time |
|------|------|
| Sign up Render | 2 min |
| Connect GitHub | 1 min |
| Configure service | 2 min |
| Wait for deployment | 8-10 min |
| Test deployed API | 2 min |
| Submit to hackathon | 2 min |
| **TOTAL** | **~20 min** |

---

## 🎉 You're Ready!

Your API has:
- ✅ Complete functionality
- ✅ Production configuration
- ✅ All deployment files
- ✅ Comprehensive testing
- ✅ Documentation

**Just deploy and submit! Good luck! 🏆**

---

## 📞 Need Help?

Open these files for more details:
- `HACKATHON_SUBMISSION.md` - Complete submission guide
- `DEPLOYMENT_GUIDE.md` - Detailed deployment steps
- `GENERIC_API_CONFIRMATION.md` - API functionality proof

**Your API is production-ready! Time to deploy! 🚀**
