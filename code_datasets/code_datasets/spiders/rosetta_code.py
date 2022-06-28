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
        toc_links = toc_links = response.xpath('//div[@id="toc"]/ul/li/a/@href').getall()
        toc_languages = response.xpath('//div[@id="toc"]/ul/li/a/span[@class="toctext"]').getall()
        assert len(toc_links) == len(toc_languages)
        for link, language in zip(toc_links, toc_languages):
            yield {
                "task_url": response.url,
                "language_url": link,
                "language_name": bs_strip_tags(language),
                "code": bs_strip_tags(response.xpath(f'//h2[span[@id="{link[1:]}"]]/following-sibling::pre').get().replace('<br>', '\n')),
            }
