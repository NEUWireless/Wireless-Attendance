"""
Utilities for reading card IDs over NFC.
"""

import logging
from datetime import datetime, timedelta
from typing import Optional

import busio
from adafruit_pn532.spi import PN532_SPI
from digitalio import DigitalInOut

from wireless_attendance import settings

logger = logging.getLogger(__name__)


class BaseHuskyCardReader:
    """
    Base class for nfc card readers. Extend this if you want to mock a card
    reader for e.g. testing purposes.
    """

    def read_card(self) -> Optional[str]:
        raise NotImplemented


class HuskyCardReader(BaseHuskyCardReader):
    """
    Card ready that reads card IDs via NFC using the AdaFruit PN532 library.
    """

    def __init__(self, timeout: timedelta):
        # Delay loading board module until a reader object is constructed
        # to allow testing on non-supported devies
        import board

        spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
        cs_pin = DigitalInOut(board.D5)
        self.pn532 = PN532_SPI(spi, cs_pin, debug=True)

        ic, ver, rev, support = self.pn532.get_firmware_version()
        logger.info('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        self.pn532.SAM_configuration()

        self.timeout = timeout
        self.card_timeouts = {}

    def read_card(self) -> Optional[str]:
        """
        Attempt to read a card ID.

        If no card is found, or if the card found was recently scanned, return
        `None`. Otherwise, return the card's ID, formatted into a readable
        string.
        """
        uid = self.pn532.read_passive_target(timeout=settings.CARD_READER_READ_TIMEOUT.seconds)

        if not uid:
            return None

        uid = format_binary(uid)
        logger.info("Read card with UID: {}".format(uid))

        current_time = datetime.now()

        # Check if the card was read too recently
        try:
            last_read = self.card_timeouts[uid]
            if current_time - last_read < self.timeout:
                logger.debug("Card {} was read recently! Ignoring most recent read".format(uid))
                return None
        except KeyError:
            # Card uuid has not been read before, so we can proceed with
            # returning it to the user
            pass

        self.card_timeouts[uid] = current_time
        return uid


class MockHuskyCardReader(BaseHuskyCardReader):
    """
    Mock card ready to testing the Google API connection.
    """

    def read_card(self) -> Optional[str]:
        """
        Prompts and reads mock card IDs from stdin.
        """
        card_uuid = input("Card ID: ")
        if card_uuid:
            return card_uuid
        return None


def format_binary(byte_array: bytearray):
    """
    Formats the given byte array into a readable binary string.
    """
    return ''.join('{:08b}_'.format(i) for i in byte_array)
