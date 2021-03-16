from peewee import Model, CharField, PrimaryKeyField, ForeignKeyField

def migrate(migrator, database, fake=False, **kwargs):

    class Role(Model):
        pass

    @migrator.create_model 
    class Participant(Model):
        id = PrimaryKeyField()
        name = CharField()
        surename = CharField()
        role = ForeignKeyField(Role, backref='participant')

def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model('participant')