import scrapy
from bs4 import BeautifulSoup

def bs_strip_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    a = soup.find_all('a', {'class':'__cf_email__'})
    for i in a:
        i.string = decode_email(i.attrs['data-cfemail'])  
    return soup.get_text()

def decode_email(email):
    decoded = ""
    for i in range(2, len(email)-1, 2):
        decoded += chr(int(email[i:i+2], 16)^(int(email[:2], 16)))
    return decoded

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
        task_description = response.xpath('//div[@id="mw-content-text"]//div[@id="toc"]/preceding-sibling::*').getall()
        task_description = '\n'.join([bs_strip_tags(i.replace('<br>', '\n')) for i in task_description[1:]])
        for link, language in zip(toc_links, toc_languages):
            yield {
                "task_url": response.url,
                "task_name": response.xpath('//h1[@id="firstHeading"]/text()').get(),
                "task_description": task_description,
                "language_url": link,
                "language_name": bs_strip_tags(language),
                "code": bs_strip_tags(response.xpath(f'//h2[span[@id="{link[1:]}"]]/following-sibling::pre').get().replace('<br>', '\n')),
            }
