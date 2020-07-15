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
        if 'base_url' in kwargs:
            self.baseUrl = [kwargs.get('base_url')][0]
            productName = self.baseUrl.split('/')[3]
            productId = self.baseUrl.split('/')[5]
            self.newBaseUrl = 'https://www.amazon.com/'+ productName + '/product-reviews/' + productId + \
                                 '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber='
            self.start_urls = ['https://www.amazon.com/'+ productName + '/product-reviews/' + productId + \
                                '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber=1']
        else:
            print('Please input url by running: [scrapy crawl amazonbot -a base_url="YOUR URL"]')
            pass

    def parse(self, response):
        review_pages_str = response.xpath('.//span[@data-hook="cr-filter-info-review-count"]/text()').extract_first()
        review_pages = int(review_pages_str.split(' ')[3])//10
        product_name = response.xpath('.//a[@data-hook="product-link"]/text()').extract_first()
        product_link = self.baseUrl
        for page in range(review_pages):
            newStartUrl = self.newBaseUrl+str(page)
            yield Request(newStartUrl,
                          callback=self.parse_reviews,
                          dont_filter=True,
                          meta={'product_name': product_name,
                                'product_link': product_link, })

    def parse_reviews(self, response):
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