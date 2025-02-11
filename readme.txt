# Merch Scrapers

Code Written by Shawn Lim

A collection of scrapers for websites which sell merchandise/collectibles.
Extracts numerous data points including title, price, images, urls etc. Differs per website
as they will contain different information.
Inserts all data found into a local MongoDB instance.

**Destination URLs:**
https://animeworks.com.au/collections/pre-orders
https://www.kaika.com.au/preorder

**Important: Requires MongoDB to be run on local port with:**
```
mongod
```

Database name is websites-db. Each spider run will need a respective collection
(i.e. the kaika spider requires a kaika collection to store data)

MongoDB shell can be opened with (in a seperate terminal):
```
mongosh
```

Run scrapy shell (debugging)
```
scrapy shell [target website]
```

**Terminal directory:** `\scrapyproject\Scrapers\(website-scraper)`

To run spiders (ensure command is run in appropriate terminal directory)
```
scrapy crawl [spider name]
```
