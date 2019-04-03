from interface import controller, module
from protocol.message import Message
from string import Template


class APT:
    def __init__(self):
        self.controller = controller.Controller()

        message = Message(0x0005, [0x00, 0x00], 0x11)

        self.controller.write_data(message.get_data())
        data = self.controller.read_data(90, 1)

        # Last byte of response is the amount of channels available, each channel is a motor module
        for x in range(data[len(data) - 1]):
            module_name = Template('module$indent')
            setattr(self, module_name.substitute(indent=x), module.Module(controller, x))
