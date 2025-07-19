#!/usr/bin/env python3
"""
Publication data scraper for SINTA

This module handles scraping of publication data (Scopus, Google Scholar, Web of Science) from SINTA profiles.
"""

import csv
import re
from bs4 import BeautifulSoup
from . import BaseScraper


class PublicationScraper(BaseScraper):
    """Scraper for publication data (Scopus, Google Scholar, Web of Science)"""
    
    def scrape(self, author_id, author_name, publication_type='all'):
        """Scrape publication data for a specific author"""
        if publication_type == 'scopus':
            return self.scrape_scopus(author_id, author_name)
        elif publication_type == 'gs':
            return self.scrape_google_scholar(author_id, author_name)
        elif publication_type == 'wos':
            return self.scrape_wos(author_id, author_name)
        else:
            # Scrape all publication types
            results = {}
            results['scopus'] = self.scrape_scopus(author_id, author_name)
            results['gs'] = self.scrape_google_scholar(author_id, author_name)
            results['wos'] = self.scrape_wos(author_id, author_name)
            return results
    
    def scrape_scopus(self, author_id, author_name):
        """Scrape Scopus publications"""
        base_url = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}"
        url = f"{base_url}?page=1&view=scopus"
        response = self.session.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, "html.parser")
        pagination_elem = soup.find(class_='pagination-text')
        all_results = []

        if pagination_elem:
            pagination_text = pagination_elem.text.strip()
            page_info = pagination_text.split('|')[0].strip()
            total_pages = int(page_info.split()[-1])
        else:
            total_pages = 1

        print(f"   📚 Scopus Total Pages: {total_pages}")

        for page in range(1, total_pages + 1):
            print(f"   📚 Processing Scopus page {page} of {total_pages}")
            url = f"{base_url}?page={page}&view=scopus"
            response = self.session.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all(class_='ar-list-item')

            for item in items:
                try:
                    judul = item.find(class_='ar-title').text.strip()
                    link = item.find(class_='ar-pub')['href']
                    journal = item.find(class_='ar-pub').text.strip()
                    quartile = item.find(class_='ar-quartile').text.strip()
                    creator_elem = item.find('a', string=lambda text: text and 'Creator :' in text)
                    penulis = creator_elem.parent.text.split(':')[-1].strip() if creator_elem else None
                    tahun = item.find(class_='ar-year').text.strip().split()[-1]
                    sitasi = item.find(class_='ar-cited').text.strip()

                    all_results.append({
                        "Judul Artikel": judul,
                        "Nama Jurnal": journal,
                        "Quartile": quartile,
                        "Penulis": penulis,
                        "Tahun": tahun,
                        "Sitasi": sitasi,
                        "Link": link,
                        "ID Sinta": author_id,
                        "Nama Sinta": author_name
                    })
                except Exception as e:
                    print(f"   ⚠️ Error processing Scopus item: {e}")
                    continue

        return all_results
    
    def scrape_google_scholar(self, author_id, author_name):
        """Scrape Google Scholar publications"""
        base_url = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}"
        url = f"{base_url}?page=1&view=googlescholar"
        response = self.session.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, "html.parser")
        pagination_elem = soup.find(class_='pagination-text')
        all_results = []

        if pagination_elem:
            pagination_text = pagination_elem.text.strip()
            page_info = pagination_text.split('|')[0].strip()
            total_pages = int(page_info.split()[-1])
        else:
            total_pages = 1

        print(f"   🎓 Google Scholar Total Pages: {total_pages}")

        for page in range(1, total_pages + 1):
            print(f"   🎓 Processing Google Scholar page {page} of {total_pages}")
            url = f"{base_url}?page={page}&view=googlescholar"
            response = self.session.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all(class_='ar-list-item')

            for item in items:
                try:
                    judul = item.find('div', class_='ar-title').text.strip()
                    link = item.find('div', class_='ar-title').a['href']
                    jurnal = item.find('div', class_='ar-meta').find('a', class_='ar-pub').text
                    penulis = item.find('a', string=re.compile(r'Authors')).text.split(':')[-1].strip()
                    tahun = item.find('a', class_='ar-year').text.strip().split()[-1]
                    sitasi = item.find('a', class_='ar-cited').text.strip().split()[0]

                    all_results.append({
                        "Judul Artikel": judul,
                        "Nama Jurnal": jurnal,
                        "Penulis": penulis,
                        "Tahun": tahun,
                        "Sitasi": sitasi,
                        "Link": link,
                        "ID Sinta": author_id,
                        "Nama Sinta": author_name
                    })
                except Exception as e:
                    print(f"   ⚠️ Error processing Google Scholar item: {e}")
                    continue

        return all_results
    
    def scrape_wos(self, author_id, author_name):
        """Scrape Web of Science publications"""
        base_url = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}"
        url = f"{base_url}?page=1&view=wos"
        response = self.session.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, "html.parser")
        pagination_elem = soup.find(class_='pagination-text')
        all_results = []

        if pagination_elem:
            pagination_text = pagination_elem.text.strip()
            page_info = pagination_text.split('|')[0].strip()
            total_pages = int(page_info.split()[-1])
        else:
            total_pages = 1

        print(f"   🔬 Web of Science Total Pages: {total_pages}")

        for page in range(1, total_pages + 1):
            print(f"   🔬 Processing Web of Science page {page} of {total_pages}")
            url = f"{base_url}?page={page}&view=wos"
            response = self.session.session.get(url, timeout=30)
            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.find_all(class_='ar-list-item')

            for item in items:
                try:
                    link = item.find('div', class_='ar-title').a['href']
                    judul = item.find('div', class_='ar-title').text.strip()
                    quartile_elem = item.find('a', class_='ar-quartile')
                    quartile = quartile_elem.text.strip() if quartile_elem else "N/A"
                    edisi = item.find('a', class_='ar-pub').text.strip()
                    jurnal = item.find('div', class_='ar-meta').find_all('a', class_='ar-pub')[-1].text.strip()
                    link_jurnal = item.find('div', class_='ar-meta').find_all('a', class_='ar-pub')[-1]['href']
                    urutan_penulis, total_penulis = map(int, re.findall(r'\d+', item.find('a', string=re.compile(r'Author Order')).text))
                    author_tag = item.find('div', class_='ar-meta').find_all('a')
                    penulis = None
                    for tag in author_tag:
                        if re.search(r'Authors\s*:', tag.text):
                            penulis = tag.text.split(':')[-1].strip()
                            break
                    tahun = item.find('a', class_='ar-year').text.strip().split()[-1]
                    sitasi = item.find('a', class_='ar-cited').text.strip().split()[-2]
                    terindex_scopus = "Yes" if item.find('span', class_='scopus-indexed') else "No"
                    doi_tag = item.find('a', class_='ar-sinta')
                    doi = doi_tag.text.strip().split(':')[-1] if doi_tag else "N/A"

                    all_results.append({
                        "Judul Artikel": judul,
                        "Nama Jurnal": jurnal,
                        "Quartile": quartile,
                        "Edition": edisi,
                        "Link Jurnal": link_jurnal,
                        "Penulis": penulis,
                        "Urutan Penulis": urutan_penulis,
                        "Total Penulis": total_penulis,
                        "Tahun": tahun,
                        "Sitasi": sitasi,
                        "Terindex Scopus": terindex_scopus,
                        "DOI": doi,
                        "Link": link,
                        "ID Sinta": author_id,
                        "Nama Sinta": author_name
                    })
                except Exception as e:
                    print(f"   ⚠️ Error processing WoS item: {e}")
                    continue

        return all_results
    
    def save_to_csv(self, data, filename, publication_type):
        """Save publication data to CSV"""
        fieldnames = {
            "scopus": ["Judul Artikel", "Nama Jurnal", "Quartile", "Penulis", "Tahun", "Sitasi", "Link", "ID Sinta", "Nama Sinta"],
            "gs": ["Judul Artikel", "Nama Jurnal", "Penulis", "Tahun", "Sitasi", "Link", "ID Sinta", "Nama Sinta"],
            "wos": ["Judul Artikel", "Nama Jurnal", "Quartile", "Edition", "Link Jurnal", "Penulis", "Urutan Penulis", "Total Penulis", "Tahun", "Sitasi", "Terindex Scopus", "DOI", "Link", "ID Sinta", "Nama Sinta"]
        }
        
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames[publication_type])
            writer.writeheader()
            writer.writerows(data)
