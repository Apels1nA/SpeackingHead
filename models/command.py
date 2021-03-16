from peewee import CharField, IntegerField
from db import db

class Command(db.Model):
    name_eng = CharField()
    name_rus = CharField()