#!/usr/bin/env python3
"""
Community service (PPM) data scraper for SINTA

This module handles scraping of community service data from SINTA profiles.
"""

import csv
import re
from bs4 import BeautifulSoup
from . import BaseScraper


class CommunityServiceScraper(BaseScraper):
    """Scraper for community service (PPM) data"""
    
    def scrape(self, author_id, author_name):
        """Scrape community service data for a specific author"""
        return self.scrape_services(author_id, author_name)
    
    def scrape_services(self, author_id, author_name):
        """Scrape community service data for a specific author"""
        base_url = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}"
        url = f"{base_url}?view=services"
        response = self.session.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, "html.parser")

        # Check pagination
        total_pages = self.get_pagination_total(soup)

        all_results = []

        for page in range(1, total_pages + 1):
            print(f"   🤝 Processing page {page} of {total_pages}")
            url = f"{base_url}?page={page}&view=services"
            response = self.session.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all(class_='ar-list-item')

            for item in items:
                try:
                    title = item.find('div', class_='ar-title').text.strip().replace('\"', '"').replace('\n', ' ')
                    leader = item.find('a', string=lambda text: 'Leader :' in text).text.split(':')[-1].strip()
                    skim = item.find('a', class_='ar-pub').text.strip()
                    personnel = [p.text.strip() for p in item.find_all('a', href=lambda href: href and '/authors/profile/' in href)]
                    year = item.find('a', class_='ar-year').text.strip()
                    funding = item.find_all('a', class_='ar-quartile')[0].text.strip()
                    status = item.find_all('a', class_='ar-quartile')[1].text.strip()
                    source = item.find_all('a', class_='ar-quartile')[2].text.strip()

                    all_results.append({
                        "Judul PPM": re.sub(r'\s+', ' ', title),
                        "Ketua PPM": leader,
                        "Skim PPM": skim,
                        "Anggota PPM": "; ".join(personnel),
                        "Tahun": year,
                        "Besar Dana": funding,
                        "Status": status,
                        "Sumber": source,
                        "ID Sinta": author_id,
                        "Nama Sinta": author_name
                    })
                except Exception as e:
                    print(f"   ⚠️ Error processing community service item: {e}")
                    continue

        return all_results
    
    def save_to_csv(self, data, filename):
        """Save community service data to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ["Judul PPM", "Ketua PPM", "Skim PPM", "Anggota PPM", "Tahun", "Besar Dana", "Status", "Sumber", "ID Sinta", "Nama Sinta"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                cleaned_row = {}
                for key, value in row.items():
                    if isinstance(value, str):
                        cleaned_row[key] = value.replace('\n', ' ').replace('\"', '\"')
                    else:
                        cleaned_row[key] = value
                writer.writerow(cleaned_row)
