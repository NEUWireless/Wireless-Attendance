import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


WORKSHEETS = {
    'access_log': {
        'name': "Access Log",
        'columns': ['Card UUID', 'Timestamp'],
    },
    'name_registry': {
        'name': "Club Members",
        'columns': ['Card UUID', "Member Name"],
    },
    'statistics': {
        'name': "Attendance Statistics",
        'columns': ['Member Name', 'Total Meetings']
    }
}

CARD_READER_REPEAT_TIMEOUT = timedelta(seconds=10)

CARD_READER_READ_TIMEOUT = timedelta(seconds=1)

CARD_READER_DELAY = timedelta(seconds=0.5)

DEFAULT_GOOGLE_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'wireless-attendance-credentials.json')

LOGGING_FILE = os.path.join(BASE_DIR, 'wireless-attendance.log')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'default_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGGING_FILE,
            'formatter': 'default',
        },
        'default_stderr': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stderr',
        },
    },
    'formatters': {
        'default': {
            'format': "[{asctime}] {levelname}:{name}({process}) - {message}",
            'style': '{',
        }
    },
    'loggers': {
        '': { # root logger
            'level': 'DEBUG',
            'handlers': ['default_file', 'default_stderr'],
            'propagate': False,
        },
    },
}
