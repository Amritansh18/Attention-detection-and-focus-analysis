import cv2
import mediapipe as mp


class VisionProcessor:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        try:
            self.mp_face_detection = mp.solutions.face_detection
            self.mp_drawing = mp.solutions.drawing_utils

            self.face_detection = self.mp_face_detection.FaceDetection(
                min_detection_confidence=0.5
            )
        except:
            raise Exception("MediaPipe installation issue: 'solutions' not found")

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, False

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_detection.process(rgb_frame)

        face_present = False

        if results.detections:
            face_present = True
            for detection in results.detections:
                self.mp_drawing.draw_detection(frame, detection)

        return frame, face_present

    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()