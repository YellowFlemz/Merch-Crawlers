import re
import scrapy
from scraper.items import HLJGoodSmileItem

class HLJGoodSmileSpider(scrapy.Spider):
    name = "hljgoodsmile"
    allowed_domains = ["hlj.com"]
    start_urls = ["https://www.hlj.com/search/?Word=good+smile&Sort=rss+desc&Page=1"]

    def parse(self, response):
        names = response.css("p.product-item-name > a::text").getall()
        urls = ["https://www.hlj.com" + url for url in response.css("p.product-item-name > a::attr(href)").getall()]
        images = [self._modify_image_url(source) for source in response.css("a.item-img-wrapper > img::attr(src)").getall()]

        # Create a new item for each product
        for i, _ in enumerate(names):
            item = HLJGoodSmileItem()
            # Name (required)
            item["name"] = names[i].strip()
            # Image (required)
            item["image"] = images[i]
            # URL (required)
            item["url"] = urls[i]
            # Send item
            yield item

        # Pagination (brute forced)
        urlmain, urlpageno = response.url.rsplit("&Page=", 1)
        next_page_url = urlmain + "&Page=" + str(int(urlpageno) + 1)
        yield scrapy.Request(url=next_page_url, callback=self.parse)

    # Function to format image URLs correctly
    def _modify_image_url(self, url):
        # Remove query params
        url = re.sub(r'\?.*$', '', url)
        # Add https: if missing
        if url.startswith("//"):
            return "https:" + url
        return url
