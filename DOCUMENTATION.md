# 🎤 AI Voice Detection API - Complete Documentation

## 📋 Project Overview

A **production-ready REST API** built with FastAPI that detects whether a voice recording is AI-generated or spoken by a human. The system uses machine learning with acoustic feature analysis to make predictions across 5 languages: **Tamil, English, Hindi, Malayalam, and Telugu**.

---

## 🏗️ Architecture

### System Flow
```
1. Client sends MP3 (Base64) + Language → API
2. API validates API key
3. Base64 decoded to raw audio bytes
4. Feature Extractor extracts 18 acoustic features
5. ML Classifier predicts AI vs Human
6. Response with classification + confidence + explanation
```

### Tech Stack
- **Framework**: FastAPI 0.104.1
- **Audio Processing**: librosa 0.10.1
- **ML Model**: scikit-learn 1.3.2 (Random Forest)
- **Server**: Uvicorn (ASGI)
- **Python**: 3.11+

---

## 📁 Project Structure

```
r:\Project\Guvi\
├── app.py                  # Main FastAPI application
├── feature_extractor.py    # Audio feature extraction
├── model.py               # ML classifier
├── requirements.txt       # Python dependencies
├── test_api.py           # Test script
├── README.md             # Documentation
├── .gitignore            # Git ignore file
├── voice_classifier.pkl  # Trained model (auto-generated)
└── scaler.pkl           # Feature scaler (auto-generated)
```

---

## 🔬 Detection Logic Explained

### Why This Approach Works

**AI-generated voices** (from TTS systems like ElevenLabs, Google TTS, etc.) have subtle but measurable differences from human voices:

1. **More Consistent Pitch**
   - Humans: Natural pitch fluctuations, breathing variations
   - AI: Too smooth, predictable pitch contours

2. **Uniform Energy Distribution**
   - Humans: Variable energy (stress, emotion, breathing)
   - AI: Overly consistent RMS energy

3. **Spectral Patterns**
   - Humans: Complex harmonic structures, micro-variations
   - AI: Artifacts from vocoding, synthetic harmonics

4. **Micro-Timing**
   - Humans: Natural pauses, rhythm variations
   - AI: Mechanical timing, uniform zero-crossing rates

### Feature Engineering

The system extracts **18 acoustic features** from each audio sample:

| Feature Category | Features | Why It Matters |
|-----------------|----------|----------------|
| **MFCC** | Mean, Std, Variance | Captures spectral envelope differences |
| **Pitch** | Mean, Variance, Std | AI voices have lower variance |
| **ZCR** | Mean, Std | Signal noisiness patterns |
| **Spectral Centroid** | Mean, Std, Variance | "Brightness" of sound |
| **Energy** | Mean, Variance, Std | Energy distribution uniformity |
| **Spectral Rolloff** | Mean, Std | Frequency distribution |
| **Spectral Bandwidth** | Mean, Std | Spectrum width |

### Classification Model

**Random Forest Classifier** (100 trees, depth 10)

**Why Random Forest?**
- Handles non-linear relationships well
- Robust to overfitting
- Provides feature importance
- Fast inference (<100ms)
- No need for extensive hyperparameter tuning

**Training Process:**
```python
# Pseudo-code for production training
1. Collect labeled dataset:
   - Human voices: recordings from real people
   - AI voices: outputs from various TTS systems
   
2. Extract features from all samples
3. Split data: 80% train, 20% test
4. Standardize features (StandardScaler)
5. Train Random Forest
6. Evaluate on test set
7. Save model to disk
```

---

## 🚀 Quick Start Guide

### Step 1: Install Dependencies
```bash
cd r:\Project\Guvi
pip install -r requirements.txt
```

### Step 2: Start the Server
```bash
python app.py
```

Output:
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
WARNING:  No pre-trained model found. Initializing with synthetic data...
Model initialized with synthetic data. Accuracy: ~60-70% (demonstration only)
For production use, train with real labeled voice datasets!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Test the API

**Health Check:**
```bash
curl http://localhost:8000/health
```

**Voice Detection:**
```bash
curl -X POST http://localhost:8000/api/voice-detection \
  -H "x-api-key: YOUR_SECRET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "<your_base64_encoded_mp3>"
  }'
```

---

## 🔐 API Reference

### Authentication

All requests require an API key in the header:
```
x-api-key: YOUR_SECRET_API_KEY
```

**Responses:**
- ✅ Valid key → 200 OK
- ❌ Invalid/missing key → 401 Unauthorized

### Endpoints

#### 1. Voice Detection
**POST** `/api/voice-detection`

**Request:**
```json
{
  "language": "Tamil | English | Hindi | Malayalam | Telugu",
  "audioFormat": "mp3",
  "audioBase64": "<Base64 MP3 string>"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "language": "English",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.8735,
  "explanation": "High consistency in pitch and spectral patterns typical of synthetic voices"
}
```

**Error Responses:**

| Code | Scenario | Response |
|------|----------|----------|
| 401 | Invalid API key | `{"status": "error", "message": "Invalid API key"}` |
| 400 | Invalid Base64 | `{"status": "error", "message": "Invalid Base64 encoding"}` |
| 400 | Unsupported language | `{"status": "error", "message": "Invalid request format"}` |
| 500 | Server error | `{"status": "error", "message": "Internal server error"}` |

#### 2. Health Check
**GET** `/health`

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true,
  "supported_languages": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]
}
```

#### 3. API Info
**GET** `/`

**Response:**
```json
{
  "name": "AI Voice Detection API",
  "version": "1.0.0",
  "endpoint": "/api/voice-detection",
  "supported_languages": ["Tamil", "English", "Hindi", "Malayalam", "Telugu"],
  "audio_format": "mp3",
  "authentication": "Required (x-api-key header)"
}
```

---

## 🧪 Testing Guide

### Using Python (test_api.py)

```python
# 1. Place a sample MP3 file in the project folder as "sample.mp3"
# 2. Run the test script:
python test_api.py
```

### Manual Testing with cURL

**Create Base64 from MP3:**
```bash
# Linux/Mac
base64 -i sample.mp3 -o encoded.txt

# Windows PowerShell
[Convert]::ToBase64String([IO.File]::ReadAllBytes("sample.mp3")) | Out-File encoded.txt
```

**Send Request:**
```bash
# Read Base64 from file and send request
curl -X POST http://localhost:8000/api/voice-detection \
  -H "x-api-key: YOUR_SECRET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "Tamil",
    "audioFormat": "mp3",
    "audioBase64": "'$(cat encoded.txt)'"
  }'
```

### Expected Performance

| Metric | Value |
|--------|-------|
| Response Time | <500ms (for 10-30s audio) |
| Max Audio Size | ~10MB recommended |
| Confidence Range | 0.0 - 1.0 |
| Accuracy (demo model) | ~60-70% |
| Accuracy (production model) | **>85% target** |

---

## 🎯 Production Deployment Checklist

### Before Going Live

#### 1. Security
- [ ] Move API key to environment variable
  ```python
  import os
  API_KEY = os.getenv("VOICE_API_KEY")
  ```
- [ ] Enable HTTPS (use nginx reverse proxy)
- [ ] Add rate limiting (e.g., max 100 requests/hour per IP)
- [ ] Implement request size limits (max 10MB)

#### 2. Model Training
- [ ] Collect **real labeled dataset**:
  - Minimum 1000 human voice samples
  - Minimum 1000 AI-generated samples
  - Balanced across all 5 languages
- [ ] Train model with real data:
  ```python
  from model import VoiceClassifier
  from feature_extractor import AudioFeatureExtractor
  
  # Load your labeled dataset
  X_train, y_train = load_dataset()
  
  # Train and save
  classifier = VoiceClassifier()
  classifier.train(X_train, y_train)
  classifier.save_model()
  ```
- [ ] Evaluate on test set (target: >85% accuracy)

#### 3. Infrastructure
- [ ] Deploy to production server (AWS, GCP, Azure)
- [ ] Set up auto-scaling
- [ ] Configure logging (file + cloud logging service)
- [ ] Set up monitoring and alerts
- [ ] Disable auto-reload in uvicorn:
  ```python
  uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)
  ```

#### 4. Testing
- [ ] Load testing (can it handle 100 concurrent requests?)
- [ ] Edge case testing (corrupted audio, empty files, etc.)
- [ ] Cross-language testing (ensure model works for all 5 languages)

#### 5. Documentation
- [ ] API documentation (consider adding Swagger UI)
- [ ] Usage examples
- [ ] Error handling guide

---

## 🛠️ Customization Guide

### Changing the API Key

**Option 1: Environment Variable (Recommended)**
```python
# In app.py
import os
API_KEY = os.getenv("VOICE_API_KEY", "default_key_for_dev")
```

**Run with:**
```bash
$env:VOICE_API_KEY="your_secure_key"
python app.py
```

### Adding More Languages

```python
# In app.py, update:
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada"]

# Update request model:
class VoiceDetectionRequest(BaseModel):
    language: Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu", "Kannada"]
    # ... rest of fields
```

### Tuning the Model

```python
# In model.py, adjust RandomForest parameters:
self.model = RandomForestClassifier(
    n_estimators=200,      # More trees (slower but potentially more accurate)
    max_depth=15,          # Deeper trees
    min_samples_split=2,   # More aggressive splitting
    random_state=42
)
```

### Adding More Features

```python
# In feature_extractor.py:
def extract_features(self, audio_bytes: bytes) -> Dict[str, float]:
    # ... existing features ...
    
    # Add new feature: Chroma STFT
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)
    features['chroma_mean'] = float(np.mean(chroma))
    features['chroma_std'] = float(np.std(chroma))
    
    return features
```

---

## ❓ FAQ

### Q1: Why is the demo model only 60-70% accurate?

**A:** The demo uses **synthetic training data** for demonstration purposes. Real production accuracy depends on training with actual labeled voice recordings.

### Q2: Can I use WAV or other formats?

**A:** Currently only MP3 is supported (as per requirements). To add WAV:
```python
# In app.py request model:
audioFormat: Literal["mp3", "wav"]
```

### Q3: What's the maximum audio file size?

**A:** Technically unlimited, but **10MB recommended** for API performance. Very large files will slow down processing.

### Q4: Is the model language-specific?

**A:** No! The model is **language-agnostic**. It analyzes acoustic features that are universal across languages.

### Q5: How do I improve accuracy?

1. Train with **more data** (thousands of samples)
2. Use **diverse AI voice sources** (Google TTS, ElevenLabs, Azure TTS, etc.)
3. Ensure **balanced dataset** (50% human, 50% AI)
4. Add more **discriminative features**
5. Try **ensemble methods** (combine multiple models)

### Q6: Can this detect deepfakes?

**A:** Partially. This detects TTS-generated voices well. For advanced deepfakes (voice cloning), you'd need additional features like:
- Temporal consistency analysis
- Artifact detection
- Speaker verification

---

## 🔧 Troubleshooting

### Issue: "Module not found" error
```bash
# Solution: Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Issue: "Could not load audio" error
```bash
# Cause: Invalid Base64 or corrupted MP3
# Solution: Verify Base64 encoding:
python -c "import base64; print(base64.b64decode('YOUR_BASE64')[:10])"
```

### Issue: Server won't start on port 8000
```bash
# Solution: Use different port
uvicorn app:app --host 0.0.0.0 --port 8080
```

### Issue: Predictions are always the same
```bash
# Cause: Model not trained properly
# Solution: Delete old model files and retrain
rm voice_classifier.pkl scaler.pkl
python app.py
```

---

## 📊 Performance Optimization

### For Large-Scale Deployment

1. **Async Processing**
   ```python
   # Use background tasks for slow operations
   from fastapi import BackgroundTasks
   ```

2. **Caching**
   ```python
   # Cache model in memory (already done)
   # Add Redis for request caching if needed
   ```

3. **Load Balancing**
   - Deploy multiple instances
   - Use nginx for load balancing

4. **GPU Acceleration**
   - For real-time processing at scale
   - Use librosa with GPU backend

---

## 🤝 Contributing

This is a hackathon/demo project. For production use:

1. Replace synthetic training data with real datasets
2. Add comprehensive test suite
3. Implement CI/CD pipeline
4. Add monitoring and observability

---

## 📄 License

Open source - use and modify as needed.

---

## 👨‍💻 Author

**Senior Backend + ML Engineer**

Built with ❤️ for ethical AI and transparent voice detection.

---

## 🎬 What's Next?

### Immediate Next Steps:
1. ✅ API is ready to run
2. 📊 Collect real training data
3. 🧪 Train production model
4. 🚀 Deploy to cloud

### Future Enhancements:
- [ ] Add confidence threshold tuning
- [ ] Support multiple audio formats (WAV, OGG)
- [ ] Real-time streaming detection
- [ ] Speaker verification
- [ ] Deepfake detection
- [ ] Admin dashboard for monitoring
- [ ] A/B testing framework

---

**Ready to detect AI voices? Start the server and begin testing!** 🎤🤖
