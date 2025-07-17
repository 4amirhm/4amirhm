# YOLO11 Object Detection API Backend

A robust FastAPI backend for serving a fine-tuned YOLO11 object detection model with comprehensive error handling to prevent 500 server errors.

## 🚀 Features

- **FastAPI Backend**: High-performance async API with automatic OpenAPI documentation
- **YOLO11 Integration**: Support for custom fine-tuned YOLO11 models
- **Comprehensive Error Handling**: Prevents 500 server errors with graceful error management
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Health Monitoring**: Built-in health check endpoints
- **CORS Enabled**: Ready for web integration
- **File Validation**: Secure file upload with type and size validation
- **Logging**: Comprehensive logging for debugging and monitoring

## 📋 Prerequisites

- Python 3.8+
- pip or conda
- Docker (optional, for containerized deployment)

## 🛠️ Installation

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/4amirhm/4amirhm.git
   cd 4amirhm
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup directories**:
   ```bash
   mkdir -p models logs temp
   ```

5. **Add your model** (optional):
   - Place your fine-tuned YOLO11 model file in the `models/` directory
   - Name it `best.pt` or set the `MODEL_PATH` environment variable

6. **Run the server**:
   ```bash
   python main.py
   ```

### Docker Deployment

1. **Build and run with Docker Compose**:
   ```bash
   docker-compose up --build
   ```

2. **Or build manually**:
   ```bash
   docker build -t yolo11-api .
   docker run -p 8000:8000 -v ./models:/app/models yolo11-api
   ```

## 📡 API Endpoints

### Health Check
```http
GET /health
```
Returns API and model status.

### Object Detection
```http
POST /predict
```
Upload an image file for object detection.

**Parameters:**
- `file`: Image file (jpg, png, bmp, tiff, webp)

**Response:**
```json
{
  "success": true,
  "message": "Detection completed successfully. Found 3 objects.",
  "detections": [
    {
      "class_name": "person",
      "confidence": 0.85,
      "bbox": [100, 50, 200, 300]
    }
  ],
  "image_size": {
    "width": 640,
    "height": 480
  }
}
```

### Documentation
- Interactive API docs: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

## ⚙️ Configuration

Create a `.env` file based on `.env.example`:

```env
MODEL_PATH=models/best.pt
MODEL_CONFIDENCE_THRESHOLD=0.25
MAX_FILE_SIZE=10485760
LOG_LEVEL=INFO
DEBUG=False
```

## 🧪 Testing

Run the test script to verify the API:

```bash
python test_api.py
```

## 🔧 Troubleshooting

### Common Issues and Solutions

1. **500 Server Error - Model not found**:
   - Ensure your model file exists in the specified path
   - Check the `MODEL_PATH` environment variable
   - The API will fallback to YOLO11n if custom model is not found

2. **Memory Issues**:
   - Reduce image size before upload
   - Increase system memory or use smaller model
   - Set appropriate confidence thresholds

3. **CORS Errors**:
   - Configure `CORS_ORIGINS` in environment variables
   - Update CORS middleware settings in `main.py`

4. **File Upload Issues**:
   - Check file format (supported: jpg, png, bmp, tiff, webp)
   - Verify file size limits (`MAX_FILE_SIZE`)

## 📁 Project Structure

```
├── main.py              # Main FastAPI application
├── config.py            # Configuration settings
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── test_api.py         # API testing script
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
├── models/             # Model files directory
├── logs/               # Log files directory
└── temp/               # Temporary files directory
```

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**:
   ```bash
   export MODEL_PATH=/path/to/your/model.pt
   export DEBUG=False
   export LOG_LEVEL=WARNING
   ```

2. **Using Gunicorn** (recommended for production):
   ```bash
   pip install gunicorn
   gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
   ```

3. **Using Docker in production**:
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- 📧 [Email](mailto:4AMIRHM@gmail.com)
- 💼 [LinkedIn](https://www.linkedin.com/in/4amirhm)
- 📊 [Kaggle](https://www.kaggle.com/amirhoseinmousavian)

---

## 🎯 About the Developer

**Amir H. Mousavian** - Computer Vision Engineer specializing in:
- **Computer Vision**: OpenCV, YOLO, TensorFlow, PyTorch
- **Backend Development**: FastAPI, Docker, MLOps
- **AI Applications**: Healthcare, Robotics, Traffic Management

### Featured Projects
- **[Vehicle Detection with YOLO11](https://www.kaggle.com/code/amirhoseinmousavian/vehicle-detection-yolo11)**: Traffic management system
- **[Brain Tumor Detection](https://www.kaggle.com/code/amirhoseinmousavian/brain-tumor-detection-95)**: Medical imaging with 95% accuracy
- **[Rice Classification](https://www.kaggle.com/code/amirhoseinmousavian/rice-detection-using-pytorch)**: Agricultural AI with 98% accuracy
