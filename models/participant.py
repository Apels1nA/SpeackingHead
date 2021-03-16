from peewee import IntegerField, CharField
from db import db

class Participant(db.Model):
    id = IntegerField(primary_key=True)
    name = CharField()
    surename = CharField()
    role_id = CharField()