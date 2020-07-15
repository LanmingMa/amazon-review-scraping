# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonItem(scrapy.Item):
    # define the fields for your item here like:
    product_name = scrapy.Field()
    product_link = scrapy.Field()
    user_links = scrapy.Field()
    names = scrapy.Field()
    titles = scrapy.Field()
    ratings = scrapy.Field()
    review_contents = scrapy.Field()
    found_helpfuls = scrapy.Field()

class UserItem(scrapy.Item):
    insights = scrapy.Field()
