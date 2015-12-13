# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


from peewee import *


database = MySQLDatabase('ninja', **{'user': 'root'})


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
        item = League(hometeam=item['hometeam'],
                      id=int(item['id']),
                      )
        item.save()

if __name__ == "__main__":
    database.create_tables([Game, League, Matches, Odds, Sport], safe=True)
