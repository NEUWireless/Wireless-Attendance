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

GOOGLE_SPREADSHEET_NAME = "Wireless Attendance Tracking"

DEFAULT_GOOGLE_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'wireless-attendance-credentials.json')

LOGGING_FILE = 'wireless-attendance.log'

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
    },
    'formatters': {
        'default': {
            'format': "[{asctime}] {levelname}:{name}({process}) - {message}",
            'style': '{',
        }
    },
    'loggers': {
        'wireless_attendace': {
            'level': 'DEBUG',
            'handlers': ['default_file'],
            'propagate': False,
        },
    },
}
