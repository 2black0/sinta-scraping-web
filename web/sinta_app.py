#!/usr/bin/env python3
"""
Main SINTA Scraping Application

This module provides the main application class that orchestrates all scraping operations.
"""

import sys
from .session import SessionManager, LecturerManager
from .utils import Utils
from .scrapers.book_scraper import BookScraper
from .scrapers.haki_scraper import HakiScraper
from .scrapers.publication_scraper import PublicationScraper
from .scrapers.research_scraper import ResearchScraper
from .scrapers.community_service_scraper import CommunityServiceScraper
from .scrapers.profile_scraper import ProfileScraper


class SintaScrapingApp:
    """Main application class for SINTA scraping"""
    
    def __init__(self):
        self.session_manager = SessionManager()
        self.lecturer_manager = LecturerManager()
        self.scrapers = {
            'buku': BookScraper(self.session_manager),
            'haki': HakiScraper(self.session_manager),
            'publikasi': PublicationScraper(self.session_manager),
            'penelitian': ResearchScraper(self.session_manager),
            'ppm': CommunityServiceScraper(self.session_manager),
            'profil': ProfileScraper(self.session_manager)
        }
    
    def initialize(self):
        """Initialize the application"""
        print("🚀 SINTA Scraping Application")
        print("=" * 50)
        
        # Load lecturers
        if not self.lecturer_manager.load_lecturers():
            return False
        
        # Initialize session
        if not self.session_manager.initialize_session():
            return False
        
        # Ensure output directory exists
        Utils.ensure_output_dir()
        
        return True
    
    def scrape_buku(self):
        """Scrape book data for all lecturers"""
        print("\n📖 Scraping Book Data...")
        print("-" * 30)
        
        scraper = self.scrapers['buku']
        all_results = []
        
        for author_id, _ in self.lecturer_manager.get_lecturers():
            # Get real author name
            author_name = Utils.get_author_name(self.session_manager.session, author_id)
            print(f"👤 Processing: {author_name} (ID: {author_id})")
            results = scraper.scrape(author_id, author_name)
            all_results.extend(results)
            print(f"   ✅ Found {len(results)} books")
        
        # Save to CSV
        csv_filename = Utils.get_output_file("buku")
        scraper.save_to_csv(all_results, csv_filename)
        print(f"💾 Saved {len(all_results)} book records to {csv_filename}")
        return all_results
    
    def scrape_haki(self):
        """Scrape HAKI data for all lecturers"""
        print("\n🏛️ Scraping HAKI Data...")
        print("-" * 30)
        
        scraper = self.scrapers['haki']
        all_results = []
        
        for author_id, _ in self.lecturer_manager.get_lecturers():
            # Get real author name
            author_name = Utils.get_author_name(self.session_manager.session, author_id)
            print(f"👤 Processing: {author_name} (ID: {author_id})")
            results = scraper.scrape(author_id, author_name)
            all_results.extend(results)
            print(f"   ✅ Found {len(results)} HAKI records")
        
        # Save to CSV
        csv_filename = Utils.get_output_file("haki")
        scraper.save_to_csv(all_results, csv_filename)
        print(f"💾 Saved {len(all_results)} HAKI records to {csv_filename}")
        return all_results
    
    def scrape_publikasi(self, publication_types=None):
        """Scrape publication data for all lecturers"""
        if publication_types is None:
            publication_types = ['scopus', 'gs', 'wos']
        
        print(f"\n📚 Scraping Publication Data: {', '.join(publication_types)}")
        print("-" * 50)
        
        scraper = self.scrapers['publikasi']
        results_by_type = {}
        
        for pub_type in publication_types:
            print(f"\n📊 Processing {pub_type.upper()} publications...")
            all_results = []
            
            for author_id, _ in self.lecturer_manager.get_lecturers():
                # Get real author name
                author_name = Utils.get_author_name(self.session_manager.session, author_id)
                print(f"👤 Processing: {author_name} (ID: {author_id})")
                
                if pub_type == 'scopus':
                    results = scraper.scrape_scopus(author_id, author_name)
                elif pub_type == 'gs':
                    results = scraper.scrape_google_scholar(author_id, author_name)
                elif pub_type == 'wos':
                    results = scraper.scrape_wos(author_id, author_name)
                
                all_results.extend(results)
                print(f"   ✅ Found {len(results)} {pub_type.upper()} publications")
            
            # Save to CSV
            csv_filename = Utils.get_output_file(f"publikasi_{pub_type}")
            scraper.save_to_csv(all_results, csv_filename, pub_type)
            print(f"💾 Saved {len(all_results)} {pub_type.upper()} records to {csv_filename}")
            results_by_type[pub_type] = all_results
        
        return results_by_type
    
    def scrape_penelitian(self):
        """Scrape research data for all lecturers"""
        print("\n🔬 Scraping Research Data...")
        print("-" * 30)
        
        scraper = self.scrapers['penelitian']
        all_results = []
        
        for author_id, _ in self.lecturer_manager.get_lecturers():
            # Get real author name
            author_name = Utils.get_author_name(self.session_manager.session, author_id)
            print(f"👤 Processing: {author_name} (ID: {author_id})")
            results = scraper.scrape(author_id, author_name)
            all_results.extend(results)
            print(f"   ✅ Found {len(results)} research records")
        
        # Save to CSV
        csv_filename = Utils.get_output_file("penelitian")
        scraper.save_to_csv(all_results, csv_filename)
        print(f"💾 Saved {len(all_results)} research records to {csv_filename}")
        return all_results
    
    def scrape_ppm(self):
        """Scrape community service data for all lecturers"""
        print("\n🤝 Scraping Community Service Data...")
        print("-" * 40)
        
        scraper = self.scrapers['ppm']
        all_results = []
        
        for author_id, _ in self.lecturer_manager.get_lecturers():
            # Get real author name
            author_name = Utils.get_author_name(self.session_manager.session, author_id)
            print(f"👤 Processing: {author_name} (ID: {author_id})")
            results = scraper.scrape(author_id, author_name)
            all_results.extend(results)
            print(f"   ✅ Found {len(results)} community service records")
        
        # Save to CSV
        csv_filename = Utils.get_output_file("ppm")
        scraper.save_to_csv(all_results, csv_filename)
        print(f"💾 Saved {len(all_results)} community service records to {csv_filename}")
        return all_results
    
    def scrape_profil(self):
        """Scrape profile data for all lecturers"""
        print("\n👤 Scraping Profile Data...")
        print("-" * 30)
        
        scraper = self.scrapers['profil']
        all_results = []
        
        for author_id, _ in self.lecturer_manager.get_lecturers():
            # Get real author name
            author_name = Utils.get_author_name(self.session_manager.session, author_id)
            print(f"👤 Processing: {author_name} (ID: {author_id})")
            result = scraper.scrape(author_id, author_name)
            all_results.append(result)
            print(f"   ✅ Profile data collected")
        
        # Save to CSV
        csv_filename = Utils.get_output_file("profil")
        scraper.save_to_csv(all_results, csv_filename)
        print(f"💾 Saved {len(all_results)} profile records to {csv_filename}")
        return all_results
    
    def scrape_all(self):
        """Scrape all categories for all lecturers"""
        print("\n🎯 Scraping ALL Categories...")
        print("=" * 50)
        
        results = {}
        results['buku'] = self.scrape_buku()
        results['haki'] = self.scrape_haki()
        results['publikasi'] = self.scrape_publikasi()
        results['penelitian'] = self.scrape_penelitian()
        results['ppm'] = self.scrape_ppm()
        results['profil'] = self.scrape_profil()
        
        print("\n✅ All scraping completed successfully!")
        print(f"📁 Results saved in: {Utils.get_output_dir()}")
        return results
