# -*- coding: utf-8 -*-
import scrapy


class OddsCheckerSpider(scrapy.Spider):
    name = "odds_checker"
    allowed_domains = ["oddschecker.com"]
    start_urls = (
        'http://www.oddschecker.com/e-sports/dota',
    )

    def parse(self, response):
        pass
