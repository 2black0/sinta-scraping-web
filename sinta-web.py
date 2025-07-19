#!/usr/bin/env python3
"""
SINTA Scraping Web Interface
Launcher script untuk web interface dan CLI modular
"""

import sys
import subprocess
import argparse
from pathlib import Path

# Add the web package to the path
sys.path.insert(0, str(Path(__file__).parent))

from web.sinta_app import SintaScrapingApp
from web.utils import Utils


def create_argument_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='SINTA Scraping Application - Scrape data dari SINTA untuk berbagai kategori',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sinta-web.py                             # Launch web interface
  python sinta-web.py --buku                      # Scrape hanya data buku
  python sinta-web.py --haki                      # Scrape hanya data HAKI
  python sinta-web.py --publikasi                 # Scrape semua publikasi
  python sinta-web.py --publikasi-scopus          # Scrape hanya Scopus
  python sinta-web.py --publikasi-gs              # Scrape hanya Google Scholar
  python sinta-web.py --publikasi-wos             # Scrape hanya Web of Science
  python sinta-web.py --penelitian                # Scrape hanya penelitian
  python sinta-web.py --ppm                       # Scrape hanya PPM
  python sinta-web.py --profil                    # Scrape hanya profil
        """
    )
    
    # Category arguments
    parser.add_argument('--buku', action='store_true', help='Scrape data buku')
    parser.add_argument('--haki', action='store_true', help='Scrape data HAKI')
    parser.add_argument('--publikasi', action='store_true', help='Scrape semua publikasi (Scopus, Google Scholar, WoS)')
    parser.add_argument('--publikasi-scopus', action='store_true', help='Scrape publikasi Scopus saja')
    parser.add_argument('--publikasi-gs', action='store_true', help='Scrape publikasi Google Scholar saja')
    parser.add_argument('--publikasi-wos', action='store_true', help='Scrape publikasi Web of Science saja')
    parser.add_argument('--penelitian', action='store_true', help='Scrape data penelitian')
    parser.add_argument('--ppm', action='store_true', help='Scrape data pengabdian masyarakat')
    parser.add_argument('--profil', action='store_true', help='Scrape data profil dosen')
    
    # Additional options
    parser.add_argument('--force-login', action='store_true', help='Force new login (ignore saved session)')
    parser.add_argument('--config', default='dosen.txt', help='Path to lecturer configuration file (default: dosen.txt)')
    
    return parser


def run_cli():
    """Run CLI interface"""
    parser = create_argument_parser()
    args = parser.parse_args()
    
    # Create the application instance
    app = SintaScrapingApp()
    
    # Set lecturer config file if specified
    if args.config != 'dosen.txt':
        app.lecturer_manager.config_file = args.config
    
    # Initialize the application
    if not app.initialize():
        print("❌ Failed to initialize application")
        sys.exit(1)
    
    # Force new login if requested
    if args.force_login:
        app.session_manager.initialize_session(force_new_login=True)
    
    # Determine what to scrape based on arguments
    scrape_something = False
    
    if args.buku:
        app.scrape_buku()
        scrape_something = True
    
    if args.haki:
        app.scrape_haki()
        scrape_something = True
    
    if args.publikasi:
        app.scrape_publikasi()
        scrape_something = True
    
    if args.publikasi_scopus:
        app.scrape_publikasi(['scopus'])
        scrape_something = True
    
    if args.publikasi_gs:
        app.scrape_publikasi(['gs'])
        scrape_something = True
    
    if args.publikasi_wos:
        app.scrape_publikasi(['wos'])
        scrape_something = True
    
    if args.penelitian:
        app.scrape_penelitian()
        scrape_something = True
    
    if args.ppm:
        app.scrape_ppm()
        scrape_something = True
    
    if args.profil:
        app.scrape_profil()
        scrape_something = True
    
    # If no specific category was specified, launch web interface
    if not scrape_something:
        launch_web_interface()
    else:
        print("\n🎉 SINTA Scraping completed successfully!")
        print(f"📁 Check results in: {Utils.get_output_dir()}")


def launch_web_interface():
    """Launch the web interface"""
    print("🚀 Starting SINTA Scraper Web Interface...")
    
    # Get the web directory path
    project_root = Path(__file__).parent
    web_dir = project_root / 'web'
    
    if not web_dir.exists():
        print("❌ Error: Web directory not found!")
        print(f"   Expected location: {web_dir}")
        sys.exit(1)
    
    # Run the web interface launcher
    launcher_script = web_dir / 'run.py'
    
    if not launcher_script.exists():
        print("❌ Error: Web launcher script not found!")
        print(f"   Expected location: {launcher_script}")
        sys.exit(1)
    
    try:
        subprocess.run([sys.executable, str(launcher_script)], cwd=web_dir)
    except KeyboardInterrupt:
        print("\n👋 Web interface stopped")
    except Exception as e:
        print(f"❌ Error running web interface: {e}")
        sys.exit(1)


def main():
    """Main entry point"""
    # Check if any CLI arguments are provided
    if len(sys.argv) > 1:
        # Run CLI interface
        run_cli()
    else:
        # Launch web interface by default
        launch_web_interface()


if __name__ == "__main__":
    main()
