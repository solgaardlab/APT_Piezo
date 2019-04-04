from interface.controller import Controller
from interface.module import Module
from protocol.message import Message
from string import Template


class APT:
    def __init__(self):
        self.controller = Controller()

        # Last byte of response is the amount of channels available, each channel is a motor module
        for x in range(10):
            bay_name = Template('bay$indent')
            bay_name = bay_name.substitute(indent=x)
            bay_code = self.controller.SOURCE_DESTINATION[bay_name]

            destination = self.controller.SOURCE_DESTINATION["rack/motherboard"]
            bay_used_message = Message(0x0060, [bay_code, 0x00], destination)

            self.controller.write_data(bay_used_message.get_data())
            response = self.controller.read_data(6, 1)

            if response[3] == 0x01:
                module_name = Template('module$indent')
                setattr(self, module_name.substitute(indent=x), Module(self.controller, x))
