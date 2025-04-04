# Face Recognition Attendance System

Modern facial recognition system that automates attendance tracking. Captures faces in real-time, logs attendance with timestamps, and provides an intuitive dashboard for managing records - all accessible through a simple web interface.

![Python](https://img.shields.io/badge/python-v3.9-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![OpenCV](https://img.shields.io/badge/opencv-%23white.svg?style=flat&logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Try it at : https://face-recognition-attendance-system-d8b4.onrender.com/

![Interface Example](https://github.com/Psantaniello24/FACE_RECOGNITION_ATTENDANCE_SYSTEM/blob/main/face_recognition.png)

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
git clone https://github.com/Psantaniello24/FACE_RECOGNITION_ATTENDANCE_SYSTEM.git
cd facetrack-pro

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The application will be available at `http://localhost:8000`

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

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- MTCNN for face detection
- FaceNet for face recognition
- OpenCV for image processing
- FastAPI for the web framework 
