import pylibftdi
import time


class USBBridge:
    FLOW_CONTROL_MODES = {
        "none": 0x0000,
        "RTS/CTS": 0x0100,
        "DTR/DSR": 0x0200,
        "XON/XOFF": 0x0300
    }
    DATA_BYTES = {
        "8": 8,
        "7": 7
    }
    STOP_BITS = {
        "1": 0,
        "2": 1
    }
    PARITY = {
        "none": 0,
        "odd": 1,
        "even": 2,
        "mark": 3,
        "space": 4
    }
    PURGE_CHANNELS = {
        "rx": 1,
        "tx": 2
    }

    def get_device(self):
        try:
            dev = pylibftdi.Device()
            dev.ftdi_fn.ftdi_set_baud_rate(115200)

            dev.ftdi_fn.ftdi_set_data_charecteristics(self.DATA_BYTES["8"], self.STOP_BITS["1"], self.PARITY["none"])

            time.sleep(0.05)
            dev.ftdi_fn.ftdi_purge(self.PURGE_CHANNELS["rx"] | self.PURGE_CHANNELS["tx"])
            time.sleep(0.05)

            dev.ftdi_fn.reset_device()
            dev.ftdi_fn.set_flow_control(self.FLOW_CONTROL_MODES["RTS/CTS"], 0, 0)
            dev.ftdi_fn.set_rts()

            return dev
        except pylibftdi.FtdiError as e:
            raise e


usb_bridge = USBBridge()
device = usb_bridge.get_device()

print(device)
