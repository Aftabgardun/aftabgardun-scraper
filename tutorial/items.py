# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DmozItem(scrapy.Item):
    name = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
    mail = scrapy.Field()
    photo = scrapy.Field()

class DmozyItem(scrapy.Item):
    author = scrapy.Field()
    position = scrapy.Field()
    keywords = scrapy.Field()
    homePage = scrapy.Field()
    coAuthors = scrapy.Field()
    articles = scrapy.Field()
