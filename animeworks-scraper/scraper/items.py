# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductsItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    release_date = scrapy.Field()
    image = scrapy.Field()
    url = scrapy.Field()