from peewee import Model, CharField, DateTimeField, ForeignKeyField

def migrate(migrator, database, fake=False, **kwargs):

    class Participant(Model):
        pass

    @migrator.create_model 
    class Kick(Model):
        id_vk = ForeignKeyField(Participant, backref='kick')
        from_id_vk = CharField()
        start_time = DateTimeField()
        end_time = DateTimeField()
        description = CharField()

def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model('kick')