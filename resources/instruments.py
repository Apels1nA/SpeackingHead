import re

from peewee import PostgresqlDatabase, DoesNotExist

from random import getrandbits

from models.command import Command

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.longpoll import VkLongPoll, VkEventType

from models.command import Command

from config import config

#подключение к апи
token = config['api']['api_key']
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


#READY
def recognize_lang(text): #Принимает непустую строку, возвращает 'eng' или 'rus'
    number = text[0].encode('windows-1251')
    number = ord(number)
    if 61 <= number <= 122:
        return('eng')
    elif 224 <= number <= 255:
        return('rus')

#READY
def recognize_command(text, peer_id, echo): #Принимает сообщение написанное в чат, возвращает [True, command_id] если на существует, в противном случает вернет [False, 'Not command']
    #Если первый символ ! и пришло сообщение в котором помимо ! есть слова, то есть сообщение не было просто восклицательным знаком
    if text[0] == '!' and len(text) > 1:
        text = text[1:] #Удаляем восклицательный знак
        word = text.split(' ')[0] #Берем первое слово из сообщения
        if recognize_lang(word) == 'eng':
            try:#Если введенная команда есть в бд
                command_id = Command.get(Command.name_eng == word).id
                return [True, command_id]
            except DoesNotExist:#Если введенной команды нет в бд
                if echo:
                    write_msg(peer_id, 'Команда не найдена')
                return [False, 'Not command']
        elif recognize_lang(word) == 'rus':
            try:#Если введенная команда есть в бд
                command_id = Command.get(Command.name_rus == word).id
                return [True, command_id]
            except DoesNotExist:#Если введенной команды нет в бд
                if echo:
                    write_msg(peer_id, 'Команда не найдена')
                return [False, 'Not command']
    else:
        return [False, 'Not command']

#READY
def write_msg(peer_id, message): # отправляет сообщение message в беседу peer_id
        
        vk.method('messages.send', {
            'peer_id': peer_id,
            'message': message,
            'random_id': getrandbits(64)})

#READY
def validate_arg_time(time):#принимает строку, предположительно содержащую время. вернет [True, {'count': count, 'unit': unit}] если аргумент написан правильно. Вернет [False, {}] если аргумент не является параметром времени
    range_d = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    range_w = ['m', 'd', 'h', 'м', 'д', 'ч']

    if len(time) == 2:
        if time[0] in range_d and time[1] in range_w:
            count = int(time[0])
            unit = str(time[1])
            return (True, {'time': {'count': count, 'unit': unit}})
    elif len(time) == 3:
        if time[0] in range_d and time[1] in range_d and time[2] in range_w:
            count = int(str(time[0] + time[1]))
            unit = str(time[2])
            return (True, {'time': {'count': count, 'unit': unit}})
    return (False, {})

def validate_params(event):#Принимает event, возвращает [command_id, {'params_nam': value}] если параметры верные и [False] если команда написана неправильно
    #берем айди команды
    command_id = recognize_command(event.raw[5].lower(), event.peer_id, echo=False)[1]
    command_name = Command.get(Command.id == command_id).name_eng
    message = event.text.lower()
    params = message.split(' ')
    del params[0]
    count_of_params = len(params)
    #Определяем, пересылали ли сообщение или нет
    is_reply = True
    try:
        event.raw[7]['reply']
    except KeyError:
        is_reply = False

    #READY
    if command_name == 'help': # !help
        if count_of_params == 0:
            return (command_id, {})
        else:
            return (False, {})

    #READY
    elif command_name == 'online': #!onile
        if count_of_params == 0:
            return (command_id, {})
        else:
            return (False, {})

    elif command_name == 'inactive': # !inacitve <time>
        if count_of_params == 0:
            return (command_id, {'time:': {'count': 7, 'unit': 'd'}})
        elif count_of_params == 1:
            return validate_arg_time(params[0])
        else:
            return (False, {})


    elif command_name == 'kickdog':
        pass
    elif command_name == 'kickinactive':
        pass
    elif command_name == 'ban':
        pass
    elif command_name == 'unban':
        pass
    elif command_name == 'mute':
        pass
    elif command_name == 'unmute':
        pass
    elif command_name == 'banlist':
        pass
    elif command_name == 'mutelist':
        pass
    elif command_name == 'role':
        pass
    elif command_name == 'administration':
        pass
    elif command_name == 'createrole':
        pass
    elif command_name == 'droprole':
        pass
    elif command_name == 'renamerole':
        pass
    elif command_name == 'who':
        pass
    elif command_name == 'list':
        pass
    elif command_name == 'ping':
        pass
    elif command_name == 'give':
        pass
    elif command_name == 'drop':
        pass
    elif command_name == 'quit':
        pass
    elif command_name == 'kick':
        pass
    elif command_name == 'randompussy':
        pass