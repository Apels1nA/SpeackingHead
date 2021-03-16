from peewee import PostgresqlDatabase, DoesNotExist
from config import config

db = PostgresqlDatabase(
    database=config['db']['db'],
    user=config['db']['user'],
    password=config['db']['password'],
    host=config['db']['host'])

from models.participant import Participant
from models.role import Role

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


#подключение к апи
token = config['api']['api_key']
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def import_participant(peer_id): #импортирует участников беседы
    all_members = vk.method('messages.getConversationMembers', {
        'peer_id': peer_id
    })['profiles']

    for i in range(len(all_members)):
        participant = Participant()
        participant.id = all_members[i]['id']
        participant.name = all_members[i]['first_name']
        participant.surename = all_members[i]['last_name']
        participant.role_id = Role.get(Role.role_name == 'user')
        try:
            Participant.get(Participant.id == participant.id)
        except DoesNotExist:
            participant.save(force_insert=True)
    print('Импорт завершен')


for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.text:
        if event.to_me:
            import_participant(event.peer_id)
            break