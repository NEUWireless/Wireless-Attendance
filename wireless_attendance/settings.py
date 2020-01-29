import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

_secrets_default = os.path.join(BASE_DIR, '.secrets.json')

with open(os.getenv('FLASK_SETTINGS_SECRETS', _secrets_default)) as secrets_file:
    SECRETS = json.load(secrets_file)


GOOGLE_SPREADSHEET_NAME = SECRETS['GOOGLE_SPREADSHEET_NAME']

GOOGLE_CREDENTIALS_FILE = SECRETS['GOOGLE_CREDENTIALS_FILE']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'default_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': SECRETS.get('log_file') or os.devnull,
            'formatter': 'default',
        },
    },
    'formatters': {
        'default': {
            'format': "[{asctime}] {levelname}:{name}({process}) - {message}",
            'style': '{',
        }
    },
    'loggers': {
        'slack2doc': {
            'level': 'DEBUG',
            'handlers': ['default_file'],
            'propagate': False,
        },
    },
}
