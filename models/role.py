from peewee import CharField, IntegerField
from db import db

class Role(db.Model):
    role_name = CharField()
    level = IntegerField()