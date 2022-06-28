import scrapy
from bs4 import BeautifulSoup

def bs_strip_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

class RosettaSpider(scrapy.Spider):
    name = 'rosetta'
    start_urls = ['http://rosettacode.org/wiki/Category:Programming_Tasks']

    

    def parse(self, response):
        tasks = [response.urljoin(t) for t in  response.xpath('//div[@id="mw-pages"]//li//a/@href').getall()]
        yield from response.follow_all(tasks, callback=self.parse_task)
    
    def parse_task(self, response):
        
        yield {
            
        }
