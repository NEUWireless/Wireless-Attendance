"""
Package settings.
"""

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
"""
Dictionary describing the structure the the Google Sheets spreadsheets
that this package interfaces with.
"""

CARD_READER_REPEAT_TIMEOUT = timedelta(seconds=10)
"""
The period of time that must be elapsed between two instances of the same
card UUID being read.

Repeated reads that occur in less than this amount of time will be ignored.
"""

CARD_READER_READ_TIMEOUT = timedelta(seconds=1)
"""
The duration of time for which the card reader will search for a card before
concluding that no card was found.
"""

CARD_READER_DELAY = timedelta(seconds=0.5)
"""
The duration of time that the process will remain idle between attempted card
reads.
"""

DEFAULT_GOOGLE_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'wireless-attendance-credentials.json')
"""
The default location to search for the google credentials file if no credentials
file is specified via the command line.
"""

LOGGING_FILE = os.path.join(BASE_DIR, 'wireless-attendance.log')
"""
The path to the log file used by this package.
"""

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
