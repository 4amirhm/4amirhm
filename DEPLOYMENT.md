# 🚀 Quick Start Deployment Guide

## Option 1: Quick Local Setup (Recommended for Testing)

1. **Clone and Setup**:
   ```bash
   git clone https://github.com/4amirhm/4amirhm.git
   cd 4amirhm
   chmod +x start.sh
   ./start.sh
   ```

2. **Access the API**:
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Demo: Open `demo.html` in your browser

## Option 2: Docker Deployment (Recommended for Production)

1. **Build and Run**:
   ```bash
   docker-compose up --build
   ```

2. **With Custom Model**:
   ```bash
   # Place your model in models/ directory
   cp your_model.pt models/best.pt
   docker-compose up --build
   ```

## Option 3: Manual Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Setup Environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Run Server**:
   ```bash
   python main.py
   ```

## Adding Your Custom Model

1. **Place Model File**:
   ```bash
   mkdir -p models
   cp your_fine_tuned_model.pt models/best.pt
   ```

2. **Or Set Custom Path**:
   ```bash
   export MODEL_PATH=/path/to/your/model.pt
   ```

## Testing Your Deployment

```bash
# Test API health
curl http://localhost:8000/health

# Test with image (replace with your image)
curl -X POST "http://localhost:8000/predict" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@test_image.jpg"
```

## Web Integration

1. **Open `demo.html`** in your browser for a ready-to-use web interface
2. **Use JavaScript fetch** to integrate with your web application:
   ```javascript
   const formData = new FormData();
   formData.append('file', imageFile);
   
   const response = await fetch('http://localhost:8000/predict', {
       method: 'POST',
       body: formData
   });
   
   const result = await response.json();
   ```

## Production Deployment

For production, consider:
- Using a reverse proxy (nginx)
- Setting up SSL certificates
- Configuring proper CORS origins
- Using environment variables for sensitive data
- Setting up monitoring and logging
- Using a process manager (systemd, PM2)

## Support

If you encounter issues:
1. Check `TROUBLESHOOTING.md` for common solutions
2. Review application logs
3. Test with the health endpoint
4. Verify all dependencies are installed

The API is designed to handle errors gracefully and prevent 500 server errors through comprehensive error handling.