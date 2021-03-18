import re

from peewee import PostgresqlDatabase, DoesNotExist

from random import getrandbits

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from models.command import Command
from models.participant import Participant
from models.role import Role

from config import config

#подключение к апи
token = config['api']['api_key']
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


#READY
def recognize_lang(text): #Принимает непустую строку, возвращает 'eng'/'rus' или False если первый символ не буква
    if len(text) != 0:
        number = text[0].encode('windows-1251')
        number = ord(number)
        if 61 <= number <= 122:
            return('eng')
        elif 224 <= number <= 255:
            return('rus')
    return False

#READY
def recognize_command(text, peer_id, echo): #Принимает сообщение написанное в чат, возвращает [True, command_id] если на существует, в противном случает вернет [False, 'Not command']
    #Если первый символ ! и пришло сообщение в котором помимо ! есть слова, то есть сообщение не было просто восклицательным знаком
    if len(text) != 0 and text[0] == '!' and len(text) > 1:
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
    return [False, 'Not command']

#READY
def write_msg(peer_id, message): # отправляет сообщение message в беседу peer_id
        
        vk.method('messages.send', {
            'peer_id': peer_id,
            'message': message,
            'random_id': getrandbits(64)})

#READY
def validate_arg_time(time):#принимает строку, предположительно содержащую время. вернет [True, 'time': {'count': count, 'unit': unit}}] если аргумент написан правильно. Вернет [False, {}] если аргумент не является параметром времени!inactive 
    range_d = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    range_w = ['m', 'd', 'h', 'м', 'д', 'ч']

    if len(time) == 2:
        if time[0] in range_d and time[1] in range_w:
            count = int(time[0])
            unit = str(time[1])
            if count == 0:
                count = 1
                unit = 'h'
            return (True, {'time': {'count': count, 'unit': unit}})
    elif len(time) == 3:
        if time[0] in range_d and time[1] in range_d and time[2] in range_w:
            count = int(str(time[0] + time[1]))
            unit = str(time[2])
            if count == 0:
                count = 1
                unit = 'h'
            return (True, {'time': {'count': count, 'unit': unit}})
    return (False, {})

#READY
def validate_arg_link(raw, link, scenario):
    if scenario == 1: #Ссылка в event.raw
        try:
            intruder_id = str(raw[6]['mentions'])[1:-1]
        except KeyError: 
            return (False, {})
        from_id = raw[6]['from']
        return (True, {'links': {'from_id': from_id, 'intruder_id': intruder_id}})
    if scenario == 2: #Ссылка в event.text
        if link[0] == '[': # '[id116582288|маргарита]'
            try:
                intruder_id = str(raw[6]['mentions'])[1:-1]
            except KeyError:
                return (False, {})
            bad_link = link[3:12]
            try: #Если ввлели '[...[id116582288|маргарита]'
                Participant.get(Participant.id == bad_link)
            except Exception:
                return (False, {})
            from_id = raw[6]['from']
            return (True, {'links': {'from_id': from_id, 'intruder_id': intruder_id}})
        elif link[0:15] == 'https://vk.com/':# 'https://vk.com/id237350735'
            return (False, {})
    return (False, {})


def validate_params(event):#Принимает event, возвращает (command_id, {'params_nam': value}) если параметры верные и (False, {}) если команда написана неправильно
    #берем айди команды
    command_id = recognize_command(event.raw[5].lower(), event.peer_id, echo=False)[1]
    command_name = Command.get(Command.id == command_id).name_eng
    message = event.text.lower()
    params = message.split(' ')
    del params[0]
    count_of_params = len(params)
    
    answer = [
        0, #command_id
        False,{ #is_args
            'links':{
                'from_id': 0,
                'intruder_id': 0
            }
        },{
            'time':{
                'count': 0,
                'unit': ''
            }
        },{
            'role_id': 0
        }
    ]

    #Определяем, пересылали ли сообщение или нет
    is_reply = True
    try:
        event.raw[7]['reply']
    except KeyError:
        is_reply = False

    #READY
    if command_name == 'help': # !help
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name == 'online': #!onile
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name == 'inactive': # !inacitve <time>
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            answer[3]['time']['count'] = 7
            answer[3]['time']['unit'] = 'd'
            return answer
        elif count_of_params == 1:
            answer[0] = command_id
            answer[1] = True
            if validate_arg_time(params[0])[0]:
                answer[3]['time'] = validate_arg_time(params[0])[1]['time']
                return answer
        answer[0] = command_id
        answer[1] = False
        return answer

    #READY
    elif command_name == 'kickdog': #!kickdog
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name == 'kickinactive': # !kickinacitve <time>
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            answer[3]['time']['count'] = 7
            answer[3]['time']['unit'] = 'd'
            return answer
        elif count_of_params == 1:
            answer[0] = command_id
            answer[1] = True
            if validate_arg_time(params[0])[0]:
                answer[3]['time'] = validate_arg_time(params[0])[1]['time']
                return answer
        answer[0] = command_id
        answer[1] = False
        return answer

    #READY
    elif command_name == 'ban': # !ban <user>
        if is_reply: #Сообщение пересылали. Ссылка в event.raw
            if count_of_params == 0:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        else: #Сообщение не пересылали. Ссылка в event.text
            if count_of_params == 1 and validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[0]:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        answer[0] = command_id
        answer[1] = False
        return answer

    #READY
    elif command_name == 'unban': # !unban <user>
        if is_reply: #Сообщение пересылали. Ссылка в event.raw
            if count_of_params == 0:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        else: #Сообщение не пересылали. Ссылка в event.text
            if count_of_params == 1 and validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[0]:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        answer[0] = command_id
        answer[1] = False
        return answer

    #READY
    elif command_name == 'mute': # !mite <user> <time>
        if is_reply: #Сообщение пересылали. Ссылка в event.raw
            if count_of_params == 0: # !mute
                if validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]: #Забираем ссылки, время дефолтное
                    answer[0] = command_id
                    answer[1] = True
                    answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                    answer[3]['time']['count'] = 1
                    answer[3]['time']['unit'] = 'h'
                    return answer
                else:
                    answer[0] = command_id
                    answer[1] = False
                    return answer
            elif count_of_params == 1: # !mute <time>
                if validate_arg_link(raw=event.raw, link=params, scenario = 1)[0]: #Забираем ссылки и время
                    answer[0] = command_id
                    answer[1] = True
                    answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                else:
                    answer[0] = command_id
                    answer[1] = False
                    return answer
                if validate_arg_time(params[0])[0]:
                    answer[3]['time'] = validate_arg_time(params[0])[1]['time']
                else:
                    answer[0] = command_id
                    answer[1] = False
                    return answer
                return answer

        else:  #Сообщение не пересылали. Ссылка в event.text
            if count_of_params == 1: # !mute <user>
                if validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[1]: #Забираем ссылки, время дефолтное
                    answer[0] = command_id
                    answer[1] = True
                    answer[2]['links'] = validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[1]['links']
                    answer[3]['time']['count'] = 1
                    answer[3]['time']['unit'] = 'h'
                    return answer
                else:
                    answer[0] = command_id
                    answer[1] = False
                    return answer
            elif count_of_params == 2: # !mute <user> <time>
                if validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[0]: #Забираем ссылки и время
                    answer[0] = command_id
                    answer[1] = True
                    answer[2]['links'] = validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[1]['links']
                else:
                    answer[0] = command_id
                    answer[1] = False
                    return answer
                if validate_arg_time(params[1])[0]:
                    answer[3]['time'] = validate_arg_time(params[1])[1]['time']
                else:
                    answer[0] = command_id
                    answer[1] = False
                    return answer
                return answer

    #READY
    elif command_name == 'unmute': # !unmute <user>
        if is_reply: #Сообщение пересылали. Ссылка в event.raw
            if count_of_params == 0:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        else: #Сообщение не пересылали. Ссылка в event.text
            if count_of_params == 1 and validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[0]:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        answer[0] = command_id
        answer[1] = False
        return answer

    #READY
    elif command_name == 'banlist': # !banlist
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name == 'mutelist': # !mutelist
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name == 'role': # !role
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name == 'administration': # !administration
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer


    elif command_name == 'createrole':
        answer[0] = command_id
        answer[1] = False
        return answer

    elif command_name == 'droprole':
        answer[0] = command_id
        answer[1] = False
        return answer

    elif command_name == 'renamerole':
        answer[0] = command_id
        answer[1] = False
        return answer


    #READY
    elif command_name == 'who': # !who <user>
        if is_reply: #Сообщение пересылали. Ссылка в event.raw
            if count_of_params == 0:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        else: #Сообщение не пересылали. Ссылка в event.text
            if count_of_params == 1 and validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[0]:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        answer[0] = command_id
        answer[1] = False
        return answer

    #READY
    elif command_name == 'list': # !list <role>
        if count_of_params == 1:
            try:
                answer[0] = command_id
                answer[1] = True
                answer[4]['role_id'] = Role.get(Role.role_name == params[0]).id
                return answer
            except DoesNotExist:
                answer[0] = command_id
                answer[1] = False
                return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name == 'ping': # !ping <role>
        if count_of_params == 1:
            try:
                answer[0] = command_id
                answer[1] = True
                answer[4]['role_id'] = Role.get(Role.role_name == params[0]).id
                return answer
            except DoesNotExist:
                answer[0] = command_id
                answer[1] = False
                return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer


    elif command_name == 'give':
        answer[0] = command_id
        answer[1] = False
        return answer


    #READY
    elif command_name == 'drop': # !drop <user>
        if is_reply: #Сообщение пересылали. Ссылка в event.raw
            if count_of_params == 0:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        else: #Сообщение не пересылали. Ссылка в event.text
            if count_of_params == 1 and validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[0]:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        answer[0] = command_id
        answer[1] = False
        return answer

    #READY
    elif command_name == 'quit': # !quite
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name == 'kick': # !kick <user>
        if is_reply: #Сообщение пересылали. Ссылка в event.raw
            if count_of_params == 0:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        else: #Сообщение не пересылали. Ссылка в event.text
            if count_of_params == 1 and validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[0]:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        answer[0] = command_id
        answer[1] = False
        return answer

    #READY
    elif command_name == 'pussy': # !pussy
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name == 'gay': # !gay
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer