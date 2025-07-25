# compare_sp_mp_prober.py

import os
import json
import statistics
from datetime import datetime, timedelta
from collections import defaultdict
import matplotlib.pyplot as plt

ARCHIVE_DIR = ""
SP_PREFIX = "prober_"
MP_PREFIX = "mp-prober_"
TIME_WINDOW = timedelta(minutes=15)


def parse_filename_timestamp(fname):
    try:
        return datetime.strptime(fname.split("_")[1], "%Y-%m-%dT%H:%M")
    except Exception as e:
        print(f"[WARN] Could not parse timestamp from filename {fname}: {e}")
        return None


def load_prober_files(prefix):
    data = defaultdict(lambda: defaultdict(dict))  # ia -> timestamp -> fingerprint -> stats
    for fname in os.listdir(ARCHIVE_DIR):
        if not fname.startswith(prefix) or not fname.endswith(".json"):
            continue
        timestamp = parse_filename_timestamp(fname)
        if not timestamp:
            continue

        path = os.path.join(ARCHIVE_DIR, fname)
        try:
            with open(path) as f:
                doc = json.load(f)
                ia = doc.get("ia")
                if not ia or not doc.get("probes"):
                    continue

                for probe in doc["probes"]:
                    ping = probe.get("ping_result", {})
                    stats = ping.get("statistics", {})
                    fp = probe.get("fingerprint")
                    if not ping or not stats or not fp:
                        continue

                    data[ia][timestamp][fp] = {
                        "avg_rtt": stats.get("avg_rtt"),
                        "mdev": stats.get("mdev_rtt"),
                        "loss": stats.get("packet_loss"),
                    }
        except Exception as e:
            print(f"[WARN] Failed to load {fname}: {e}")
    return data


def match_and_compare(sp_data, mp_data):
    results = []
    for ia in sp_data:
        for sp_time in sp_data[ia]:
            for mp_time in mp_data.get(ia, {}):
                if abs(sp_time - mp_time) > TIME_WINDOW:
                    continue

                for fp, sp_stats in sp_data[ia][sp_time].items():
                    mp_stats = mp_data[ia][mp_time].get(fp)
                    if not mp_stats:
                        continue

                    try:
                        diff_rtt = sp_stats["avg_rtt"] - mp_stats["avg_rtt"]
                        diff_jitter = sp_stats["mdev"] - mp_stats["mdev"]
                        diff_loss = sp_stats["loss"] - mp_stats["loss"]
                        results.append({
                            "ia": ia,
                            "fp": fp,
                            "rtt_diff": diff_rtt,
                            "jitter_diff": diff_jitter,
                            "loss_diff": diff_loss
                        })
                    except:
                        continue
    return results


def summarize_differences(results):
    rtts = [x["rtt_diff"] for x in results if x["rtt_diff"] is not None]
    jitters = [x["jitter_diff"] for x in results if x["jitter_diff"] is not None]
    losses = [x["loss_diff"] for x in results if x["loss_diff"] is not None]

    summary = {
        "matched_paths": len(results),
        "avg_rtt_diff": round(statistics.mean(rtts), 2) if rtts else None,
        "avg_jitter_diff": round(statistics.mean(jitters), 2) if jitters else None,
        "avg_loss_diff": round(statistics.mean(losses), 2) if losses else None,
    }
    return summary

def plot_differences(results):
    output_dir = "sp_mp_prober_plots"
    os.makedirs(output_dir, exist_ok=True)

    # Extract values
    rtt_diffs = [r["rtt_diff"] for r in results if r["rtt_diff"] is not None]
    jitter_diffs = [r["jitter_diff"] for r in results if r["jitter_diff"] is not None]
    loss_diffs = [r["loss_diff"] for r in results if r["loss_diff"] is not None]

    # Boxplot
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot([rtt_diffs, jitter_diffs, loss_diffs], tick_labels=["RTT (ms)", "Jitter (ms)", "Loss (%)"], patch_artist=True)
    ax.set_title("SP - MP Differences (Boxplot)")
    ax.set_ylabel("Difference (SP - MP)")
    ax.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "sp_mp_diff_boxplot.png"))
    plt.close()

    # Scatter plot over index (optional, helps see trends)
    for name, diffs in [("rtt (ms)", rtt_diffs), ("jitter (ms)", jitter_diffs), ("loss (%)", loss_diffs)]:
        plt.figure(figsize=(8, 4))
        plt.scatter(range(len(diffs)), diffs, alpha=0.6, marker="o", color="steelblue")
        plt.axhline(0, linestyle="--", color="red")
        plt.title(f"{name.upper()} Difference per Matched Path")
        plt.xlabel("Matched Path Index")
        plt.ylabel(f"Difference (SP - MP) {name}") # was changed
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, f"{name}_diff_scatter.png"))
        plt.close()

    print(f"[Saved SP/MP prober difference plots to ./{output_dir}/]")


def main():
    output_file = "sp_mp_prober_comparison.txt"
    output_lines = []

    def log(line=""):
        print(line)
        output_lines.append(line)

    log("=== SCION SP vs MP Prober Path Comparison ===\n")

    log("Loading SP data...")
    sp_data = load_prober_files(SP_PREFIX)

    log("Loading MP data...")
    mp_data = load_prober_files(MP_PREFIX)

    log("Matching and comparing paths...\n")
    comparison_results = match_and_compare(sp_data, mp_data)
    summary = summarize_differences(comparison_results)

    log(f"→ Matched Fingerprints: {summary['matched_paths']}")
    log(f"→ Avg RTT difference (SP - MP): {summary['avg_rtt_diff']} ms")
    log(f"→ Avg Jitter difference (SP - MP): {summary['avg_jitter_diff']} ms")
    log(f"→ Avg Loss difference (SP - MP): {summary['avg_loss_diff']} %\n")

    log("[Saved comparison results to sp_mp_prober_comparison.txt]")
    with open(output_file, "w") as f:
        for line in output_lines:
            f.write(line + "\n")

    plot_differences(comparison_results)


if __name__ == "__main__":
    main()
