# FaceTrack Pro

Modern facial recognition system that automates attendance tracking. Captures faces in real-time, logs attendance with timestamps, and provides an intuitive dashboard for managing records - all accessible through a simple web interface.

![Python](https://img.shields.io/badge/python-v3.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=flat&logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- Real-time face detection and recognition
- User registration with face capture
- Automatic attendance logging
- User-friendly web interface
- Attendance record management
- Modern, responsive UI

## Requirements

- Python 3.9+
- OpenCV
- FastAPI
- TensorFlow (CPU version)
- SQLite
- Webcam (for capturing faces)
- Internet connection (for downloading dependencies)

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/facetrack-pro.git
cd facetrack-pro

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:8000`

## Deployment Options

### Option 1: Local Deployment

This is the simplest option for creating a public demo with a shareable link:

1. Sign up for a free account at [Render.com](https://render.com/)

2. Connect your GitHub repository to Render:
   - In the Render dashboard, click "New +" and select "Web Service"
   - Connect your GitHub account and select your repository
   - Choose "Use render.yaml" if prompted

3. Alternatively, deploy directly using this button:
   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

4. Once deployed, Render will provide you with a public URL like:
   `https://face-recognition-attendance.onrender.com`

5. Share this URL with anyone to access your demo

**Note:** For the free tier, the service may "sleep" after 15 minutes of inactivity. The first access after inactivity may take a minute to wake up.

## Important Notes for Production Deployment

1. **Database**: For production, consider using a more robust database like PostgreSQL instead of SQLite.

2. **Security**: Add proper authentication and authorization before deployment.

3. **Storage**: Use a cloud storage service for storing face embeddings in production.

4. **HTTPS**: Ensure you're using HTTPS in production as camera access requires secure origin.

5. **Environment Variables**: Store sensitive information in environment variables.

## Usage

1. Start the FastAPI server:
```bash
python app.py
```

2. Open your web browser and navigate to:
```
http://localhost:8000
```

3. Using the web interface:
   - Click "Start Camera" to begin video feed
   - To register a new face:
     - Enter the person's name
     - Position their face in the camera
     - Click "Register Face"
   - To mark attendance:
     - Position the person's face in the camera
     - Click "Capture"
   - View attendance records in the right panel

## API Endpoints

- `POST /register`: Register a new face
  - Parameters: name (string), file (image)
  - Returns: Success message or error

- `POST /recognize`: Recognize faces in an image
  - Parameters: file (image)
  - Returns: Annotated image with face detections

- `GET /attendance`: Get attendance records
  - Returns: List of attendance records with names and timestamps

## Database Schema

### Users Table
- id (INTEGER, PRIMARY KEY)
- name (TEXT)
- face_embedding (BLOB)
- created_at (TIMESTAMP)

### Attendance Table
- id (INTEGER, PRIMARY KEY)
- user_id (INTEGER, FOREIGN KEY)
- timestamp (TIMESTAMP)

## Security Considerations

- The system stores face embeddings locally in a SQLite database
- No sensitive information is transmitted over the network
- Camera access requires user permission
- Face recognition threshold can be adjusted for security/accuracy balance

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MTCNN for face detection
- FaceNet for face recognition
- OpenCV for image processing
- FastAPI for the web framework 


- venv = FACE_RECOGNITION