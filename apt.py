from interface.controller import Controller
from interface.module import Module
from protocol.message import Message
from string import Template

class APT:
    def __init__(self):
        self.controller = Controller()
        self.modules = dict()

        # Last byte of response is the amount of channels available, each channel is a motor module
        for x in range(10):
            destination = self.controller.SOURCE_DESTINATION["rack/motherboard"]
            bay_used_message = Message(0x0060, [x, 0x00], destination)

            self.controller.write_data(bay_used_message.get_data())
            response = self.controller.read_data(6, 3)

            if response[2] == 0x01:
                module_name = Template('module$indent')
                self.modules[module_name.substitute(indent=x+1)] = Module(self.controller, x)
