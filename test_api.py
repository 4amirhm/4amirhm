"""
Test script for YOLO11 API
"""

import requests
import json
import os
from pathlib import Path

def test_api(base_url: str = "http://localhost:8000"):
    """Test the API endpoints"""
    
    print(f"Testing API at {base_url}")
    print("=" * 50)
    
    # Test 1: Root endpoint
    try:
        response = requests.get(f"{base_url}/")
        print(f"✓ Root endpoint: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Root endpoint failed: {e}")
    
    print()
    
    # Test 2: Health check
    try:
        response = requests.get(f"{base_url}/health")
        print(f"✓ Health check: {response.status_code}")
        health_data = response.json()
        print(f"  Status: {health_data.get('status')}")
        print(f"  Model loaded: {health_data.get('model_loaded')}")
        print(f"  Message: {health_data.get('message')}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
    
    print()
    
    # Test 3: Prediction endpoint (if test image exists)
    test_image_path = "test_image.jpg"
    if os.path.exists(test_image_path):
        try:
            with open(test_image_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(f"{base_url}/predict", files=files)
            
            print(f"✓ Prediction endpoint: {response.status_code}")
            result = response.json()
            print(f"  Success: {result.get('success')}")
            print(f"  Message: {result.get('message')}")
            if result.get('detections'):
                print(f"  Detections found: {len(result['detections'])}")
                for i, det in enumerate(result['detections'][:3]):  # Show first 3
                    print(f"    {i+1}. {det['class_name']} ({det['confidence']:.2f})")
        except Exception as e:
            print(f"✗ Prediction endpoint failed: {e}")
    else:
        print("ℹ Skipping prediction test (no test image found)")
    
    print()
    print("Testing complete!")

if __name__ == "__main__":
    test_api()