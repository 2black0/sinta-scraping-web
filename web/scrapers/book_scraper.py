#!/usr/bin/env python3
"""
Book data scraper for SINTA

This module handles scraping of book data from SINTA profiles.
"""

import csv
from bs4 import BeautifulSoup
from . import BaseScraper


class BookScraper(BaseScraper):
    """Scraper for book data"""
    
    def scrape(self, author_id, author_name):
        """Scrape book data for a specific author"""
        return self.scrape_books(author_id, author_name)
    
    def scrape_books(self, author_id, author_name):
        """Scrape book data for a specific author"""
        base_url = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}"
        url = f"{base_url}?page=1&view=books"
        response = self.session.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, "html.parser")

        # Check pagination
        total_pages = self.get_pagination_total(soup)

        all_results = []

        for page in range(1, total_pages + 1):
            print(f"   📖 Processing page {page} of {total_pages}")
            url = f"{base_url}?page={page}&view=books"
            response = self.session.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all(class_='ar-list-item')

            for item in items:
                try:
                    title = item.find('div', class_='ar-title').text.strip()
                    category = item.find('a', string=lambda text: 'Category' in text).text.split(':')[-1].strip()

                    # Extract authors
                    authors = []
                    ar_meta_divs = item.find_all('div', class_='ar-meta')
                    for meta_div in ar_meta_divs:
                        for author_link in meta_div.find_all('a', href="#!"):
                            if not author_link.has_attr('class'):
                                authors.append(author_link.text.strip())
                    authors = ", ".join(authors)

                    # Clean up authors
                    if ',' in authors:
                        authors = authors.split(',', 1)[1].strip()

                    publisher = item.find('a', class_='ar-pub').text.strip()
                    year = item.find('a', class_='ar-year').text.strip()
                    city = item.find('a', class_='ar-cited').text.strip()
                    isbn = item.find('a', class_='ar-quartile').text.split(':')[-1].strip()

                    all_results.append({
                        "Judul Buku": title,
                        "Kategori Buku": category,
                        "Penulis": authors,
                        "Penerbit": publisher,
                        "Tahun": year,
                        "Kota": city,
                        "ISBN": isbn,
                        "ID Sinta": author_id,
                        "Nama Sinta": author_name
                    })
                except Exception as e:
                    print(f"   ⚠️ Error processing book item: {e}")
                    continue

        return all_results
    
    def save_to_csv(self, data, filename):
        """Save book data to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ["Judul Buku", "Kategori Buku", "Penulis", "Penerbit", "Tahun", "Kota", "ISBN", "ID Sinta", "Nama Sinta"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                row["Penulis"] = str(row["Penulis"])
                writer.writerow(row)
