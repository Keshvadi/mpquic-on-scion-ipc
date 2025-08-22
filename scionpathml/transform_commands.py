from transform_manager import TransformManager
from cli_utils import print_error, print_example, print_header, print_section, print_info, Colors
import sys

class TransformCommands:
    """Handle transformation CLI commands"""
    
    def __init__(self):
        self.manager = TransformManager()
        self.default_data_path = "Data/Archive"  # Default path from your folder structure
    
    def handle_transform_command(self, transform_type=None, output_dir=None):
        """Handle 'transform' command (uses default Data/Archive path)"""
        print_info(f"Using default data path: {self.default_data_path}")
        
        # Default to all transformations if no type specified
        if not transform_type:
            transform_type = "all"
        
        if transform_type.lower() == "all":
            return self.manager.run_all_transforms(self.default_data_path, output_dir)
        elif transform_type.lower() == "standard":
            return self.manager.run_standard_transform(self.default_data_path, output_dir)
        elif transform_type.lower() == "multipath":
            return self.manager.run_multipath_transform(self.default_data_path, output_dir)
        else:
            print_error(f"Invalid transformation type: {transform_type}")
            print_error("Valid types: all, standard, multipath")
            print()
            print_info("💡 Usage:")
            print_example("scionpathml transform", "Transform all data from Data/Archive")
            print_example("scionpathml transform standard", "Transform standard data only")
            print_example("scionpathml transform multipath", "Transform multipath data only")
            return False
    
    def handle_transform_data_command(self, data_path, transform_type=None, output_dir=None):
        """Handle 'transform-data' command (requires custom path)"""
        print(f"DEBUG: Received data_path = '{data_path}'")  # Debug line
        
        if not data_path:
            print_error("Missing data path")
            print()
            print_info("💡 Usage:")
            print_example("scionpathml transform-data /path/to/json/files", "Transform all data")
            print_example("scionpathml transform-data /path/to/json/files standard", "Standard only")
            print_example("scionpathml transform-data /path/to/json/files multipath", "Multipath only")
            print_example("scionpathml transform-data /path/to/json/files --output-dir /custom/output", "Custom output")
            print()
            print_info("💡 Or use the simple command:")
            print_example("scionpathml transform", "Transform from default Data/Archive path")
            return False
        
        # Default to all transformations if no type specified
        if not transform_type:
            transform_type = "all"
        
        if transform_type.lower() == "all":
            return self.manager.run_all_transforms(data_path, output_dir)
        elif transform_type.lower() == "standard":
            return self.manager.run_standard_transform(data_path, output_dir)
        elif transform_type.lower() == "multipath":
            return self.manager.run_multipath_transform(data_path, output_dir)
        else:
            print_error(f"Invalid transformation type: {transform_type}")
            print_error("Valid types: all, standard, multipath")
            return False
    
    def handle_transform_status_command(self, output_dir=None):
        """Handle 'transform-status' command"""
        self.manager.show_transform_status(output_dir)
    
    def handle_transform_help_command(self):
        """Handle 'transform-help' command"""
        self.show_transform_help()
    
    def show_transform_help(self):
        """Show transformation help"""
        print_header("DATA TRANSFORMATION HELP")
        
        print_section("🔄 TRANSFORMATION COMMANDS")
        print(f"{Colors.BOLD}Simple Commands (uses Data/Archive):{Colors.END}")
        print_example("scionpathml transform", "Transform all data from Data/Archive")
        print_example("scionpathml transform standard", "Standard transformation only")
        print_example("scionpathml transform multipath", "Multipath transformation only")
        
        print(f"\n{Colors.BOLD}Custom Path Commands:{Colors.END}")
        print_example("scionpathml transform-data /path/to/json", "Transform from custom path")
        print_example("scionpathml transform-data /path/to/json standard", "Standard from custom path")
        print_example("scionpathml transform-data /path/to/json multipath", "Multipath from custom path")
        
        print(f"\n{Colors.BOLD}Status Commands:{Colors.END}")
        print_example("scionpathml transform-status", "Show transformation status")
        
        print_section("📂 PATHS")
        print(f"{Colors.BOLD}Default data path:{Colors.END} Data/Archive")
        print(f"{Colors.BOLD}Default output path:{Colors.END} ./transformers/datasets")
        print()
        print_example("scionpathml transform --output-dir /custom/output", "Custom output with default data")
        print_example("scionpathml transform-data /custom/data --output-dir /custom/output", "Both custom")
        
        print_section("📊 WHAT GETS CREATED")
        print(f"{Colors.BOLD}Standard transformation creates:{Colors.END}")
        print("   📄 data_PG.csv - Ping measurements")
        print("   📄 data_BW.csv - Bandwidth measurements") 
        print("   📄 data_TR.csv - Traceroute measurements")
        print("   📄 data_SP.csv - Showpaths measurements")
        print("   📄 data_CP.csv - Path changes")
        
        print(f"\n{Colors.BOLD}Multipath transformation creates:{Colors.END}")
        print("   📄 data_PG-MP.csv - Multipath ping measurements")
        print("   📄 data_BW-MP.csv - Multipath bandwidth measurements")
        
    
    def show_transform_epilog_examples(self):
        """Return transformation examples for CLI epilog"""
        return f"""
{Colors.CYAN}Data Transformation:{Colors.END}
  scionpathml transform                              # Transform from Data/Archive (default)
  scionpathml transform standard                     # Standard transformation only
  scionpathml transform multipath                    # Multipath transformation only
  scionpathml transform-data /custom/path            # Transform from custom path
  scionpathml transform-status                       # Show transformation status
  scionpathml transform-help                         # Transformation help
        """
    
    def show_transform_no_args_section(self):
        """Return transformation section for no-arguments display"""
        return f"""
    print_section("🔄 TRANSFORM YOUR DATA")
    print_example("scionpathml transform", "Transform from Data/Archive (simple)")
    print_example("scionpathml transform-status", "Check transformation status")
    print_example("scionpathml transform-help", "Transformation guide")
        """

class TransformHelpDisplay:
    """Dedicated class for transformation help and documentation"""
    
    @staticmethod
    def show_transform_quick_reference():
        """Show quick transformation reference"""
        print_header("TRANSFORMATION QUICK REFERENCE")
        
        print_section("🚀 QUICK START")
        print("1. Transform your measurement data (simplest):")
        print_example("scionpathml transform", "Uses default Data/Archive path")
        
        print("\n2. Check the results:")
        print_example("scionpathml transform-status", "See generated CSV files")
        
        print("\n3. Transform specific types:")
        print_example("scionpathml transform standard", "Standard data only")
        print_example("scionpathml transform multipath", "Multipath data only")
        
        print("\n4. Custom paths (advanced):")
        print_example("scionpathml transform-data /custom/path", "Transform from custom location")
        
        print_section("💡 COMMON WORKFLOWS")
        
        print(f"{Colors.BOLD}Daily Data Processing:{Colors.END}")
        print_example("scionpathml transform", "Transform from Data/Archive")
        print_example("scionpathml transform-status", "Check what was created")
        
        print(f"\n{Colors.BOLD}Selective Processing:{Colors.END}")
        print_example("scionpathml transform standard", "Only standard measurements")
        print_example("scionpathml transform multipath", "Only multipath measurements")
        
        print(f"\n{Colors.BOLD}Analysis Projects:{Colors.END}")
        print_example("scionpathml transform-data /archive/week1 --output-dir /analysis/project1", "Week 1 analysis")
        
        print_section("🎯 PATHS & DEFAULTS")
        print("• Default data source: Data/Archive")
        print("• Default output: ./transformers/datasets")
        print("• Use 'transform' for defaults, 'transform-data' for custom paths")