import pandas as pd
import os

input_folder = "./pandas_converted"
dataframes = {}

for filename in os.listdir(input_folder):
    if filename.endswith(".pkl"):
        path = os.path.join(input_folder, filename)
        name = os.path.splitext(filename)[0]
        dataframes[name] = pd.read_pickle(path)

# Access an example DataFrame
print(dataframes["ping_data"].head())