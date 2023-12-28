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
import shutil

# Read the videos
# video_path = r"C:\Users\stiva\OneDrive\Área de Trabalho\videos_fauna\passagem 1"
video_path = r"C:\Users\stiva\Desktop\videos passagens\passagem 1"
# video_path = "E:/101EK113"

auto_reference = False

# Read the reference image
# referencia = cv2.imread(os.path.join(video_path, "referencia.png"))

# List of videos in the folder

videos = [video for video in os.listdir(video_path) if video.endswith(".MP4")]

if auto_reference:
    videoFrames = VideoFrames()
    video_frames = videoFrames.get_frames(os.path.join(video_path, videos[-1]))
    referencia = video_frames[0]
    referencia = cv2.resize(referencia, (video_frames[0].shape[1], video_frames[0].shape[0]))
else:
    referencia = Image.open(os.path.join(video_path, "referencia.png"))

try:
    referencia = cv2.cvtColor(np.array(referencia), cv2.COLOR_RGB2BGR)
except:
    pass

#List of methods to find key frames
avalible_methods = [
                    diff_betweens_pixels,
                    diff_betweens_boxes,
                    diff_betweens_histogram,
                    diff_edge_maps
                ]

# Loop for all videos in the folder
diff_frames = {}

for video in videos:
    videoFrames = VideoFrames()
    video_frames = videoFrames.get_frames(os.path.join(video_path, video))
    #First frame
    first_frame = video_frames[0]

    # referencia = video_frames[0]
    if referencia.shape[0] != first_frame.shape[0] or referencia.shape[1] != first_frame.shape[1]:
        referencia = cv2.resize(referencia, (first_frame.shape[1], first_frame.shape[0]))
    
    try:
        referencia = cv2.cvtColor(referencia, cv2.COLOR_BGR2GRAY)
    except:
        pass

    key_frames, _ = emsemble_mapping(video_frames, referencia, avalible_methods, threshold=3)
    print(len(key_frames))
    diff_frames[video] = key_frames

    # Create the "capturas" folder if it doesn't exist
    capturas_folder = "capturas"
    capturas_folder = os.path.join(video_path, capturas_folder)
    
    if not os.path.exists(capturas_folder):
        os.makedirs(capturas_folder)

    if len(diff_frames[video]) >= 6:
        # Move the video to the capturas_folder
        video_path_old = os.path.join(video_path, video)
        video_path_new = os.path.join(capturas_folder, video)
        shutil.copy(video_path_old, video_path_new)

    # # Save the frames as images
    # for frame in diff_frames[video]:
    #     if frame == 99999:
    #         continue
    #     else:
    #         image_name = f"{frame}.png"
    #         image_path = os.path.join(capturas_folder, image_name)
    #         image = Image.fromarray(video_frames[frame])
    #         image = image.resize((1024, 768))
    #         image.save(image_path)

    del video_frames
    cv2.destroyAllWindows()

print("Done")
    # over_frames, value, all_frames = diff_method(frame, referencia, T1=64, T2_tax=0.9)
    # print(len(over_frames))
    # diff_frames[video] = over_frames

    # Compare the diff between each frame and reference and select that have diff bigger than T1


    # Save the name of videos and frames that have diff bigger than T1
