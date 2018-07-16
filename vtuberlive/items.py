# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VtuberliveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    videoId = scrapy.Field()
    videoUrl = scrapy.Field()
    channel = scrapy.Field()
    channelName = scrapy.Field()
    actualStartTime = scrapy.Field()
    viewCount = scrapy.Field()
    concurrentViewCount = scrapy.Field()

