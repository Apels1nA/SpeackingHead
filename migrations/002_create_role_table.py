from peewee import Model, CharField, IntegerField

def migrate(migrator, database, fake=False, **kwargs):

    class Participant(Model):
        pass

    @migrator.create_model 
    class Role(Model):
        role_name = CharField(unique=True)
        level = IntegerField()

def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model('role')