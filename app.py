"""
FastAPI REST API for AI Voice Detection
Detects whether a voice recording is AI-generated or spoken by a human.
"""

from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field, validator
from typing import Literal
import base64
from feature_extractor import AudioFeatureExtractor
from model import VoiceClassifier
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

# API Key (In production, use environment variables or secret management)
API_KEY = "YOUR_SECRET_API_KEY"

# Initialize feature extractor and classifier
feature_extractor = AudioFeatureExtractor()
classifier = VoiceClassifier()


# Request Model
class VoiceDetectionRequest(BaseModel):
    """Request schema for voice detection."""
    language: Literal["Tamil", "English", "Hindi", "Malayalam", "Telugu"] = Field(
        ..., 
        description="Language of the audio recording"
    )
    audioFormat: Literal["mp3"] = Field(
        ..., 
        description="Audio format (only MP3 supported)"
    )
    audioBase64: str = Field(
        ..., 
        description="Base64-encoded MP3 audio file"
    )

    @validator('audioBase64')
    def validate_base64(cls, v):
        """Validate that audioBase64 is valid Base64 string."""
        if not v or len(v.strip()) == 0:
            raise ValueError("audioBase64 cannot be empty")
        return v


# Success Response Model
class VoiceDetectionResponse(BaseModel):
    """Success response schema."""
    status: Literal["success"] = "success"
    language: str
    classification: Literal["AI_GENERATED", "HUMAN"]
    confidenceScore: float = Field(..., ge=0.0, le=1.0)
    explanation: str


# Error Response Model
class ErrorResponse(BaseModel):
    """Error response schema."""
    status: Literal["error"] = "error"
    message: str


def validate_api_key(x_api_key: str = Header(..., alias="x-api-key")) -> None:
    """
    Validate API key from request header.
    
    Args:
        x_api_key: API key from x-api-key header
        
    Raises:
        HTTPException: If API key is invalid or missing
    """
    if x_api_key != API_KEY:
        logger.warning(f"Invalid API key attempt: {x_api_key[:10]}...")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )


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
    x_api_key: str = Header(..., alias="x-api-key")
) -> VoiceDetectionResponse:
    """
    Detect whether a voice recording is AI-generated or human.
    
    **Authentication:** Requires valid API key in `x-api-key` header.
    
    **Process:**
    1. Validate API key
    2. Decode Base64 audio
    3. Extract audio features (MFCC, pitch, ZCR, spectral centroid, energy variance)
    4. Classify using ML model (language-agnostic)
    5. Return prediction with confidence score
    
    **Important:** Audio is NOT modified (no resampling, no trimming).
    """
    try:
        # Step 1: Validate API key
        validate_api_key(x_api_key)
        
        # Step 2: Decode Base64 audio safely
        try:
            audio_bytes = base64.b64decode(request.audioBase64, validate=True)
        except Exception as e:
            logger.error(f"Base64 decoding failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid Base64 encoding in audioBase64"
            )
        
        # Validate audio is not empty
        if len(audio_bytes) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Decoded audio is empty"
            )
        
        logger.info(f"Processing {request.language} audio ({len(audio_bytes)} bytes)")
        
        # Step 3: Extract features (NO audio modification)
        try:
            features = feature_extractor.get_feature_vector(audio_bytes)
        except Exception as e:
            logger.error(f"Feature extraction failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to extract features from audio: {str(e)}"
            )
        
        # Step 4: Classify using ML model
        try:
            classification, confidence_score, explanation = classifier.predict(features)
        except Exception as e:
            logger.error(f"Classification failed: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Classification failed"
            )
        
        # Step 5: Return response
        logger.info(f"Result: {classification} ({confidence_score:.2f})")
        
        return VoiceDetectionResponse(
            status="success",
            language=request.language,
            classification=classification,
            confidenceScore=round(confidence_score, 4),
            explanation=explanation
        )
    
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    
    except Exception as e:
        # Catch-all for unexpected errors
        logger.exception("Unexpected error in voice detection")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
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
    return {
        "status": "error",
        "message": "Invalid request format or malformed request"
    }


if __name__ == "__main__":
    import uvicorn
    
    # Load or initialize model on startup
    logger.info("Initializing voice classifier...")
    if not classifier.load_model():
        logger.warning("No pre-trained model found. Initializing with synthetic data...")
        classifier._load_pretrained_model()
    
    # Run server
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Development only
        log_level="info"
    )
