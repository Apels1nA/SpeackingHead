import peewee
import peewee_async

from config import config


db = peewee_async.PostgresqlDatabase(
    config['db'].pop('db'),
    **config['db'],
    autorollback=True
)


class BaseModel(peewee.Model):
    class Meta:
        database = db


db.Model = BaseModel