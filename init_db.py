import psycopg2
from config import config

con = psycopg2.connect(
        database=config['db']['db'], 
        user=config['db']['user'], 
        password=config['db']['password'], 
        host=config['db']['host'], 
        port=config['db']['port']
    )

command = (
    (1, 'help', 'помощь'),
    (2, 'online', 'онлайн'),
    (3, 'inactive', 'неактив'),
    (4, 'kickdog', 'кикдог'),
    (5, 'kickinactive', 'кикнеактив'),
    (6, 'ban', 'бан'),
    (7, 'unban', 'разбанить'),
    (8, 'mute', 'мут'),
    (9, 'unmute', 'размутить'),
    (10, 'banlist', 'банлист'),
    (11, 'mutelist', 'мутлист'),
    (12, 'role', 'роли'),
    (13, 'administration', 'администрация'),
    (14, 'who', 'кто'),
    (15, 'list', 'список'),
    (16, 'ping', 'пинг'),
    (17, 'give', 'выдать'),
    (18, 'drop', 'уволить'),
    (19, 'quit', 'уволиться'),
    (20, 'kick', 'кик'),
    (21, 'warn', 'пердупреждение'),
    (22, 'pussy', 'пиздюлина'),
    (23, 'gay', 'пидор'))

role = (
    (1, 'creator', 4), #может делать все
    (2, 'admin', 3), #не может назначать новых админов и не можеть делать ничего в сторону создателя
    (3, 'moderator', 2), #не может ban/unban/give/drop/kick
    (4, 'user', 1)) #1 12 13 14 15 16

roletocommand = (
    (1, 1, 1),
    (2, 1, 2),
    (3, 1, 3),
    (4, 1, 4),
    (5, 1, 5),
    (6, 1, 6),
    (7, 1, 7),
    (8, 1, 8),
    (9, 1, 9),
    (10, 1, 10),
    (11, 1, 11),
    (12, 1, 12),
    (13, 1, 13),
    (14, 1, 14),
    (15, 1, 15),
    (16, 1, 16),
    (17, 1, 17),
    (18, 1, 18),
    (19, 1, 19),
    (20, 1, 20),
    (21, 1, 21),

    (22, 2, 1),
    (23, 2, 2),
    (24, 2, 3),
    (25, 2, 4),
    (26, 2, 5),
    (27, 2, 6),
    (28, 2, 7),
    (29, 2, 8),
    (30, 2, 9),
    (31, 2, 10),
    (32, 2, 11),
    (33, 2, 12),
    (34, 2, 13),
    (35, 2, 14),
    (36, 2, 15),
    (37, 2, 16),
    (38, 2, 17),
    (39, 2, 18),
    (40, 2, 19),
    (41, 2, 20),
    (42, 2, 21),

    (43, 3, 1),
    (44, 3, 2),
    (45, 3, 3),
    (46, 3, 4),
    (47, 3, 8),
    (48, 3, 9),
    (49, 3, 10),
    (50, 3, 11),
    (51, 3, 12),
    (52, 3, 13),
    (53, 3, 14),
    (54, 3, 15),
    (55, 3, 16),
    (56, 3, 19),
    (57, 3, 21),
    
    (58, 3, 1),
    (59, 3, 12),
    (60, 3, 13),
    (61, 3, 14),
    (62, 3, 15),
    (63, 3, 16))


with con:

    cur = con.cursor()

    cur.execute("TRUNCATE TABLE command CASCADE")
    query_command = "INSERT INTO command (id, name_eng, name_rus) VALUES (%s, %s, %s)"
    cur.executemany(query_command, command)

    cur.execute("TRUNCATE TABLE role CASCADE")
    query_role = "INSERT INTO role (id, role_name, level) VALUES (%s, %s, %s)"
    cur.executemany(query_role, role)
    
    cur.execute("TRUNCATE TABLE roletocommand CASCADE")
    query_roletocommand = "INSERT INTO roletocommand (id, role_name_id, command_id) VALUES (%s, %s, %s)"
    cur.executemany(query_roletocommand, roletocommand)

    con.commit()
