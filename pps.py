import visa
from ThorlabsPM100 import ThorlabsPM100


class PPS:
    def __init__(self):
        rm = visa.ResourceManager()
        inst = rm.open_resource('USB0::0x0000::0x0000::xxxxxxxxx::INSTR',
                                term_chars='\\n', timeout=1)
        self.module = ThorlabsPM100(inst=inst)

    def read(self):
        return self.module.read()
