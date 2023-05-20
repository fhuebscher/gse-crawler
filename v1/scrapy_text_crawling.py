import scrapy

class ScrapyTextCrawler(scrapy.Spider):
    name = 'ScrapyTextCrawler'
    start_urls = ['http://www.example.com']

    def parse(self, response):
        # Extract text content from the page
        text = response.css('::text').extract()

        # Print the extracted text
        print(text)
