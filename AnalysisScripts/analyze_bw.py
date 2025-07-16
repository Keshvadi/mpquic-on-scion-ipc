import os
import json
import statistics
from datetime import datetime
from collections import defaultdict

ARCHIVE_DIR = ""
BW_PREFIX = "BW_"

def parse_bps_field(bps_str):
    try:
        return float(bps_str.split(" ")[0]) / 1e6  # Convert to Mbps
    except:
        return None

def parse_interarrival(inter_str):
    try:
        parts = inter_str.replace(" ms", "").split("/")
        return tuple(map(float, parts))  # min, avg, max, mdev
    except:
        return None, None, None, None

def compute_full_stats(values):
    if not values:
        return {"count": 0, "avg": None, "jitter": None, "min": None, "max": None}
    return {
        "count": len(values),
        "avg": round(statistics.mean(values), 2),
        "jitter": round(statistics.stdev(values), 2) if len(values) > 1 else 0.0,
        "min": round(min(values), 2),
        "max": round(max(values), 2)
    }

def load_bw_data(archive_dir):
    bw_data = defaultdict(lambda: defaultdict(lambda: {
        "sc_bandwidth": [],
        "cs_bandwidth": [],
        "sc_loss": [],
        "cs_loss": [],
        "sc_interarrival": [],
        "cs_interarrival": [],
        "sc_interarrival_minmax": [],
        "cs_interarrival_minmax": [],
        "sc_interarrival_mdev": [],
        "cs_interarrival_mdev": [],
        "files": 0,
    }))

    for fname in os.listdir(archive_dir):
        if not fname.startswith(BW_PREFIX) or not fname.endswith(".json"):
            continue

        path = os.path.join(archive_dir, fname)
        try:
            with open(path) as f:
                doc = json.load(f)
                ia = doc.get("target_server", {}).get("ia") or doc.get("as")
                mbps = doc.get("target", {}).get("tier_mbps") or doc.get("target_mbps")
                if not ia or not mbps:
                    continue

                bw_data[ia][mbps]["files"] += 1

                paths = doc.get("paths", [doc])

                for path_result in paths:
                    result = path_result.get("result", {})
                    if result.get("invalid_format"):
                        continue

                    for direction_key, prefix in [("S->C results", "sc"), ("C->S results", "cs")]:
                        dir_result = result.get(direction_key)
                        if not dir_result:
                            continue

                        bw = parse_bps_field(dir_result.get("achieved_bps", ""))
                        if bw is not None:
                            bw_data[ia][mbps][f"{prefix}_bandwidth"].append(bw)

                        loss_str = dir_result.get("loss_rate", "").strip('%')
                        try:
                            loss = float(loss_str)
                            bw_data[ia][mbps][f"{prefix}_loss"].append(loss)
                        except:
                            pass

                        inter_str = dir_result.get("interarrival time min/avg/max/mdev")
                        if inter_str:
                            min_i, avg_i, max_i, mdev = parse_interarrival(inter_str)
                            if avg_i is not None:
                                bw_data[ia][mbps][f"{prefix}_interarrival"].append(avg_i)
                                bw_data[ia][mbps][f"{prefix}_interarrival_minmax"].append((min_i, max_i))
                            if mdev is not None:
                                bw_data[ia][mbps][f"{prefix}_interarrival_mdev"].append(mdev)

        except Exception as e:
            print(f"[WARN] Failed to parse {fname}: {e}")

    return bw_data


def write_output_to_file(output_lines, filename):
    with open(filename, "w") as f:
        for line in output_lines:
            f.write(line + "\n")


def print_bw_summary(bw_data):
    output_file = f"sp_bw_analysis.txt"
    output_lines = []

    def log(line=""):
        print(line)
        output_lines.append(line)

    log("=== SCION Bandwidth Test Summary ===")

    for ia in sorted(bw_data):
        print(f"→ Destination IA: {ia}")
        for mbps in sorted(bw_data[ia]):
            data = bw_data[ia][mbps]
            log(f"  - Tier:         {mbps} Mbps")
            log(f"    Files:        {data['files']}\n")

            for direction in ["sc", "cs"]:
                dir_label = "S→C" if direction == "sc" else "C→S"
                bw_stats = compute_full_stats(data[f"{direction}_bandwidth"])
                loss_stats = compute_full_stats(data[f"{direction}_loss"])
                inter_stats = compute_full_stats(data[f"{direction}_interarrival"])
                inter_mdev = compute_full_stats(data[f"{direction}_interarrival_mdev"])
                inter_minmax = data.get(f"{direction}_interarrival_minmax", [])
                min_vals = [x[0] for x in inter_minmax if x]
                max_vals = [x[1] for x in inter_minmax if x]
                inter_min = round(min(min_vals), 4) if min_vals else None
                inter_max = round(max(max_vals), 2) if max_vals else None

                log(f"    [{dir_label}]")
                log(f"      Count:           {bw_stats['count']}")
                log(f"      Avg BW:          {bw_stats['avg']} Mbps")
                log(f"      BW Jitter:       {bw_stats['jitter']} Mbps")
                log(f"      BW Min/Max:      {bw_stats['min']} / {bw_stats['max']} Mbps")
                log(f"      Avg Loss:        {loss_stats['avg']}%")
                log(f"      Loss Jitter:     {loss_stats['jitter']}%")
                log(f"      Interarrival:    {inter_stats['avg']} ms")
                log(f"      IA Jitter:       {inter_mdev['avg']} ms")
                log(f"      IA Min/Max:      {inter_min} / {inter_max} ms")
                log("")

    write_output_to_file(output_lines, output_file)
    log(f"\n[Saved output to {output_file}]")


def main():
    bw_data = load_bw_data(ARCHIVE_DIR)
    print_bw_summary(bw_data)

if __name__ == "__main__":
    main()
