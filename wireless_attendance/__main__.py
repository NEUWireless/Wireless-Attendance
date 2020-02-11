import argparse
import logging.config
import sys
import time
from datetime import datetime

import gspread

from . import google_utils, nfc, settings

logging.config.dictConfig(settings.LOGGING)

logger = logging.getLogger(__name__)


def make_parser() -> argparse.ArgumentParser:
    """Construct the argument parser for this script."""
    parser = argparse.ArgumentParser(
        description="Wireless Attendance Tracking",
        prog='wireless_attendance',
    )

    parser.add_argument(
        '--credentials-file',
        type=str,
        help="""The path to the Google Service Account credentials.
        See the gspread documentation for information on how to obtain a credentials file: https://gspread.readthedocs.io/en/latest/oauth2.html
        """,
        default=settings.DEFAULT_GOOGLE_CREDENTIALS_FILE,
    )

    spreadsheet_id_group = parser.add_mutually_exclusive_group(required=True)
    spreadsheet_id_group.add_argument(
        '--spreadsheet-id',
        type=str,
        help="The ID of the spreadsheet to store attendance data."
    )
    spreadsheet_id_group.add_argument(
        '--spreadsheet-name',
        type=str,
        help="The name of the spreadsheet to store attendance data.",
    )
    spreadsheet_id_group.add_argument(
        '--spreadsheet-url',
        type=str,
        help="The complete URL to the spreadsheet to store attendance data.",
    )
    spreadsheet_id_group.add_argument(
        '-no-sheet',
        action='store_true',
        help="If specified, the process will not attempt to connect to the "
             "Google Sheets API. All card reads will still be written the the logger."
    )

    parser.add_argument(
        '-mock-reader',
        action='store_true',
        help="If specified, the process will not attempt to access the card reader. "
             "Mock UUIDs will be read from stdin."
    )

    return parser


def open_spreadsheet_from_args(google_client: gspread.Client, args):
    """
    Attempt to open the Google Sheets spreadsheet specified by the given
    command line arguments.
    """
    if args.spreadsheet_id:
        logger.info("Opening spreadsheet by ID '{}'".format(args.spreadsheet_id))
        return google_client.open_by_key(args.spreadsheet_id)
    elif args.spreadsheet_url:
        logger.info("Opening spreadsheet by URL '{}'".format(args.spreadsheet_url))
        return google_client.open_by_url(args.spreadsheet_url)
    elif args.spreadsheet_name:
        logger.info("Opening spreadsheet by name '{}'".format(args.spreadsheet_name))
        return google_client.open(args.spreadsheet_name)
    else:
        raise ValueError("Invalid command line arguments - no spreadsheet identifier was provided")


def run_attendance_tacking(card_reader: nfc.BaseHuskyCardReader, card_callback):
    """Run the read-card write-id procedure indefinitely."""
    delay = settings.CARD_READER_DELAY
    while True:
        uid = card_reader.read_card()
        if uid:
            card_callback(uid)
        time.sleep(delay.total_seconds())


def main(raw_args):
    parser = make_parser()
    args = parser.parse_args(raw_args)

    if args.mock_reader:
        logging.debug("Using mock card reader")
        card_reader = nfc.MockHuskyCardReader()
    else:
        logging.debug("Using NFC card reading. Attempting connection...")
        card_reader = nfc.HuskyCardReader(settings.CARD_READER_REPEAT_TIMEOUT)

    if args.no_sheet:
        logging.debug("Running with Google Sheets API disabled")

        def card_callback(card_uuid):
            logger.info("Read card with ID: {}".format(card_uuid))
    else:
        logging.debug("Running with live Google Sheet. Attempting Google Sheets API connecting...")
        google_client = google_utils.get_google_client(args.credentials_file)
        try:
            spreadsheet = google_utils.WirelessAttendanceSpreadsheet(
                open_spreadsheet_from_args(google_client, args)
            )
        except gspread.SpreadsheetNotFound:
            logger.exception("Failed to open spreadsheet : no such sheet exists")
            raise

        def card_callback(card_uuid):
            logging.debug("Writing access with card '{}' to the Google Sheet".format(card_uuid))
            spreadsheet.write_access_log(card_uuid, datetime.now())

    run_attendance_tacking(card_reader, card_callback)


main(sys.argv[1:])
