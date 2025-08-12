import os
import subprocess
from cli_utils import *

class CronManager:
    def __init__(self, script_name="./mpquic-on-scion-ipc/runner/pipeline.sh", env_var="SCRIPT_PATH"):
        self.script_name = script_name
        self.env_var = env_var
    
    def read_crontab(self):
        """Read current user's crontab"""
        result = subprocess.run(["crontab", "-l"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout if result.returncode == 0 else ""

    def write_crontab(self, content):
        """Write content to user's crontab"""
        subprocess.run(["crontab", "-"], input=content, text=True)

    def get_current_cron_frequency(self):
        """Get the current cron frequency for scionpathml."""
        current_cron = self.read_crontab()
        for line in current_cron.splitlines():
            if "pipeline.sh" in line and line.strip() and not line.strip().startswith("#"):
                parts = line.strip().split()
                if len(parts) >= 5 and parts[0].startswith("*/"):
                    try:
                        return int(parts[0][2:])
                    except ValueError:
                        return None
        return None

    def get_script_path(self, path_override=None):
        """Get the path to pipeline.sh script."""
        if path_override:
            script_path = os.path.join(path_override, "pipeline.sh")
            print_info(f"Using manual path override: {script_path}")
            return script_path
            
        env_path = os.getenv(self.env_var)
        if env_path:
            script_path = os.path.join(env_path, "pipeline.sh")
            print_info(f"Using environment variable path: {script_path}")
            return script_path
            
        # Try automatic detection
        current_path = os.path.abspath(__file__)
        parts = current_path.split(os.sep)
        if "mpquic-on-scion-ipc" in parts:
            mpquic_index = parts.index("mpquic-on-scion-ipc")
            base_path = os.sep.join(parts[:mpquic_index + 1])
            script_path = os.path.join(base_path, "runner", "pipeline.sh")
            if os.path.isfile(script_path):
                print_info(f"Auto-detected script path: {script_path}")
                return script_path
                
        raise EnvironmentError(
            f"{self.env_var} environment variable is not set and automatic detection failed.\n"
            f"{Colors.CYAN}💡 Solutions:{Colors.END}\n"
            f"   1. Use -p flag: scionpathml -f 30 -p /path/to/runner\n"
            f"   2. Set environment: export {self.env_var}=/path/to/runner"
        )

    def explain_frequency_calculation(self):
        """Explain how frequency calculation works"""
        print_info("💡 How frequency calculation works:")
        print("  • Each AS needs time to complete its measurements")
        print("  • We recommend 10 minutes per AS to avoid conflicts")
        print("  • Formula: Number of AS × 10 = Recommended frequency")
        print()
        print("  📈 Examples:")
        print("    2 AS → 20 minutes frequency")
        print("    4 AS → 40 minutes frequency") 
        print("    6 AS → 60 minutes frequency")

    def check_frequency_warning(self, config):
        """Check if current frequency needs adjustment and show warnings"""
        unique_ases = set(config.AS_FOLDER_MAP.keys()) | set(config.AS_TARGETS.keys())
        num_ases = len(unique_ases)
        recommended = num_ases * 10
        current = self.get_current_cron_frequency()
        
        if current is None:
            print_warning("No cron frequency currently set for scionpathml")
            self.explain_frequency_calculation()
            print_example(f"scionpathml -f {recommended}", "Set optimal frequency for your configuration")
            return
        
        if current < recommended:
            print_warning(f"Current frequency ({current} min) might be too aggressive!")
            print(f"  • You have {num_ases} AS(es) configured")
            print(f"  • Current frequency: {current} minutes")
            print(f"  • Recommended frequency: {recommended} minutes")
            print()
            print_info("🚨 Why this matters:")
            print("  • Too frequent execution can cause resource conflicts")
            print("  • Each AS measurement needs time to complete properly")
            print("  • Overlapping executions can produce unreliable results")
            print()
            print_example(f"scionpathml -f {recommended}", "Update to recommended frequency")

    def update_cron(self, frequency, path_override=None, config=None):
        """Update cron job with new frequency."""
        print_header(f"UPDATING CRON FREQUENCY TO {frequency} MINUTES")
        
        try:
            full_path = self.get_script_path(path_override)
        except EnvironmentError as e:
            print_error(str(e))
            return False
            
        if not os.path.isfile(full_path):
            print_error(f"Script not found at: {full_path}")
            print_info("Please check the path and try again")
            return False
        
        cron_line = f"*/{frequency} * * * * {full_path}"
        current_cron = self.read_crontab()
        
        # Remove existing entries to avoid duplicates
        existing_lines = [line for line in current_cron.splitlines() if "pipeline.sh" not in line]
        
        # Add new cron line
        existing_lines.append(cron_line)
        new_cron_content = "\n".join(existing_lines) + "\n"
        
        self.write_crontab(new_cron_content)
        
        print_success(f"Cron job updated successfully!")
        print(f"  • Frequency: Every {frequency} minutes")
        print(f"  • Script: {full_path}")
        print(f"  • Cron entry: {cron_line}")
        
        # Check if frequency is optimal
        if config:
            unique_ases = set(config.AS_FOLDER_MAP.keys()) | set(config.AS_TARGETS.keys())
            num_ases = len(unique_ases)
            recommended = num_ases * 10
            
            if frequency == recommended:
                print_success("🎯 Perfect! This frequency matches our recommendation.")
            elif frequency < recommended:
                print_warning(f"Consider using {recommended} minutes for {num_ases} AS(es)")
                self.explain_frequency_calculation()
            else:
                print_info(f"📊 This is more conservative than our {recommended}-minute recommendation")
                print("  • More conservative frequencies are generally safer")
                print("  • You can always decrease it later if needed")
        
        return True

    def stop_cron(self):
        """Remove scionpathml cron job"""
        print_header("STOPPING SCIONPATHML CRON JOB")
        
        current_cron = self.read_crontab()
        original_lines = current_cron.splitlines()
        remaining_lines = [line for line in original_lines if "pipeline.sh" not in line]
        
        removed_count = len(original_lines) - len(remaining_lines)
        
        if removed_count == 0:
            print_info("🔍 No active scionpathml cron jobs found")
            print("  • The cron job might already be stopped")
            print("  • Or it was never configured")
            print()
            print_example("scionpathml -f 30", "Start with 30-minute frequency")
            return
        
        self.write_crontab("\n".join(remaining_lines) + "\n" if remaining_lines else "")
        
        print_success(f"🛑 Removed {removed_count} cron job(s)")
        print("  • scionpathml is no longer scheduled to run automatically")
        print("  • You can still run it manually anytime")
        print()
        print_example("scionpathml -f 30", "Restart with 30-minute frequency")