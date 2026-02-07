import cv2
import mss
import numpy as np


class VideoCamera(object):
    def __init__(self):
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]

    def get_frame(self):
        sct_img = self.sct.grab(self.monitor)
        frame = np.array(sct_img)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        ret, jpeg = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 50])

        return jpeg.tobytes()