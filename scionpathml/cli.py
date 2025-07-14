#!/usr/bin/env python3

import os
import subprocess
import argparse
import sys

from pathlib import Path

SCRIPT_NAME = "pipeline.sh"
SCRIPT_FOLDER_NAME = "mpquic-on-scion-ipc/Scripts"
ENV_VAR = "SCRIPT_PATH"

def find_script_automatically():
    """Search for mpquic-on-scion-ipc/Scripts/pipeline.sh in common paths."""
    home = Path.home()
    possible_roots = [
        Path.cwd(),             # current directory
        home,                   # home directory
        home / "Documents",     # common location
    ]

    for root in possible_roots:
        for path in root.rglob(SCRIPT_FOLDER_NAME):
            candidate = path / SCRIPT_NAME
            if candidate.exists():
                return str(candidate)

    raise FileNotFoundError(f"Could not find {SCRIPT_FOLDER_NAME}/{SCRIPT_NAME} in known locations.")

def get_script_path(path_override=None):
    if path_override:
        return os.path.join(path_override, SCRIPT_NAME)

    path_from_env = os.getenv(ENV_VAR)
    if path_from_env:
        return os.path.join(path_from_env, SCRIPT_NAME)

    # Automatic fallback
    return find_script_automatically()

def read_crontab():
    result = subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout if result.returncode == 0 else ""

def write_crontab(content):
    subprocess.run(["crontab", "-"], input=content, text=True)

def update_cron(frequency, path_override=None):
    full_path = get_script_path(path_override)
    cron_line = f"*/{frequency} * * * * {full_path}"

    current_cron = read_crontab()
    lines = [line for line in current_cron.splitlines() if SCRIPT_NAME not in line]
    lines.append(cron_line)

    write_crontab("\n".join(lines) + "\n")
    print(f"[✓] Cron updated to run every {frequency} minutes:\n  {cron_line}")

def stop_cron():
    current_cron = read_crontab()
    lines = [line for line in current_cron.splitlines() if SCRIPT_NAME not in line]
    write_crontab("\n".join(lines) + "\n")
    print("[✓] Cronjob removed.")

def main():
    parser = argparse.ArgumentParser(description="SCIONPathML CLI Tool")
    parser.add_argument("-f", "--frequency", type=int, help="Set frequency in minutes")
    parser.add_argument("--path", type=str, help="Override script folder path")
    parser.add_argument("command", nargs="?", choices=["stop"], help="Stop the cronjob")

    args = parser.parse_args()

    if args.command == "stop":
        stop_cron()
    elif args.frequency:
        update_cron(args.frequency, args.path)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
