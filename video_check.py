import numpy as np
import cv2
import matplotlib.pyplot as plt
from collections import Counter
from tqdm import tqdm
from PIL import Image

import matplotlib.pyplot as plt

#Methods to check the diff between frames
from change_methods import diff_betweens_histogram, diff_betweens_boxes, diff_betweens_pixels, diff_edge_maps, diff_betweens_feature_space
from video_frames import VideoFrames
from change_decte import emsemble_mapping
import os
import shutil
from tqdm import tqdm

# Read the videos
video_path = r"C:\Users\stiva\OneDrive\Área de Trabalho\videos_fauna\todos"
# video_path = r"C:\Users\stiva\Desktop\videos passagens\passagem 1"
# video_path = "E:/101EK113"

reference_path = os.path.join(video_path, "reference.png")

auto_reference = True

import matplotlib.pyplot as plt
#Methods to check the diff between frames
class ChangeDetection:
    def __init__(self, video_path, auto_reference=True, tolerance=6, num_methods=1, reference_path=None):
        self.video_path = video_path
        self.auto_reference = auto_reference
        self.tolerance = tolerance
        self.num_methods = num_methods
        self.reference_path = reference_path
        self.total_over_threshold = 0

    def check_videos(self):
        videos = [video for video in os.listdir(self.video_path) if video.endswith(".MP4")]

        videoFrames = VideoFrames()
        # # Get the first frame of the first video
        # if self.auto_reference == True:
        #     video_frames = videoFrames.get_frames(os.path.join(self.video_path, videos[0]))

        # # Get the first frame of the reference video
        # else:
        #     video_frames = videoFrames.get_frames(os.path.join(self.video_path, self.reference_path))
        
        # referencia = video_frames[0]
        # referencia = cv2.resize(referencia, (video_frames[0].shape[1], video_frames[0].shape[0]))

        # try:
        #     referencia = cv2.cvtColor(np.array(referencia), cv2.COLOR_RGB2BGR)
        # except:
        #     pass

        #List of methods to find key frames
        avalible_methods = [
            # diff_betweens_pixels,
            # diff_betweens_boxes,
            # diff_betweens_histogram,
            # diff_edge_maps,
            diff_betweens_feature_space
        ]

        # Loop for all videos in the folder
        diff_frames = {}
        
        pbar = tqdm(videos)
        for video in pbar:
            # print(f"Processing video: {video}")
            pbar.set_description(f"Processando {video} (Total Selecionado: {self.total_over_threshold})")
            
            videoFrames = VideoFrames()
            video_frames = videoFrames.get_frames(os.path.join(self.video_path, video))
            #First frame
            # first_frame = video_frames[0]

            # # referencia = video_frames[0]
            # if referencia.shape[0] != first_frame.shape[0] or referencia.shape[1] != first_frame.shape[1]:
            #     referencia = cv2.resize(referencia, (first_frame.shape[1], first_frame.shape[0]))

            # try:
            #     referencia = cv2.cvtColor(referencia, cv2.COLOR_BGR2GRAY)
            # except:
            #     pass

            # key_frames, _ = emsemble_mapping(video_frames, referencia, avalible_methods, threshold=self.num_methods)
            key_frames, list_print = emsemble_mapping(video_frames, None, avalible_methods, threshold=self.num_methods)
            if len(key_frames) >self.tolerance:
                self.total_over_threshold += 1
            diff_frames[video] = key_frames

            # Create the "capturas" folder if it doesn't exist
            capturas_folder = "capturas"
            capturas_folder = os.path.join(self.video_path, capturas_folder)

            if not os.path.exists(capturas_folder):
                os.makedirs(capturas_folder)

            if len(diff_frames[video]) >= self.tolerance:
                # Move the video to the capturas_folder
                video_path_old = os.path.join(self.video_path, video)
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

if __name__ == "__main__":
    method = ChangeDetection(video_path, auto_reference,num_methods=1, reference_path=reference_path)
    method.check_videos()