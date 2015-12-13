# -*- coding: utf-8 -*-
import json
import os.path
from urlparse import urlparse
# from xml.dom import minidom

from scrapy.spiders import Spider
from scrapy import Selector

from api_client.items import LeagueItem
from api_client.items import OddsItem
from api_client.items import SportItem
from api_client.items import MatchItem


class PinnacleAPISpider(Spider):
    api_base_uri = 'https://api.pinnaclesports.com/v1'

    name = "pinnacle"
    allowed_domains = ["pinnaclesports.com"]
    start_urls = (
        api_base_uri + '/sports',
        api_base_uri + '/leagues?sportid=12',
        api_base_uri + '/odds?sportId=12&leagueid=149079&oddsFormat=DECIMAL',
        api_base_uri + '/fixtures?sportId=12&leaguesids=149079'
    )

    def parse(self, response):
        # get current endpoint name
        endpoint_name = os.path.split(urlparse(response.url).path)[1]
        # set reposnse type for parsing
        if 'xml' in response.headers['Content-Type']:
            selector = Selector(text=response.body, type="xml")
            pass
        elif 'json' in response.headers['Content-Type']:
            json_response = json.loads(response.body_as_unicode())

        # parse sports
        if endpoint_name == 'sports':
            print response.url
            for sel in selector.xpath('//sport'):
                item = SportItem()

        # parse leagues
        if endpoint_name == 'leagues':
            for sel in selector.xpath('//league'):
                item = LeagueItem()
                item['name'] = sel.xpath('./text()').extract_first()
                item['id'] = sel.xpath('./@id').extract_first()
                item['hometeam'] = sel.xpath('./@homeTeamType').extract_first()
                yield item

        # parse odds
        if endpoint_name == 'odds':
            print response.url
            for sel in json_response:
                item = OddsItem()

        # parse matches
        if endpoint_name == 'fixtures':
            print response.url
            for sel in json_response:
                item = MatchItem()

        # xmldoc = minidom.parseString(response.body)
        # leagues = xmldoc.getElementsByTagName('league')
        # for child in leagues:
        #    print(' League['+child.attributes["id"].value+'] - ' +
        #          child.firstChild.nodeValue)
            # lg = LG.League(
            #    child.attributes["id"].value,
            #    child.firstChild.nodeValue,
            #    child.attributes["homeTeamType"].value)
            # print lg
