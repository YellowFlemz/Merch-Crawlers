import scrapy
import re

from scraper.items import ProductsItem

class AnimeworksSpider(scrapy.Spider):
    name = "animeworks"
    allowed_domains = ["animeworks.com.au"]
    start_urls = ["https://animeworks.com.au/collections/pre-orders"]

    def parse(self, response):
        # Regex pattern to extract date only in [DD/MM/YYYY, D/MM/YYYY, DD/M/YYYY, D/M/YYYY] format
        date_pattern = r"\d{1,2}/\d{1,2}/\d{4}"
        # Scrapes product names, prices and release dates
        names = response.css("a.full-unstyled-link::text").getall()
        prices = response.css("span.price-item--regular::text").getall()
        release_dates = []
        for release in response.css("div.card-information"):
            release_date_text = release.css("h4::text").get()
            if release_date_text:
                match = re.search(date_pattern, release_date_text)
                if match:
                    release_dates.append(match.group())
                else:
                    release_dates.append(None)
            else:
                release_dates.append(None)

        # Create a new item for each product
        for i, _ in enumerate(names):
            item = ProductsItem()
            # Name (required)
            item["name"] = names[i].strip()
            # Price (required)
            item["price"] = prices[i].strip()
            # Release date (optional, may be None)
            item["release_date"] = release_dates[i]
            # Send item
            yield item

        # Pagination
        next_page = response.css('a.pagination__item-arrow[aria-label="Next page"]::attr(href)').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)
