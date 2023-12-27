import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm

class VideoFrames():
    def __init__(self) -> None:
        self.video_frames = []
    
    def read_video(self, video_url):
        video = cv2.VideoCapture(video_url)
        return video

    def convert2gray(self, image):
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return gray_image
    
    def get_frames(self, video_url):
        self.video = self.read_video(video_url)

        while(True):
            # Capture frame-by-frame
            ret, frame = self.video.read()
            #print cap.isOpened(), ret
            if frame is not None:
                # Display the resulting frame
                self.video_frames.append(frame)
            else:
                break

        return np.array(list(map(self.convert2gray, self.video_frames)))


if __name__ == "__main__":
    video_path = r"C:\Users\stiva\Downloads\10280049.MP4"
    
    video_frames = VideoFrames()
    frames = video_frames.get_frames(video_path)