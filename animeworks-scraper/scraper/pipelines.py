import hashlib
import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class WebsitesPipeline:

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # Select collection based on spider name
        collection_name = spider.name
        collection = self.db[collection_name]

        # Hash ID of item
        item_id = self.compute_item_id(item)
        item_dict = ItemAdapter(item).asdict()

        # Upsert item
        collection.update_one(
            filter={"_id": item_id},
            update={"$set": item_dict},
            upsert=True
        )

        return item

    def compute_item_id(self, item):
        """
        Compute a unique item ID based on the URL of the item.

        Args:
            item (Item): The item being processed

        Returns:
            str: A SHA-256 hash of the item's URL, encoded as a hexadecimal string.
        """
        url = item["url"]
        return hashlib.sha256(url.encode("utf-8")).hexdigest()
