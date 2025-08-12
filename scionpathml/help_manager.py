from cli_utils import *

class HelpManager:
    @staticmethod
    def show_help():
        """Show comprehensive help with examples"""
        print_header("SCIONPATHML CLI - COMPREHENSIVE GUIDE")
        
        print_section("🚀 QUICK START")
        print("1. First, add an AS:")
        print_example("scionpathml add-as -a 19-ffaa:1:11de -i 192.168.1.100 -n MyAS", 
                     "Add your first Autonomous System")
        
        print("\n2. Add a bandwidth test server:")
        print_example("scionpathml add-server -a 19-ffaa:1:22ef -i 10.0.0.50 -n TestServer", 
                     "Add your first test server")
        
        print("\n3. Configure which commands to run:")
        print_example("scionpathml show-cmds", "View available pipeline commands")
        print_example("scionpathml disable-cmd -m bandwidth", "Skip bandwidth tests (optional)")
        
        print("\n4. Set execution frequency:")
        print_example("scionpathml -f 40", 
                     "Run every 40 minutes (recommended for 4 AS)")
        
        print("\n5. Check your configuration:")
        print_example("scionpathml show", 
                     "View current setup and status")
        
        print("\n6. Check your measurement data:")
        print_example("scionpathml data-overview", 
                     "See all your measurement data")
                     
        
        print_section("📋 ALL COMMANDS")
        
        print(f"{Colors.BOLD}Configuration Management:{Colors.END}")
        print_example("scionpathml add-as -a <AS_ID> -i <IP> -n <NAME>", "Add new AS")
        print_example("scionpathml add-server -a <AS_ID> -i <IP> -n <NAME>", "Add new server")
        print_example("scionpathml up-as -a <AS_ID> -i <IP> -n <NAME>", "Update existing AS")
        print_example("scionpathml up-server -a <AS_ID> -i <IP> -n <NAME>", "Update existing server")
        print_example("scionpathml rm-as -a <AS_ID>", "Remove AS")
        print_example("scionpathml rm-server -a <AS_ID>", "Remove server")
        
        print(f"\n{Colors.BOLD}Pipeline Command Management:{Colors.END}")
        print_example("scionpathml show-cmds", "View all pipeline commands and status")
        print_example("scionpathml enable-cmd -m <COMMAND>", "Enable specific command")
        print_example("scionpathml disable-cmd -m <COMMAND>", "Disable specific command")
        print_example("scionpathml enable-category -c <CATEGORY>", "Enable command category")
        print_example("scionpathml disable-category -c <CATEGORY>", "Disable command category")
        print_example("scionpathml enable-all-cmds", "Enable all commands")
        print_example("scionpathml disable-all-cmds", "Disable all commands")
        print_example("scionpathml cmd-help", "Comprehensive command management guide")
        
        print(f"\n{Colors.BOLD}Log Management:{Colors.END}")
        print_example("scionpathml logs", "Show all available logs")
        print_example("scionpathml logs pipeline", "View pipeline.log")
        print_example("scionpathml logs bandwidth", "List bandwidth log files")
        print_example("scionpathml view-log pipeline", "View pipeline.log")
        print_example("scionpathml view-log bandwidth 1", "View bandwidth file #1")
        print_example("scionpathml view-log traceroute latest --all", "View complete traceroute")
        print_example("scionpathml log-help", "Log management help guide")
        
        print(f"\n{Colors.BOLD}Data Transformation:{Colors.END}")
        print_example("scionpathml transform", "Transform Data/Archive to CSV (simple)")
        print_example("scionpathml transform standard", "Transform standard data only")
        print_example("scionpathml transform multipath", "Transform multipath data only")
        print_example("scionpathml transform-data /custom/path", "Transform from custom path")
        print_example("scionpathml transform-status", "Show transformation status")
        print_example("scionpathml transform-help", "Transformation help guide")
        
        print(f"\n{Colors.BOLD}Data Management:{Colors.END}")
        print_example("scionpathml data-overview", "Show overview of all data directories")
        print_example("scionpathml data-show Archive", "Show detailed Archive contents")
        print_example("scionpathml data-search BW_2025", "Search for bandwidth files from 2025")
        print_example("scionpathml data-move Archive History", "Move Archive files to History")
        print_example("scionpathml data-move Archive /backup", "Move Archive to external backup")
        print_example("scionpathml data-delete History --category Prober", "Delete specific measurement type")
        print_example("scionpathml data-help", "Data management help guide")
        
        print(f"\n{Colors.BOLD}Scheduling:{Colors.END}")
        print_example("scionpathml -f <MINUTES>", "Set execution frequency")
        print_example("scionpathml stop", "Stop automatic execution")
        print_example("scionpathml show", "View configuration & status")
        
        print_section("📝 PARAMETER FORMATS")
        
        print(f"{Colors.BOLD}AS ID Format:{Colors.END}")
        print("  • Pattern: number-ffaa:hex:hex")
        print("  • Example: 19-ffaa:1:11de")
        print("  • Example: 64-ffaa:0:110")
        
        print(f"\n{Colors.BOLD}IP Address:{Colors.END}")
        print("  • Must be valid IPv4")
        print("  • Example: 192.168.1.100")
        print("  • Example: 10.0.0.50")
        
        print(f"\n{Colors.BOLD}Names:{Colors.END}")
        print("  • Alphanumeric + hyphens/underscores only")
        print("  • Max 50 characters")
        print("  • Examples: MyAS, test-server-1, AS_Production")
        
        print(f"\n{Colors.BOLD}Command Names (-m):{Colors.END}")
        print("  • pathdiscovery, comparer, prober, mp-prober")
        print("  • traceroute, bandwidth, mp-bandwidth")
        
        print(f"\n{Colors.BOLD}Command Categories (-c):{Colors.END}")
        print("  • discovery, analysis, probing, tracing, bandwidth")
        
        print(f"\n{Colors.BOLD}Data Categories (--category):{Colors.END}")
        print("  • Showpaths, Bandwidth, Comparer, Prober")
        print("  • Traceroute, MP-Prober, BandwidthParallel")
        
        print_section("📊 DATA FILE PATTERNS")
        print("Your measurement data follows these naming patterns:")
        print("  📊 Showpaths:        AS-1_2025-06-25T22:52_19-ffaa_0_1301.json")
        print("  📊 Bandwidth:        BW_2025-06-26T18:45_AS_16-ffaa_0_1001_5Mbps.json")
        print("  📊 Comparer:         delta_2025-06-26T18:45_19-ffaa_0_1301.json")
        print("  📊 Prober:           prober_2025-06-26T18:45_19-ffaa_0_1301.json")
        print("  📊 Traceroute:       TR_2025-06-26T18:12_AS_17-ffaa_0_1101_p_3.json")
        print("  📊 MP-Prober:        mp-prober_2025-07-19T00:07_18-ffaa_1_11e5.json")
        print("  📊 BandwidthParallel: BW-P_2025-07-19T10-43-48_AS_19-ffaa_0_1303_50Mbps.json")
        
        print_section("⏱️ FREQUENCY RECOMMENDATIONS")
        print_info("💡 How frequency calculation works:")
        print("  • Each AS needs time to complete its measurements")
        print("  • We recommend 10 minutes per AS to avoid conflicts")
        print("  • Formula: Number of AS × 10 = Recommended frequency")
        print()
        print("  📈 Examples:")
        print("    2 AS → 20 minutes frequency")
        print("    4 AS → 40 minutes frequency") 
        print("    6 AS → 60 minutes frequency")
        
        print_section("⚙️ COMMAND MANAGEMENT TIPS")
        
        print(f"{Colors.BOLD}Performance Optimization:{Colors.END}")
        print("• Bandwidth commands are resource-intensive - disable if not needed")
        print("• Running fewer commands = faster pipeline execution")
        print("• Consider your network capacity when enabling bandwidth tests")
        
        print(f"\n{Colors.BOLD}Common Scenarios:{Colors.END}")
        print_example("scionpathml disable-category -c bandwidth", "Skip all bandwidth tests")
        print_example("scionpathml disable-all-cmds && scionpathml enable-cmd -m traceroute", "Only traceroute")
        print_example("scionpathml enable-all-cmds", "Full measurement suite")

        print_section("📋 LOG VIEWING")
        
        print(f"{Colors.BOLD}Basic Log Commands:{Colors.END}")
        print_example("scionpathml logs", "Show all available logs")
        print_example("scionpathml logs pipeline", "View pipeline.log (last 30 lines)")
        print_example("scionpathml logs bandwidth", "List bandwidth log files")
        print_example("scionpathml logs traceroute", "List traceroute log files")
        
        print(f"\n{Colors.BOLD}View Specific Files:{Colors.END}")
        print_example("scionpathml view-log pipeline", "View pipeline.log (last 50 lines)")
        print_example("scionpathml view-log bandwidth 1", "View bandwidth file #1")
        print_example("scionpathml view-log traceroute latest", "View latest traceroute")
        print_example("scionpathml view-log prober 3", "View prober file #3")
        
        print(f"\n{Colors.BOLD}View Complete Files:{Colors.END}")
        print_example("scionpathml view-log pipeline --all", "View entire pipeline.log")
        print_example("scionpathml view-log bandwidth 1 --all", "View complete bandwidth file")
        print_example("scionpathml view-log traceroute latest --all", "View complete traceroute")
        
        print_section("🔄 DATA TRANSFORMATION & MANAGEMENT")
        
        print(f"{Colors.BOLD}Transform Data to CSV:{Colors.END}")
        print_example("scionpathml transform", "Transform Data/Archive to CSV (simplest)")
        print_example("scionpathml transform standard", "Transform standard measurements only")
        print_example("scionpathml transform-data /custom/path", "Transform from custom location")
        print_example("scionpathml transform-status", "Check transformation results")
        
        print(f"\n{Colors.BOLD}Manage Your Data:{Colors.END}")
        print_example("scionpathml data-overview", "See all your measurement data")
        print_example("scionpathml data-show Archive", "Detailed view of Archive directory")
        print_example("scionpathml data-search BW_2025", "Find bandwidth files from 2025")
        
        print(f"\n{Colors.BOLD}Move and Organize Data:{Colors.END}")
        print_example("scionpathml data-move Archive History", "Archive old measurements")
        print_example("scionpathml data-move Archive /backup/data", "Backup to external location")
        print_example("scionpathml data-move Archive History --category Bandwidth", "Move specific data type")
        
        print(f"\n{Colors.BOLD}Clean Up Data:{Colors.END}")
        print_example("scionpathml data-delete History", "Delete old archived data")
        print_example("scionpathml data-delete Archive --category Comparer", "Delete specific data type")
        
        print_section("🔧 TROUBLESHOOTING")
        
        print(f"{Colors.BOLD}Script Path Issues:{Colors.END}")
        print("If you get script path errors:")
        print_example("export SCRIPT_PATH=/path/to/runner", "Set environment variable")
        print_example("scionpathml -f 30 -p /path/to/runner", "Use manual path override")
        
        print(f"\n{Colors.BOLD}Configuration Issues:{Colors.END}")
        print("• Make sure you're in the correct directory")
        print("• Check that ./collector/config.py exists")
        print("• Verify file permissions")
        
        print(f"\n{Colors.BOLD}Command Management Issues:{Colors.END}")
        print("• Use 'scionpathml show-cmds' to verify command status")
        print("• Check pipeline logs if enabled commands aren't running")
        print("• Ensure script files exist for enabled commands")
        
        print(f"\n{Colors.BOLD}Log Issues:{Colors.END}")
        print("• If logs directory not found:")
        print_example("scionpathml logs --log-dir /path/to/logs", "Use custom log directory")
        print("• If no log files in category:")
        print("  - Check if measurements are running")
        print("  - Verify log directory permissions")
        print("  - Ensure pipeline has executed at least once")
        
        print(f"\n{Colors.BOLD}Data Management Issues:{Colors.END}")
        print("• If 'No JSON files found': Check the data path contains .json files")
        print("• If permission denied: Check write permissions in destination directory")
        print("• If move fails: Ensure destination path is accessible")
        print("• Files are automatically categorized by naming patterns")
        
        print(f"\n{Colors.BOLD}Transformation Issues:{Colors.END}")
        print("• If transformation scripts not found: Ensure they're in transformers/ directory")
        print("• If 'No JSON files found': Check Data/Archive contains measurement files")
        print("• Default transformation uses Data/Archive automatically")
        
        print(f"\n{Colors.BOLD}Cron Issues:{Colors.END}")
        print("• Check cron service is running: systemctl status cron")
        print("• View cron logs: tail -f /var/log/cron")
        print("• Test manually first before scheduling")

    @staticmethod
    def show_welcome():
        """Show welcome message when no arguments provided"""
        print_header("WELCOME TO SCIONPATHML CLI")
        print_info("No command specified. Here are your options:")
        print()
        print_section("📚 LEARN & GET HELP")
        print_example("scionpathml help", "See comprehensive guide")
        print_example("scionpathml cmd-help", "Learn about command management")
        print_example("scionpathml log-help", "Quick log reference guide")
        print_example("scionpathml -h", "View quick command reference")
        print()
        print_section("📊 VIEW YOUR SETUP")
        print_example("scionpathml show", "View your current configuration")
        print_example("scionpathml show-cmds", "View pipeline commands status")
        print()
        print_section("📂 MANAGE YOUR DATA")
        print_example("scionpathml data-overview", "See all your measurement data")
        print_example("scionpathml data-show Archive", "Show Archive directory details")
        print_example("scionpathml data-search BW_2025", "Search for specific files")
        print_example("scionpathml data-move Archive /backup", "Backup to external location")
        print_example("scionpathml data-help", "Data management guide")   
        print()
        print_section("🔄 TRANSFORM YOUR DATA")
        print_example("scionpathml transform", "Transform Data/Archive to CSV (simple)")
        print_example("scionpathml transform-status", "Check transformation status")
        print_example("scionpathml transform-data --data-path /custom/path", "Transform custom path (advanced)")
        print_example("scionpathml transform-help", "Transformation guide")
        print()
        print_section("📋 VIEW YOUR LOGS")
        print_example("scionpathml logs", "See available log categories")
        print_example("scionpathml logs pipeline", "Quick view of pipeline.log")
        print_example("scionpathml view-log pipeline --all", "View complete pipeline.log")
        print_example("scionpathml logs bandwidth", "Browse bandwidth logs")
        print()
        print_info("💡 New to SCIONPATHML? Start with 'scionpathml help' for a complete guide!")

        