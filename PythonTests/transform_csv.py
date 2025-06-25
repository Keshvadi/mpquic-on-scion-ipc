import os
import json
import pandas as pd

TRACEROUTE_DIR = "Data/History/Traceroute"


def extract_data_from_json(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)

    path_info = data.get("path", {})
    hops_list = path_info.get("hops", [])
    rtt_values = [rtt for hop in data.get("hops", []) for rtt in hop.get("round_trip_times", [])]
    rtt_avg = sum(rtt_values) / len(rtt_values) if rtt_values else None

    # Count unique ISD-AS pairs in the sequence to estimate hop count correctly
    sequence_parts = path_info.get("sequence", "").split()
    hop_count = len(sequence_parts)

    return {
        "file": os.path.basename(filepath),
        "source": sequence_parts[0].split("#")[0] if sequence_parts else None,
        "destination": sequence_parts[-1].split("#")[0] if sequence_parts else None,
        #"fingerprint": path_info.get("fingerprint"),
        "hop_count": hop_count,
        "sequence": path_info.get("sequence"),
        "avg_rtt": rtt_avg,
        "max_rtt": max(rtt_values) if rtt_values else None,
        "min_rtt": min(rtt_values) if rtt_values else None
    }

# Load all JSON files
records = []
for folder in os.listdir(TRACEROUTE_DIR):
    full_path = os.path.join(TRACEROUTE_DIR, folder)
    if os.path.isdir(full_path):
        for file in os.listdir(full_path):
            if file.endswith(".json"):
                try:
                    data = extract_data_from_json(os.path.join(full_path, file))
                    records.append(data)
                except Exception as e:
                    print(f"Error parsing {file}: {e}")

# Create the DataFrame
df = pd.DataFrame(records)
print(df.head())

# Export to CSV
csv_output_path = os.path.join(TRACEROUTE_DIR, "traceroute_summary.csv")
df.to_csv(csv_output_path, index=False)
print(f"[OK] CSV exported to {csv_output_path}")
