import logging
from datetime import datetime

import gspread

from . import google_utils, nfc, settings

logger = logging.getLogger(__name__)


def main():
    google_client = google_utils.get_google_client()

    try:
        spreadsheet = google_utils.WirelessAttendanceSpreadsheet(
            google_client.open_by_key("15Bge-9tZdjdAm3T8ftFzZWL6C7cKkfl2gDs6xoNw3go")
        )
    except gspread.SpreadsheetNotFound:
        logger.exception(f"Failed to open spreadsheet {settings.GOOGLE_SPREADSHEET_NAME}: no such sheet exists")
        raise

    card_reader = nfc.HuskyCardReader(settings.CARD_READER_REPEAT_TIMEOUT)

    while True:
        card_uuid = card_reader.read_card(settings.CARD_READER_READ_TIMEOUT)
        spreadsheet.write_access_log(card_uuid, datetime.now())


main()
