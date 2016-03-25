# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
from urlparse import urlparse

from peewee import *
from scrapy.utils.project import get_project_settings


SETTINGS = get_project_settings()


if SETTINGS['SCRAPY_ENV'] == 'local':
    database = MySQLDatabase(SETTINGS['DB_NAME'],
                             **{'user': SETTINGS['DB_USER']})
else:
    url = urlparse(os.getenv('CLEARDB_DATABASE_URL'))
    db_name = url.path.strip("/")
    database = MySQLDatabase(db_name, host=url.hostname, user=url.username,
                             passwd=url.password)


class BaseModel(Model):
    class Meta:
        database = database


class Game(BaseModel):
    id = IntegerField(index=True)
    name = CharField()
    timestamp = IntegerField()

    class Meta:
        db_table = 'game'


class League(BaseModel):
    game = IntegerField(db_column='game_id', null=True)
    hometeam = CharField()
    id = IntegerField(index=True)
    name = CharField()
    sport = IntegerField(db_column='sport_id', null=True)
    timestamp = IntegerField()

    class Meta:
        db_table = 'league'


class Matches(BaseModel):
    id = IntegerField(index=True)
    start = DateTimeField(null=True)
    team1 = CharField()
    team2 = CharField()
    timestamp = IntegerField()

    class Meta:
        db_table = 'matches'


class Odds(BaseModel):
    event = IntegerField(db_column='event_id')
    team1_odds = FloatField(null=True)
    team2_odds = FloatField(null=True)
    timestamp = IntegerField()

    class Meta:
        db_table = 'odds'


class Sport(BaseModel):
    id = IntegerField(index=True)
    name = CharField()
    timestamp = IntegerField()

    class Meta:
        db_table = 'sport'

database.connect()


class PinnacleLeaguesPipeline(object):
    def process_item(self, item, spider):
        query = League.select().where(League.id == item["id"])
        # query = "select * from league where id = %s" % item["id"]
        current_league = None
        try:
            current_league = query
        except Exception as e:
            print e
        if len(current_league) == 0:
            print 'creating league'
            League.create(
                          id=item['id'], name=item['name'],
                          hometeam=item['hometeam'],
                          timestamp=time.mktime(time.gmtime()), sport_id=12)
        else:
            print 'updating league'
            item = League(hometeam=item['hometeam'], id=int(item['id']))
            item.save()

if __name__ == "__main__":
    database.create_tables([Game, League, Matches, Odds, Sport], safe=True)
