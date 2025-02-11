Code Written by Shawn Lim

Destination URL: https://animeworks.com.au/collections/pre-orders

# Important: Requires MongoDB to be run on local port with:
mongod
# MongoDB shell can be opened with (in a seperate terminal):
mongosh

# Run Animeworks Shell (debugging)
scrapy shell https://animeworks.com.au/collections/pre-orders

Terminal directory: \scrapyproject\Scrapers\(website-scraper)

# To run Animeworks spider (ensure command is run in appropriate terminal directory)
scrapy crawl animeworks
