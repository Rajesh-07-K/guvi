"""
FastAPI REST API for AI Voice Detection
Detects whether a voice recording is AI-generated or spoken by a human.
"""

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import Literal, Optional
import base64
from fastapi.responses import JSONResponse
from feature_extractor import AudioFeatureExtractor
from model import VoiceClassifier
from language_detector import LanguageDetector
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="AI Voice Detection API",
    description="Production-ready REST API to detect AI-generated vs human voices",
    version="1.0.0"
)

# Supported languages (strictly fixed)
SUPPORTED_LANGUAGES = ["Tamil", "English", "Hindi", "Malayalam", "Telugu"]

# API Key for Hackathon (Bearer token format)
# For hackathon endpoint tester, use: Authorization: Bearer <this-key>
API_KEY = "hackathon-ai-voice-12345"

# Initialize feature extractor and classifier
feature_extractor = AudioFeatureExtractor()
classifier = VoiceClassifier()
language_detector = LanguageDetector()

# Load models immediately on module import
logger.info("Loading voice classifier...")
if not classifier.load_model():
    logger.warning("No pre-trained voice model found. Initializing with synthetic data...")
    classifier._load_pretrained_model()

logger.info("Loading language detector...")
if not language_detector.load_model():
    logger.warning("No pre-trained language model found. Initializing with synthetic data...")
    language_detector.initialize_with_synthetic_data()

logger.info("[SUCCESS] All models loaded successfully!")


# ... imports ...
import requests

# ... (logging setup - unchanged)

# ... (app init - unchanged)

# ... (Supported languages - unchanged)

# ... (API Key - unchanged)

# ... (Model initialization - unchanged)


# Request Model
class VoiceDetectionRequest(BaseModel):
    """Request schema for voice detection."""
    language: Optional[Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"]] = Field(
        None, 
        description="Language of the audio recording (optional - will be auto-detected if not provided)"
    )
    audioFormat: Literal["mp3"] = Field(
        ..., 
        description="Audio format (only MP3 supported)"
    )
    # Make audioBase64 optional since audioUrl might be used instead
    audioBase64: Optional[str] = Field(
        None, 
        description="Base64-encoded MP3 audio file (priority over URL)"
    )
    audioUrl: Optional[str] = Field(
        None,
        description="URL to download MP3 audio file (used if audioBase64 not provided)"
    )

    @validator('audioBase64')
    def validate_base64_content(cls, v):
        """Validate that audioBase64 is not empty if provided."""
        if v is not None and len(v.strip()) == 0:
            raise ValueError("audioBase64 cannot be empty if provided")
        return v


# Success Response Model - Unchanged
class VoiceDetectionResponse(BaseModel):
    """Success response schema."""
    status: Literal["success"] = "success"
    language: str
    classification: Literal["AI_GENERATED", "HUMAN"]
    confidenceScore: float = Field(..., ge=0.0, le=1.0)
    explanation: str


# Error Response Model - Unchanged
class ErrorResponse(BaseModel):
    """Error response schema."""
    status: Literal["error"] = "error"
    message: str


def validate_api_key(
    x_api_key: Optional[str] = Header(None, alias="x-api-key"),
    authorization: Optional[str] = Header(None)
) -> None:
    """
    Validate API key from EITHER x-api-key header OR Authorization: Bearer header.
    Needed for Hackathon tester compatibility.
    """
    # 1. Check x-api-key
    if x_api_key == API_KEY:
        return

    # 2. Check Authorization: Bearer <token>
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1].strip()
        if token == API_KEY:
            return

    # If neither matched
    logger.warning("Authentication failed: Missing or invalid API key")
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API key. Use 'x-api-key' header or 'Authorization: Bearer <token>'"
    )


def get_audio_bytes(payload: VoiceDetectionRequest) -> bytes:
    """
    Retrieve audio bytes from either Base64 string or URL.
    Input Priority: audioBase64 > audioUrl
    """
    # 1. Try Base64
    if payload.audioBase64:
        try:
            return base64.b64decode(payload.audioBase64, validate=True)
        except Exception as e:
            raise ValueError(f"Invalid Base64 encoding: {str(e)}")

    # 2. Try URL
    if payload.audioUrl:
        try:
            logger.info(f"Downloading audio from URL: {payload.audioUrl}")
            response = requests.get(payload.audioUrl, timeout=15)
            if response.status_code != 200:
                raise ValueError(f"Failed to download audio. Status: {response.status_code}")
            return response.content
        except Exception as e:
            raise ValueError(f"Audio download failed: {str(e)}")

    # 3. No input provided
    raise ValueError("No audio input provided. Send either 'audioBase64' or 'audioUrl'.")


@app.post(
    "/api/voice-detection",
    response_model=VoiceDetectionResponse,
    responses={
        401: {"model": ErrorResponse, "description": "Invalid API key"},
        400: {"model": ErrorResponse, "description": "Bad request"},
        500: {"model": ErrorResponse, "description": "Internal server error"}
    }
)
async def detect_voice(
    request: VoiceDetectionRequest,
    x_api_key: Optional[str] = Header(None, alias="x-api-key"),
    authorization: Optional[str] = Header(None)
) -> VoiceDetectionResponse:
    """
    Detect whether a voice recording is AI-generated or human.
    Supports Base64 input OR URL input.
    """
    try:
        # Step 1: Validate API key (Dual Support)
        validate_api_key(x_api_key, authorization)
        
        # Step 2: Get Audio Bytes
        try:
            audio_bytes = get_audio_bytes(request)
        except ValueError as e:
            logger.error(f"Input error: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        
        # Validate audio is not empty
        if len(audio_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Audio content is empty"
            )
        
        # Step 3: Detect language (if not provided)
        detected_language = request.language
        language_confidence = 1.0
        
        if detected_language is None:
            try:
                detected_language, language_confidence = language_detector.predict(audio_bytes)
                logger.info(f"Auto-detected language: {detected_language} (confidence: {language_confidence:.2f})")
            except Exception as e:
                # Fallback to English if detection fails completely (shouldn't happen often)
                logger.error(f"Language detection failed: {str(e)}")
                detected_language = "English" 
                # Don't crash here - proceed with fallback
                
        logger.info(f"Processing {detected_language} audio ({len(audio_bytes)} bytes)")
        
        # Step 4: Extract features (NO audio modification)
        try:
            features = feature_extractor.get_feature_vector(audio_bytes)
        except Exception as e:
            logger.error(f"Feature extraction failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to extract features from audio: {str(e)}"
            )
        
        # Step 5: Classify using ML model
        try:
            classification, confidence_score, explanation = classifier.predict(features)
        except Exception as e:
            logger.error(f"Classification failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Classification failed"
            )
        
        # Step 6: Return response
        logger.info(f"Result: {classification} ({confidence_score:.2f})")
        
        return VoiceDetectionResponse(
            status="success",
            language=detected_language,
            classification=classification,
            confidenceScore=round(confidence_score, 4),
            explanation=explanation
        )
    
    except HTTPException:
        # Re-raise known HTTP exceptions
        raise
    
    except Exception as e:
        # CRITICAL: Catch-all for unexpected errors to prevent server crash
        # Return a structured error response instead of 500 crash
        logger.exception("Unexpected global error in voice detection")
        # For the hackathon tester, functionality is key. 
        # We return 500 but with a clean JSON message.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal processing error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": classifier.is_trained,
        "supported_languages": SUPPORTED_LANGUAGES
    }


@app.get("/")
async def root():
    """API information endpoint."""
    return {
        "name": "AI Voice Detection API",
        "version": "1.0.0",
        "endpoint": "/api/voice-detection",
        "supported_languages": SUPPORTED_LANGUAGES,
        "audio_format": "mp3",
        "authentication": "Required (x-api-key header)"
    }


# Custom exception handler for validation errors
@app.exception_handler(422)
async def validation_exception_handler(request, exc):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "error",
            "message": "Invalid request format or malformed request",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    import os
    
    # Support dynamic port for cloud deployment (Render, Railway, etc.)
    port = int(os.environ.get("PORT", 8000))
    
    # Run server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
