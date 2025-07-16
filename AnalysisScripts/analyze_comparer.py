import os
import json
from datetime import datetime
from collections import defaultdict

ARCHIVE_DIR = "/home/lars/Desktop/Scion_Project_Canada/GithubProject/mpquic-on-scion-ipc/AnalysisScripts"
COMPARER_PREFIX = "delta_"

def extract_path_features(sequence):
    segments = sequence.split()
    ases = [seg.split('#')[0] for seg in segments if '#' in seg]
    unique_ases = list(dict.fromkeys(ases))
    return {
        "ases": unique_ases,
        "length": len(unique_ases)
    }

def load_comparer_data(archive_dir):
    comparer_data = defaultdict(list)
    for fname in os.listdir(archive_dir):
        if not fname.startswith(COMPARER_PREFIX) or not fname.endswith(".json"):
            continue
        path = os.path.join(archive_dir, fname)
        try:
            with open(path) as f:
                data = json.load(f)
                destination = data.get("destination")
                if destination:
                    comparer_data[destination].append(data)
        except Exception as e:
            print(f"[WARN] Failed to read {fname}: {e}")
    return comparer_data

def analyze_comparer(data_by_ia):
    results = {}
    churn_by_as = defaultdict(int)
    churn_by_length = defaultdict(int)
    lifetime_data_by_ia = defaultdict(list)

    for ia, entries in data_by_ia.items():
        entries_sorted = sorted(entries, key=lambda x: x.get("timestamp", ""))
        total = len(entries_sorted)
        added_total, removed_total, change_events = 0, 0, 0
        path_lengths = []
        last_seen = {}

        for entry in entries_sorted:
            timestamp = entry.get("timestamp")
            ts = None
            for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M"):
                try:
                    ts = datetime.strptime(timestamp, fmt)
                    break
                except:
                    continue
            if ts is None:
                continue  # skip if no format matched

            if entry.get("change_status") == "change_detected":
                change_events += 1

            for change in entry.get("changes", []):
                change_type = change.get("change")
                if change_type not in {"added", "removed"}:
                    continue

                sequence = change.get("sequence", "")
                features = extract_path_features(sequence)
                path_id = sequence.strip()

                if change_type == "added":
                    added_total += 1
                    last_seen[path_id] = ts
                elif change_type == "removed":
                    removed_total += 1
                    if path_id in last_seen:
                        duration = (ts - last_seen[path_id]).total_seconds()
                        lifetime_data_by_ia[ia].append(duration)
                        del last_seen[path_id]

                path_lengths.append(features["length"])
                churn_by_length[features["length"]] += 1
                for ashop in features["ases"]:
                    churn_by_as[ashop] += 1

        avg_path_length = round(sum(path_lengths) / len(path_lengths), 2) if path_lengths else 0
        lifetimes = lifetime_data_by_ia[ia]
        avg_lifetime = round(sum(lifetimes) / len(lifetimes), 2) if lifetimes else None

        results[ia] = {
            "total_comparisons": total,
            "change_events": change_events,
            "added_paths": added_total,
            "removed_paths": removed_total,
            "avg_path_length_of_changes": avg_path_length,
            "avg_path_lifetime_sec": avg_lifetime
        }

    churn_insights = {
        "churn_by_path_length": dict(sorted(churn_by_length.items())),
        "top_unstable_ases": sorted(churn_by_as.items(), key=lambda x: -x[1])[:10]
    }

    return results, churn_insights

def write_output_to_file(output_lines, filename):
    with open(filename, "w") as f:
        for line in output_lines:
            f.write(line + "\n")

def main():
    output_file = f"comparer_analysis.txt"
    output_lines = []

    def log(line=""):
        print(line)
        output_lines.append(line)

    log("=== SCION Path Comparer Analysis ===")
    comparer_data = load_comparer_data(ARCHIVE_DIR)
    comparer_results, churn_insights = analyze_comparer(comparer_data)

    log(f"\nComparer data summary:\n")
    for ia, stats in comparer_results.items():
        log(f"→ Destination AS: {ia}")
        for k, v in stats.items():
            log(f"   {k.replace('_', ' ').capitalize()}: {v}")
        log()

    log("=== Global Churn Insights ===")
    log("Top ASes in changing paths:")
    for ashop, count in churn_insights["top_unstable_ases"]:
        log(f"  {ashop:25} → {count} path changes")

    log("\nChurn by path length:")
    for length, count in churn_insights["churn_by_path_length"].items():
        log(f"  Length {length}: {count} changes")

    write_output_to_file(output_lines, output_file)
    log(f"\n[Saved output to {output_file}]")

if __name__ == "__main__":
    main()
