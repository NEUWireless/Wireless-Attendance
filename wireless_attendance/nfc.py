import logging
from datetime import datetime, timedelta
from typing import Optional

import busio
from adafruit_pn532.spi import PN532_SPI
from digitalio import DigitalInOut

from wireless_attendance import settings

logger = logging.getLogger(__name__)


class BaseHuskyCardReader:

    def read_card(self) -> Optional[str]:
        raise NotImplemented


class HuskyCardReader(BaseHuskyCardReader):

    def __init__(self, timeout: timedelta):
        # Delay loading board module until a reader object is constructed
        # to allow testing on non-supported devies
        import board

        spi = busio.SPI(board.SCLK, board.MOSI, board.MISO)
        cs_pin = DigitalInOut(board.D5)
        self.pn532 = PN532_SPI(spi, cs_pin, debug=True)

        ic, ver, rev, support = self.pn532.get_firmware_version()
        logger.debug('Found PN532 with firmware version: {0}.{1}'.format(ver, rev))

        self.timeout = timeout
        self.card_timeouts = {}

    def read_card(self) -> Optional[str]:
        uid = self.pn532.read_passive_target(timeout=settings.CARD_READER_READ_TIMEOUT)
        if uid:
            uid = format_binary(uid)
            logger.debug(f"Found card with UID: {uid}")

        current_time = datetime.now()

        try:
            last_read = self.card_timeouts[uid]
            if current_time - last_read < self.timeout:
                return None
        except KeyError:
            # Card uuid has not been read before, so we can proceed with
            # returning it to the user
            pass

        self.card_timeouts[uid] = current_time
        return uid


class MockHuskyCardReader(BaseHuskyCardReader):

    def read_card(self) -> Optional[str]:
        card_uuid = input("Card ID: ")
        if card_uuid:
            return card_uuid
        return None


def format_binary(byte_array: bytearray):
    return ''.join('{:08b}_'.format(i) for i in byte_array)
