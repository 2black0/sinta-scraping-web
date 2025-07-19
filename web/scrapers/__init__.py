#!/usr/bin/env python3
"""
Base scraper class and common scraping functionality

This module provides the base class for all SINTA scrapers.
"""

import csv
from abc import ABC, abstractmethod


class BaseScraper(ABC):
    """Base class for all SINTA scrapers"""
    
    def __init__(self, session_manager):
        """Initialize the scraper with a session manager"""
        self.session = session_manager
    
    @abstractmethod
    def scrape(self, author_id, author_name):
        """Scrape data for a specific author"""
        pass
    
    @abstractmethod
    def save_to_csv(self, data, filename):
        """Save scraped data to CSV file"""
        pass
    
    def get_pagination_total(self, soup):
        """Get total pages from pagination element"""
        pagination_elem = soup.find(class_='pagination-text')
        if pagination_elem:
            return int(pagination_elem.text.split('of')[-1].strip().split()[0])
        return 1
