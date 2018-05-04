#!/usr/bin/env python

""" A spider for Rita Store """
import time
import random
import scrapy

class RitastoreSpider(scrapy.Spider):
    """ A spider for Rita Store """

    name = "ritastore"
    start_urls = [
        'https://agebler.aliexpress.com/store/1911525/search/1.html?spm=2114.12010615.0.0.6768d70fjosXiT&origin=n&SortType=new_desc',
    ]

    def parse(self, response):
        no_more = response.css('a.ui-pagination-next.ui-pagination-disabled').extract_first()
        if no_more is None:
            for li in response.css('ul.items-list>li.item .detail'):
                url = li.css('a::attr(href)').extract_first()
                yield {'url':'https:'+url}

            next_page = response.css('a.ui-pagination-next::attr(href)').extract_first()
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)

        stop = random.randint(5, 15)
        print 'sleep'
        print stop
        print 'sleeping'
        time.sleep(stop)
