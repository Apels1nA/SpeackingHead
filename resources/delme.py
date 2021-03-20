def check(vk_id, command_id):
    #берем поле role_id у участника из отношения Participant
    print(f'VK FROM: {vk_id}\nCOMMAND ID: {command_id}')
    role_id = Participant.get(Participant.id == vk_id).role_id
    #делаем выборку поля command_id по условию полученное_role_id == role_id_из_бд
    list_command_id = []
    for role_name_id in RoleToCommand.select():
        if role_name_id.role_name_id == int(role_id):
            list_command_id.append(role_name_id.command_id)

    if list_command_id.count(int(str(command_id))):
        return True
    else:
        return False

def check_permition(args):
    

    def get_lvl(id_vk):
        role_id = Participant.get(Participant.id == id_vk).role_id
        lvl = Role.get(Role.id == role_id).level
        return lvl

    if args[0] in [1, 2]: #help online
        return True

    if args[0] in [3, 4, 5]: #inactive, kickinactive
        try:
            from_lvl = get_lvl(args[2]['links']['from_id'])
        except DoesNotExist:
            return [False, 'Участника нет в бд']
        if from_lvl < 3:
            return [True, '']
        else:
            return [False, 'Не хватает уровня роли']

    if args[0] in [6]: #ban mute
        try:
            from_lvl = get_lvl(args[2]['links']['from_id'])
            to_lvl = get_lvl(args[2]['links']['intruder_id'])
        except DoesNotExist:
            return [False, 'Участника нет в бд']
        if from_lvl < to_lvl:
            return [True, '']
        else:
            return [False, 'Не хватает уровня роли']

    if args[0] in [8]: #mute
        try:
            from_lvl = get_lvl(args[2]['links']['from_id'])
            to_lvl = get_lvl(args[2]['links']['intruder_id'])
        except DoesNotExist:
            return [False, 'Участника нет в бд']
        if from_lvl < to_lvl:
            return [True, '']
        else:
            return [False, 'Не хватает уровня роли']

    if args[0] in [7]: #unban
        ban_to = args[2]['links']['intruder_id']
        try:
            ban_from = Ban.get(Ban.id_vk_id == ban_to).from_id_vk_id
            unban_from = args[2]['links']['from_id']
            ban_from_lvl = get_lvl(ban_from)
            unban_from_lvl = get_lvl(unban_from)
        except DoesNotExist:
            return [False, 'Такого участника нет в списке забаненных']
        if unban_from_lvl <= ban_from_lvl:
            return [True, '']
        else:
            return [False, 'Не хватает уровня роли']

    if args[0] in [9]: #unmute
        ban_to = args[2]['links']['intruder_id']
        try:
            mute_from = Mute.get(Mute.id_vk_id == ban_to).from_id_vk_id
            unmute_from = args[2]['links']['from_id']
            print(f'MUTE FROM: {mute_from}\nUNMUTE FROM: {unmute_from}')
            mute_from_lvl = get_lvl(mute_from)
            unmute_from_lvl = get_lvl(unmute_from)
        except DoesNotExist:
            return [False, 'Такого участника нет в списке забаненных']
        if unmute_from_lvl <= mute_from_lvl:
            return [True, '']
        else:
            return [False, 'Не хватает уровня роли']

    if args[0] in [10]:
        pass
    if args[0] in [11]:
        pass
    if args[0] in [12]:
        pass
    if args[0] in [13]:
        pass
    if args[0] in [14]:
        pass
    if args[0] in [15]:
        pass
    if args[0] in [16]:
        pass
    if args[0] in [17]:
        pass
    if args[0] in [18]:
        pass
    if args[0] in [19]:
        pass
    if args[0] in [20]:
        pass
    if args[0] in [21]:
        pass
    if args[0] in [22]:
        pass
    if args[0] in [23]:
        pass
    if args[0] in [24]:
        pass
    if args[0] in [25]:
        pass