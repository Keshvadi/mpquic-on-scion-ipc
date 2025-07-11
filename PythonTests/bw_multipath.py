import os
import subprocess
import json
import time
import random
from datetime import datetime
from math import ceil
from concurrent.futures import ThreadPoolExecutor, as_completed
from config import (
    BWTEST_SERVERS
)

# Bandwidth tiers in Mbps
TARGET_MBPS = [10, 50, 100]

# Parameters
DURATION = 3  # seconds
PACKET_SIZE = 1000  # bytes

# Directories
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "Data"))
RESULT_DIR = os.path.join(BASE_DIR, "History", "BandwidthParallel")
LOG_DIR = os.path.join(BASE_DIR, "Logs", "BandwidthParallel")
os.makedirs(LOG_DIR, exist_ok=True)


def normalize_as(as_str):
    return as_str.replace(":", "_")


def get_paths_info(dst_ia):
    try:
        cmd = ["scion", "showpaths", dst_ia, "--format", "json", "-m", "40", "-e"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            print(f"[ERROR] showpaths failed for {dst_ia}: {result.stderr.strip()}")
            return []

        path_data = json.loads(result.stdout)
        paths = path_data.get("paths", [])

        path_list = []
        for i, p in enumerate(paths):
            fingerprint = p.get("fingerprint", "")

            hops = p.get("hops", [])
            sequence_hops = []
            last_ia = None
            for hop in hops:
                ia = hop.get("ia") or hop.get("isd_as") or hop.get("isd_as_str") or "?"
                if ia != last_ia:
                    sequence_hops.append(ia)
                    last_ia = ia

            sequence = " -> ".join(sequence_hops)
            path_list.append((i, fingerprint, sequence))
        return path_list
    except Exception as e:
        print(f"[EXCEPTION] while getting paths for {dst_ia}: {e}")
        return []


def parse_output(text):
    result = {
        "S->C results": {},
        "C->S results": {},
        "invalid_format": False
    }
    if "S->C results" not in text or "C->S results" not in text:
        result["invalid_format"] = True
        result["raw_output"] = text.strip()
        return result
    try:
        sections = text.split("C->S results")
        sc_block = sections[0].split("S->C results")[-1].strip()
        cs_block = sections[1].strip()
    except Exception as e:
        result["invalid_format"] = True
        result["raw_output"] = text.strip()
        result["error"] = f"Split failed: {e}"
        return result

    def extract_metrics(block):
        import re
        def _match(pattern, text):
            match = re.search(pattern, text)
            return match.group(1) if match else None
        return {
            "attempted_bps": _match(r"Attempted bandwidth:\s+(.+)", block),
            "achieved_bps": _match(r"Achieved bandwidth:\s+(.+)", block),
            "loss_rate": _match(r"Loss rate:\s+(.+)", block),
            "interarrival time min/avg/max/mdev": _match(r"Interarrival time.*?=\s+(.+)", block)
        }

    result["S->C results"] = extract_metrics(sc_block)
    result["C->S results"] = extract_metrics(cs_block)
    return result


def run_bwtest(ia, ip, target_mbps, fingerprint):
    bps_target = int(target_mbps * 1_000_000)
    packet_count = ceil(bps_target * DURATION / (PACKET_SIZE * 8))

    cmd = [
        "scion-bwtestclient",
        "-s", f"{ia},[{ip}]:30100",
        "-cs", f"{DURATION},{PACKET_SIZE},{packet_count},?",
        "-sc", f"{DURATION},{PACKET_SIZE},{packet_count},?"
    ]

    command_str = " ".join(cmd)

    try:
        env = os.environ.copy()
        env["SCION_PATH_SELECTION"] = f"fingerprint:{fingerprint}"

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=30, env=env)

        stdout = result.stdout.strip()
        stderr = result.stderr.strip()
        all_output = stdout + "\n" + stderr

        if "Fatal: no path to" in all_output:
            return {
                "error_type": "no_path_error",
                "raw_output": all_output,
                "stderr": stderr,
                "return_code": result.returncode,
                "command": command_str,
                "target": {
                    "tier_mbps": target_mbps,
                    "duration_sec": DURATION,
                    "packet_size_bytes": PACKET_SIZE,
                    "packet_count": packet_count
                },
                "target_server": {
                    "ia": ia,
                    "ip": ip
                }
            }

        parsed = parse_output(stdout)
        return {
            "result": parsed,
            "stderr": stderr,
            "return_code": result.returncode,
            "command": command_str,
            "target": {
                "tier_mbps": target_mbps,
                "duration_sec": DURATION,
                "packet_size_bytes": PACKET_SIZE,
                "packet_count": packet_count
            },
            "target_server": {
                "ia": ia,
                "ip": ip
            }
        }

    except subprocess.TimeoutExpired:
        return {
            "error_type": "timeout",
            "command": command_str,
            "target": {
                "tier_mbps": target_mbps,
                "duration_sec": DURATION,
                "packet_size_bytes": PACKET_SIZE,
                "packet_count": packet_count
            },
            "target_server": {
                "ia": ia,
                "ip": ip
            }
        }
    except Exception as e:
        return {
            "error_type": "exception",
            "exception": str(e),
            "command": command_str,
            "target": {
                "tier_mbps": target_mbps,
                "duration_sec": DURATION,
                "packet_size_bytes": PACKET_SIZE,
                "packet_count": packet_count
            },
            "target_server": {
                "ia": ia,
                "ip": ip
            }
        }


if __name__ == "__main__":
    start = time.time()

    print("==== START BANDWIDTH MULTIPATH TESTING ====")

    for ia, (ip, folder) in BWTEST_SERVERS.items():
        log_filename = f"BW_AS_{normalize_as(ia)}.log"
        log_path = os.path.join(LOG_DIR, log_filename)

        with open(log_path, "a") as log_file:
            log_file.write("==== START BANDWIDTH MULTIPATH TESTING ====\n")

            paths_info = get_paths_info(ia)
            if not paths_info:
                timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                msg = f"[ERROR] {timestamp} - AS {ia}: No paths found or failed to retrieve paths"
                print(msg)
                log_file.write(msg + "\n")

                for mbps in TARGET_MBPS:
                    error_result = {
                        "timestamp": timestamp,
                        "as": ia,
                        "target_mbps": mbps,
                        "error": "no paths found or failed to retrieve paths",
                        "target_server": {
                            "ia": ia,
                            "ip": ip
                        }
                    }
                    output_dir = os.path.join(RESULT_DIR, folder)
                    os.makedirs(output_dir, exist_ok=True)
                    filename = f"BW_{timestamp}_AS_{normalize_as(ia)}_{mbps}Mbps.json"
                    with open(os.path.join(output_dir, filename), "w") as f:
                        json.dump(error_result, f, indent=2)

                log_file.write("==== END BANDWIDTH MULTIPATH TESTING ====\n")
                continue  # skip bandwidth testing for this AS

            for mbps in TARGET_MBPS:
                all_results = {
                    "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"),
                    "as": ia,
                    "target_mbps": mbps,
                    "paths": []
                }

                num_paths = len(paths_info)

                if num_paths < 2:
                    if num_paths == 1:
                        timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                        msg = f"[INFO] {timestamp} - AS {ia} - {mbps}Mbps: Just one path available, skipping parallel test."
                        print(msg)
                        log_file.write(msg + "\n")

                    for path_index, fingerprint, sequence in paths_info:
                        start_test_ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                        print(f"[START] {start_test_ts} - AS {ia} - {mbps}Mbps - path {path_index}")
                        log_file.write(f"[START] {start_test_ts} - AS {ia} - {mbps}Mbps - path {path_index}\n")

                        result = run_bwtest(ia, ip, mbps, fingerprint)

                        end_test_ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                        print(f"[END] {end_test_ts} - AS {ia} - {mbps}Mbps - path {path_index}")
                        log_file.write(f"[END] {end_test_ts} - AS {ia} - {mbps}Mbps - path {path_index}\n")

                        path_result = {
                            "path_index": path_index,
                            "fingerprint": fingerprint,
                            "sequence": sequence,
                            **result
                        }
                        all_results["paths"].append(path_result)

                        if result.get("error_type"):
                            msg = f"[ERROR] {end_test_ts} - AS {ia} - {mbps}Mbps - path {path_index}: {result.get('error_type')}"
                        else:
                            msg = f"[OK] {end_test_ts} - AS {ia} - {mbps}Mbps - path {path_index}"

                        print(msg)
                        log_file.write(msg + "\n")

                else:
                    selected_paths = random.sample(paths_info, 2)

                    def test_path(path):
                        path_index, fingerprint, sequence = path
                        start_test_ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                        print(f"[START] {start_test_ts} - AS {ia} - {mbps}Mbps - path {path_index}")
                        # No need to log here because main context handles logging after future completes
                        result = run_bwtest(ia, ip, mbps, fingerprint)
                        end_test_ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
                        print(f"[END] {end_test_ts} - AS {ia} - {mbps}Mbps - path {path_index}")
                        return {
                            "path_index": path_index,
                            "fingerprint": fingerprint,
                            "sequence": sequence,
                            **result,
                            "start_ts": start_test_ts,
                            "end_ts": end_test_ts
                        }

                    with ThreadPoolExecutor(max_workers=2) as executor:
                        futures = [executor.submit(test_path, p) for p in selected_paths]
                        for future in as_completed(futures):
                            path_result = future.result()
                            all_results["paths"].append(path_result)

                            end_test_ts = path_result.get("end_ts", datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S"))
                            if path_result.get("error_type"):
                                msg = f"[ERROR] {end_test_ts} - AS {ia} - {mbps}Mbps - path {path_result['path_index']}: {path_result.get('error_type')}"
                            else:
                                msg = f"[OK] {end_test_ts} - AS {ia} - {mbps}Mbps - path {path_result['path_index']}"

                            print(msg)
                            log_file.write(msg + "\n")

                output_dir = os.path.join(RESULT_DIR, folder)
                os.makedirs(output_dir, exist_ok=True)
                filename = f"BW_{datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')}_AS_{normalize_as(ia)}_{mbps}Mbps.json"
                with open(os.path.join(output_dir, filename), "w") as f:
                    json.dump(all_results, f, indent=2)

            log_file.write("==== END BANDWIDTH MULTIPATH TESTING ====\n")

    print("==== END BANDWIDTH MULTIPATH TESTING ====")

    end = time.time()
    elapsed = end - start

    print(f"[LOG] Total execution time: {elapsed:.2f} seconds")
    duration_log = os.path.join(LOG_DIR, "script_duration.log")
    with open(duration_log, "a") as f:
        f.write(f"{datetime.utcnow().strftime('%Y-%m-%dT%H-%M-%S')} - Total execution time: {elapsed:.2f} seconds\n")
