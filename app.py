import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from resources.instruments import recognize_command
from resources.instruments import write_msg
from resources.instruments import check_params

from config import config

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

    if event.raw[0] == 4: #если пришло сообщение
        print(recognize_command(event.raw[5].lower(), event.peer_id, echo=False))
        if recognize_command(event.raw[5].lower(), event.peer_id, echo=True)[0]: #если пришла команда
            print('\n\n')
            print('Пришла команда')
            print('\n\n')
            check_params(event)

        else:
            print('\n\n')
            print('Это не команда')
            print('\n\n')

    if event.raw[1] == 6: #Если это новый участник
        write_msg(event.peer_id, 'Новый уастник')