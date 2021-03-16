from peewee import CharField
from db import db

class Role(db.Model):
    role_name = CharField()