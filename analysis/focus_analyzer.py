class FocusAnalyzer:
    def __init__(self):
        self.face_time = 0
        self.total_time = 0

    def update_time(self, face_present, frame_time):
        self.total_time += frame_time

        if face_present:
            self.face_time += frame_time

    def calculate_focus(self, blink_count, eye_closed_time):
        if self.total_time == 0:
            return 0, "No Data"

        # ---- Base Focus ----
        base_focus = (self.face_time / self.total_time) * 100

        # ---- Blink Rate (per minute approximation) ----
        minutes = self.total_time / 60
        blink_rate = blink_count / minutes if minutes > 0 else 0

        if blink_rate <= 20:
            blink_penalty = 0
        elif blink_rate <= 30:
            blink_penalty = 5
        else:
            blink_penalty = 10

        # ---- Eye Closed Percentage ----
        eye_closed_percent = (eye_closed_time / self.total_time) * 100

        if eye_closed_percent <= 5:
            eye_penalty = 0
        elif eye_closed_percent <= 15:
            eye_penalty = 10
        else:
            eye_penalty = 20

        # ---- Final Score ----
        focus_score = base_focus - blink_penalty - eye_penalty

        # Clamp between 0–100
        focus_score = max(0, min(100, focus_score))

        # ---- Interpretation ----
        if focus_score >= 75:
            level = "Highly Focused"
        elif focus_score >= 50:
            level = "Moderately Focused"
        else:
            level = "Low Focus"

        return round(focus_score, 2), level