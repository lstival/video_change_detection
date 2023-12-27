from collections import Counter
from tqdm import tqdm
import numpy as np

def diff_betweens_boxes(gray_video_frames, reference, T1_limiar=2, T2_limit=0.9, box_size=8):
    #Limiar to MSE
    H = gray_video_frames.shape[1] / box_size
    W = gray_video_frames.shape[2] / box_size

    T1 = H / W * T1_limiar
    
    # T2 = len(gray_video_frames) * T2_limit

    #List of frames that transpase the threshould T1
    list_pixels_diff = []

    #Loop in each frame
    for frame in tqdm(range(len(gray_video_frames)-1)):
        #Loop in rows
        for row in range(int(gray_video_frames[frame].shape[0]/box_size)):
            #Loop in collumns
            for col in range(int(gray_video_frames[frame].shape[1]/box_size)):
                
                #Indicies of liit of boxes
                nxt_row = row+box_size
                nxt_col = col+box_size

                #Get the box of actual frame and next, cast them in int to subtract
                actual_frame = gray_video_frames[frame, row:nxt_row, col:nxt_col].astype(int)
                if reference is None:
                    next_frames = gray_video_frames[frame+1, row:nxt_row, col:nxt_col].astype(int)
                else:
                    next_frames = reference[row:nxt_row, col:nxt_col].astype(int)

                #Calculate MSE between the boxs
                norm = (1/(box_size*box_size))
                box_diff =  norm * (np.sum(np.abs(actual_frame - next_frames) ** 2))

                if box_diff > T1:
                    list_pixels_diff.append(frame)

    #List with diff pixel bigger than T2
    list_diff_pixels_MSE = []
    dict_pixels_diff = Counter(list_pixels_diff)

    T2 = max(dict_pixels_diff.values())*T2_limit

    #Loop to count how many boxes each frame have with diff.
    for disct_frame, value in dict_pixels_diff.items():
        if value > T2:
            list_diff_pixels_MSE.append(disct_frame)

    #Plot the distribution of MSE in frames
    # plot_hist_diff(np.array(list(dict_pixels_diff.values())), T2)

    return list_diff_pixels_MSE, T2, np.array(list(dict_pixels_diff.values()))