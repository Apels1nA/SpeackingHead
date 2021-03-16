from peewee import IntegerField, CharField
from db import db

class UserWarn(db.Model):
    id_vk_id = IntegerField()
    count = IntegerField()