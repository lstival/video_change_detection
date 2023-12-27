from tqdm import tqdm
import numpy as np

def diff_betweens_histogram(gray_video_frames, reference):
    #Bins amount
    histSize = 256

    #List with de difference betweeen the histogram
    dif_hist = []

    #Factor of std
    sigma = 2

    #Loop for each frame in the video
    for frame in tqdm(range(len(gray_video_frames)-1)):
        actual = np.histogram(gray_video_frames[frame], np.arange(histSize))[0]
        if reference is None:
            next = np.histogram(gray_video_frames[frame+1], np.arange(histSize))[0]
        else:
            next = np.histogram(reference, np.arange(histSize))[0]

        #Save the absulute diference
        dif_hist.append(sum(abs(actual-next)))

    dif_hist = np.asarray(dif_hist)
    T1 = round(np.mean(dif_hist) + (np.std(dif_hist) * sigma))

    frames_over_t1 = []
    for i in range(len(dif_hist)):
        if dif_hist[i] > T1:
            frames_over_t1.append(i)

    # plot_hist_diff(dif_hist, T1)

    return frames_over_t1, T1, dif_hist