import scrapy


class Article(scrapy.Item):
    __table_name__ = 'articles'

    # define the uniq field names for your items here like: (Optional)
    __uniq_fields__ = [
        'company_name',
        'base_url',
        'url',
    ]

    # define the fields for your items here like:
    company_name = scrapy.Field()
    base_url = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    published_at = scrapy.Field()
    hatena_bookmark_count = scrapy.Field()
    hatena_bookmark_newest_comment_at = scrapy.Field()
    hatena_bookmark_oldest_comment_at = scrapy.Field()
