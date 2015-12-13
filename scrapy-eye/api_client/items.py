# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GameItem(scrapy.Item):

    id = scrapy.Field()
    name = scrapy.Field()
    timestamp = scrapy.Field()


class LeagueItem(scrapy.Item):

    game = scrapy.Field()
    hometeam = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    sport = scrapy.Field()
    timestamp = scrapy.Field()


class MatchItem(scrapy.Item):

    id = scrapy.Field()
    start = scrapy.Field()
    team1 = scrapy.Field()
    team2 = scrapy.Field()
    timestamp = scrapy.Field()


class OddsItem(scrapy.Item):

    event = scrapy.Field()
    team1_odds = scrapy.Field()
    team2_odds = scrapy.Field()
    timestamp = scrapy.Field()


class SportItem(scrapy.Item):

    id = scrapy.Field()
    name = scrapy.Field()
    timestamp = scrapy.Field()
