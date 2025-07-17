import os
import json
import pandas as pd
import numpy as np
from datetime import datetime

def extract_timestamp_from_filename(filename):
    try:
        for part in filename.split("_"):
            if len(part) >= 16 and "T" in part:
                return datetime.fromisoformat(part)
    except Exception:
        pass
    return datetime.now()

def format_sequence_with_ifaces(sequence_str):
    parts = sequence_str.split()
    formatted_parts = []
    for part in parts:
        if "#" in part:
            as_part, ifaces = part.split("#", 1)
            formatted_parts.append(f"{as_part} [in,out]=({ifaces})")
        else:
            formatted_parts.append(part)
    return " ".join(formatted_parts)

def parse_ping(data, src_as):
    rows = []
    timestamp = data.get("timestamp") or datetime.now().isoformat()
    dst_as = data.get("ia")
    for probe in data.get("probes", []):
        rtts = [r["round_trip_time"] for r in probe.get("ping_result", {}).get("replies", []) if r.get("state") == "success"]
        stats = probe.get("ping_result", {}).get("statistics", {})
        replies = probe.get("ping_result", {}).get("replies", [])
        sent = stats.get("sent", 0)
        received = stats.get("received", 0)
        loss_rate = 1 - received / sent if sent > 0 else None
        path_info = probe.get("ping_result", {}).get("path", {})
        sequence = path_info.get("sequence")
        hops = path_info.get("hops", [])
        fingerprint = probe.get("fingerprint")
        src_sequence = sequence.split()[0].split("#")[0] if sequence else None

        if sequence:
            sequence = format_sequence_with_ifaces(sequence)

        row = {
            "timestamp": timestamp,
            "src_as": src_sequence,
            "dst_as": dst_as,
            "path_fingerprint": fingerprint,
            "sequence": sequence,
            "sent (count)": sent,
            "received (count)": received,
            "loss_rate (%)": loss_rate,
            "min_rtt (ms)": stats.get("min_rtt"),
            "avg_rtt (ms)": stats.get("avg_rtt"),
            "max_rtt (ms)": stats.get("max_rtt"),
            "mdev_rtt (ms)": stats.get("mdev_rtt"),
            "replies_rtt (ms)": rtts
        }

        rows.append(row)

    return rows

def parse_bandwidth(data, src_as):
    rows = []
    timestamp = data.get("timestamp") or datetime.now().isoformat()

    def parse_bps(value):
        try:
            return float(value.split("/")[-1].strip().split()[0])
        except:
            return None

    if "paths" in data:
        for path in data.get("paths", []):
            try:
                f = path.get("fingerprint")
                sequence_str = path.get("sequence", "")
                sequence_parts = [p.strip() for p in sequence_str.split("->") if p.strip()]
                src_as_path = sequence_parts[0] if sequence_parts else src_as
                dst_as_path = sequence_parts[-1] if sequence_parts else None

                res = path.get("result", {})
                sc = res.get("S->C results", {})
                cs = res.get("C->S results", {})
                target = path.get("target", {})

                row = {
                    "timestamp": timestamp,
                    "src_as": src_as_path,
                    "dst_as": dst_as_path,
                    "path_fingerprint": f,
                    "target_mbps (Mbps)": target.get("tier_mbps"),
                    "target_duration_sec (sec)": target.get("duration_sec"),
                    "target_packet_size_bytes (bytes)": target.get("packet_size_bytes"),
                    "target_packet_count (count)": target.get("packet_count"),
                    "sequence": sequence_str,
                    "sc_attempted_bps (bps)": sc.get("attempted_bps"),
                    "sc_achieved_bps (bps)": sc.get("achieved_bps"),
                    "sc_loss_rate_percent (%)": sc.get("loss_rate"),
                    "sc_interarrival (ms)": sc.get("interarrival time min/avg/max/mdev"),
                    "cs_attempted_bps (bps)": cs.get("attempted_bps"),
                    "cs_achieved_bps (bps)": cs.get("achieved_bps"),
                    "cs_loss_rate_percent (%)": cs.get("loss_rate"),
                    "cs_interarrival (ms)": cs.get("interarrival time min/avg/max/mdev")
         
                }

                bw_sc = parse_bps(sc.get("achieved_bps", "0/0"))
                bw_cs = parse_bps(cs.get("achieved_bps", "0/0"))
                row["avg_bandwidth (Mbps)"] = (bw_sc + bw_cs) / 2 if bw_sc and bw_cs else None

                rows.append(row)
            except Exception as e:
                print(f"⚠️ Erreur parsing bandwidth (paths): {e}")
                continue

    elif "result" in data and isinstance(data["result"], dict):
        res = data["result"]
        sc = res.get("S->C results", {})
        cs = res.get("C->S results", {})
        target = data.get("target", {})

        dst_as = data.get("target_server", {}).get("ia")

        row = {
            "timestamp": timestamp,
            "src_as": src_as,
            "dst_as": dst_as,
            "path_fingerprint": None,
            "target_mbps (Mbps)": target.get("tier_mbps"),
            "target_duration_sec (sec)": target.get("duration_sec"),
            "target_packet_size_bytes (bytes)": target.get("packet_size_bytes"),
            "target_packet_count (count)": target.get("packet_count"),
            "sequence": None,
            "sc_attempted_bps (bps)": sc.get("attempted_bps"),
            "sc_achieved_bps (bps)": sc.get("achieved_bps"),
            "sc_loss_rate_percent (%)": sc.get("loss_rate"),
            "sc_interarrival (ms)": sc.get("interarrival time min/avg/max/mdev"),
            "cs_attempted_bps (bps)": cs.get("attempted_bps"),
            "cs_achieved_bps (bps)": cs.get("achieved_bps"),
            "cs_loss_rate_percent (%)": cs.get("loss_rate"),
            "cs_interarrival (ms)": cs.get("interarrival time min/avg/max/mdev")
            
        }

        bw_sc = parse_bps(sc.get("achieved_bps", "0/0"))
        bw_cs = parse_bps(cs.get("achieved_bps", "0/0"))
        row["avg_bandwidth (Mbps)"] = (bw_sc + bw_cs) / 2 if bw_sc and bw_cs else None

        rows.append(row)

    return rows




def collect_all_data(base_path):
    all_ping = []
    all_bandwidth = []
    all_traceroute = []
    all_showpaths = []

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".json"):
                fpath = os.path.join(root, file)
                file_ts = extract_timestamp_from_filename(file).isoformat()
                try:
                    with open(fpath) as f:
                        data = json.load(f)

                    src_as = data.get("ia") or data.get("as") or data.get("local_isd_as")

                    if "probes" in data and any("ping_result" in probe for probe in data.get("probes", [])):
                        parsed = parse_ping(data, src_as)
                        all_ping.extend(parsed)

                    elif "paths" in data and any(
                        "result" in path and ("S->C results" in path["result"] or "C->S results" in path["result"])
                        for path in data.get("paths", [])
                    ):
                        parsed = parse_bandwidth(data, src_as)
                        all_bandwidth.extend(parsed)

                    elif "result" in data and "S->C results" in data["result"] and "C->S results" in data["result"]:
                        parsed = parse_bandwidth(data, src_as)
                        all_bandwidth.extend(parsed)

 
                except Exception as e:
                    print(f"⚠️ Error parsing file {fpath}: {e}")

    return all_ping, all_bandwidth, all_traceroute, all_showpaths

def save_dfs(base_path, output_dir="parsed_output"):
    os.makedirs(output_dir, exist_ok=True)

    ping, bandwidth, traceroute, showpaths = collect_all_data(base_path)

    if ping:
        df_ping = pd.DataFrame(ping).sort_values("timestamp")
        df_ping.to_csv(os.path.join(output_dir, "ping_data.csv"), index=False)

    if bandwidth:
        df_bw = pd.DataFrame(bandwidth).sort_values("timestamp")
        df_bw.to_csv(os.path.join(output_dir, "bandwidth_data.csv"), index=False)

    if traceroute:
        df_tr = pd.DataFrame(traceroute).sort_values("timestamp")
        df_tr.to_csv(os.path.join(output_dir, "traceroute_data.csv"), index=False)

    if showpaths:
        df_sp = pd.DataFrame(showpaths).sort_values("timestamp")
        df_sp.to_csv(os.path.join(output_dir, "showpaths_data.csv"), index=False)


if __name__ == "__main__":
    base_path = "/home/scion/Documents/DataMachine1/Data/Archive"
    save_dfs(base_path)
