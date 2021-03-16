from peewee import Model, CharField, ForeignKeyField

def migrate(migrator, database, fake=False, **kwargs):

    class Command(Model):
        pass
    class Role(Model):
        pass

    @migrator.create_model 
    class RoleToCommand(Model):
        role_name = ForeignKeyField(Role, backref='conn_role_name')
        command_id = ForeignKeyField(Command ,backref='conn_command_id')

def rollback(migrator, database, fake=False, **kwargs):
    migrator.remove_model('role_to_command')