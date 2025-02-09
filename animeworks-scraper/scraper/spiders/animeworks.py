import scrapy

from scraper.items import ProductsItem

class AnimeworksSpider(scrapy.Spider):
    name = "animeworks"
    allowed_domains = ["animeworks.com.au"]
    start_urls = ["https://animeworks.com.au/collections/pre-orders"]

    def parse(self, response):
        names = response.css("a.full-unstyled-link::text").getall()
        prices = response.css("span.price-item--regular::text").getall()
        for i, _ in enumerate(names):
            item = ProductsItem()
            item["name"] = names[i].strip()
            item["price"] = prices[i].strip()
            yield item
