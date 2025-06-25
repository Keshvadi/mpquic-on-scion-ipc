import os
import json
import subprocess
from datetime import datetime

AS_TARGETS = {
    "17-ffaa:0:1101": ("127.0.0.1", "AS-1"),
    "19-ffaa:1:11de": ("127.0.0.1", "AS-2"),
    "19-ffaa:0:1310": ("127.0.0.1", "AS-3"),
}

# Base directories
BASE_DIR = "Data"
BASE_TRACEROUTE_DIR = os.path.join(BASE_DIR, "History", "Traceroute")
LOG_DIR = os.path.join(BASE_DIR, "Logs", "Traceroute")

os.makedirs(LOG_DIR, exist_ok=True)

def normalize_as(as_str):
    return as_str.replace(":", "_")

# Run scion traceroute on all available paths

def run_all_traceroutes(ia, ip_target, as_folder):
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    log_filename = f"TR_AS_{normalize_as(ia)}.txt"
    log_path = os.path.join(LOG_DIR, log_filename)

    output_dir = os.path.join(BASE_TRACEROUTE_DIR, as_folder)
    os.makedirs(output_dir, exist_ok=True)

    # Get all available paths via scion showpaths
    showpaths_result = subprocess.run(
        ["scion", "showpaths", ia, "--format", "json", "-m", "40"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True
    )

    if showpaths_result.returncode != 0:
        print(f"[ERROR] Failed to get paths for {ia}: {showpaths_result.stderr}")
        with open(log_path, "a") as log_file:
            log_file.write(f"[ERROR] Failed to get paths for {ia}: {showpaths_result.stderr}\n")
        return

    try:
        path_data = json.loads(showpaths_result.stdout)
        paths = path_data.get("paths", [])
    except json.JSONDecodeError:
        print(f"[ERROR] Failed to parse showpaths JSON for {ia}")
        with open(log_path, "a") as log_file:
            log_file.write(f"[ERROR] Invalid JSON from showpaths for {ia}\n")
        return

    if not paths:
        print(f"[WARNING] No paths found for {ia}")
        with open(log_path, "a") as log_file:
            log_file.write(f"[WARNING] No paths found for {ia} at {timestamp}\n")
        return

    # Run traceroute on each path using --sequence
    for i, path in enumerate(paths):
        sequence = path.get("sequence")
        if not sequence:
            continue

        # Get hop count from the sequence string
        hop_count = len(sequence.split())

        traceroute_result = subprocess.run(
            ["scion", "traceroute", f"{ia},{ip_target}", "--format", "json", "--sequence", sequence],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )

        if traceroute_result.returncode != 0:
            print(f"[ERROR] Traceroute failed on path {i+1} for {ia}: {traceroute_result.stderr}")
            with open(log_path, "a") as log_file:
                log_file.write(f"[ERROR] Traceroute failed on path {i+1} for {ia}: {traceroute_result.stderr}\n")
            continue

        try:
            traceroute_data = json.loads(traceroute_result.stdout)
        except json.JSONDecodeError:
            print(f"[ERROR] Failed to parse traceroute JSON for path {i+1} of {ia}")
            with open(log_path, "a") as log_file:
                log_file.write(f"[ERROR] Invalid traceroute JSON for path {i+1} of {ia}\n")
            continue

        # Save hop count into the traceroute JSON
        traceroute_data["hop_count"] = hop_count

        filename = f"{timestamp}_p_{i+1}.json"
        output_path = os.path.join(output_dir, filename)
        with open(output_path, "w") as f:
            json.dump(traceroute_data, f, indent=2)

        print(f"[OK] Traceroute saved to {output_path}")
        with open(log_path, "a") as log_file:
            log_file.write(f"[SUCCESS] Traceroute path {i+1} (hops: {hop_count}) saved for AS {ia} at {timestamp}\n")


if __name__ == "__main__":
    for ia, (ip, folder) in AS_TARGETS.items():
        run_all_traceroutes(ia, ip, folder)