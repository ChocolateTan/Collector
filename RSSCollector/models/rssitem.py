import scrapy

class RssItem(scrapy.Item):
    title = scrapy.Field()
    link = scrapy.Field()
    pubDate = scrapy.Field()
