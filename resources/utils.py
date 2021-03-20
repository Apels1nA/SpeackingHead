import re

from peewee import PostgresqlDatabase, DoesNotExist

from random import getrandbits

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from models.command import Command
from models.participant import Participant
from models.role import Role
from models.role_to_command import RoleToCommand
from models.ban import Ban
from models.mute import Mute

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

def validate_role(role): #принимает строку, возвращает (True, {'role_id': role_id}) если аргумент верный, в противном случае вернет (False, {})
    try:
        role_id = Role.get(Role.role_name == role).id
        return (True, {'role_id': role_id})
    except DoesNotExist:
        return (False, {})

#READY
def validate_params(event): #Принимает event, возвращает список: answer
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
    if command_name in ['help', 'online', 'banlist', 'mutelist', 'role', 'administration', 'quit']: # !<command_name>
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            answer[2]['links']['from_id'] = event.raw[6]['from']
            return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name in ['kickdog']: # !kickdog <time>
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            answer[2]['links']['from_id'] = event.raw[6]['from']
            answer[3]['time']['count'] = 7
            answer[3]['time']['unit'] = 'd'
            return answer
        answer[0] = command_id
        answer[1] = False
        return answer

    #READY
    elif command_name in ['inactive', 'kickinactive']: # !inacitve <time>
        if count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            answer[2]['links']['from_id'] = event.raw[6]['from']
            answer[3]['time']['count'] = 7
            answer[3]['time']['unit'] = 'd'
            return answer
        elif count_of_params == 1:
            answer[0] = command_id
            answer[1] = True
            answer[2]['links']['from_id'] = event.raw[6]['from']
            if validate_arg_time(params[0])[0]:
                answer[3]['time'] = validate_arg_time(params[0])[1]['time']
                return answer
        answer[0] = command_id
        answer[1] = False
        return answer

    #READY
    elif command_name in ['ban', 'unban', 'unmute', 'who', 'drop', 'kick', 'warn']: # !ban <user>
        if is_reply: #Сообщение пересылали. Ссылка в event.raw
            if count_of_params == 0:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links']['from_id'] = event.raw[6]['from']
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        else: #Сообщение не пересылали. Ссылка в event.text
            if count_of_params == 1 and validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[0]:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links']['from_id'] = event.raw[6]['from']
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
    elif command_name == 'list': # !list <role>
        if count_of_params == 1:
            try:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links']['from_id'] = event.raw[6]['from']
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
            if validate_role(params[0])[0]:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links']['from_id'] = event.raw[6]['from']
                answer[4] = validate_role(params[0])[1]
                return answer
            else:
                answer[0] = command_id
                answer[1] = False
                return answer
        else:
            answer[0] = command_id
            answer[1] = False
            return answer

    #READY
    elif command_name == 'give': # !give <user> <role>
        if is_reply: #Сообщение пересылали. Ссылка в event.raw
            if count_of_params == 1: # !give <role>
                if validate_role(params[1])[0]:
                    answer[0] = command_id
                    answer[1] = True
                    answer[2]['links'] = validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[1]['links']
                    answer[4] = validate_role(params[1])[1]
                    return answer
                else:
                    answer[0] = command_id
                    answer[1] = False
                    return answer
        else:  #Сообщение не пересылали. Ссылка в event.text
            if count_of_params == 2: # !give <user> <role>
                if validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[0]: #Забираем ссылки и id роли
                    answer[0] = command_id
                    answer[1] = True
                    answer[2]['links'] = validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[1]['links']
                else:
                    answer[0] = command_id
                    answer[1] = False
                    return answer
                if validate_role(params[1])[0]:
                    answer[4] = validate_role(params[1])[1]
                else:
                    answer[0] = command_id
                    answer[1] = False
                    return answer
                return answer

    #READY
    elif command_name in ['pussy', 'gay']: # !pussy
        if is_reply: #Сообщение пересылали. Ссылка в event.raw
            if count_of_params == 0:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links']['from_id'] = event.raw[6]['from']
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        elif count_of_params == 0:
            answer[0] = command_id
            answer[1] = True
            answer[2]['links']['from_id'] = event.raw[6]['from']
            return answer
        else: #Сообщение не пересылали. Ссылка в event.text
            if count_of_params == 1 and validate_arg_link(raw=event.raw, link=params[0], scenario = 2)[0]:
                answer[0] = command_id
                answer[1] = True
                answer[2]['links']['from_id'] = event.raw[6]['from']
                answer[2]['links'] = validate_arg_link(raw=event.raw, link=params, scenario = 1)[1]['links']
                return answer
        answer[0] = command_id
        answer[1] = False
        return answer

def check_permition(data):
    # 1 - Проверить, есть ли человек написавший команду в базе данных.
    # 2 - Проверить наличия доступа его роли к написанной команде
    # 3 - Функция возвращает кортэж типа [bool, 'comment']
    #Берем ссылки того кто написал команду и кому она предназначена
    command_sender = data[2]['links']['from_id']
    intruder_id = data[2]['links']['intruder_id']
    list_command_id = []

    if data[0] in [22, 23]: # pussy/gay only for Me and Denis
        if int(data[2]['links']['from_id']) in [294211206, 204388290]:
            return [True, '']

    try:
        role_id_sender = Participant.get(Participant.id == command_sender).role_id
    except DoesNotExist:
        return [False, f'Для использования команд [id{command_sender}|вы] должны присутствовать в базе данных']

    for i in RoleToCommand.select():
        if int(i.role_name_id) == int(role_id_sender):
            list_command_id.append(int(i.command_id))
    if data[0] not in list_command_id:
        return [False, f'У [id{command_sender}|вас] нет доступа к этой команде']

    #Ниже идет проверка доступа к команде относительно уровня роли
    #Тоесть: надо исключить ситуации в которых админ банит создателя
    #или админ снимает бан который выдал создатель

    if data[0] in [6, 8]: #ban/mute | Нельзя наказать человека с вашей ролью или выше
        #Берем уровни полицейского и нарушителя
        try:
            role_id_policeman = Participant.get(Participant.id == command_sender).role_id ###
            role_id_intruder = Participant.get(Participant.id == intruder_id).role_id
            lvl_policeman = Role.get(Role.id == role_id_policeman).level
            lvl_intruder = Role.get(Role.id == role_id_intruder).level
        except DoesNotExist:
            return [False, 'Пользователь отсутствует в базе данных']
        if lvl_intruder >= lvl_policeman:
            return [False, f'[id{command_sender}|Ваш] уровень слишком низкий']

    if data[0] in [7, 9]: #unban/unmute | Нельзя снять наказание если его дала роль выше вашей
        if data[0] == 7: #unban
            #Берем ссылку того кто дал бан
            try:
                creator_id = Ban.get(Ban.id_vk_id == intruder_id).from_id_vk_id
            except DoesNotExist:
                return [False, 'Пользователья нет в списке забаненых']
        elif data[0] == 9: #unmute
            #Берем ссылку того кто дал мут
            try:
                creator_id = Mute.get(Mute.id_vk_id == intruder_id).from_id_vk_id
            except DoesNotExist:
                return [False, 'Пользователья нет в списке забаненых']
        #Берем уровни полицейского и спасителя
        try:
            role_id_policeman = Participant.get(Participant.id == creator_id).role_id
            role_id_savior = Participant.get(Participant.id == command_sender).role_id ###
            lvl_policeman = Role.get(Role.id == role_id_policeman).level
            lvl_savior = Role.get(Role.id == role_id_savior).level
        except:
            return [False, 'Пользователь отсутствует в базе данных']
        if lvl_policeman > lvl_savior:
            return [False, f'[id{command_sender}|Ваш] уровень слишком низкий']

    if data[0] == 17: #give | Нельзя дать роль если она равна вашей или выше
        try:
            lvl_sender = Role.get(Role.id == role_id_sender).level
            lvl_recipient = Role.get(Role.id == data[4]['role_id']).level
        except DoesNotExist:
            return [False, 'Пользователь отсутствует в базе данных']
        if lvl_recipient >= lvl_sender:
            return [False, f'[id{command_sender}|Вы] не можете выдать роль вашего уровня или выше']

    if data[0] in [18, 20, 21]: #drop/kick/warn | Нельзя наказать нарушителя если его роль равна вашей или выше
        try:
            lvl_sender = Role.get(Role.id == role_id_sender).level
            intruder_id = Participant.get(Participant.id == intruder_id).role_id
            lvl_intruder = Role.get(Role.id == intruder_id).level
        except DoesNotExist:
            return [False, 'Пользователь отсутствует в базе данных']
        if lvl_intruder >= lvl_sender:
            return [False, f'[id{command_sender}|Вы] не можете наказать участника с уровнем роли равному вашему или выше']

    return [True, '']
