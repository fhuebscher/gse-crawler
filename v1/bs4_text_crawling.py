import requests
from bs4 import BeautifulSoup

class Crawler:
    """A node in the trie structure"""

    def __init__(self):
        pass

    def get_text_from_url(self, url):
        # Get the HTML content of the page
        try:
            response = requests.get(url, timeout=3)
            html_content = response.content
            
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract all the text from the page and remove HTML tags
            text = soup.get_text(separator='\n')
            
            return text.strip().replace("\n"," ")
        except:
            return [""]

    def get_links_from_url(self, url):
        # Get the HTML content of the page
        response = requests.get(url)
        html_content = response.content
        
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all the hyperlinks in the page
        links = []
        for link in soup.find_all('a'):
            href = link.get('href')
            if href:
                links.append(href)
        
        return links

    def get_elements_from_url(self, url, elements):
        try:
            # Get the HTML content of the page
            response = requests.get(url, timeout=3)
            html_content = response.content
            
            # Parse the HTML content with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Extract the content of all the specified HTML tags
            results = []
            for element in elements:
                for tag in soup.find_all(element):
                    tag_text = tag.get_text().strip().replace("\n"," ")
                    if tag_text:
                        results.append(tag_text)
            
            return results
    
        except:
            return [""]


if __name__ == "__main__":

    url = 'https://www.uni-mannheim.de'

    crawler = Crawler()

    text = crawler.get_text_from_url(url)
    print(text)

    links = crawler.get_links_from_url(url)
    print(links)

    # more elements can be added
    elements = ['h1', 'h2']
    headers = crawler.get_elements_from_url(url, elements)
    print(headers)
