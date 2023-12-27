import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm

import matplotlib.pyplot as plt

#Methods to check the diff between frames
from change_methods import diff_betweens_histogram, diff_betweens_boxes, diff_betweens_pixels, diff_edge_maps
from video_frames import VideoFrames
from change_decte import emsemble_mapping
import os

video_frames = VideoFrames()
diff_method = diff_betweens_pixels

# Read the videos
video_path = os.path.join(r"C:\Users\stiva\OneDrive\Área de Trabalho\Pendrive 26-12-2023\Vídeos passagens","Todos")
# video_path = "E:/101EK113"

# Read the reference image
# referencia = cv2.imread(os.path.join(video_path, "referencia.png"))
# referencia = cv2.cvtColor(referencia, cv2.COLOR_BGR2GRAY)

# List of videos in the folder
videos = os.listdir(video_path)

#List of methods to find key frames
avalible_methods = [diff_betweens_pixels,
                    # diff_betweens_boxes,
                    diff_betweens_histogram,
                    # diff_edge_maps
]

# Loop for all videos in the folder

diff_frames = {}

for video in videos:
    video_frames = video_frames.get_frames(os.path.join(video_path, video))
    for frame in video_frames:
        referencia = video_frames[0]
        if referencia.shape[0] != frame.shape[0] or referencia.shape[1] != frame.shape[1]:
            referencia = cv2.resize(referencia, (frame.shape[1], frame.shape[0]))

        key_frames, list_print = emsemble_mapping(frame, referencia, avalible_methods, threshold=2)
        print(len(key_frames))
        diff_frames[video] = key_frames

        # over_frames, value, all_frames = diff_method(frame, referencia, T1=64, T2_tax=0.9)
        # print(len(over_frames))
        # diff_frames[video] = over_frames

# Compare the diff between each frame and reference and select that have diff bigger than T1


# Save the name of videos and frames that have diff bigger than T1