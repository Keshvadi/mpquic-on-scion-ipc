import os
import json
import subprocess
from datetime import datetime

# Map each AS to its folder
AS_FOLDER_MAP = {
    "19-ffaa:0:1301": "AS-1",
    "19-ffaa:1:11de": "AS-2",
    "19-ffaa:0:1310": "AS-3",
}

# Directory structure
BASE_DIR = "../Data"
HISTORY_BASE = os.path.join(BASE_DIR, "History", "Showpaths")
CURRENTLY_DIR = os.path.join(BASE_DIR, "Currently")
LOG_DIR = os.path.join(BASE_DIR, "Logs", "Showpaths")

# Ensure required directories exist
os.makedirs(HISTORY_BASE, exist_ok=True)
os.makedirs(CURRENTLY_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# Normalize AS for filenames
def normalize_as(as_str):
    return as_str.replace(":", "_")

# Execute scion showpaths and save outputs
def discover_paths(ia):
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    filename_base = normalize_as(ia)
    as_folder = AS_FOLDER_MAP.get(ia, "UNKNOWN_AS")

    # Paths
    history_dir = os.path.join(HISTORY_BASE, as_folder)
    os.makedirs(history_dir, exist_ok=True)

    history_file = os.path.join(history_dir, f"{timestamp}_{filename_base}.json")
    latest_file = os.path.join(CURRENTLY_DIR, f"{timestamp}_{filename_base}.json")
    log_file = os.path.join(LOG_DIR, f"SP_AS_{filename_base}.txt")

    # Run scion command
    result = subprocess.run(
        ["scion", "showpaths", ia, "--format", "json", "-m", "40", "-e"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    if result.returncode != 0:
        print(f"[ERROR] Failed for {ia}: {result.stderr}")
        with open(log_file, "a") as f:
            f.write(f"[ERROR] Failed for {ia}: {result.stderr}\n")
        return

    try:
        json_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"[ERROR] Invalid JSON output for {ia}")
        with open(log_file, "a") as f:
            f.write(f"[ERROR] Invalid JSON output for {ia} at {timestamp}\n")
        return


    # Save to "currently"
    with open(latest_file, "w") as f:
        json.dump(json_data, f, indent=2)

    print(f"[OK] Saved paths to {latest_file}")
    with open(log_file, "a") as f:
        f.write(f"[SUCCESS] at {timestamp} for AS {ia}\n")

# Run the script
if __name__ == "__main__":
    for ia in AS_FOLDER_MAP:
        discover_paths(ia)
