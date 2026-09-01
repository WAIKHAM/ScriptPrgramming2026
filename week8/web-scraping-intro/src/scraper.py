# web-scraping-intro/src/scraper.py
import requests
from bs4 import BeautifulSoup

class SimpleWebScraper:
    """A class to scrape Wikipedia pages."""
    
    def __init__(self, target_url):
        self.target_url = target_url

    def _get_html_content(self):
        """Downloads HTML content from target URL with basic error handling."""
        print(f"Downloading content from: {self.target_url}")
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.target_url, headers=headers, timeout=10)
            response.raise_for_status()
            print("Successfully downloaded content.")
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error downloading page: {e}")
            return None

    def scrape_main_titles(self):
        """Scrapes the main title and section headers from Wikipedia."""
        html_content = self._get_html_content()
        if not html_content:
            return None

        soup = BeautifulSoup(html_content, 'html.parser')

        # Wikipedia main page heading / welcome title
        page_title_tag = soup.find('h1', id='firstHeading') or soup.find('span', id='mp-welcome')
        page_title = page_title_tag.get_text(strip=True) if page_title_tag else "Page Title Not Found"

        # Section headers on Wikipedia Main Page
        section_titles = []
        headers = soup.find_all(['h2', 'h3'])
        for header in headers:
            text = header.get_text(strip=True).replace('[edit]', '')
            if text and text not in ["Contents", "Navigation menu"]:
                section_titles.append(text)

        return {
            "book_title": page_title,
            "chapter_titles": section_titles
        }