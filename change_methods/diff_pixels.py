from tqdm import tqdm
import numpy as np

def diff_betweens_pixels(gray_video_frames, reference, T1=64, T2_tax = 0.8):

    #List with the diff between the frames
    list_pixels_diff = []

    #List with indexs where the pixel pass the secong threshould
    list_over_T2 = []

    for frame in tqdm(range(len(gray_video_frames)-1)):

        actual = gray_video_frames[frame]
        # if reference is None:
        #     next =  gray_video_frames[frame+1]
        # else:
        next = reference
    
        list_pixels_diff.append(np.unique((actual - next) > T1, return_counts=True)[1][1])
    
    T2 = int(max(list_pixels_diff) * T2_tax)

    for diff_pixel in range(len(list_pixels_diff)):

        if list_pixels_diff[diff_pixel] > T2:
                list_over_T2.append(diff_pixel)

        # plot_hist_diff(list_pixels_diff, T2)

    return list_over_T2, T2, list_pixels_diff