import scrapy


class TwitterScraperItem(scrapy.Item):
    handle = scrapy.Field()
    profile_name = scrapy.Field()
    follower_count = scrapy.Field()