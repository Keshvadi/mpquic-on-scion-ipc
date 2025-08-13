import argparse
import sys
from command_manager import (
    show_pipeline_commands,
    update_pipeline_command, 
    enable_commands_by_category,
    disable_commands_by_category,
    enable_all_commands,
    disable_all_commands,
    get_available_command_names,
    get_available_categories,
    show_command_help
)
from log_commands import LogCommands, LogHelpDisplay
from cli_utils import *
from cron_manager import CronManager
from config_manager import ConfigManager
from help_manager import HelpManager
from transform_commands import TransformCommands
from data_commands import DataCommands, DataHelpDisplay

def main():
    # MINIMAL FIX: Handle transform-data with path before argparse
    if len(sys.argv) > 1 and sys.argv[1] == 'transform-data':
        if len(sys.argv) < 3:
            print_error("Missing data path for transform-data command")
            print_example("scionpathml transform-data /path/to/json", "Correct usage")
            sys.exit(1)
        
        data_path = sys.argv[2]
        transform_type = 'all'  # default
        output_dir = None
        
        # Parse optional arguments
        for i in range(3, len(sys.argv)):
            if sys.argv[i] == '--output-dir' and i + 1 < len(sys.argv):
                output_dir = sys.argv[i + 1]
            elif sys.argv[i] in ['standard', 'multipath', 'all'] and not sys.argv[i].startswith('--'):
                transform_type = sys.argv[i]
        
        # Initialize and run transform
        transform_commands = TransformCommands()
        transform_commands.handle_transform_data_command(data_path, transform_type, output_dir)
        sys.exit(0)

    # Initialize managers
    cron_manager = CronManager()
    config_manager = ConfigManager()
    help_manager = HelpManager()
    transform_commands = TransformCommands()
    data_commands = DataCommands()
    
    parser = argparse.ArgumentParser(
        prog="scionpathml",
        description=f"""
{Colors.BOLD}{Colors.BLUE}🧠 SCIONPATHML CLI{Colors.END}
{Colors.CYAN}Manage AS & Server Configuration + Pipeline Commands + Scheduling + Log Viewing{Colors.END}

{Colors.BOLD}Quick Examples:{Colors.END}
  {Colors.GREEN}scionpathml add-as -a 19-ffaa:1:11de -i 10.0.0.1 -n AS-1{Colors.END}
  {Colors.GREEN}scionpathml show-cmds{Colors.END}     (view/manage pipeline commands)
  {Colors.GREEN}scionpathml logs pipeline{Colors.END} (view pipeline.log)
  {Colors.GREEN}scionpathml transform{Colors.END}     (transform Data/Archive to CSV)
  {Colors.GREEN}scionpathml data-overview{Colors.END} (see all your measurement data)
  {Colors.GREEN}scionpathml data-browse{Colors.END}   (interactive data browser)
  {Colors.GREEN}scionpathml view-log bandwidth{Colors.END} (view first bandwidth file - script_duration.log)
  {Colors.GREEN}scionpathml logs pipeline --all{Colors.END} (view entire pipeline.log)
  {Colors.GREEN}scionpathml -f 40{Colors.END}         (set 40-minute frequency)
  {Colors.GREEN}scionpathml show{Colors.END}          (view full configuration)

Use {Colors.BOLD}scionpathml help{Colors.END} for comprehensive guide.
            """,
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=True,
        epilog=f"""
{Colors.BOLD}DETAILED EXAMPLES:{Colors.END}

{Colors.CYAN}Managing AS (Autonomous Systems):{Colors.END}
  scionpathml add-as -a 19-ffaa:1:11de -i 10.0.0.1 -n AS-Production
  scionpathml up-as -a 19-ffaa:1:11de -i 10.0.0.2 -n AS-Updated  
  scionpathml rm-as -a 19-ffaa:1:11de

{Colors.CYAN}Managing Servers:{Colors.END}
  scionpathml add-server -a 19-ffaa:1:22ef -i 10.0.0.50 -n TestServer
  scionpathml up-server -a 19-ffaa:1:22ef -i 10.0.0.51 -n NewTestServer
  scionpathml rm-server -a 19-ffaa:1:22ef

{Colors.CYAN}Pipeline Command Management:{Colors.END}
  scionpathml show-cmds                    # View all commands
  scionpathml disable-cmd -m bandwidth    # Disable bandwidth tests
  scionpathml enable-category -c tracing  # Enable all tracing commands
  scionpathml cmd-help                     # Comprehensive command guide*

{Colors.CYAN}Data Management:{Colors.END}
  scionpathml data-overview                    # Show overview of all data directories
  scionpathml data-show Archive               # Show Archive directory details
  scionpathml data-browse                     # Interactive data browser (all directories)
  scionpathml data-browse Archive             # Interactive browser for Archive
  scionpathml data-search BW_2025             # Search for bandwidth files from 2025
  scionpathml data-move Archive History       # Move Archive files to History
  scionpathml data-move Archive /backup/data  # Move Archive to external backup
  scionpathml data-delete History --category Prober  # Delete specific measurement type
  scionpathml data-help                       # Data management help

{Colors.CYAN}Log Management:{Colors.END}
  scionpathml logs                         # List all log categories
  scionpathml logs pipeline               # View pipeline.log (last 30 lines)
  scionpathml logs pipeline --all         # View entire pipeline.log
  scionpathml view-log bandwidth          # View FIRST bandwidth file (script_duration.log) - DEFAULT
  scionpathml view-log bandwidth latest   # View LATEST bandwidth file (highest numbered)
  scionpathml view-log bandwidth 1        # View bandwidth file #1 (last 50 lines)
  scionpathml view-log bandwidth 1 --all  # View complete bandwidth file #1
  scionpathml view-log pipeline --all     # View entire pipeline.log
  scionpathml log-help                     # Log viewing guide

{Colors.CYAN}Data Transformation:{Colors.END}
  scionpathml transform                              # Transform from Data/Archive (default)
  scionpathml transform standard                     # Standard transformation only
  scionpathml transform multipath                    # Multipath transformation only
  scionpathml transform-data /custom/path            # Transform from custom path
  scionpathml transform-status                       # Show transformation status
  scionpathml transform --output-dir /custom/output  # Custom output directory
  scionpathml transform-help                         # Transformation help

{Colors.CYAN}Frequency Management:{Colors.END}
  scionpathml -f 60        # Run every 60 minutes
  scionpathml stop         # Stop automatic execution
  scionpathml show         # Check current status

{Colors.YELLOW}💡 TIP: Use 'scionpathml show' to see your complete setup including logs status{Colors.END}
            """)

    parser.add_argument(
        'command',
        nargs='?',
        choices=[
            'stop', 'show', 'help',
            'add-as', 'add-server',
            'rm-as', 'rm-server', 
            'up-as', 'up-server',
            'show-cmds', 'enable-cmd', 'disable-cmd',           
            'enable-category', 'disable-category',                
            'enable-all-cmds', 'disable-all-cmds',                     
            'cmd-help',   
            'logs',      
            'view-log',
            'log-help',
            'transform',      
            'transform-status',    
            'transform-help',
            'data-overview', 
            'data-show',
            'data-browse',    # Add the new browse command
            'data-move', 
            'data-delete', 
            'data-search', 
            'data-help'                                     
        ],
        help="""
Command to execute:
  show        - Display current configuration and status
  stop        - Stop automatic execution (remove cron job)
  help        - Show comprehensive help guide
  add-as      - Add new Autonomous System
  add-server  - Add new bandwidth test server  
  rm-as       - Remove Autonomous System
  rm-server   - Remove bandwidth test server
  up-as       - Update existing Autonomous System
  up-server   - Update existing bandwidth test server
  logs        - View logs (pipeline, bandwidth, traceroute, etc.)
  view-log    - View specific log file
  log-help    - Quick log reference guide
  transform         - Transform data from Data/Archive (default)
  transform-status  - Show transformation status
  transform-help    - Transformation help guide
  data-overview     - Show overview of all data directories
  data-show         - Show detailed directory contents
  data-browse       - Interactive data browser
  data-move         - Move data between directories
  data-delete       - Delete data from directories
  data-search       - Search for files
  data-help         - Data management help
            """
    )
    
    # Arguments
    parser.add_argument("-m", type=str, help="Command module name (e.g., bandwidth, traceroute, prober)")
    parser.add_argument("-f", type=int, help="Set script frequency in minutes (e.g., 30 for every 30 minutes)")
    parser.add_argument("-p", type=str, help="Override path to runner directory containing pipeline.sh")
    parser.add_argument("-a", type=str, help="AS ID in format: number-ffaa:hex:hex (e.g., 19-ffaa:1:11de)")
    parser.add_argument("-i", type=str, help="IPv4 address (e.g., 192.168.1.100)")
    parser.add_argument("-n", type=str, help="Name for AS folder or server (alphanumeric + hyphens/underscores)")
    parser.add_argument("-c", type=str, help="Category name for commands (e.g., bandwidth, tracing)")
    parser.add_argument('log_category', nargs='?', help='Log category (pipeline, bandwidth, traceroute, etc.)')
    parser.add_argument('file_number', nargs='?', help='File number or "latest"')
    parser.add_argument('--log-dir', type=str, default="Data/Logs/", help='Log directory path')
    parser.add_argument('--all', action='store_true', help='Show entire log file instead of just last lines')
    parser.add_argument('--interactive', action='store_true', help='Enable interactive mode for data commands')
    parser.add_argument('--output-dir', type=str, help='Custom output directory for CSV files')
    parser.add_argument('--category', type=str, help='Category for data operations (Bandwidth, Traceroute, etc.)')
    parser.add_argument('--no-confirm', action='store_true', help='Skip confirmation prompts')

    # Handle no arguments
    if len(sys.argv) == 1:
        help_manager.show_welcome()
        sys.exit(0)

    # Parse arguments
    args = parser.parse_args()
    
    # Initialize log commands
    log_commands = LogCommands(args.log_dir)

    # Handle help command
    if args.command == "help":
        help_manager.show_help()
        sys.exit(0)

    # Load configuration for commands that need it
    config = None
    if args.command in ['show', 'add-as', 'add-server', 'rm-as', 'rm-server', 'up-as', 'up-server'] or args.f:
        config = load_config()
        if not config and args.command != 'show':
            sys.exit(1)

    # Command handlers
    if args.command == "stop":
        cron_manager.stop_cron()
        
    elif args.command == "show":
        config_manager.show_config(cron_manager)
        
    elif args.command == "add-as":
        if not (args.a and args.i and args.n):
            print_error("Missing required parameters for add-as")
            print_info("Required: AS ID (-a), IP address (-i), and name (-n)")
            print_example("scionpathml add-as -a 19-ffaa:1:11de -i 192.168.1.100 -n MyAS", "Complete example")
            sys.exit(1)
        
        if config_manager.add_as(args.a, args.i, args.n):
            cron_manager.check_frequency_warning(load_config())
        
    elif args.command == "add-server":
        if not (args.a and args.i and args.n):
            print_error("Missing required parameters for add-server")
            print_info("Required: AS ID (-a), IP address (-i), and name (-n)")
            print_example("scionpathml add-server -a 19-ffaa:1:22ef -i 10.0.0.50 -n TestServer", "Complete example")
            sys.exit(1)
        
        if config_manager.add_server(args.a, args.i, args.n):
            cron_manager.check_frequency_warning(load_config())
        
    elif args.command == "rm-as":
        if not args.a:
            print_error("Missing AS ID parameter")
            print_example("scionpathml rm-as -a 19-ffaa:1:11de", "Remove specific AS")
            sys.exit(1)
        
        if config_manager.remove_as(args.a):
            cron_manager.check_frequency_warning(load_config())
        
    elif args.command == "rm-server":
        if not args.a:
            print_error("Missing server ID parameter")
            print_example("scionpathml rm-server -a 19-ffaa:1:22ef", "Remove specific server")
            sys.exit(1)
        
        config_manager.remove_server(args.a)
        
    elif args.command == "up-as":
        if not (args.a and args.i and args.n):
            print_error("Missing required parameters for up-as")
            print_info("Required: AS ID (-a), IP address (-i), and name (-n)")
            print_example("scionpathml up-as -a 19-ffaa:1:11de -i 192.168.1.101 -n UpdatedAS", "Complete example")
            sys.exit(1)
        
        if config_manager.update_as(args.a, args.i, args.n):
            cron_manager.check_frequency_warning(load_config())
        
    elif args.command == "up-server":
        if not (args.a and args.i and args.n):
            print_error("Missing required parameters for up-server")
            print_info("Required: Server ID (-a), IP address (-i), and name (-n)")
            print_example("scionpathml up-server -a 19-ffaa:1:22ef -i 10.0.0.51 -n UpdatedServer", "Complete example")
            sys.exit(1)
        
        config_manager.update_server(args.a, args.i, args.n)

    # Pipeline command management
    elif args.command == "show-cmds":
        show_pipeline_commands()
        
    elif args.command == "enable-cmd":
        if not args.m:
            print_error("Missing command name (-m)")
            print_info("Available commands:")
            for cmd in get_available_command_names():
                print(f"  • {cmd}")
            print_example("scionpathml enable-cmd -m bandwidth", "Enable bandwidth command")
            sys.exit(1)
        update_pipeline_command(args.m, True)
        
    elif args.command == "disable-cmd":
        if not args.m:
            print_error("Missing command name (-m)")
            print_info("Available commands:")
            for cmd in get_available_command_names():
                print(f"  • {cmd}")
            print_example("scionpathml disable-cmd -m traceroute", "Disable traceroute command")
            sys.exit(1)
        update_pipeline_command(args.m, False)
        
    elif args.command == "enable-category":
        if not args.c:
            print_error("Missing category name (-c)")
            print_info("Available categories:")
            for cat in get_available_categories():
                print(f"  • {cat}")
            print_example("scionpathml enable-category -c bandwidth", "Enable all bandwidth commands")
            sys.exit(1)
        enable_commands_by_category(args.c)
        
    elif args.command == "disable-category":
        if not args.c:
            print_error("Missing category name (-c)")
            print_info("Available categories:")
            for cat in get_available_categories():
                print(f"  • {cat}")
            print_example("scionpathml disable-category -c probing", "Disable all probing commands")
            sys.exit(1)
        disable_commands_by_category(args.c)
        
    elif args.command == "enable-all-cmds":
        enable_all_commands()
        
    elif args.command == "disable-all-cmds":
        disable_all_commands()
        
    elif args.command == "cmd-help":
        show_command_help()   

    # Log management
    elif args.command == "logs":
        log_commands.handle_logs_command(args.log_category, show_all=args.all)
    
    elif args.command == "view-log":
        file_selector = args.file_number
        log_commands.handle_view_log_command(args.log_category, file_selector, args.all)   
        
    elif args.command == "log-help":
        LogHelpDisplay.show_log_quick_reference()
        
    # Transform management
    elif args.command == "transform":
        # Simple transform command using default Data/Archive path
        # Parse transform type from positional args if available
        transform_type = None
        if hasattr(args, 'log_category') and args.log_category in ['standard', 'multipath', 'all']:
            transform_type = args.log_category
        transform_commands.handle_transform_command(transform_type, args.output_dir)

    elif args.command == "transform-status":
        transform_commands.handle_transform_status_command(args.output_dir)
        
    elif args.command == "transform-help":
        transform_commands.handle_transform_help_command()
        
    # Data management commands
    elif args.command == "data-overview":
        data_commands.handle_data_overview_command()

    elif args.command == "data-show":
        # Handle --interactive flag for data-show
        data_commands.handle_data_show_command(args.log_category, interactive=args.interactive)

    elif args.command == "data-browse":
        # New interactive browse command
        data_commands.handle_data_browse_command(args.log_category)

    elif args.command == "data-move":
        source = args.log_category
        dest = args.file_number
        data_commands.handle_data_move_command(source, dest, args.category, args.no_confirm)

    elif args.command == "data-delete":
        data_commands.handle_data_delete_command(args.log_category, args.category, args.no_confirm)

    elif args.command == "data-search":
        pattern = args.log_category
        directory = args.file_number
        data_commands.handle_data_search_command(pattern, directory)

    elif args.command == "data-help":
        data_commands.handle_data_help_command()

    # Frequency management
    elif args.f:
        try:
            if cron_manager.update_cron(args.f, args.p, config):
                print()
                print_info("🔄 Next steps:")
                print_example("scionpathml show", "Check your configuration")
                print_example("crontab -l", "View all your cron jobs")
        except EnvironmentError as e:
            print_error(str(e))
            sys.exit(1)
            
    else:
        print_header("SCIONPATHML CLI")
        print_error("No valid command or option provided")
        print()
        print_info("🚀 Quick start options:")
        print_example("scionpathml show", "View current configuration")
        print_example("scionpathml help", "See comprehensive guide") 
        print_example("scionpathml -h", "View quick command reference")
        print()
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
