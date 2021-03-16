from peewee import IntegerField, CharField
from db import db

class MuteWarn(db.Model):
    id_vk_id = IntegerField()
    count = IntegerField()