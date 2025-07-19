#!/usr/bin/env python3
"""
Utility functions for the SINTA scraping application

This module provides common utility functions used across the application.
"""

import os
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup
from .config import config


class Utils:
    """Utility functions for the scraping application"""
    
    @staticmethod
    def get_output_dir():
        """Get output directory name with current date"""
        today = datetime.now()
        
        # Get date format from config with type safety
        date_format_val = config.get('output.date_format', '%d%m%Y')
        date_format = str(date_format_val) if date_format_val is not None else '%d%m%Y'
        date_str = today.strftime(date_format)
        
        # Get directory format from config with type safety
        directory_format_val = config.get('output.directory_format', 'output-{date}')
        directory_format = str(directory_format_val) if directory_format_val is not None else 'output-{date}'
        return directory_format.format(date=date_str)
    
    @staticmethod
    def ensure_output_dir():
        """Create output directory if it doesn't exist"""
        # Get project root directory (parent of web directory)
        current_dir = Path(__file__).parent  # web directory
        project_root = current_dir.parent    # project root
        
        output_dir_name = Utils.get_output_dir()
        output_dir = project_root / output_dir_name
        
        if not output_dir.exists():
            output_dir.mkdir(parents=True, exist_ok=True)
            print(f"📁 Created output directory: {output_dir}")
        else:
            print(f"📁 Using existing output directory: {output_dir}")
        return str(output_dir)
    
    @staticmethod
    def get_output_file(filename_base):
        """Get full output file path"""
        # Get project root directory (parent of web directory)
        current_dir = Path(__file__).parent  # web directory
        project_root = current_dir.parent    # project root
        
        output_dir_name = Utils.get_output_dir()
        output_dir = project_root / output_dir_name
        filename = f"{filename_base}.csv"
        return str(output_dir / filename)
    
    @staticmethod
    def get_author_name(session, author_id):
        """Get real author name from SINTA profile"""
        try:
            url = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}"
            response = session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Extract name from profile
            profile_section = soup.find('div', class_='col-lg col-md')
            if profile_section:
                name_element = profile_section.find('h3').find('a')
                if name_element:
                    return name_element.text.strip()
            
            return f"Author_{author_id}"
        except Exception as e:
            print(f"   ⚠️ Error getting author name for ID {author_id}: {e}")
            return f"Author_{author_id}"
