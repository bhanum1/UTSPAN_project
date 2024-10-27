from animate import animate_trial
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def find_points(data):
    '''
    Input trial in data form
    Outputs a standardized time series based on when the participant gets and releases the ball.
    
    '''
    ball_frames = []
    for frame in range(len(data["tracking"])):
        ball_frames.append(data['tracking'][frame]["data"]['ball'][0])

    non_nans = ~np.isnan(ball_frames)
    non_nan_indices = np.where(non_nans)[0]

    return non_nan_indices[0], non_nan_indices[-1]


def standardize(folder):
    key_frames = []

    output_folder = 'standardized_data'

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Iterate through all files in the input folder
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            input_file_path = os.path.join(folder, filename)
            output_file_path = os.path.join(output_folder, filename)

            # Read the JSON file
            with open(input_file_path, 'r') as infile:
                data = json.load(infile)
                
                # Process the JSON data using your function
                entry_frame, exit_frame = find_points(data)
                processed_data = data
                processed_data['tracking'] = processed_data['tracking'][entry_frame+10:exit_frame]
            with open(output_file_path, 'w') as outfile:
                json.dump(processed_data, outfile, indent=4)


standardize('P0001')
t1 = animate_trial('standardized_data/BB_FT_P0001_T0104.json')
t2 = animate_trial('P0001/BB_FT_P0001_T0104.json')

plt.show()