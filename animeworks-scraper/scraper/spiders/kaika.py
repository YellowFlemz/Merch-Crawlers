import re
import scrapy
from scraper.items import KaikaItem

class KaikaSpider(scrapy.Spider):
    name = "kaika"
    allowed_domains = ["kaika.com.au"]
    start_urls = ["https://www.kaika.com.au/preorder"]

    def parse(self, response):
        names = response.css("div.caption > h3 > a::attr(title)").getall()
        prices = response.css("p.price > span::text").getall()
        images = [self._modify_image_url(source) for source in response.css("img.product-image::attr(src)").getall()]
        urls = response.css("div.caption > h3 > a::attr(href)").getall()

        # Create a new item for each product
        for i in enumerate(names):
            item = KaikaItem()
            # Name (required)
            item["name"] = names[i].strip()
            # Price (required)
            item["price"] = prices[i].strip()
            # Image (required)
            item["image"] = images[i]
            # URL (required)
            item["url"] = urls[i]
            # Send item
            yield item

        # Pagination
        next_page = "https://www.kaika.com.au" + response.xpath('//i[contains(@class, "fa-chevron-right")]/parent::a/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_url, callback=self.parse)

    # Function to format image URLs correctly
    def _modify_image_url(self, url):
        # Remove query params
        url = re.sub(r'\?.*$', '', url)
        # Append base URL
        return "https://www.kaika.com.au" + url
