from peewee import IntegerField
from db import db

class RoleToCommand(db.Model):
    role_name_id = IntegerField()
    command_id = IntegerField()