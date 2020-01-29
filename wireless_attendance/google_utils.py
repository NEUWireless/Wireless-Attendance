import logging

import gspread
from oauth2client.service_account import ServiceAccountCredentials as SACreds

GOOGLE_ACCESS_SCOPES = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

_client: gspread.Client = None
"""
Client instance used to interface with the Google Sheets API.
"""

logger = logging.getLogger(__name__)


def get_google_client():
    """
    Return this module's Google API client, creating a connection is one
    does not already exist.
    """
    global _client
    if not _client:
        # Connecting to google's API
        logger.debug("Connecting to Google API...")
        creds = SACreds.from_json_keyfile_name(settings.GOOGLE_CREDENTIALS_FILE, GOOGLE_ACCESS_SCOPES)
        _client = gspread.authorize(creds)

    return _client
