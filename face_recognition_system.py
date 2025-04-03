import cv2
import numpy as np
from mtcnn import MTCNN
import tensorflow as tf
import sqlite3
from datetime import datetime
import os
from typing import List, Tuple, Optional

class FaceRecognitionSystem:
    def __init__(self, db_path: str = "attendance.db"):
        self.detector = MTCNN()
        # Create a simple CNN model for face recognition
        self.facenet_model = self._create_simple_model()
        self.db_path = db_path
        self._init_database()
        
    def _create_simple_model(self):
        """Create a simple CNN model for face recognition."""
        model = tf.keras.Sequential([
            tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(160, 160, 3)),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.MaxPooling2D((2, 2)),
            tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
            tf.keras.layers.Flatten(),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dense(128, activation='relu')
        ])
        return model
        
    def _init_database(self):
        """Initialize SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                face_embedding BLOB NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create attendance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()

    def detect_faces(self, image: np.ndarray) -> List[dict]:
        """Detect faces in the image using MTCNN."""
        return self.detector.detect_faces(image)

    def get_face_embedding(self, face_img: np.ndarray) -> np.ndarray:
        """Generate face embedding for a face image."""
        # Preprocess image
        face_img = cv2.resize(face_img, (160, 160))
        face_img = face_img.astype('float32')
        face_img = (face_img - 127.5) / 128.0
        face_img = np.expand_dims(face_img, axis=0)
        
        # Generate embedding
        embedding = self.facenet_model.predict(face_img, verbose=0)[0]
        return embedding

    def register_new_face(self, name: str, face_img: np.ndarray) -> bool:
        """Register a new face in the database."""
        faces = self.detect_faces(face_img)
        if not faces:
            return False
            
        # Get the largest face
        face = max(faces, key=lambda x: x['confidence'])
        x, y, w, h = face['box']
        face_img = face_img[y:y+h, x:x+w]
        
        # Generate embedding
        embedding = self.get_face_embedding(face_img)
        
        # Store in database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO users (name, face_embedding) VALUES (?, ?)',
            (name, embedding.tobytes())
        )
        conn.commit()
        conn.close()
        return True

    def identify_face(self, face_embedding: np.ndarray, threshold: float = 0.7) -> Optional[Tuple[int, str]]:
        """Identify a face by comparing with stored embeddings."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, face_embedding FROM users')
        users = cursor.fetchall()
        conn.close()

        min_dist = float('inf')
        matched_user = None

        for user_id, name, stored_embedding in users:
            stored_embedding = np.frombuffer(stored_embedding, dtype=np.float32)
            dist = np.linalg.norm(face_embedding - stored_embedding)
            
            if dist < min_dist:
                min_dist = dist
                matched_user = (user_id, name)

        if min_dist < threshold:
            return matched_user
        return None

    def log_attendance(self, user_id: int):
        """Log attendance for a user."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO attendance (user_id) VALUES (?)',
            (user_id,)
        )
        conn.commit()
        conn.close()

    def process_frame(self, frame: np.ndarray) -> Tuple[np.ndarray, List[dict]]:
        """Process a video frame and return annotated frame and detection results."""
        faces = self.detect_faces(frame)
        annotated_frame = frame.copy()
        
        for face in faces:
            x, y, w, h = face['box']
            face_img = frame[y:y+h, x:x+w]
            embedding = self.get_face_embedding(face_img)
            
            # Identify face
            result = self.identify_face(embedding)
            if result:
                user_id, name = result
                self.log_attendance(user_id)
                color = (0, 255, 0)  # Green for recognized faces
                label = f"Known: {name}"
            else:
                color = (0, 0, 255)  # Red for unknown faces
                label = "Unknown"
            
            # Draw rectangle and label
            cv2.rectangle(annotated_frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(annotated_frame, label, (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        return annotated_frame, faces 