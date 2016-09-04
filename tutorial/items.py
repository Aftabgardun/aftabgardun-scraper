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
    itemtype = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()
    mail = scrapy.Field()
    photo = scrapy.Field()
    homePage = scrapy.Field()
    keywords = scrapy.Field()
    position = scrapy.Field()
    coAuthors = scrapy.Field()
    articles = scrapy.Field()
    dmozid = scrapy.Field()


class DmozyArticle(scrapy.Item):
    itemtype = scrapy.Field()
    link = scrapy.Field()
    name = scrapy.Field()
    authors = scrapy.Field()
    date = scrapy.Field()
    publisher = scrapy.Field()
    description = scrapy.Field()
