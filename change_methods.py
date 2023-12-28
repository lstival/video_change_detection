import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm
from PIL import Image

import matplotlib.pyplot as plt

#Methods to check the diff between frames
from change_methods import diff_betweens_histogram, diff_betweens_boxes, diff_betweens_pixels, diff_edge_maps
from video_frames import VideoFrames
from change_decte import emsemble_mapping
import os

videoFrames = VideoFrames()
diff_method = diff_betweens_pixels

# Read the videos
video_path = r"C:\Users\stiva\OneDrive\Área de Trabalho\videos_fauna\passagem 1"
# video_path = "E:/101EK113"

# Read the reference image
# referencia = cv2.imread(os.path.join(video_path, "referencia.png"))
referencia = Image.open(os.path.join(video_path, "referencia.png"))

try:
    referencia = cv2.cvtColor(np.array(referencia), cv2.COLOR_RGB2BGR)
except:
    pass

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
    video_frames = videoFrames.get_frames(os.path.join(video_path, video))
    #First frame
    frame = video_frames[0]

    # referencia = video_frames[0]
    if referencia.shape[0] != frame.shape[0] or referencia.shape[1] != frame.shape[1]:
        referencia = cv2.resize(referencia, (frame.shape[1], frame.shape[0]))
    
    try:
        referencia = cv2.cvtColor(referencia, cv2.COLOR_BGR2GRAY)
    except:
        pass

    key_frames, list_print = emsemble_mapping(video_frames, referencia, avalible_methods, threshold=2)
    print(len(key_frames))
    diff_frames[video] = key_frames

    # Create the "capturas" folder if it doesn't exist
    capturas_folder = "capturas"
    capturas_folder = os.path.join(video_path, capturas_folder)
    if not os.path.exists(capturas_folder):
        os.makedirs(capturas_folder)

    # Save the frames as images
    for frame in diff_frames[video]:
        if frame == 99999:
            continue
        else:
            image_name = f"{video}_{frame}.png"
            image_path = os.path.join(capturas_folder, image_name)
            image = Image.fromarray(video_frames[frame])
            image.save(image_path)

    del video_frames
        # over_frames, value, all_frames = diff_method(frame, referencia, T1=64, T2_tax=0.9)
        # print(len(over_frames))
        # diff_frames[video] = over_frames

# Compare the diff between each frame and reference and select that have diff bigger than T1


# Save the name of videos and frames that have diff bigger than T1