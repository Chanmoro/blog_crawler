import re
from datetime import datetime
from urllib.parse import urlparse

from dateutil import parser
from pytz import timezone
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from ..items import Article


def normalize_url(url):
    return re.sub(r'\?.*', '', url)


class SiteCrawlerSpider(CrawlSpider):
    name = 'site_crawl'
    allowed_domains = []
    start_urls = []
    rules = []

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
    }

    def __init__(self, company_name: str, url: str, *args, **kwargs):
        self._company_name = company_name
        self._base_url = url
        domain = urlparse(url).netloc
        path = urlparse(url).path

        self.start_urls = [url]
        self.allowed_domains = [domain]
        self.rules = [
            Rule(LinkExtractor(allow=rf'^http(s)?://{domain}{path}.*', process_value=normalize_url),
                 callback=self.parse_page, follow=True),
        ]
        super().__init__(*args, **kwargs)

    def parse_page(self, response):
        published_at = None
        published_at_timestamp = response.css('meta[property="article:published_time"]::attr(content)').extract_first()
        if published_at_timestamp:
            try:
                # unixtime がセットされている場合
                published_at = datetime.fromtimestamp(int(published_at_timestamp)).astimezone(timezone('Asia/Tokyo'))
            except Exception:
                # タイムスタンプ文字列がセットされている場合
                published_at = parser.parse(published_at_timestamp).astimezone(timezone('Asia/Tokyo'))

        yield Article(
            company_name=self._company_name,
            base_url=self._base_url,
            url=response.url,
            title=response.css('title::text').extract_first(),
            published_at=published_at,
        )
