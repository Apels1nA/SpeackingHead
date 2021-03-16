import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from config import config
from resources.commands import commands
from resources.functional import write_msg

#подключение к апи
token = config['api']['api_key']
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)

# Основной цикл
for event in longpoll.listen():
    print('-'*22)
    print('event.raw:')
    print(event.raw)
    print('-'*22)

    if event.type == VkEventType.MESSAGE_NEW and event.text:
        if event.to_me:
            write_msg(event.peer_id, event.text)