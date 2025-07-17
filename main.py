"""
FastAPI backend for YOLO11 object detection with comprehensive error handling.
Prevents 500 server errors with proper exception handling and validation.
"""

import os
import logging
import traceback
from typing import Optional, List, Dict, Any
from io import BytesIO
import tempfile

from fastapi import FastAPI, File, UploadFile, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="YOLO11 Object Detection API",
    description="API for object detection using fine-tuned YOLO11 model",
    version="1.0.0"
)

# Configure CORS to prevent CORS-related errors
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for model
model = None
model_loaded = False

# Response models
class DetectionResult(BaseModel):
    class_name: str
    confidence: float
    bbox: List[float]  # [x1, y1, x2, y2]

class PredictionResponse(BaseModel):
    success: bool
    message: str
    detections: Optional[List[DetectionResult]] = None
    image_size: Optional[Dict[str, int]] = None

class HealthResponse(BaseModel):
    status: str
    model_loaded: bool
    message: str

def load_model():
    """Load YOLO11 model with proper error handling."""
    global model, model_loaded
    
    try:
        # Try to import ultralytics
        try:
            from ultralytics import YOLO
        except ImportError as e:
            logger.error(f"Failed to import ultralytics: {e}")
            raise HTTPException(
                status_code=500,
                detail="ultralytics library not installed. Please install with: pip install ultralytics"
            )
        
        # Check for model file
        model_path = os.getenv("MODEL_PATH", "best.pt")
        
        if not os.path.exists(model_path):
            logger.warning(f"Model file not found at {model_path}. Using default YOLO11n model.")
            model_path = "yolo11n.pt"  # Fallback to default model
        
        logger.info(f"Loading model from: {model_path}")
        model = YOLO(model_path)
        model_loaded = True
        logger.info("Model loaded successfully")
        
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        logger.error(traceback.format_exc())
        model_loaded = False
        # Don't raise exception here, let the API start and handle gracefully

@app.on_event("startup")
async def startup_event():
    """Initialize the model on startup."""
    logger.info("Starting YOLO11 API...")
    load_model()

@app.get("/", response_model=Dict[str, str])
async def root():
    """Root endpoint with basic info."""
    return {
        "message": "YOLO11 Object Detection API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint to verify API and model status."""
    try:
        return HealthResponse(
            status="healthy" if model_loaded else "model_not_loaded",
            model_loaded=model_loaded,
            message="API is running" if model_loaded else "API running but model not loaded"
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="error",
            model_loaded=False,
            message=f"Health check failed: {str(e)}"
        )

@app.post("/predict", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    """
    Perform object detection on uploaded image.
    
    Args:
        file: Uploaded image file
        
    Returns:
        PredictionResponse with detection results
    """
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type: {file.content_type}. Please upload an image file."
            )
        
        # Check if model is loaded
        if not model_loaded or model is None:
            logger.error("Model not loaded")
            return PredictionResponse(
                success=False,
                message="Model not loaded. Please check server logs and model file."
            )
        
        # Read and validate file
        try:
            contents = await file.read()
            if len(contents) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Empty file uploaded"
                )
        except Exception as e:
            logger.error(f"Failed to read uploaded file: {e}")
            raise HTTPException(
                status_code=400,
                detail=f"Failed to read uploaded file: {str(e)}"
            )
        
        # Create temporary file for processing
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(contents)
                tmp_file_path = tmp_file.name
            
            # Run inference
            logger.info(f"Running inference on image: {file.filename}")
            results = model(tmp_file_path)
            
            # Process results
            detections = []
            for result in results:
                if result.boxes is not None:
                    for box in result.boxes:
                        # Extract box coordinates
                        x1, y1, x2, y2 = box.xyxy[0].tolist()
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        
                        # Get class name
                        class_name = model.names.get(class_id, f"class_{class_id}")
                        
                        detections.append(DetectionResult(
                            class_name=class_name,
                            confidence=confidence,
                            bbox=[x1, y1, x2, y2]
                        ))
            
            # Get image dimensions
            image_size = {
                "width": int(results[0].orig_shape[1]),
                "height": int(results[0].orig_shape[0])
            }
            
            logger.info(f"Detection completed. Found {len(detections)} objects.")
            
            return PredictionResponse(
                success=True,
                message=f"Detection completed successfully. Found {len(detections)} objects.",
                detections=detections,
                image_size=image_size
            )
            
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            logger.error(traceback.format_exc())
            return PredictionResponse(
                success=False,
                message=f"Inference failed: {str(e)}"
            )
        
        finally:
            # Clean up temporary file
            try:
                if 'tmp_file_path' in locals():
                    os.unlink(tmp_file_path)
            except Exception as e:
                logger.warning(f"Failed to clean up temporary file: {e}")
                
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Catch any unexpected errors
        logger.error(f"Unexpected error in predict endpoint: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler to prevent unhandled 500 errors."""
    logger.error(f"Unhandled exception: {exc}")
    logger.error(traceback.format_exc())
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error occurred",
            "detail": str(exc) if app.debug else "Please check server logs"
        }
    )

if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )