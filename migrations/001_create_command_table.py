from peewee import Model, CharField, IntegerField

def migrate(migrator, database, fake=False, **kwargs):

    @migrator.create_model
    class Command(Model):
        name_eng = CharField()
        name_rus = CharField()

def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model('command')