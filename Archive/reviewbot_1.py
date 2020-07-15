# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from scrapy.selector import Selector
import sys

from amazon_review_scraping.items import AmazonItem
import pandas as pd
from scrapy.utils.markup import remove_tags
from w3lib.html import remove_tags
import re
import re
import random
import base64
import logging


class ReviewbotSpider(scrapy.Spider):
    name = 'amazonbot'
    allowed_domains = ["www.amazon.com"]
    # Base URL for the MacBook air reviews
    # myBaseUrl = 'https://www.amazon.in/Apple-MacBook-Air-13-3-inch-MQD32HN/product-reviews/B073Q5R6VR' \
                # '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber='
    myBaseUrl = 'https://www.amazon.com/Sony-XBR60X830F-60-Inch-Ultra-Smart/product-reviews/B07CXDY7G1' \
                '/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber='

    start_urls = []
    for i in range(1, 13):
        start_urls.append(myBaseUrl + str(i))

    def parse(self, response):
        product_link = response.xpath('//div[@id="cm_cr-product_info"]/div/div/div/div/div'
                                      '/div[@class="a-row product-title"]/h1'
                                      '/a[@data-hook="product-link"]/@href').extract()
        product_name = response.xpath('//div[@id="cm_cr-product_info"]/div/div/div/div/div'
                                      '/div[@class="a-row product-title"]/h1'
                                      '/a[@data-hook="product-link"]/text()').extract()
        product_price = response.xpath('//div[@id="cm_cr-product_info"]/div/div/div/div/div'
                                       '/div[@class="a-row product-price-line"]/span'
                                       '/span[contains(@span, "a-color-price arp-price")]/text()').extract()
        names = response.xpath('//div[contains(@id, "cm_cr-review_list")]'
                               '/div[@data-hook="review"]/div'
                               '/div[@class="a-section celwidget"]/div[@data-hook="genome-widget"]/a'
                               '/div[@class="a-profile-content"]/span[@class="a-profile-name"]/text()').extract()
        titles = response.xpath('//div[contains(@id, "cm_cr-review_list")]'
                                      '/div[@data-hook="review"]/div'
                                      '/div[@class="a-section celwidget"]/div'
                                      '/a[@data-hook="review-title"]'
                                      '/span/text()').extract()
        ratings = response.xpath('//div[contains(@id, "cm_cr-review_list")]'
                                     '/div[@data-hook="review"]/div'
                                     '/div[@class="a-section celwidget"]/div/a'
                                     '/i[@data-hook="review-star-rating"]'
                                     '/span[@class="a-icon-alt"]/text()').extract()
        reviews = response.xpath('//div[contains(@id, "cm_cr-review_list")]'
                                 '/div[@data-hook="review"]/div'
                                 '/div[@class="a-section celwidget"]/div'
                                 '/span[@data-hook="review-body"]/span').extract()
        # times = response.xpath('//div[contains(@id, "cm_cr-review_list")]'
        #                        '/div[@data-hook="review"]/div'
        #                        '/div[@class="a-section celwidget"]/div'
        #                        '/span[@data-hook="review-date"]/text()').extract()

        for name, title, rating, review in zip(names, titles, ratings, reviews):
            yield {'product_link':product_link, 'product_name': product_name, 'product_price':product_price,
                   'name': name, 'title': title, 'rating': rating, 'review':review}

