# analyze_prober.py

import os
import json
import statistics
from datetime import datetime
from collections import defaultdict

ARCHIVE_DIR = ""
PROBER_PREFIX = "prober_"

def load_prober_data(archive_dir):
    prober_data = defaultdict(lambda: {
        "rtts": [],
        "packet_losses": [],
        "mdevs": [],
        "sequence_issues": 0,
        "total_probes": 0
    })

    for fname in os.listdir(archive_dir):
        if not fname.startswith(PROBER_PREFIX) or not fname.endswith(".json"):
            continue
        path = os.path.join(archive_dir, fname)
        try:
            with open(path) as f:
                doc = json.load(f)
                ia = doc.get("ia")
                probes = doc.get("probes", [])
                if not ia:
                    continue

                for probe in probes:
                    result = probe.get("ping_result", {})
                    stats = result.get("statistics", {})
                    replies = result.get("replies", [])

                    avg_rtt = stats.get("avg_rtt")
                    packet_loss = stats.get("packet_loss")
                    mdev = stats.get("mdev_rtt")

                    if avg_rtt is not None:
                        prober_data[ia]["rtts"].append(avg_rtt)
                    if packet_loss is not None:
                        prober_data[ia]["packet_losses"].append(packet_loss)
                    if mdev is not None:
                        prober_data[ia]["mdevs"].append(mdev)

                    prober_data[ia]["total_probes"] += 1

                    # Check for missing or unordered sequences
                    seqs = [r.get("scmp_seq") for r in replies if "scmp_seq" in r]
                    expected = sorted(seqs)
                    if seqs and seqs != expected:
                        prober_data[ia]["sequence_issues"] += 1

        except Exception as e:
            print(f"[WARN] Failed to parse {fname}: {e}")
    return prober_data

def compute_stats(values):
    if not values:
        return {"count": 0, "avg": None, "jitter": None}
    avg = round(statistics.mean(values), 2)
    jitter = round(statistics.stdev(values), 2) if len(values) > 1 else 0.0
    return {"count": len(values), "avg": avg, "jitter": jitter}

def write_output_to_file(output_lines, filename):
    with open(filename, "w") as f:
        for line in output_lines:
            f.write(line + "\n")

def main():
    output_file = f"prober_analysis.txt"
    output_lines = []

    def log(line=""):
        print(line)
        output_lines.append(line)

    log("=== SCION Prober Latency & Loss Analysis ===")
    prober_data = load_prober_data(ARCHIVE_DIR)

    log(f"\n Summary:\n")
    for ia, data in prober_data.items():
        latency_stats = compute_stats(data["rtts"])
        loss_stats = compute_stats(data["packet_losses"])
        seq_issues = data["sequence_issues"]
        total = data["total_probes"]

        mdevs = data.get("mdevs", [])
        avg_path_jitter = round(statistics.mean(mdevs), 2) if mdevs else None

        log(f"→ Destination IA: {ia}")
        log(f"   Probes:        {total}")
        log(f"   Avg RTT:       {latency_stats['avg']} ms")
        log(f"   Jitter:        {latency_stats['jitter']} ms")
        log(f"   Avg Path Jitter: {avg_path_jitter} ms")
        log(f"   Avg Loss:      {loss_stats['avg']}%")
        log(f"   Loss Jitter:   {loss_stats['jitter']}%")
        log(f"   Seq issues:    {seq_issues} of {total} probes\n")

    write_output_to_file(output_lines, output_file)
    log(f"\n[Saved output to {output_file}]")

if __name__ == "__main__":
    main()
