from peewee import IntegerField, CharField, DateTimeField
from db import db

class Ban(db.Model):
    id_vk_id = IntegerField()
    from_id_vk_id = IntegerField()
    description = CharField()