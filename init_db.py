import psycopg2
from config import config

print(config['db'])

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
    (14, 'createrole', 'создатьроль'),
    (15, 'droprole', 'удалитьроль'),
    (16, 'renamerole', 'переименоватьроль'),
    (17, 'who', 'кто'),
    (18, 'list', 'список'),
    (19, 'ping', 'пинг'),
    (20, 'give', 'выдать'),
    (21, 'drop', 'уволить'),
    (22, 'quit', 'уволиться'),
    (23, 'kick', 'кик'),
    (24, 'randompussy', 'рандомнаяпиздюлина'))

role = (
    (1, 'admin'),
    (2, 'moderator'),
    (3, 'user'))

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
    (22, 1, 22),

    (23, 2, 1),
    (24, 2, 2),
    (25, 2, 3),
    (26, 2, 4),
    (27, 2, 5),
    (28, 2, 6),
    (29, 2, 7),
    (30, 2, 8),
    (31, 2, 9),
    (32, 2, 10),
    (33, 2, 11),
    (34, 2, 12),
    (35, 2, 13),
    (36, 2, 17),
    (37, 2, 18),
    (38, 2, 19),
    (39, 2, 22),
    (40, 2, 23),

    (41, 3, 1),
    (42, 3, 2),
    (43, 3, 13),
    (44, 3, 17),
    (45, 3, 19))


with con:

    cur = con.cursor()

    cur.execute("TRUNCATE TABLE command CASCADE")
    query_command = "INSERT INTO command (id, name_eng, name_rus) VALUES (%s, %s, %s)"
    cur.executemany(query_command, command)

    cur.execute("TRUNCATE TABLE role CASCADE")
    query_role = "INSERT INTO role (id, role_name) VALUES (%s, %s)"
    cur.executemany(query_role, role)
    
    cur.execute("TRUNCATE TABLE roletocommand CASCADE")
    query_roletocommand = "INSERT INTO roletocommand (id, role_name_id, command_id) VALUES (%s, %s, %s)"
    cur.executemany(query_roletocommand, roletocommand)

    con.commit()
