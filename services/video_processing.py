import cv2
from PyQt5.QtCore import QTimer

class VideoProcessing:
    def __init__(self, frame_callback):
        self.frame_callback = frame_callback
        self.current_frame = None
        self.capture = None

    def load_video(self, video_path):
        self.capture = cv2.VideoCapture(video_path)
        if not self.capture.isOpened():
            print(f"Error: Unable to open video file {video_path}")
            return
        self.update_frame()

    def update_frame(self):
        if self.capture and self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                self.current_frame = frame
                self.frame_callback(self.current_frame)
                QTimer.singleShot(30, self.update_frame)  # Call this method again after 30ms
            else:
                print("Error: Unable to read the frame.")
                self.capture.release()
        else:
            print("Error: Capture object is not opened.")
