#!/usr/bin/env python3
"""
CLI interface for SINTA Scraping Application

This module provides the command-line interface for the SINTA scraping application.
"""

import sys
import argparse
from .sinta_app import SintaScrapingApp
from .utils import Utils


def create_argument_parser():
    """Create command line argument parser"""
    parser = argparse.ArgumentParser(
        description='SINTA Scraping Application - CLI Version - Scrape data dari SINTA untuk berbagai kategori',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m web.cli                       # Scrape semua kategori
  python -m web.cli --buku                # Scrape hanya data buku
  python -m web.cli --haki                # Scrape hanya data HAKI
  python -m web.cli --publikasi           # Scrape semua publikasi
  python -m web.cli --publikasi-scopus    # Scrape hanya Scopus
  python -m web.cli --publikasi-gs        # Scrape hanya Google Scholar
  python -m web.cli --publikasi-wos       # Scrape hanya Web of Science
  python -m web.cli --penelitian          # Scrape hanya penelitian
  python -m web.cli --ppm                 # Scrape hanya PPM
  python -m web.cli --profil              # Scrape hanya profil
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


def main():
    """Main CLI entry point"""
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
    
    # If no specific category was specified, scrape all
    if not scrape_something:
        app.scrape_all()
    
    print("\n🎉 SINTA Scraping completed successfully!")
    print(f"📁 Check results in: {Utils.get_output_dir()}")


if __name__ == "__main__":
    main()
