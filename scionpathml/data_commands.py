from data_manager import DataManager
from cli_utils import print_error, print_example, print_header, print_section, print_info, Colors
import sys
import os

class DataCommands:
    """Handle data management CLI commands"""
    
    def __init__(self):
        self.manager = DataManager()
    
    def handle_data_overview_command(self):
        """Handle 'data-overview' command"""
        self.manager.show_data_overview()
    
    def handle_data_show_command(self, directory_name=None, interactive=False):
        """Handle 'data-show' command with optional interactive mode"""
        if not directory_name:
            print_error("Missing directory name")
            print()
            print_info("💡 Usage:")
            print_example("scionpathml data-show Archive", "Show Archive directory details")
            print_example("scionpathml data-show Currently", "Show Currently directory details")
            print_example("scionpathml data-show History", "Show History directory details")
            print_example("scionpathml data-show /custom/path", "Show external directory details")
            print_example("scionpathml data-show Archive --interactive", "Browse Archive interactively")
            return False
        
        if interactive:
            return self.manager.interactive_directory_browser(directory_name)
        else:
            return self.manager.show_directory_details(directory_name)
    
    def handle_data_browse_command(self, directory_name=None):
        """Handle 'data-browse' command for interactive browsing"""
        if not directory_name:
            # Show all directories and let user choose
            return self.manager.interactive_main_browser()
        else:
            return self.manager.interactive_directory_browser(directory_name)
    
    # ... (rest of your existing methods remain the same)
    
    def handle_data_move_command(self, source_dir=None, dest_dir=None, category=None, no_confirm=False):
        """Handle 'data-move' command"""
        if not source_dir or not dest_dir:
            print_error("Missing source or destination directory")
            print()
            print_info("💡 Usage:")
            print_example("scionpathml data-move Archive Currently", "Move all Archive files to Currently")
            print_example("scionpathml data-move Archive /backup/data", "Move to external path")
            print_example("scionpathml data-move Archive History --category Bandwidth", "Move only Bandwidth files")
            print_example("scionpathml data-move Currently /external/backup --no-confirm", "Move without confirmation")
            return False
        
        if source_dir.lower() == dest_dir.lower() and dest_dir.lower() in ['archive', 'currently', 'history']:
            print_error("Source and destination directories cannot be the same")
            return False
        
        return self.manager.move_data(source_dir, dest_dir, category, confirm=not no_confirm)
    
    def handle_data_delete_command(self, directory_name=None, category=None, no_confirm=False):
        """Handle 'data-delete' command"""
        if not directory_name:
            print_error("Missing directory name")
            print()
            print_info("💡 Usage:")
            print_example("scionpathml data-delete Archive", "Delete all files in Archive")
            print_example("scionpathml data-delete Currently --category Bandwidth", "Delete only Bandwidth files")
            print_example("scionpathml data-delete History --no-confirm", "Delete without confirmation")
            print()
            print_info("⚠️  Use with caution - deleted files cannot be recovered!")
            return False
        
        return self.manager.delete_data(directory_name, category, confirm=not no_confirm)
    
    def handle_data_search_command(self, pattern=None, directory_name=None):
        """Handle 'data-search' command"""
        if not pattern:
            print_error("Missing search pattern")
            print()
            print_info("💡 Usage:")
            print_example("scionpathml data-search BW_2025", "Search for bandwidth files from 2025")
            print_example("scionpathml data-search AS-1 Archive", "Search in Archive for AS-1 files")
            print_example("scionpathml data-search 19-ffaa", "Search for specific AS files")
            print_example("scionpathml data-search prober /backup", "Search in external directory")
            return []
        
        return self.manager.search_files(pattern, directory_name)
    
    def handle_data_help_command(self):
        """Handle 'data-help' command"""
        self.show_data_help()
    
    def show_data_help(self):
        """Show data management help"""
        print_header("DATA MANAGEMENT HELP")
        
        print_section("📂 DATA STRUCTURE & FILE PATTERNS")
        print("Your measurement data follows these naming patterns:")
        print("   📊 Showpaths:        AS-1_2025-06-25T22:00_19-ffaa_0_1301.json")
        print("   📊 Bandwidth:        BW_2025-06-25T22:00_AS_16-ffaa_0_1001_5Mbps.json")
        print("   📊 Comparer:         delta_2025-06-25T22:00_19-ffaa_0_1301.json")
        print("   📊 Prober:           prober_2025-06-25T22:00_19-ffaa_0_1301.json")
        print("   📊 Traceroute:       TR_2025-06-25T22:00_AS_17-ffaa_0_1101_p_3.json")
        print("   📊 MP-Prober:        mp-prober_2025-06-25T22:00_18-ffaa_1_11e5.json")
        print("   📊 MP-Bandwidth: BW-P_2025-06-25T22-00-00_AS_19-ffaa_0_1303_50Mbps.json")
        
        print("\n📁 Directory Structure:")
        print("   📁 Data/Archive    - Main measurement data storage")
        print("   📁 Data/Currently  - Current/active measurements")
        print("   📁 Data/History    - Historical/archived measurements")
        
        print_section("🔍 VIEW COMMANDS")
        print_example("scionpathml data-overview", "Show overview of all directories")
        print_example("scionpathml data-show Archive", "Show detailed Archive contents")
        print_example("scionpathml data-show /backup/data", "Show external directory contents")
        print_example("scionpathml data-browse", "Interactive browser for all directories")
        print_example("scionpathml data-browse Archive", "Interactive browser for Archive")
        
        print_section("🔍 SEARCH COMMANDS")
        print_example("scionpathml data-search BW_2025", "Search for bandwidth files from 2025")
        print_example("scionpathml data-search 19-ffaa Archive", "Search Archive for AS 19-ffaa files")
        print_example("scionpathml data-search prober /backup", "Search in external directory")
        
        print_section("📦 MOVE COMMANDS")
        print("Internal moves (between Archive/Currently/History):")
        print_example("scionpathml data-move Archive History", "Move all Archive files to History")
        print_example("scionpathml data-move Currently Archive --category Bandwidth", "Move only Bandwidth files")
        
        print("\nExternal moves (to/from external paths):")
        print_example("scionpathml data-move Archive /backup/old-data", "Backup Archive to external path")
        print_example("scionpathml data-move /backup/data Currently", "Restore from external backup")  
        print_example("scionpathml data-move Archive /backup/analysis --category Traceroute", "Export Traceroute for analysis")
        print_example("scionpathml data-move Currently /external/backup --no-confirm", "Move without confirmation")
        
        print_section("🗑️ DELETE COMMANDS")
        print_example("scionpathml data-delete History", "Delete all files in History (with confirmation)")
        print_example("scionpathml data-delete Archive --category Comparer", "Delete only Comparer files")
        print_example("scionpathml data-delete Currently --no-confirm", "Delete without confirmation")
        
        print_section("💡 COMMON WORKFLOWS")
        print(f"{Colors.BOLD}Regular Maintenance:{Colors.END}")
        print_example("scionpathml data-overview", "Check current data status")
        print_example("scionpathml data-move Archive History", "Archive old data")
        print_example("scionpathml data-delete History --category MP-Bandwidth", "Clean up old parallel bandwidth data")
        
        print(f"\n{Colors.BOLD}Data Backup & Export:{Colors.END}")
        print_example("scionpathml data-move Archive /backup/$(date +%Y-%m)", "Monthly backup")
        print_example("scionpathml data-move Archive /analysis/project1 --category Bandwidth", "Export for analysis")
        print_example("scionpathml data-search BW_2025-01 | head -10", "Find January 2025 bandwidth data")
        
        print(f"\n{Colors.BOLD}Data Analysis Preparation:{Colors.END}")
        print_example("scionpathml data-show Archive", "See what data is available")
        print_example("scionpathml transform", "Transform Archive data to CSV")
        print_example("scionpathml data-move Archive /analysis/dataset1", "Export specific dataset")
        
        print(f"\n{Colors.BOLD}Finding Specific Measurements:{Colors.END}")
        print_example("scionpathml data-search AS-1_2025-01", "Find AS-1 showpaths from January")
        print_example("scionpathml data-search BW_2025-06 Currently", "Find June bandwidth in Currently")
        print_example("scionpathml data-search 19-ffaa_0_1301", "Find all data for specific AS")
        
        print_section("⚠️ SAFETY NOTES")
        print("• Move operations preserve directory structure and file patterns")
        print("• Delete operations cannot be undone - use with caution")
        print("• Use --no-confirm flag to skip confirmation prompts")
        print("• Search is case-insensitive and matches partial names")
        print("• Files are automatically categorized by their naming patterns")
        print("• External paths can be absolute (/backup/data) or relative (../backups)")
        print("• Empty directories are automatically cleaned up after moves/deletes")
        
        print_section("📋 FILE CATEGORIES RECOGNIZED")
        categories = self.manager.categories
        for i, category in enumerate(categories):
            print(f"   {i+1}. {category}")
    
    def show_data_epilog_examples(self):
        """Return data management examples for CLI epilog"""
        return f"""
{Colors.CYAN}Data Management:{Colors.END}
  scionpathml data-overview                    # Show overview of all data directories
  scionpathml data-show Archive               # Show Archive directory details
  scionpathml data-search BW_2025             # Search for bandwidth files from 2025
  scionpathml data-move Archive History       # Move Archive files to History
  scionpathml data-move Archive /backup/data  # Move Archive to external backup
  scionpathml data-delete History --category Prober  # Delete specific measurement type
  scionpathml data-help                       # Data management help
        """
    
    def show_data_no_args_section(self):
        """Return data management section for no-arguments display"""
        return f"""
    print_section("📂 MANAGE YOUR DATA")
    print_example("scionpathml data-overview", "See all your measurement data")
    print_example("scionpathml data-show Archive", "Show Archive directory details")
    print_example("scionpathml data-search BW_2025", "Search for specific files")
    print_example("scionpathml data-move Archive /backup", "Backup to external location")
    print_example("scionpathml data-help", "Data management guide")
        """

class DataHelpDisplay:
    """Dedicated class for data management help and documentation"""
    
    @staticmethod
    def show_data_quick_reference():
        """Show quick data management reference"""
        print_header("DATA MANAGEMENT QUICK REFERENCE")
        
        print_section("🚀 QUICK START")
        print("1. See what data you have:")
        print_example("scionpathml data-overview", "Overview of all directories")
        
        print("\n2. Look at specific directory:")
        print_example("scionpathml data-show Archive", "Detailed Archive view")
        
        print("\n3. Search for specific files:")
        print_example("scionpathml data-search BW_2025", "Find 2025 bandwidth measurements")
        
        print("\n4. Organize your data:")
        print_example("scionpathml data-move Archive History", "Archive old data")
        print_example("scionpathml data-move Archive /backup", "Backup to external location")
        
        print_section("📊 FILE TYPES RECOGNIZED")
        print("• Showpaths:        AS-1_2025-06-25T22:52_19-ffaa_0_1301.json")
        print("• Bandwidth:        BW_2025-06-26T18:45_AS_16-ffaa_0_1001_5Mbps.json")
        print("• Comparer:         delta_2025-06-26T18:45_19-ffaa_0_1301.json")
        print("• Prober:           prober_2025-06-26T18:45_19-ffaa_0_1301.json")
        print("• Traceroute:       TR_2025-06-26T18:12_AS_17-ffaa_0_1101_p_3.json")
        print("• MP-Prober:        mp-prober_2025-07-19T00:07_18-ffaa_1_11e5.json")
        print("• MP-Bandwidth: BW-P_2025-07-19T10-43-48_AS_19-ffaa_0_1303_50Mbps.json")
        
        print_section("📁 DIRECTORY STRUCTURE")
        print("• Archive   - Main measurement storage (used by transform command)")
        print("• Currently - Active/current measurements")
        print("• History   - Archived/historical data")
        
        print_section("💡 COMMON TASKS")
        print(f"{Colors.BOLD}Weekly Maintenance:{Colors.END}")
        print_example("scionpathml data-overview", "Check data status")
        print_example("scionpathml data-move Archive History", "Archive old measurements")
        
        print(f"\n{Colors.BOLD}Data Backup:{Colors.END}")
        print_example("scionpathml data-move Archive /backup/$(date +%Y-%m)", "Monthly backup")
        print_example("scionpathml data-move Currently /external/backup", "Backup current data")
        
        print(f"\n{Colors.BOLD}Analysis Preparation:{Colors.END}")
        print_example("scionpathml data-show Archive", "See available data")
        print_example("scionpathml transform", "Convert to CSV for analysis")
        print_example("scionpathml data-move Archive /analysis/project1", "Export for analysis")
        
        print_section("🎯 TIPS")
        print("• Always check data-overview first to understand your data")
        print("• Use data-search to find specific measurements quickly")
        print("• Files are automatically categorized by naming patterns")
        print("• External paths support both absolute and relative paths")
        print("• Transform command automatically uses Data/Archive")
        print("• Use --category to work with specific measurement types")
        print("• Use --no-confirm for automated scripts")