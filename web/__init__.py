#!/usr/bin/env python3
"""
SINTA Scraping Web Package

Modular SINTA scraping application with web interface support.
"""

from .config import config, ConfigManager
from .utils import Utils
from .session import SessionManager, LecturerManager, SintaRequestLogin
from .sinta_app import SintaScrapingApp

# Import all scrapers
from .scrapers.book_scraper import BookScraper
from .scrapers.haki_scraper import HakiScraper
from .scrapers.publication_scraper import PublicationScraper
from .scrapers.research_scraper import ResearchScraper
from .scrapers.community_service_scraper import CommunityServiceScraper
from .scrapers.profile_scraper import ProfileScraper

__version__ = '2.0.0'
__author__ = 'SINTA Scraping Team'

__all__ = [
    # Core classes
    'SintaScrapingApp',
    'ConfigManager',
    'config',
    'Utils',
    
    # Session management
    'SessionManager',
    'LecturerManager', 
    'SintaRequestLogin',
    
    # Scrapers
    'BookScraper',
    'HakiScraper',
    'PublicationScraper',
    'ResearchScraper',
    'CommunityServiceScraper',
    'ProfileScraper'
]
