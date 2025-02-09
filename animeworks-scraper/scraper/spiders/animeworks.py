import scrapy

from scraper.items import ProductsItem

class AnimeworksSpider(scrapy.Spider):
    name = "animeworks"
    allowed_domains = ["animeworks.com.au"]
    start_urls = ["https://animeworks.com.au/collections/pre-orders"]

    def parse(self, response):
        # Scrapes product names and prices
        names = response.css("a.full-unstyled-link::text").getall()
        prices = response.css("span.price-item--regular::text").getall()
        for i, _ in enumerate(names):
            item = ProductsItem()
            item["name"] = names[i].strip()
            item["price"] = prices[i].strip()
            yield item

        # Pagination
        next_page = response.css('a.pagination__item-arrow[aria-label="Next page"]::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
