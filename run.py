# import apt
#
#
# APT = apt.APT()
#
# controller = APT.controller
# module1 = APT.module1
# module2 = APT.module2
# module3 = APT.module3
# mbuilder = APT.mbuilder
#
# message = mbuilder.gen_header(0x0005, [0x00, 0x00], 0x11)
#
# controller.write_data(message)
# controller.read_data(90, 1)

from util import helpers
from protocol.message import Message
import math

# Test header message
message = Message(0x0658, [0x01, 0x00], 0x21)
helpers.debug_print('PZ_SET_ZERO', message.get_data())

# Test data messages
message = Message(0x0646, 0x04, 0x21)
message.add_word(0x0001)
message.add_word(math.floor(0.15 * 32767))
helpers.debug_print('PZ_SET_OUTPUTPOS', message.get_data())

# Test clearing the data
message.clear_data()
helpers.debug_print('PZ_SET_OUTPUTPOS', message.get_data())

# Test adding new data
message.add_word(0x0001)
message.add_word(math.floor(0.25 * 32767))
helpers.debug_print('PZ_SET_OUTPUTPOS', message.get_data())

