#!/usr/bin/env python3
"""
Research data scraper for SINTA

This module handles scraping of research data from SINTA profiles.
"""

import csv
import re
from bs4 import BeautifulSoup
from . import BaseScraper


class ResearchScraper(BaseScraper):
    """Scraper for research data"""
    
    def scrape(self, author_id, author_name):
        """Scrape research data for a specific author"""
        return self.scrape_research(author_id, author_name)
    
    def scrape_research(self, author_id, author_name):
        """Scrape research data for a specific author"""
        base_url = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}"
        url = f"{base_url}?page=1&view=researches"
        response = self.session.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, "html.parser")

        # Check pagination
        total_pages = self.get_pagination_total(soup)

        all_results = []

        for page in range(1, total_pages + 1):
            print(f"   🔬 Processing page {page} of {total_pages}")
            url = f"{base_url}?page={page}&view=researches"
            response = self.session.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all(class_='ar-list-item')

            for item in items:
                try:
                    def clean_text(text):
                        return re.sub(r"[\n\r]+", " ", text.strip())

                    title = clean_text(item.find('div', class_='ar-title').text)
                    leader = clean_text(item.find('a', string=lambda text: 'Leader :' in text).text.split(':')[-1])
                    funding_info = clean_text(item.find('a', class_='ar-pub').text)
                    personnel = [clean_text(p.text) for p in item.find_all('a', href=lambda href: href and '/authors/profile/' in href)]
                    year = clean_text(item.find('a', class_='ar-year').text)
                    funding = clean_text(item.find_all('a', class_='ar-quartile')[0].text)
                    status = clean_text(item.find_all('a', class_='ar-quartile')[1].text)
                    source = clean_text(item.find_all('a', class_='ar-quartile')[2].text)

                    all_results.append({
                        "Judul Penelitian": title,
                        "Ketua Penelitian": leader,
                        "Sumber Dana": funding_info,
                        "Anggota Penelitian": "; ".join(personnel),
                        "Tahun": year,
                        "Besar Dana": funding,
                        "Status": status,
                        "Sumber": source,
                        "ID Sinta": author_id,
                        "Nama Sinta": author_name
                    })
                except Exception as e:
                    print(f"   ⚠️ Error processing research item: {e}")
                    continue

        return all_results
    
    def save_to_csv(self, data, filename):
        """Save research data to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ["Judul Penelitian", "Ketua Penelitian", "Sumber Dana", "Anggota Penelitian", "Tahun", "Besar Dana", "Status", "Sumber", "ID Sinta", "Nama Sinta"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
