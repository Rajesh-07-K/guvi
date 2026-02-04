# AI Voice Detection API

Production-ready REST API to detect whether a voice recording is AI-generated or spoken by a human.

## 🎯 Features

- **Language Support**: Tamil, English, Hindi, Malayalam, Telugu (language-agnostic model)
- **Audio Format**: MP3 only (Base64 encoded)
- **Authentication**: API key via `x-api-key` header
- **ML Model**: Random Forest classifier with 18 acoustic features
- **No Audio Modification**: Original audio preserved (no resampling/trimming)

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## 🚀 Usage

### Start the server
```bash
python app.py
```

Server runs on `http://0.0.0.0:8000`

### API Endpoint

**POST** `/api/voice-detection`

**Headers:**
```
x-api-key: YOUR_SECRET_API_KEY
Content-Type: application/json
```

**Request Body:**
```json
{
  "language": "Tamil",
  "audioFormat": "mp3",
  "audioBase64": "<Base64 MP3 string>"
}
```

**Success Response (200):**
```json
{
  "status": "success",
  "language": "Tamil",
  "classification": "AI_GENERATED",
  "confidenceScore": 0.87,
  "explanation": "High consistency in pitch and spectral patterns typical of synthetic voices"
}
```

**Error Response (401/400/500):**
```json
{
  "status": "error",
  "message": "Invalid API key or malformed request"
}
```

## 🧠 Detection Logic

### Feature Extraction (feature_extractor.py)
The system extracts 18 acoustic features using **librosa**:

1. **MFCC (Mel-Frequency Cepstral Coefficients)**
   - Mean, Std Dev, Variance
   - Captures spectral envelope differences between AI and human voices

2. **Pitch Analysis**
   - Mean pitch, Pitch variance, Pitch std dev
   - AI voices tend to have more consistent pitch patterns

3. **Zero-Crossing Rate (ZCR)**
   - Mean, Std Dev
   - Measures signal noisiness and voice texture

4. **Spectral Centroid**
   - Mean, Std Dev, Variance
   - Indicates "brightness" of sound (AI voices often have distinct centroids)

5. **Energy Variance**
   - RMS energy mean, variance, std dev
   - AI voices typically have more uniform energy distribution

6. **Additional Features**
   - Spectral rolloff (frequency distribution)
   - Spectral bandwidth (spectrum width)

### Classification (model.py)

**Model:** Random Forest Classifier
- **Estimators:** 100 trees
- **Max Depth:** 10
- **Class Weighting:** Balanced (handles imbalanced data)
- **Language-Agnostic:** Single model works across all 5 languages

**Training Data:**
⚠️ **IMPORTANT:** The current implementation uses synthetic training data for demonstration.

**For production deployment:**
1. Collect real labeled datasets:
   - Human voice recordings (labeled 0)
   - AI-generated voices from various TTS systems (labeled 1)
2. Ensure balanced representation across all 5 languages
3. Retrain model using `model.train(X_train, y_train)`
4. Save model using `model.save_model()`

**Detection Approach:**
- AI voices typically show:
  - Lower pitch variance (more consistent)
  - Lower energy variance (uniform distribution)
  - Distinct spectral patterns
  - Reduced natural irregularities

- Human voices typically show:
  - Higher pitch variance (natural fluctuations)
  - Higher energy variance
  - Natural breathing patterns
  - Micro-variations in timbre

## 🔒 Security

- **API Key Authentication**: All requests require valid `x-api-key` header
- **Base64 Validation**: Safe decoding with error handling
- **Input Validation**: Pydantic models enforce strict schemas
- **No Audio Storage**: Audio processed in-memory only

## 📁 File Structure

```
.
├── app.py                 # FastAPI main application
├── feature_extractor.py   # Audio feature extraction using librosa
├── model.py              # ML classifier (Random Forest)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Sample Request
```bash
curl -X POST http://localhost:8000/api/voice-detection \
  -H "x-api-key: YOUR_SECRET_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "language": "English",
    "audioFormat": "mp3",
    "audioBase64": "<your_base64_string>"
  }'
```

## ⚠️ Production Checklist

Before deploying to production:

1. **Replace API Key**
   - Move `YOUR_SECRET_API_KEY` to environment variable
   - Use secure secret management (e.g., AWS Secrets Manager)

2. **Train with Real Data**
   - Collect labeled voice datasets (human + AI-generated)
   - Include samples from all 5 languages
   - Minimum 1000+ samples per class recommended

3. **Model Evaluation**
   - Test on held-out validation set
   - Calculate precision, recall, F1-score
   - Target accuracy: >85% for production use

4. **Disable Auto-Reload**
   - Set `reload=False` in uvicorn.run()

5. **Add Rate Limiting**
   - Implement request throttling (e.g., using slowapi)

6. **Logging**
   - Configure production-grade logging
   - Log to file or external service

7. **HTTPS**
   - Deploy behind reverse proxy (nginx)
   - Enable SSL/TLS certificates

8. **Monitoring**
   - Add performance metrics
   - Track prediction latency and accuracy

## 🤝 Ethical AI Practices

This API is designed with transparency and ethics in mind:

✅ **Transparent**: Clear explanation provided with each prediction
✅ **Non-Discriminatory**: Language-agnostic model treats all languages equally
✅ **Privacy-Preserving**: No audio storage, in-memory processing only
✅ **Auditable**: Comprehensive logging for accountability

## 📄 License

This is a hackathon/demonstration project. Adapt as needed for your use case.

## 👨‍💻 Author

Built by a Senior Backend + ML Engineer for production-ready AI voice detection.
