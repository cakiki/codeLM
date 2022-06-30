import scrapy
from bs4 import BeautifulSoup

def bs_strip_tags(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.get_text()

def decode_email(email):
    decoded = ""
    for i in range(2, len(e)-1, 2):
        decoded += chr(int(e[i:i+2], 16)^(int(email[:2], 16)))

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
        for link, language in zip(toc_links, toc_languages):
            pre = response.xpath(f'//h2[span[@id="{toc_links[0][1:]}"]]/following-sibling::pre').get()
            soup = BeautifulSoup(pre, 'html.parser')
            a = soup.find('a')
            if a is None:
                code = bs_strip_tags(response.xpath(f'//h2[span[@id="{link[1:]}"]]/following-sibling::pre').get().replace('<br>', '\n'))
            elif 'data-cfemail' in a.attrs:
                code = decode_email(a.attrs['data-cfemail'])
            else:
                code = "<EMPTY>"
            yield {
                "task_url": response.url,
                "language_url": link,
                "language_name": bs_strip_tags(language),
                "code": code,
            }
