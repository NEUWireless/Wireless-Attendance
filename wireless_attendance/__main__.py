import argparse
import logging
import sys
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


def main(raw_args):
    parser = make_parser()
    args = parser.parse_args(raw_args)

    # Example implementation - to be revised
    if not args.no_sheet:
        google_client = google_utils.get_google_client(args.credentials_file)
        try:
            spreadsheet = google_utils.WirelessAttendanceSpreadsheet(
                open_spreadsheet_from_args(google_client, args)
            )
        except gspread.SpreadsheetNotFound:
            logger.exception(f"Failed to open spreadsheet {settings.GOOGLE_SPREADSHEET_NAME}: no such sheet exists")
            raise

        card_reader = nfc.HuskyCardReader(settings.CARD_READER_REPEAT_TIMEOUT)

        while True:
            card_uuid = card_reader.read_card(settings.CARD_READER_READ_TIMEOUT)
            spreadsheet.write_access_log(card_uuid, datetime.now())

    else:
        # TODO
        print("Running without sheet to be implemented")


main(sys.argv[1:])
