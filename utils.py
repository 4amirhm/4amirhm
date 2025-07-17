"""
Utility functions for the YOLO11 API
"""

import os
import logging
from typing import List, Optional
from pathlib import Path

def setup_logging(log_level: str = "INFO", log_file: Optional[str] = None) -> None:
    """Setup logging configuration"""
    
    # Create logs directory if it doesn't exist
    if log_file:
        log_dir = Path(log_file).parent
        log_dir.mkdir(exist_ok=True)
    
    # Configure logging
    handlers = [logging.StreamHandler()]
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

def validate_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
    """Validate if file has allowed extension"""
    if not filename:
        return False
    
    file_ext = Path(filename).suffix.lower()
    return file_ext in [ext.lower() for ext in allowed_extensions]

def validate_file_size(file_size: int, max_size: int) -> bool:
    """Validate if file size is within limits"""
    return 0 < file_size <= max_size

def create_directories() -> None:
    """Create necessary directories"""
    directories = ["models", "logs", "temp"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)

def check_model_file(model_path: str) -> bool:
    """Check if model file exists"""
    return os.path.exists(model_path) and os.path.isfile(model_path)

def get_model_info(model_path: str) -> dict:
    """Get model file information"""
    if not check_model_file(model_path):
        return {"exists": False}
    
    stat = os.stat(model_path)
    return {
        "exists": True,
        "size": stat.st_size,
        "modified": stat.st_mtime,
        "path": model_path
    }