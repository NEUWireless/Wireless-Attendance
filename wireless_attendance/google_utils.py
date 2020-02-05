"""
Utilities for interfacing with the Google Sheet's API.
"""

import logging
from datetime import datetime
from typing import Set

import gspread
from oauth2client.service_account import ServiceAccountCredentials as SACreds

from . import settings

GOOGLE_ACCESS_SCOPES = [
    "https://spreadsheets.google.com/feeds",
    'https://www.googleapis.com/auth/spreadsheets',
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

_client = None
"""
Client instance used to interface with the Google Sheets API.
"""

logger = logging.getLogger(__name__)


def get_google_client(credentials_file):
    """
    Return this module's Google API client, creating a connection is one
    does not already exist.
    """
    global _client
    if not _client:
        # Connecting to google's API
        logger.info("Connecting to Google API using credentials file {}".format(credentials_file))
        creds = SACreds.from_json_keyfile_name(credentials_file, GOOGLE_ACCESS_SCOPES)
        _client = gspread.authorize(creds)

    return _client


class WirelessAttendanceSpreadsheet:
    """
    A Google Sheets spreadsheet that is being used to store club attendance
    data.
    """

    def __init__(self, spreadsheet: gspread.Spreadsheet):
        self.spreadsheet = spreadsheet
        self._validate_google_sheet()
        self.known_uuids = self.fetch_known_uuids()

    def fetch_known_uuids(self) -> Set[str]:
        """
        Retrieves all known card UUIDs from the Google Sheets API.
        """
        logger.info("Fetching all known card UUIDs from the Google Sheet")
        worksheet_handle = self.spreadsheet.worksheet(settings.WORKSHEETS['name_registry']['name'])
        # Ignore the first column value, which corresponds to the table header
        return set(worksheet_handle.col_values(1)[1:])

    def write_new_user(self, uuid: str, name: str):
        """
        Add the given ``uuid`` to the user-to-name registry worksheet,
        initializing the name field with the given ``name``.
        """
        logger.info("Registering new UUID for card {} associated with name {}".format(uuid, name))
        worksheet_handle = self.spreadsheet.worksheet(settings.WORKSHEETS['name_registry']['name'])
        worksheet_handle.insert_row([uuid, name], 2)

    def write_access_log(self, uuid: str, time: datetime):
        """
        Write a row to the access log worksheet denoting that the given card
        ``uuid`` was scanned at the given ``time``.

        If the ``uuid` has not been previously scanned, add it to the
        user-to-name registry worksheet.
        """
        if uuid not in self.known_uuids:
            self.write_new_user(uuid, "Member #{}".format(len(self.known_uuids) + 1))
            self.known_uuids.add(uuid)

        logger.debug("Write access with card {} to sheet".format(uuid))
        worksheet_handle = self.spreadsheet.worksheet(settings.WORKSHEETS['access_log']['name'])
        worksheet_handle.insert_row([uuid, time.isoformat()], 2)

    def write_statistics_sheet(self):
        ...  # TODO

    def _validate_google_sheet(self):
        """
        Check if all of the Google Sheets Worksheets are properly formatted with
        the correct column headers.

        If a worksheet does not exist, create it.
        """
        for worksheet in settings.WORKSHEETS.values():
            try:
                worksheet_handle = self.spreadsheet.worksheet(worksheet['name'])
            except gspread.WorksheetNotFound:
                logger.info("Worksheet '{}' does not exist. Creating new worksheet.".format(worksheet['name']))
                worksheet_handle = self.spreadsheet.add_worksheet(
                    worksheet['name'],
                    rows=1,
                    cols=len(worksheet['columns'])
                )

            # Fetch the column headers from the remote worksheet.
            worksheet_headers = worksheet_handle.row_values(1)

            if worksheet_headers[:len(worksheet['columns'])] != worksheet['columns']:
                logger.warning(
                    "Preexisting table found for {} with improper formatting: Fixing\n"
                    "  Expected headers: {}\n"
                    "  Found headers: {}".format(worksheet['name'], worksheet['columns'], worksheet_headers)
                )
                # TODO: move all data, not just headers
                worksheet_handle.insert_row(worksheet['columns'], 1)
                worksheet_handle.delete_row(2)
            else:
                logger.debug("Worksheet {} is formatted correctly".format(worksheet['name']))
