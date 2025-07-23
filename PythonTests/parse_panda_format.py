import pandas as pd
import os

# Configuration
input_folder = "/home/scion/Documents/mpquic-on-scion-ipc/parsed_output"         # Folder containing .csv files
output_folder = "./pandas_converted"   # Where to save the .pkl files

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all CSV files in the folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        input_path = os.path.join(input_folder, filename)
        output_name = os.path.splitext(filename)[0] + ".pkl"
        output_path = os.path.join(output_folder, output_name)

        try:
            df = pd.read_csv(input_path)
            df.to_pickle(output_path)
            print(f"✅ Converted: {filename} -> {output_name}")
        except Exception as e:
            print(f"❌ Failed to convert {filename}: {e}")
