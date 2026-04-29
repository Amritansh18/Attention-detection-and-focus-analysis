import tkinter as tk
import time
import threading

from vision.vision_processor import VisionProcessor
from signals.signal_extractor import SignalExtractor
from analysis.focus_analyzer import FocusAnalyzer
from ui.ui_manager import UIManager


# Initialize backend modules
vision = VisionProcessor()
signals = SignalExtractor()
analyzer = FocusAnalyzer()


def start_system(ui):
    """
    Start the vision processing loop in a separate thread to avoid blocking UI.
    Uses thread-safe queue to communicate between vision thread and UI thread.
    """
    prev_time = time.time()
    processing_lock = threading.Lock()
    last_level = None

    def vision_loop():
        """
        Runs in separate thread. Processes vision and signals without blocking UI.
        """
        nonlocal prev_time, last_level
        
        while True:
            try:
                if not ui.session_running:
                    time.sleep(0.05)  # Sleep when session not running
                    continue

                # ---- Frame ----
                frame, face_present = vision.get_frame()
                if frame is None:
                    time.sleep(0.05)
                    continue

                # ---- Time ----
                current_time = time.time()
                frame_time = current_time - prev_time
                prev_time = current_time

                # ---- Update analyzer ----
                with processing_lock:
                    analyzer.update_time(face_present, frame_time)

                    # ---- Signals ----
                    signal_data = signals.extract_signals(frame)
                    blink_count = signal_data["blink_count"]
                    eye_closed_time = signal_data["eye_closed_time"]

                    # ---- Focus Calculation ----
                    score, level = analyzer.calculate_focus(
                        blink_count,
                        eye_closed_time
                    )

                    # ---- Update UI (thread-safe) ----
                    ui.root.after(0, ui.display_score, score)
                    ui.root.after(0, ui.update_peak, score)

                    # ---- Log level changes ----
                    if level != last_level:
                        last_level = level
                        msg = f"Focus Level: {level}"
                        ui.root.after(0, ui.log_event, msg)
                        print(f"[LOG] {msg}")

                time.sleep(0.05)  # ~20 FPS

            except Exception as e:
                print(f"Error in vision loop: {e}")
                time.sleep(0.1)

    # Start vision processing in background thread
    vision_thread = threading.Thread(target=vision_loop, daemon=True)
    vision_thread.start()


# ---- MAIN ----
if __name__ == "__main__":
    root = tk.Tk()
    ui = UIManager(root)

    # Start backend loop in separate thread
    start_system(ui)

    ui.run()