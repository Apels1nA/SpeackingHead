from peewee import Model, CharField, DateTimeField, ForeignKeyField

def migrate(migrator, database, fake=False, **kwargs):

    class Participant(Model):
        pass

    @migrator.create_model 
    class Ban(Model):
        id_vk = ForeignKeyField(Participant, backref='ban')
        from_id_vk = ForeignKeyField(Participant, backref='ban')
        description = CharField()

def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model('ban')