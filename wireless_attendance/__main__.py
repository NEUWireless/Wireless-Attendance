import argparse
import logging
import sys
import time
from datetime import datetime

import gspread

from . import google_utils, nfc, settings

logger = logging.getLogger(__name__)


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Wireless Attendance Tracking'
    )

    parser.add_argument('--credentials-file', type=str,
        help="""The path to the Google Service Account credentials
        See the gspread documentation for information on how to obtain a credentials file: https://gspread.readthedocs.io/en/latest/oauth2.html
        """,
        default=settings.DEFAULT_GOOGLE_CREDENTIALS_FILE,
    )

    spreadsheet_id_group = parser.add_mutually_exclusive_group(required=True)
    spreadsheet_id_group.add_argument('--spreadsheet-id', type=str)
    spreadsheet_id_group.add_argument('--spreadsheet-name', type=str)
    spreadsheet_id_group.add_argument('--spreadsheet-url', type=str)
    spreadsheet_id_group.add_argument('-no-sheet', action='store_true')

    parser.add_argument('-mock-reader', action='store_true')

    return parser


def open_spreadsheet_from_args(google_client: gspread.Client, args):
    if args.spreadsheet_id:
        return google_client.open_by_key(args.spreadsheet_id)
    elif args.spreadsheet_url:
        return google_client.open_by_url(args.spreadsheet_url)
    elif args.spreadsheet_name:
        return google_client.open(args.spreadsheet_name)
    else:
        raise ValueError("Invalid command line arguments - no spreadsheet identifier was provided")


def run_attendance_tacking(card_reader: nfc.BaseHuskyCardReader, card_callback):
    delay = settings.CARD_READER_DELAY
    while True:
        card_callback(card_reader.read_card())
        time.sleep(delay.microseconds / 1e6)


def main(raw_args):
    parser = make_parser()
    args = parser.parse_args(raw_args)

    if args.mock_reader:
        card_reader = nfc.MockHuskyCardReader()
    else:
        card_reader = nfc.HuskyCardReader(settings.CARD_READER_REPEAT_TIMEOUT)

    if args.no_sheet:
        def card_callback(card_uuid):
            logger.info(f"Read card with ID: {card_uuid}")
    else:
        google_client = google_utils.get_google_client(args.credentials_file)
        try:
            spreadsheet = google_utils.WirelessAttendanceSpreadsheet(
                open_spreadsheet_from_args(google_client, args)
            )
        except gspread.SpreadsheetNotFound:
            logger.exception("Failed to open spreadsheet : no such sheet exists")
            raise

        def card_callback(card_uuid):
            spreadsheet.write_access_log(card_uuid, datetime.now())

    run_attendance_tacking(card_reader, card_callback)


main(sys.argv[1:])
