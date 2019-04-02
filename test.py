from interface import controller, module
from protocol import message_builder

controller = controller.Controller()
module1 = module.Module(controller, 0)
module2 = module.Module(controller, 2)
module3 = module.Module(controller, 3)

mbuilder = message_builder.MessageBuilder()
message = mbuilder.gen_header(0x0005, [0x00, 0x00], 0x11)

controller.write_data(message)
controller.read_data(90, 1)
