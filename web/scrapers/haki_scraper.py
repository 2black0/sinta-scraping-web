#!/usr/bin/env python3
"""
HAKI (Intellectual Property Rights) data scraper for SINTA

This module handles scraping of HAKI data from SINTA profiles.
"""

import csv
from bs4 import BeautifulSoup
from . import BaseScraper


class HakiScraper(BaseScraper):
    """Scraper for HAKI (Intellectual Property Rights) data"""
    
    def scrape(self, author_id, author_name):
        """Scrape HAKI data for a specific author"""
        return self.scrape_haki(author_id, author_name)
    
    def scrape_haki(self, author_id, author_name):
        """Scrape HAKI data for a specific author"""
        base_url = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}"
        url = f"{base_url}?view=iprs"
        response = self.session.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, "html.parser")

        # Check pagination
        total_pages = self.get_pagination_total(soup)

        all_results = []

        for page in range(1, total_pages + 1):
            print(f"   🏛️ Processing page {page} of {total_pages}")
            url = f"{base_url}?page={page}&view=iprs"
            response = self.session.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all(class_='ar-list-item')

            for item in items:
                try:
                    title = item.find('div', class_='ar-title').text.strip()
                    inventor = item.find('a', string=lambda text: 'Inventor :' in text).text.split(':')[-1].strip()
                    year = item.find('a', class_='ar-year').text.strip()
                    application_number = item.find('a', class_='ar-cited').text.split(':')[-1].strip()
                    haki_type = item.find('a', class_='ar-quartile').text.strip()

                    all_results.append({
                        "Judul HAKI": title,
                        "Penemu": inventor,
                        "Jenis HAKI": haki_type,
                        "Nomor HAKI": application_number,
                        "Tahun": year,
                        "ID Sinta": author_id,
                        "Nama Sinta": author_name
                    })
                except Exception as e:
                    print(f"   ⚠️ Error processing HAKI item: {e}")
                    continue

        return all_results
    
    def save_to_csv(self, data, filename):
        """Save HAKI data to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ["Judul HAKI", "Penemu", "Jenis HAKI", "Nomor HAKI", "Tahun", "ID Sinta", "Nama Sinta"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
