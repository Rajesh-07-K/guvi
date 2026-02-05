"""
FastAPI REST API for AI Voice Detection
Detects whether a voice recording is AI-generated or spoken by a human.
"""

from fastapi import FastAPI, Header, HTTPException, status, Request
from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
import base64
from fastapi.responses import JSONResponse
from feature_extractor import AudioFeatureExtractor
from model import VoiceClassifier
from language_detector import LanguageDetector
import logging
import os
import requests

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------
app = FastAPI(
    title="AI Voice Detection API",
    description="Production-ready REST API to detect AI-generated vs human voices",
    version="1.0.0"
)

# --------------------------------------------------
# Config
# --------------------------------------------------
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

API_KEY = os.getenv("API_KEY", "dev_key")

# --------------------------------------------------
# Model Initialization
# --------------------------------------------------
feature_extractor = AudioFeatureExtractor()
classifier = VoiceClassifier()
language_detector = LanguageDetector()

logger.info("Loading voice classifier...")
if not classifier.load_model():
    logger.warning("No pre-trained voice model found. Initializing with synthetic data...")
    classifier._load_pretrained_model()

logger.info("Loading language detector...")
if not language_detector.load_model():
    logger.warning("No pre-trained language model found. Initializing with synthetic data...")
    language_detector.initialize_with_synthetic_data()

logger.info("[SUCCESS] All models loaded successfully!")

# --------------------------------------------------
# Request / Response Models
# --------------------------------------------------
class VoiceDetectionRequest(BaseModel):
    language: Optional[Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"]] = None
    audioFormat: Literal["mp3"]
    audioBase64: Optional[str] = None
    audioUrl: Optional[str] = None

    @validator("audioBase64")
    def validate_base64(cls, v):
        if v is not None and not v.strip():
            raise ValueError("audioBase64 cannot be empty")
        return v


class VoiceDetectionResponse(BaseModel):
    status: Literal["success"] = "success"
    language: str
    classification: Literal["AI_GENERATED", "HUMAN"]
    confidenceScore: float = Field(..., ge=0.0, le=1.0)
    explanation: str


class ErrorResponse(BaseModel):
    status: Literal["error"] = "error"
    message: str

# --------------------------------------------------
# Auth Helper (Dual Support)
# --------------------------------------------------
def validate_api_key(
    x_api_key: Optional[str] = Header(None, alias="x-api-key"),
    authorization: Optional[str] = Header(None)
):
    if x_api_key == API_KEY:
        return

    if authorization and authorization.startswith("Bearer "):
        if authorization.split(" ")[1].strip() == API_KEY:
            return

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key"
    )

# --------------------------------------------------
# Audio Loader
# --------------------------------------------------
def get_audio_bytes(payload: VoiceDetectionRequest) -> bytes:
    if payload.audioBase64:
        try:
            return base64.b64decode(payload.audioBase64, validate=True)
        except Exception as e:
            raise ValueError(f"Invalid Base64 encoding: {str(e)}")

    if payload.audioUrl:
        response = requests.get(payload.audioUrl, timeout=15)
        if response.status_code != 200:
            raise ValueError("Failed to download audio")
        return response.content

    raise ValueError("No audio input provided")

# --------------------------------------------------
# Voice Detection Endpoint
# --------------------------------------------------
@app.post("/api/voice-detection", response_model=VoiceDetectionResponse)
async def detect_voice(
    request: VoiceDetectionRequest,
    x_api_key: Optional[str] = Header(None, alias="x-api-key"),
    authorization: Optional[str] = Header(None)
):
    validate_api_key(x_api_key, authorization)

    try:
        audio_bytes = get_audio_bytes(request)
        if not audio_bytes:
            raise HTTPException(status_code=400, detail="Empty audio")

        detected_language = request.language
        if not detected_language:
            detected_language, _ = language_detector.predict(audio_bytes)

        features = feature_extractor.get_feature_vector(audio_bytes)
        classification, confidence, explanation = classifier.predict(features)

        return VoiceDetectionResponse(
            language=detected_language,
            classification=classification,
            confidenceScore=round(confidence, 4),
            explanation=explanation
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception("Detection failed")
        raise HTTPException(status_code=500, detail="Internal processing error")

# --------------------------------------------------
# ✅ HONEYPOT ENDPOINT (FOR HACKATHON TESTER)
# --------------------------------------------------
@app.get("/api/honeypot")
@app.post("/api/honeypot")
def honeypot(
    request: Request,
    x_api_key: Optional[str] = Header(None, alias="x-api-key")
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    logger.warning("🚨 Honeypot triggered")
    logger.warning(f"IP: {request.client.host}")
    logger.warning(f"Headers: {dict(request.headers)}")

    return {
        "status": "ok",
        "message": "Service temporarily unavailable"
    }

# --------------------------------------------------
# Health & Info
# --------------------------------------------------
@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": classifier.is_trained,
        "supported_languages": SUPPORTED_LANGUAGES
    }


@app.get("/")
async def root():
    return {
        "name": "AI Voice Detection API",
        "version": "1.0.0",
        "endpoint": "/api/voice-detection",
        "supported_languages": SUPPORTED_LANGUAGES,
        "audio_format": "mp3",
        "authentication": "Required (x-api-key header)"
    }

# --------------------------------------------------
# Custom 422 → 400
# --------------------------------------------------
@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": "Invalid request format",
            "detail": str(exc)
        }
    )

# --------------------------------------------------
# Run (Local / Render)
# --------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("app:app", host="0.0.0.0", port=port)
