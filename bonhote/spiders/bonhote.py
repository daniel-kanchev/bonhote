import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from bonhote.items import Article


class BonhoteSpider(scrapy.Spider):
    name = 'bonhote'
    allowed_domains = ['bonhote.ch']
    start_urls = ['https://www.bonhote.ch/actualites']

    def parse(self, response):
        links = response.xpath('//a[@class="link-read-more"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):

        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="date"]/text()').get()
        if date:
            date = date.strip()
        else:
            return

        content = response.xpath('//article[@class="actu"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
