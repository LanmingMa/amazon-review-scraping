BOT_NAME = 'amazonbot'

SPIDER_MODULES = ['amazon_review_scraping.spiders']
NEWSPIDER_MODULE = 'amazon_review_scraping.spiders'

#EXPORT TO CSV
FEED_FORMAT = "csv"
FEED_URI = "amazon_product.csv"

#UTF 8
FEED_EXPORT_ENCODING = 'utf-8'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
DEFAULT_REQUEST_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                                         '(KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
COOKIES_ENABLED = False
AUTOTHROTTLE_ENABLED=True
AUTOTHROTTLE_DEBUG = True

DUPEFILTER_DEBUG = True
HTTPCACHE_ENABLED = True
HTTPCACHE_IGNORE_HTTP_CODES = [301, 302, 500, 503]