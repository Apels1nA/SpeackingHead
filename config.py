import os


development = {
    'project': {
        'project': 'speackinghead',
        'version': '0.0.0',
        'mode': 'development'
    },
    'db': {
        'db': 'speackinghead',
        'host': 'localhost',
        'user': 'postgres',
        'password': '',
        'port': '5432'
    },
    'api': {
        'api_key': 'e89cf97cc3b7fa7a0d3b00c53026e1ac7dc72b030d9f041757b2f397440eaf80bf89633451483cd0337ec'
    },
    'path': '/Users/ilyamiskelo/Projects/SpeackingHead/vk_api'
}

production = {
    'project': {
        'project': 'speackinghead',
        'version': '0.0.0',
        'mode': 'production'
    },
    'db': {
        'host': 'localhost',
        'db': 'speackinghead',
        'user': 'webuser',
        'password': '',
        'port': '5432'
    },
    'api': {
        'api_key': 'e89cf97cc3b7fa7a0d3b00c53026e1ac7dc72b030d9f041757b2f397440eaf80bf89633451483cd0337ec'
        }
}

app_mode = os.environ.get('APP_MODE', 'develop')
is_production = app_mode == 'production'
config = production if is_production else development
