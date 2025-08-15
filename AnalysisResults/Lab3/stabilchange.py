import os
import json
import statistics
from datetime import datetime
from collections import defaultdict
import matplotlib.pyplot as plt

ARCHIVE_DIR = "combinedData"
PROBER_PREFIX = "prober_"
TARGET_IA = "17-ffaa:1:11e4"  # change to your AS
STABILIZATION_THRESHOLD = 5  # ms difference allowed
STABILIZATION_WINDOW = 10    # consecutive points

def parse_timestamp(fname):
    try:
        return datetime.strptime(fname.split("_")[1], "%Y-%m-%dT%H:%M")
    except:
        return None

def load_prober_for_as():
    data = []
    for fname in os.listdir(ARCHIVE_DIR):
        if not fname.startswith(PROBER_PREFIX) or not fname.endswith(".json"):
            continue
        ts = parse_timestamp(fname)
        if not ts:
            continue
        path = os.path.join(ARCHIVE_DIR, fname)
        try:
            with open(path) as f:
                doc = json.load(f)
                ia = doc.get("ia")
                if ia != TARGET_IA:
                    continue
                probes = doc.get("probes", [])
                rtts = []
                fps = set()
                for probe in probes:
                    stats = probe.get("ping_result", {}).get("statistics", {})
                    avg_rtt = stats.get("avg_rtt")
                    if avg_rtt is not None:
                        rtts.append(avg_rtt)
                    fp = probe.get("fingerprint")
                    if fp:
                        fps.add(fp)
                if rtts:
                    avg_rtt_overall = statistics.mean(rtts)
                    data.append((ts, avg_rtt_overall, fps))
        except Exception as e:
            print(f"[WARN] Failed to parse {fname}: {e}")
    return sorted(data, key=lambda x: x[0])

def find_stabilization_point(data):
    rtts = [x[1] for x in data]
    for i in range(len(rtts) - STABILIZATION_WINDOW):
        window = rtts[i:i+STABILIZATION_WINDOW]
        if max(window) - min(window) <= STABILIZATION_THRESHOLD:
            return i  # index where stabilization starts
    return None

def compare_paths(before_fps, after_fps):
    lost = before_fps - after_fps
    new = after_fps - before_fps
    persistent = before_fps & after_fps
    return lost, new, persistent

def plot_results(data, stab_idx):
    times = [x[0] for x in data]
    rtts = [x[1] for x in data]
    counts = [len(x[2]) for x in data]

    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(times, rtts, marker='o', label="Avg RTT (ms)")
    if stab_idx is not None:
        ax1.axvline(times[stab_idx], color='red', linestyle='--', label="Stabilization Start")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("RTT (ms)")
    ax1.legend()
    ax1.grid(True)
    plt.title(f"RTT over Time for {TARGET_IA}")
    plt.tight_layout()
    plt.savefig("rtt_stabilization.png")
    plt.close()

    plt.figure(figsize=(12, 5))
    plt.plot(times, counts, marker='s', color='orange', label="Path Count")
    if stab_idx is not None:
        plt.axvline(times[stab_idx], color='red', linestyle='--', label="Stabilization Start")
    plt.xlabel("Time")
    plt.ylabel("Number of Paths")
    plt.title(f"Path Count over Time for {TARGET_IA}")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("path_count.png")
    plt.close()

def main():
    data = load_prober_for_as()
    if not data:
        print("No data found.")
        return

    stab_idx = find_stabilization_point(data)
    if stab_idx is None:
        print("No stabilization point detected.")
    else:
        before_fps = set().union(*[x[2] for x in data[:stab_idx]])
        after_fps = set().union(*[x[2] for x in data[stab_idx:]])
        lost, new, persistent = compare_paths(before_fps, after_fps)

        print(f"Stabilization starts at: {data[stab_idx][0]}")
        print(f"Lost paths: {len(lost)} → {lost}")
        print(f"New paths: {len(new)} → {new}")
        print(f"Persistent paths: {len(persistent)}")

    plot_results(data, stab_idx)

if __name__ == "__main__":
    main()
