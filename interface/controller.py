from pyftdi.ftdi import Ftdi
import time


class Controller:
    FLOW_CONTROL_MODES = {
        "none": '',
        "RTS/CTS": 'hw'
    }
    DATA_BYTES = {
        "8": 8,
        "7": 7
    }
    STOP_BITS = {
        "1": 1,
        "2": 2
    }
    PARITY = {
        "none": "N",
        "odd": "O",
        "even": "E",
        "mark": "M",
        "space": "S"
    }

    SOURCE_DESTINATION = {
        "host": 0x01,
        "rack/motherboard": 0x11,
        "bay0": 0x21,
        "bay1": 0x22,
        "bay2": 0x23,
        "bay3": 0x24,
        "bay4": 0x25,
        "bay5": 0x26,
        "bay6": 0x27,
        "bay7": 0x28,
        "bay8": 0x29,
        "bay9": 0x2A,
        "usb": 0x50
    }

    # Opens an FTDI connection to the USB chip inside the APT controller
    # Thorlabs/FTDI vendor code is 0x0403, product ID for the Thorlabs
    # controllers is 0xfaf0
    def __init__(self):
        connection = Ftdi()
        connection.open(vendor=0x0403, product=0xfaf0)

        # As protocol describes set the baudrate to 115200, data definition to 8 data bytes, 1 stop bit, no parity
        connection.set_baudrate(115200)
        connection.set_line_property(self.DATA_BYTES["8"], self.STOP_BITS["1"], self.PARITY["none"])

        # Pre-purge and post-purge rest, purge RX/TX buffers of the FTDI chip
        time.sleep(0.05)
        connection.purge_buffers()
        time.sleep(0.05)

        # Set flow control to RTS/CTS and flag RTS as true
        connection.set_flowctrl("hw")
        connection.set_rts(True)

        self.interface = connection

    def write_data(self, data):
        self.interface.write_data(data)

    def read_data(self, amount_bytes, retry_attempts):
        return self.interface.read_data_bytes(amount_bytes, retry_attempts)
