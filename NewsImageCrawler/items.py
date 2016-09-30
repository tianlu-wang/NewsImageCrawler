# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SubWebsiteItem(scrapy.Item):
    name = scrapy.Field()
    sub_sub_websites = scrapy.Field()


class SubSubWebsiteItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()

# class cnn_item(scrapy.item):
#
