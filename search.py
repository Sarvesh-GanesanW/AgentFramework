import requests
from bs4 import BeautifulSoup

class WebSearcher:
    def __init__(self, model):
        self.model = model

    def fetch_search_results(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(search_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.select('.BVG0Nb')
        return [result.get_text() for result in search_results]

    def get_search_page(self, search_results, query):
        return search_results[0] if search_results else None

    def scrape_website_content(self, website_url):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        try:
            response = requests.get(website_url, headers=headers, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text(separator='\n')
            clean_text = '\n'.join([line.strip() for line in text.splitlines() if line.strip()])
            return {website_url: clean_text}
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving content from {website_url}: {e}")
            return {website_url: f"Failed to retrieve content due to an error: {e}"}
