import os
import json
from datetime import datetime

# AS list and their folder names
AS_FOLDER_MAP = {
    "19-ffaa:0:1301": "AS-1",
    "19-ffaa:1:11de": "AS-2",
    "19-ffaa:0:1310": "AS-3",
}

BASE_DIR = "Data"
CURRENTLY_DIR = os.path.join(BASE_DIR, "Currently")
HISTORY_SHOWPATHS_DIR = os.path.join(BASE_DIR, "History", "Showpaths")
COMPARER_DIR = os.path.join(BASE_DIR, "History", "Comparer")
LOG_DIR = os.path.join(BASE_DIR, "Logs", "Comparer")

# Ensure directories exist
os.makedirs(CURRENTLY_DIR, exist_ok=True)
os.makedirs(COMPARER_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

def normalize_as(as_str):
    return as_str.replace(":", "_")

def load_json(filepath):
    if not os.path.isfile(filepath):
        return {}
    with open(filepath, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def extract_fingerprint_map(path_data):
    if not path_data or "paths" not in path_data:
        return {}
    return {
        p["fingerprint"]: p.get("sequence", "unknown_sequence")
        for p in path_data.get("paths", [])
    }

def compare_paths(ia):
    timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M")
    filename_base = normalize_as(ia)
    delta_filename = f"delta_{timestamp}_{filename_base}.json"

    # ➤ Load latest file from Data/Currently/
    latest_file = os.path.join(CURRENTLY_DIR, f"latest_{filename_base}.json")
    latest_data = load_json(latest_file)

    # ➤ Find most recent historical file from correct Showpaths folder
    as_folder = AS_FOLDER_MAP.get(ia, "UNKNOWN_AS")
    history_dir = os.path.join(HISTORY_SHOWPATHS_DIR, as_folder)
    os.makedirs(history_dir, exist_ok=True)

    matching_files = [
        f for f in os.listdir(history_dir)
        if f.endswith(f"_{filename_base}.json")
    ]
    matching_files.sort(reverse=True)
    history_file = os.path.join(history_dir, matching_files[0]) if matching_files else None
    history_data = load_json(history_file) if history_file else {}

    # ➤ Compare fingerprints
    latest_fps_map = extract_fingerprint_map(latest_data)
    history_fps_map = extract_fingerprint_map(history_data)

    latest_fps = set(latest_fps_map.keys())
    history_fps = set(history_fps_map.keys())

    added = sorted(latest_fps - history_fps)
    removed = sorted(history_fps - latest_fps)

    changes = []

    for fp in added:
        changes.append({
            "fingerprint": fp,
            "sequence": latest_fps_map.get(fp, "unknown"),
            "change": "added"
        })

    for fp in removed:
        changes.append({
            "fingerprint": fp,
            "sequence": history_fps_map.get(fp, "unknown"),
            "change": "removed"
        })

    # ➤ Determine change status
    if added or removed:
        change_status = "change_detected"
    elif not latest_fps and not history_fps:
        change_status = "no_paths_present"
    elif not latest_fps:
        change_status = "all_paths_lost"
    elif not history_fps:
        change_status = "all_paths_new"
    else:
        change_status = "no_change"

    output = {
        "timestamp": timestamp,
        "source": latest_data.get("local_isd_as", "unknown"),
        "destination": latest_data.get("destination", ia),
        "change_status": change_status,
        "changes": changes
    }

    # ➤ Save delta file in Comparer/AS-X/
    comparer_sub_dir = os.path.join(COMPARER_DIR, as_folder)
    os.makedirs(comparer_sub_dir, exist_ok=True)
    delta_path = os.path.join(comparer_sub_dir, delta_filename)
    with open(delta_path, "w") as f:
        json.dump(output, f, indent=2)

    # ➤ Append to log
    log_file = os.path.join(LOG_DIR, f"log_compare_{filename_base}.txt")
    with open(log_file, "a") as log:
        log.write(f"\n[{timestamp}] Compare run for AS {ia}:\n")
        log.write(f"Status: {change_status}\n")
        if not changes:
            log.write("No changes detected.\n")
        else:
            for change in changes:
                log.write(f"- {change['change'].upper()}: {change['fingerprint']} | {change['sequence']}\n")

    # ➤ Console output
    print(f"[COMPARE] {ia}: {change_status} ({len(added)} added, {len(removed)} removed)")
    for change in changes:
        print(f"    {change['change'].upper()}: {change['fingerprint']} | {change['sequence']}")

    return delta_path

# Main
if __name__ == "__main__":
    for ia in AS_FOLDER_MAP:
        compare_paths(ia)
