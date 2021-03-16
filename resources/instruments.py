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

def check_params(event):#Принимает event, возвращает [command_id,{'params_nam': value}] если параметры верные и False если команда написана неправильно
    #берем айди команды
    command_id = recognize_command(event.raw[5].lower(), event.peer_id, echo=False)[1]
    command_name = Command.get(Command.id == command_id).name_eng
    message = event.text.lower()
    #Определяем, пересылали ли сообщение или нет
    is_reply = True
    try:
        event.raw[7]['reply']
    except KeyError:
        is_reply = False

    if command_name == 'help': # !help
        if len(message) == 1:
            return (command_id, {})
        else:
            return False
    elif command_name == 'online': #!onile
        if len(message) == 1:
            return (command_id, {})
        else:
            return False

    elif command_name == 'inactive': # !inacitve <time>
        if is_reply or len(message) > 2:
            return False
        


    elif cammand_name == 'kickdog':
        pass
    elif cammand_name == 'kickinactive':
        pass
    elif cammand_name == 'ban':
        pass
    elif cammand_name == 'unban':
        pass
    elif cammand_name == 'mute':
        pass
    elif cammand_name == 'unmute':
        pass
    elif cammand_name == 'banlist':
        pass
    elif cammand_name == 'mutelist':
        pass
    elif cammand_name == 'role':
        pass
    elif cammand_name == 'administration':
        pass
    elif cammand_name == 'createrole':
        pass
    elif cammand_name == 'droprole':
        pass
    elif cammand_name == 'renamerole':
        pass
    elif cammand_name == 'who':
        pass
    elif cammand_name == 'list':
        pass
    elif cammand_name == 'ping':
        pass
    elif cammand_name == 'give':
        pass
    elif cammand_name == 'drop':
        pass
    elif cammand_name == 'quit':
        pass
    elif cammand_name == 'kick':
        pass
    elif cammand_name == 'randompussy':
        pass