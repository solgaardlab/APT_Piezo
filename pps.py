import visa
from ThorlabsPM100 import ThorlabsPM100


class PPS:
    def __init__(self):
        rm = visa.ResourceManager()
        inst = rm.open_resource('USB0::4883::32882::P2002697::0::INSTR', open_timeout=1)
        self.module = ThorlabsPM100(inst=inst)

        # inst = rm.open_resource('USB0::0x0000::0x0000::xxxxxxxxx::INSTR')

    def read(self):
        return self.module.read
