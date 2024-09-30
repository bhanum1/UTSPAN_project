import matplotlib.pyplot as plt
import json
import numpy as np
import sklearn.decomposition
from animate import animate_trial
import sklearn

data = []
for trial_number in range(1,126):

    trial_number_corrected = str(trial_number).zfill(4)

    with open(f'./standardized_data/BB_FT_P0001_T{trial_number_corrected}.json') as json_file:
        free_throw_data = json.load(json_file)

    hip_position = np.array([f['data']['player']['R_HIP'] for f in free_throw_data['tracking']])

    if free_throw_data['result'] == 'missed':
        result = 0
    else:
        result = 1
    
    mean_pos = np.mean(hip_position, axis=0)
    distances = np.linalg.norm(hip_position - mean_pos, axis=1)

    variability = np.std(distances)

    data.append((trial_number, variability, result))


values = [t[1] for t in data]
results = [t[2] for t in data]

# Creating a color map for the results: 0 -> red, 1 -> blue
colors = ['red' if result == 0 else 'blue' for result in results]

# Plotting
plt.scatter(values, [0] * len(values), c=colors, s=20)  # s is the size of the dots

# Adding labels and title
plt.xlabel('Value')
plt.yticks([])  # Hide the y-axis ticks
plt.title('Number Line with Color-Coded Dots')

# Show plot
plt.show()

max_tuple = max(data, key=lambda t: t[1])

# Extract the index of the tuple with the highest value
index_of_max_value = max_tuple[0]

#print("Index of trial with the highest value:", index_of_max_value)
trial = str(index_of_max_value).zfill(4)
t1 = animate_trial(f'./standardized_data/BB_FT_P0001_T{trial}.json')
plt.show()