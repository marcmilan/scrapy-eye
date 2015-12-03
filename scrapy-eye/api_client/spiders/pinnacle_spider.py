# -*- coding: utf-8 -*-
from xml.dom import minidom
import json
from scrapy.spiders import Spider


class PinnacleAPISpider(Spider):
    name = "pinnacle"
    allowed_domains = ["pinnaclesports.com"]
    start_urls = (
        'https://api.pinnaclesports.com/v1/sports', # sports (XML)
        'https://api.pinnaclesports.com/v1/leagues?sportid=12', # leagues (JSON)
        'https://api.pinnaclesports.com/v1/odds?sportId=12&leagueid=149079&oddsFormat=DECIMAL' # odds (JSON)
    )

    def parse(self, response):
        
        if 'xml' in response.headers['Content-Type']:
            xmldoc = minidom.parseString(response.body)
            sports = xmldoc.getElementsByTagName('sport')
            for child in sports:
                sp = SP.Sport(
                              child.attributes["id"].value,
                              child.firstChild.nodeValue)
                items.append(sp)
            
            
        elif 'json' in response.headers['Content-Type']:
            json_response = json.loads(response.body_as_unicode())
            #for item in json_response:
            #    items.append(item)
        else:
            # parse as text
            pass
        return response