from peewee import IntegerField, CharField
from db import db

class AdminWarn(db.Model):
    id_vk_id = IntegerField()
    count = IntegerField()