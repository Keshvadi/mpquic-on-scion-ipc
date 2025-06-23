import os
import json
import subprocess
from datetime import datetime

# Define AS targets and their folder name
AS_TARGETS = {
    "19-ffaa:0:1301": ("127.0.0.1", "AS-1"),
    "19-ffaa:1:11de": ("127.0.0.1", "AS-2"),
    "19-ffaa:0:1310": ("127.0.0.1", "AS-3"),
}

# Base directories
BASE_DIR = "../Data"
BASE_TRACEROUTE_DIR = os.path.join(BASE_DIR, "History", "Traceroute")
LOG_DIR = os.path.join(BASE_DIR, "Logs", "Traceroute")

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Normalize AS string (remove colons)
def normalize_as(as_str):
    return as_str.replace(":", "_")

# Run scion traceroute and log results
def run_scion_traceroute(ia, ip_target, as_folder):
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    filename = f"{timestamp}_{normalize_as(ia)}.json"
    log_filename = f"TR_AS_{normalize_as(ia)}.txt"
    log_path = os.path.join(LOG_DIR, log_filename)

    output_dir = os.path.join(BASE_TRACEROUTE_DIR, as_folder)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    result = subprocess.run(
        ["scion", "traceroute", f"{ia},{ip_target}", "--format", "json"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    if result.returncode != 0:
        print(f"[ERROR] Failed to run traceroute for {ia}: {result.stderr}")
        with open(log_path, "a") as log_file:
            log_file.write(f"[ERROR] Failed for {ia}: {result.stderr}\n")
        return

    try:
        traceroute_data = json.loads(result.stdout)
    except json.JSONDecodeError:
        print(f"[ERROR] Failed to parse JSON output for {ia}")
        with open(log_path, "a") as log_file:
            log_file.write(f"[ERROR] Failed to parse JSON for {ia}\n")
        return

    with open(output_path, "w") as f:
        json.dump(traceroute_data, f, indent=2)

    print(f"[OK] Saved traceroute JSON to {output_path}")
    with open(log_path, "a") as log_file:
        log_file.write(f"[SUCCESS] at {timestamp} for AS {ia}\n")

# Main entry point
if __name__ == "__main__":
    for ia, (ip, folder) in AS_TARGETS.items():
        run_scion_traceroute(ia, ip, folder)
