import mediapipe as mp
import numpy as np
import cv2
import time

class SignalExtractor:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(refine_landmarks=True)

        # Blink variables
        self.blink_count = 0
        self.eye_closed = False
        self.eye_closed_start = None
        self.total_closed_time = 0

        # EAR threshold
        self.EAR_THRESHOLD = 0.2

    def calculate_ear(self, eye_landmarks):
        # Calculate Eye Aspect Ratio
        vertical_1 = np.linalg.norm(eye_landmarks[1] - eye_landmarks[5])
        vertical_2 = np.linalg.norm(eye_landmarks[2] - eye_landmarks[4])
        horizontal = np.linalg.norm(eye_landmarks[0] - eye_landmarks[3])

        ear = (vertical_1 + vertical_2) / (2.0 * horizontal)
        return ear

    def extract_signals(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_frame)

        if not results.multi_face_landmarks:
            return {
                "blink_count": self.blink_count,
                "eye_closed_time": self.total_closed_time
            }

        landmarks = results.multi_face_landmarks[0]

        h, w, _ = frame.shape

        # Left eye landmarks (approx indices)
        left_eye_indices = [33, 160, 158, 133, 153, 144]

        eye_points = []
        for idx in left_eye_indices:
            x = int(landmarks.landmark[idx].x * w)
            y = int(landmarks.landmark[idx].y * h)
            eye_points.append(np.array([x, y]))

        ear = self.calculate_ear(eye_points)

        current_time = time.time()

        # Eye closed
        if ear < self.EAR_THRESHOLD:
            if not self.eye_closed:
                self.eye_closed = True
                self.eye_closed_start = current_time
        else:
            # Eye reopened → blink detected
            if self.eye_closed:
                self.blink_count += 1

                if self.eye_closed_start:
                    self.total_closed_time += (current_time - self.eye_closed_start)

                self.eye_closed = False
                self.eye_closed_start = None

        return {
            "blink_count": self.blink_count,
            "eye_closed_time": self.total_closed_time
        }