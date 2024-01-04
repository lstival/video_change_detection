import cv2
import numpy as np

def diff_edge_maps(video_frames, reference, down_limit = 10, up_limite = 50, T1_limiar = 0.99):

    edges_diffences = []

    for frame in range(len(video_frames)-1):

        actual = cv2.Canny(video_frames[frame],down_limit, up_limite)
        if reference is None:
            next = cv2.Canny(video_frames[frame+1],down_limit, up_limite)
        else:
            next = cv2.Canny(reference, down_limit, up_limite)

        edges_diffences.append(np.sum(abs(actual-next)))

    T1 = int(max(edges_diffences) * T1_limiar)

    frames_over_T1 = []
    for frame_diff in range(len(edges_diffences)):
        if edges_diffences[frame_diff] > T1:
            frames_over_T1.append(frame_diff)

    # plot_hist_diff(edges_diffences, T1)

    return frames_over_T1, T1, edges_diffences