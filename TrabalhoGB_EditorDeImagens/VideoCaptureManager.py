import cv2 as cv

class VideoCaptureManager:
    def __init__(self):
        self.capture = cv.VideoCapture(0)

    def capture_frame(self):
        """Captura um frame da webcam."""
        ret, frame = self.capture.read()
        if not ret:
            raise RuntimeError("Erro ao capturar frame.")
        return frame

    def release(self):
        """Libera a webcam."""
        self.capture.release()
