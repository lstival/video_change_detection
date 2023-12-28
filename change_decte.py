import numpy as np

def emsemble_mapping(gray_video_frames, reference, avalible_methods, threshold=2):

    #List with all frames of the methods
    all_key_frames = []
    list_print = []

    #Loop to execute all methods and save the frames selecteds
    for method in avalible_methods:

        #Call the method and save the information
        list_diff_pixels, threshould, plot_values = method(gray_video_frames, reference)

        #Add values to facility the plot
        list_print.append([plot_values, threshould, method.__name__])

        #Save the values for comparation and make the summary video
        all_key_frames.extend(list_diff_pixels)

    #Get the most selected frames
    key_frames = np.unique(all_key_frames)[np.unique(all_key_frames, 
                                        return_counts=True)[1] >= threshold]

    #Avoid return none frame
    if len(key_frames) == 0:
        # key_frames = emsemble_mapping(gray_video_frames, avalible_methods, threshold-1)
        key_frames = np.array([99999])
    
    #Return the frames that apears more or equal the limiar
    return key_frames, list_print