import scrapy
from bs4 import BeautifulSoup

class GSECrawler(scrapy.Spider):
    name = 'gse-crawler'
    start_urls = ['http://www.example.com']

    def parse(self, response):
        # Extract text content from the page
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text()

        # Print the extracted text
        print(text)

        # Follow links to other pages
        links = soup.find_all('a')
        for link in links:
            url = link.get('href')
            if url is not None:
                yield scrapy.Request(url, callback=self.parse)