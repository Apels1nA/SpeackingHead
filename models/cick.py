from peewee import IntegerField, CharField, DateTimeField
from db import db

class Ban(db.Model):
    id_vk_id = IntegerField()
    from_id_vk = IntegerField()
    start_time = DateTimeField()
    end_time = DateTimeField()
    description = CharField()