# -*- coding: utf-8 -*-

# Please run:
#scrapy crawl amazonbot -a start_url="TARGET_URL"

import scrapy
import pandas as pd
from scrapy import Spider
from scrapy.http import Request
from scrapy import Request
from scrapy.selector import Selector
from amazon_review_scraping.items import AmazonItem
from datetime import datetime
import re


class ReviewbotSpider(scrapy.Spider):
    name = 'amazonbot'
    allowed_domains = ["www.amazon.com"]

    def __init__(self, *args, **kwargs):
        super(ReviewbotSpider, self).__init__(*args, **kwargs)
        if 'start_url' in kwargs:
            self.start_urls = [kwargs.get('start_url')]
        else:
            print('Please input url by running: [scrapy crawl amazonbot -a start_url="YOUR URL"]')
            pass

    def parse(self, response):
        product_link = self.start_urls
        product_name = response.xpath('//span[@id="productTitle"]/text()').extract_first()
        if product_name is not None:
            product_name = product_name.replace('\n', '').strip()
        all_reviews_url = response.xpath('//a[@data-hook="see-all-reviews-link-foot"]/@href').extract_first()
        try:
            if len(all_reviews_url) > 0:
                all_reviews_url = "https://www.amazon.com" + all_reviews_url
                print("=" * 20, "the url for the review page:", all_reviews_url, '=' * 20)
                yield Request(all_reviews_url,
                              callback=self.parse_review,
                              dont_filter=True,
                              meta={'product_name': product_name,
                                    'product_link': product_link,})
                print("=" * 30, 'Now redirecting to the review page', '=' * 30)
        except:
            pass

    def parse_review(self, response):

        print('=' * 30, 'start parsing reviews', '=' * 30)
        product_name = response.meta['product_name']
        product_link = response.meta['product_link']
        review_all = response.xpath('//div[contains(@id, "cm_cr-review_list")]/div[@data-hook="review"]')
        print('=' * 30, 'getting all reviews info', '=' * 30)
        found_helpfuls = response.xpath('//div[contains(@id, "cm_cr-review_list")]/div/div/div'
                                        '/div[contains(@class, "a-row review-comments comments-for-")]/div'
                                        '/span[@data-hook="review-voting-widget"]'
                                        '/div[1]/span[1]').extract()
        for i, h in enumerate(found_helpfuls):
            if h.find('<span data-hook="helpful-vote-statement"') == -1:
                found_helpfuls[i] = 0
            else:
                h = re.sub(
                    r'<span data-hook="helpful-vote-statement" class="a-size-base a-color-tertiary cr-vote-text">', '',
                    h)
                h = re.sub(r'</span>', '', h)
                h = re.sub(r' people found this helpful', '', h)
                h = re.sub(r' person found this helpful', '', h)
                if h == 'One':
                    found_helpfuls[i] = 1
                else:
                    found_helpfuls[i] = int(h)

        for i, review in enumerate(review_all):
            user_link = review.xpath('.//div[@class="a-section celwidget"]'
                                     '/div[@data-hook="genome-widget"]/a/@href').extract_first()

            name = review.xpath('.//span[@class="a-profile-name"]/text()').extract_first()

            title = review.xpath('.//a[@data-hook="review-title"]/span/text()').extract_first()

            rating = review.xpath('.//i[@data-hook="review-star-rating"]'
                                  '/span[@class="a-icon-alt"]/text()').extract_first()

            review_content = review.xpath('.//div/span[@data-hook="review-body"]/span').extract()

            item = AmazonItem()
            item['product_name'] = product_name
            item['product_link'] = product_link
            item['user_links'] = user_link
            item['names'] = name
            item['titles'] = title
            item['ratings'] = rating
            item['review_contents'] = review_content
            item['found_helpfuls'] = found_helpfuls[i]
            yield item

        # Click next on reviews page
        next_page_reviews = response.xpath('//li[@class="a-last"]/a/@href').extract_first()
        try:
            if len(next_page_reviews) > 0:
                next_page_reviews = "https://www.amazon.com" + next_page_reviews
                print("-" * 30)
                print("Clicking Next (Reviews): ", next_page_reviews)
                yield Request(next_page_reviews,
                              callback=self.parse_review,
                              dont_filter=True,
                              meta={'product_name': product_name,
                                    'product_link': product_link})
        except:
            pass