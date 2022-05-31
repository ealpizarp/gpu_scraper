from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider, Rule
from gpu_scraper.article import Article
import json
import re


def process_value(value):
    match = re.search(r'\d+/\d+/\d+/(.+)/', value)
    if not match:
        return None

    slug = match.group(1)
    api_pattern = 'https://techcrunch.com/wp-json/wp/v2/posts?slug={}'
    return api_pattern.format(slug)


class TechcrunchSpider(CrawlSpider):
    name = 'techcrunch'
    allowed_domains = ['techcrunch.com']
    start_urls = ['http://techcrunch.com/']
    current_url = ''

    rules = (
        Rule(
            LinkExtractor(
                allow_domains=allowed_domains,
                process_value=process_value
            ),
            callback='parse_item'
        ),
    )

    def parse_item(self, response):
        self.current_url = response.url
        json_res = json.loads(response.body)
        if not isinstance(json_res, list) or len(json_res) < 1:
            return None

        data = json_res[0]
        content = HtmlResponse(
            response.url,
            body=bytes(data['content']['rendered'], 'utf-8')
        )

        loader = ItemLoader(item=Article(), response=content)
        loader.add_value('title', data['title']['rendered'])
        loader.add_value('publish_date', data['date_gmt'])

        loader.add_css('content', '*::text')
        loader.add_css('image_urls', 'img::attr(src)')
        loader.add_css('links', 'a::attr(href)')
        return loader.load_item()