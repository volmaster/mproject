# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MouserprojectItem(scrapy.Item):
    ven_part_id = scrapy.Field()
    mfg_part_id = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    inventory = scrapy.Field()
    lead_time = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()
