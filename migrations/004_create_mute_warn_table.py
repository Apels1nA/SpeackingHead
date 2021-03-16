from peewee import Model, ForeignKeyField, IntegerField


def migrate(migrator, database, fake=False, **kwargs):

    class Participant(Model):
        pass

    @migrator.create_model
    class MuteWarn(Model):
        id_vk = ForeignKeyField(Participant, backref='mute_warn')
        count = IntegerField(default=0)

def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model('mute_warn')