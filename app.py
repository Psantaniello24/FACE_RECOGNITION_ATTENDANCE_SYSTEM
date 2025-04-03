from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Form
from fastapi.responses import StreamingResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from face_recognition_system import FaceRecognitionSystem
import io
from typing import List
import json
import os
import sqlite3

app = FastAPI(title="Face Recognition Attendance System")

# Create templates directory if it doesn't exist
os.makedirs("templates", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates configuration
templates = Jinja2Templates(directory="templates")

# Add CORS middleware to allow access from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Initialize face recognition system
face_system = FaceRecognitionSystem()

def process_image_file(file_content: bytes) -> np.ndarray:
    """Convert uploaded file content to numpy array."""
    nparr = np.frombuffer(file_content, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Serve the main page."""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/register")
async def register_face(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    """Register a new face in the system."""
    try:
        contents = await file.read()
        image = process_image_file(contents)
        
        # Validate name
        if not name or len(name.strip()) == 0:
            raise HTTPException(status_code=400, detail="Name cannot be empty")
            
        success = face_system.register_new_face(name.strip(), image)
        if success:
            return {"message": f"Successfully registered {name}"}
        else:
            raise HTTPException(status_code=400, detail="No face detected in the image")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recognize")
async def recognize_face(file: UploadFile = File(...)):
    """Recognize faces in the uploaded image."""
    try:
        contents = await file.read()
        image = process_image_file(contents)
        
        annotated_frame, faces = face_system.process_frame(image)
        
        # Convert the annotated frame to bytes for response
        _, buffer = cv2.imencode('.jpg', annotated_frame)
        return StreamingResponse(io.BytesIO(buffer.tobytes()), media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/attendance")
async def get_attendance():
    """Get attendance records."""
    try:
        # Create a new database connection
        conn = sqlite3.connect(face_system.db_path)
        cursor = conn.cursor()
        
        # Get the attendance records with user names
        cursor.execute('''
            SELECT u.name, a.timestamp 
            FROM attendance a 
            JOIN users u ON a.user_id = u.id 
            ORDER BY a.timestamp DESC
            LIMIT 50
        ''')
        
        records = cursor.fetchall()
        
        # Close the connection
        cursor.close()
        conn.close()
        
        # Format the records
        attendance_records = [
            {
                "name": name,
                "timestamp": timestamp
            }
            for name, timestamp in records
        ]
        
        return attendance_records
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.delete("/attendance")
async def delete_attendance():
    """Delete all attendance records."""
    try:
        # Create a new database connection
        conn = sqlite3.connect(face_system.db_path)
        cursor = conn.cursor()
        
        # Delete all attendance records
        cursor.execute('DELETE FROM attendance')
        
        # Commit the changes
        conn.commit()
        
        # Close the connection
        cursor.close()
        conn.close()
        
        return {"message": "All attendance records deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 