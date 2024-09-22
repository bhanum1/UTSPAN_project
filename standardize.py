from animate import animate_trial
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

def find_point(data):
    '''
    Input trial in data form
    Outputs a standardized time series based on when the participant releases the ball.
    
    '''
    ball_frames = []
    for frame in range(len(data["tracking"])):
        ball_frames.append(data['tracking'][frame]["data"]['ball'][0])

    non_nans = ~np.isnan(ball_frames)
    non_nan_indices = np.where(non_nans)[0]
    return non_nan_indices[-1]


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
            release_frame = find_point(data)
            key_frames.append(release_frame)

    slice = max(key_frames) - min(key_frames)

    #Standardize
    for filename in os.listdir(folder):
        if filename.endswith('.json'):
            input_file_path = os.path.join(folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            
            # Read the JSON file
            with open(input_file_path, 'r') as infile:
                data = json.load(infile)
                processed_data = data
                processed_data['tracking'] = processed_data['tracking'][slice:]

            with open(output_file_path, 'w') as outfile:
                json.dump(processed_data, outfile, indent=4)
