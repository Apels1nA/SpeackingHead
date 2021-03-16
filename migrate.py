#!./env/bin/python3
from sys import exit

from argparse import ArgumentParser

from peewee_migrate import Router
from peewee import PostgresqlDatabase


router = Router(PostgresqlDatabase('speackinghead'))

parser = ArgumentParser(description='Данный скрипт запускает миграции')

parser.add_argument('actions',
                    metavar='actions',
                    type=str,
                    choices=['migrate', 'create'],
                    help='Данный параметр выбирает действие migrate/create')

parser.add_argument('name',
                    default=None,
                    metavar='migrations name',
                    type=str)

args = parser.parse_args()

if args.actions == 'create':
    if args.name:
        try:
            router.create(args.name)
        except Exception:
            print('Can`t create migration "{0}". Exiting'.format(args.name))
            exit(1)
    else:
        ArgumentParser.error()

elif args.actions == 'migrate':
    if args.name == 'all':
            try:
                router.run()
            except Exception as e:
                print('Can`t apply migrations. Exiting')
                print(e)
                exit(1)
    else:
        try:
            router.run(args.name)
        except Exception as e:
            print('Can`t apply migration "{0}". Exiting'.format(args.name))
            print(e)
            exit(1)
else:
    ArgumentParser.error()