# Troubleshooting Guide for YOLO11 API

## Common 500 Server Errors and Solutions

This guide addresses the most common 500 server errors that occur when deploying YOLO11 models and provides solutions.

### 1. **Missing Dependencies Error**

**Error**: `ModuleNotFoundError: No module named 'ultralytics'`

**Solution**:
```bash
pip install ultralytics
```

**Full Requirements**:
```bash
pip install -r requirements.txt
```

### 2. **Model File Not Found Error**

**Error**: Model file not found at specified path

**Solutions**:
- Place your fine-tuned model file in the `models/` directory
- Name it `best.pt` or set the `MODEL_PATH` environment variable
- The API will automatically fallback to YOLO11n if custom model is missing

**Example**:
```bash
export MODEL_PATH=/path/to/your/custom_model.pt
```

### 3. **File Upload Errors**

**Error**: Invalid file type or size errors

**Solutions**:
- Ensure file is an image (jpg, png, bmp, tiff, webp)
- Check file size is under limit (default: 10MB)
- Verify file is not corrupted

### 4. **Memory Errors**

**Error**: Out of memory during inference

**Solutions**:
- Reduce image size before upload
- Use a smaller YOLO model (e.g., yolo11n instead of yolo11x)
- Increase system memory or use cloud deployment
- Set batch size to 1 for inference

### 5. **CORS Errors**

**Error**: Cross-Origin Request Blocked

**Solutions**:
- Configure CORS origins in environment variables
- For development: set `CORS_ORIGINS=*`
- For production: specify exact domains

**Example**:
```env
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

### 6. **Permission Errors**

**Error**: Permission denied when accessing model files

**Solutions**:
- Check file permissions: `chmod 644 models/best.pt`
- Ensure the application has read access to model directory
- For Docker: check volume mounting permissions

### 7. **Path Resolution Errors**

**Error**: Model path not found in container

**Solutions**:
- Use absolute paths in production
- Mount model directory properly in Docker
- Set MODEL_PATH environment variable correctly

**Docker Example**:
```bash
docker run -v /host/models:/app/models -e MODEL_PATH=/app/models/best.pt yolo-api
```

### 8. **GPU/CUDA Errors**

**Error**: CUDA out of memory or device not available

**Solutions**:
- Install CPU-only version for CPU deployment:
  ```bash
  pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
  ```
- For GPU deployment, ensure CUDA drivers are installed
- Use appropriate PyTorch version for your CUDA version

### 9. **Port Already in Use**

**Error**: Port 8000 already in use

**Solutions**:
- Change port: `uvicorn main:app --host 0.0.0.0 --port 8001`
- Kill existing process: `lsof -ti:8000 | xargs kill -9`
- Use environment variable: `export API_PORT=8001`

### 10. **Import Errors**

**Error**: Various import-related errors

**Solutions**:
- Create fresh virtual environment
- Install exact dependency versions from requirements.txt
- Clear Python cache: `find . -name "*.pyc" -delete`

## Testing Your Deployment

Use the provided test script to verify everything works:

```bash
python test_api.py
```

## Health Monitoring

Check API health at any time:
```bash
curl http://localhost:8000/health
```

Expected response when working:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "message": "API is running"
}
```

## Production Deployment Checklist

- [ ] Install all dependencies from requirements.txt
- [ ] Place model file in correct location
- [ ] Set appropriate environment variables
- [ ] Configure CORS for your domain
- [ ] Set up proper logging
- [ ] Configure reverse proxy (nginx, etc.)
- [ ] Set up SSL certificates
- [ ] Monitor resource usage
- [ ] Set up automated backups of model files
- [ ] Configure error alerting

## Getting Help

If you're still experiencing issues:

1. Check the application logs for detailed error messages
2. Verify all environment variables are set correctly
3. Test with the default YOLO11n model first
4. Review the GitHub issues for similar problems
5. Contact support with detailed error logs

## Performance Optimization

For better performance in production:

- Use GPU acceleration when available
- Implement request queuing for high load
- Use caching for frequently processed images
- Consider model quantization for faster inference
- Set up load balancing for multiple instances