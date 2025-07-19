#!/usr/bin/env python3
"""
Profile data scraper for SINTA

This module handles scraping of profile data from SINTA profiles.
"""

import csv
from bs4 import BeautifulSoup
from . import BaseScraper


class ProfileScraper(BaseScraper):
    """Scraper for profile data"""
    
    def scrape(self, author_id, author_name):
        """Scrape profile data for a specific author"""
        return self.scrape_profile(author_id, author_name)
    
    def scrape_profile(self, author_id, author_name):
        """Scrape profile data for a specific author"""
        url = f"https://sinta.kemdikbud.go.id/authors/profile/{author_id}"
        response = self.session.session.get(url, timeout=30)
        soup = BeautifulSoup(response.content, "html.parser")

        try:
            # Extract profile information
            profile_section = soup.find('div', class_='col-lg col-md')
            
            # Extract name
            name_element = profile_section.find('h3').find('a')
            real_name = name_element.text.strip() if name_element else author_name
            
            # Extract university
            university_element = profile_section.find('a', href=lambda x: x and 'affiliations/profile' in x)
            university = university_element.text.strip().replace('Universitas ', '') if university_element else "N/A"
            
            # Extract study program
            prodi_element = profile_section.find('a', href=lambda x: x and 'departments/profile' in x)
            prodi = prodi_element.text.strip() if prodi_element else "N/A"
            
            # Extract SINTA Scores
            sinta_score_overall = "N/A"
            sinta_score_3yr = "N/A"
            
            # Find SINTA Score sections - look for the specific score pattern
            score_rows = soup.find_all('div', class_='row no-gutters')
            for row in score_rows:
                # Look for pr-txt elements containing score text
                pr_txt_elements = row.find_all('div', class_='pr-txt')
                pr_num_elements = row.find_all('div', class_='pr-num')
                
                for i, pr_txt in enumerate(pr_txt_elements):
                    text_content = pr_txt.text.strip()
                    if 'SINTA Score Overall' in text_content:
                        # Find corresponding pr-num element
                        if i < len(pr_num_elements):
                            sinta_score_overall = pr_num_elements[i].text.strip()
                    elif 'SINTA Score 3Yr' in text_content:
                        # Find corresponding pr-num element
                        if i < len(pr_num_elements):
                            sinta_score_3yr = pr_num_elements[i].text.strip()
            
            # Alternative method if first method fails
            if sinta_score_overall == "N/A" or sinta_score_3yr == "N/A":
                # Try to find by pattern matching
                all_pr_divs = soup.find_all('div', class_='pr-txt')
                for pr_div in all_pr_divs:
                    if 'SINTA Score Overall' in pr_div.text:
                        # Get the sibling pr-num div
                        parent = pr_div.parent
                        pr_num = parent.find('div', class_='pr-num')
                        if pr_num and sinta_score_overall == "N/A":
                            sinta_score_overall = pr_num.text.strip()
                    elif 'SINTA Score 3Yr' in pr_div.text:
                        # Get the sibling pr-num div  
                        parent = pr_div.parent
                        pr_num = parent.find('div', class_='pr-num')
                        if pr_num and sinta_score_3yr == "N/A":
                            sinta_score_3yr = pr_num.text.strip()
            
            # Extract statistics table
            table = soup.find('table', class_='stat-table')
            rows = table.find_all('tr')

            data = {
                "Nama Sinta": real_name,
                "ID Sinta": author_id,
                "Universitas": university,
                "Program Studi": prodi,
                "SINTA Score Overall": sinta_score_overall,
                "SINTA Score 3Yr": sinta_score_3yr
            }

            metrics = ["Article", "Citation", "Cited Document", "H-Index", "i10-Index", "G-Index"]
            sources = ["Scopus", "GScholar"]

            for i, metric in enumerate(metrics):
                for j, source in enumerate(sources):
                    value = rows[i + 1].find_all('td')[j + 1].text.strip()
                    data[f"{source} {metric}"] = value

            return data
        except Exception as e:
            print(f"   ⚠️ Error processing profile for {author_name}: {e}")
            return {
                "Nama Sinta": author_name,
                "ID Sinta": author_id,
                "Universitas": "N/A",
                "Program Studi": "N/A",
                "SINTA Score Overall": "N/A",
                "SINTA Score 3Yr": "N/A",
                "Scopus Article": "N/A",
                "Scopus Citation": "N/A",
                "Scopus Cited Document": "N/A",
                "Scopus H-Index": "N/A",
                "Scopus i10-Index": "N/A",
                "Scopus G-Index": "N/A",
                "GScholar Article": "N/A",
                "GScholar Citation": "N/A",
                "GScholar Cited Document": "N/A",
                "GScholar H-Index": "N/A",
                "GScholar i10-Index": "N/A",
                "GScholar G-Index": "N/A"
            }
    
    def save_to_csv(self, data, filename):
        """Save profile data to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            fieldnames = ["Nama Sinta", "ID Sinta", "Universitas", "Program Studi", "SINTA Score Overall", "SINTA Score 3Yr", "Scopus Article", "Scopus Citation", "Scopus Cited Document", "Scopus H-Index", "Scopus i10-Index", "Scopus G-Index", "GScholar Article", "GScholar Citation", "GScholar Cited Document", "GScholar H-Index", "GScholar i10-Index", "GScholar G-Index"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
