
import tkinter as tk
from tkinter import font as tkfont
import time
import math
import random

class UIManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Focus Analyzer")
        self.root.state("zoomed")
        self.root.configure(bg="#0D0F14")

        self.session_running = False
        self.start_time = None
        self.current_score = 0
        self._peak = 0

        # Colors
        self.bg_dark   = "#0D0F14"
        self.bg_card   = "#151820"
        self.bg_card2  = "#1A1E28"
        self.accent    = "#00E5FF"
        self.green     = "#00E676"
        self.red       = "#FF5252"
        self.amber     = "#FFD740"
        self.text_hi   = "#E8EAF0"
        self.text_lo   = "#5A6070"

        self._build_ui()
        self._animate()

    # ───────────── SCROLLABLE UI ─────────────
    def _build_ui(self):
        container = tk.Frame(self.root, bg=self.bg_dark)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg=self.bg_dark, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        self._inner = tk.Frame(canvas, bg=self.bg_dark)
        window = canvas.create_window((0, 0), window=self._inner, anchor="n")

        def on_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        self._inner.bind("<Configure>", on_configure)

        def resize_inner(event):
            canvas.itemconfig(window, width=event.width)
        canvas.bind("<Configure>", resize_inner)

        # Mouse scroll
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        c = self._inner

        # ── Header
        header = tk.Frame(c, bg=self.bg_dark)
        header.pack(fill="x", padx=24, pady=(24, 0))

        tk.Label(header, text="◉  FOCUS ANALYZER",
                 font=("Courier", 15, "bold"),
                 bg=self.bg_dark, fg=self.accent).pack(side="left")

        self.live_dot = tk.Label(header, text="● IDLE",
                                 font=("Courier", 11),
                                 bg=self.bg_dark, fg=self.text_lo)
        self.live_dot.pack(side="right")

        # ── Canvas Ring
        self.canvas = tk.Canvas(c, width=220, height=220,
                                bg=self.bg_dark, highlightthickness=0)
        self.canvas.pack(pady=(10,6))
        self._draw_ring(0)

        # ── Score
        score_frame = tk.Frame(c, bg=self.bg_dark)
        score_frame.pack()

        self.score_value_lbl = tk.Label(score_frame, text="0",
                                       font=("Courier", 56, "bold"),
                                       bg=self.bg_dark, fg=self.text_hi)
        self.score_value_lbl.pack(side="left")

        tk.Label(score_frame, text="%",
                 font=("Courier", 24),
                 bg=self.bg_dark, fg=self.text_lo).pack(side="left")

        self.score_tag_lbl = tk.Label(c, text="AWAITING SESSION",
                                     font=("Courier", 11),
                                     bg=self.bg_dark, fg=self.text_lo)
        self.score_tag_lbl.pack(pady=10)

        # ── Stats
        stats_frame = tk.Frame(c, bg=self.bg_dark)
        stats_frame.pack(fill="x", padx=24, pady=10)

        self.timer_card  = self._stat_card(stats_frame, "ELAPSED", "0s", self.accent)
        self.status_card = self._stat_card(stats_frame, "STATUS", "IDLE", self.amber)
        self.avg_card    = self._stat_card(stats_frame, "PEAK", "--", self.green)

        self.timer_card.pack(side="left", expand=True, fill="both", padx=4)
        self.status_card.pack(side="left", expand=True, fill="both", padx=4)
        self.avg_card.pack(side="left", expand=True, fill="both", padx=4)

        # ── Attention Bar
        bar_outer = tk.Frame(c, bg=self.bg_card)
        bar_outer.pack(fill="x", padx=24, pady=10)

        tk.Label(bar_outer, text="ATTENTION LEVEL",
                 font=("Courier", 9),
                 bg=self.bg_card, fg=self.text_lo).pack(anchor="w", padx=8)

        bar_bg = tk.Frame(bar_outer, bg="#1E2230", height=16)
        bar_bg.pack(fill="x", padx=8, pady=8)

        self.attention_bar = tk.Frame(bar_bg, bg=self.accent, height=16, width=0)
        self.attention_bar.place(x=0, y=0)

        # ── Log
        log_frame = tk.Frame(c, bg=self.bg_card)
        log_frame.pack(fill="both", padx=24, pady=10)

        tk.Label(log_frame, text="EVENT LOG",
                 font=("Courier", 9),
                 bg=self.bg_card, fg=self.text_lo).pack(anchor="w", padx=8)

        self.log_text = tk.Text(log_frame, height=4,
                                font=("Courier", 9),
                                bg="#101318", fg="#4ADE80",
                                bd=0, wrap="word")
        self.log_text.pack(fill="both", expand=True, padx=8, pady=5)
        self.log_text.config(state="normal")
        self.log_text.insert("1.0", "Ready to start session...\n")

        # ── Buttons
        self.start_btn = tk.Button(c, text="▶ START SESSION",
                                  font=("Courier", 13, "bold"),
                                  bg=self.accent, fg="#000",
                                  command=self.start_session)
        self.start_btn.pack(fill="x", padx=24, pady=5)

        self.stop_btn = tk.Button(c, text="■ STOP SESSION",
                                 font=("Courier", 13, "bold"),
                                 bg=self.bg_card2, fg=self.text_lo,
                                 command=self.stop_session)
        self.stop_btn.pack(fill="x", padx=24, pady=10)

    # ───────────── HELPERS ─────────────
    def _stat_card(self, parent, label, value, color):
        frame = tk.Frame(parent, bg=self.bg_card)
        tk.Label(frame, text=label, font=("Courier", 8),
                 bg=self.bg_card, fg=self.text_lo).pack()
        lbl = tk.Label(frame, text=value, font=("Courier", 14, "bold"),
                       bg=self.bg_card, fg=color)
        lbl.pack()
        frame._value_label = lbl
        return frame

    def _draw_ring(self, score):
        self.canvas.delete("all")
        self.canvas.create_text(140, 140, text=f"{score}%",
                                font=("Courier", 30, "bold"),
                                fill=self.text_hi)

    def _animate(self):
        if self.session_running:
            self.live_dot.config(text="● LIVE", fg=self.green)
        else:
            self.live_dot.config(text="● IDLE", fg=self.text_lo)
        self.root.after(300, self._animate)

    # ───────────── LOGIC ─────────────
    def start_session(self):
        self.session_running = True
        self.start_time = time.time()
        self._peak = 0  # Reset peak for new session
        self.avg_card._value_label.config(text="--", fg=self.green)
        self.status_card._value_label.config(text="ACTIVE", fg=self.green)
        self.log_event("✓ Session started")
        self._tick()

    def stop_session(self):
        self.session_running = False
        self.status_card._value_label.config(text="STOPPED", fg=self.amber)
        self.log_event("⊗ Session stopped")

    def display_score(self, score):
        score = max(0, min(100, int(score)))
        self.current_score = score
        self._draw_ring(score)
        self.score_value_lbl.config(text=str(score))

        self.attention_bar.place_configure(width=int(score*5))

    def update_peak(self, score):
        """Update peak score if current score exceeds previous peak."""
        if score > self._peak:
            self._peak = score
            self.avg_card._value_label.config(text=str(int(self._peak)), fg=self.green)

    def log_event(self, event_text):
        """Add an event to the log with timestamp."""
        try:
            timestamp = time.strftime("%H:%M:%S")
            log_entry = f"[{timestamp}] {event_text}\n"
            
            # Insert at end
            self.log_text.insert("end", log_entry)
            self.log_text.see("end")  # Auto-scroll to end
            
            # Keep only last 100 lines to prevent memory bloat
            line_count = int(self.log_text.index("end").split('.')[0])
            if line_count > 100:
                self.log_text.delete("1.0", "2.0")
        except Exception as e:
            print(f"Log error: {e}")

    def _tick(self):
        if not self.session_running:
            return
        elapsed = int(time.time() - self.start_time)
        self.timer_card._value_label.config(text=f"{elapsed}s")
        self.root.after(1000, self._tick)

    def run(self):
        self.root.mainloop()


# ───────────── RUN ─────────────
if __name__ == "__main__":
    root = tk.Tk()
    ui = UIManager(root)

    def fake():
        if ui.session_running:
            ui.display_score(random.randint(10, 95))
        root.after(2000, fake)

    root.after(2000, fake)
    ui.run()

