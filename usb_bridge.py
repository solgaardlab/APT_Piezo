from pyftdi.ftdi import Ftdi
import time


class USBBridge:
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

    def get_device(self):
        ftdi = Ftdi()
        ftdi.open(vendor=0x0403, product=0xfaf0)

        ftdi.set_baudrate(115200)
        ftdi.set_line_property(self.DATA_BYTES["8"], self.STOP_BITS["1"], self.PARITY["none"])

        time.sleep(0.05)
        ftdi.purge_buffers()
        time.sleep(0.05)

        ftdi.set_flowctrl("hw")
        ftdi.set_rts(True)

        return ftdi
