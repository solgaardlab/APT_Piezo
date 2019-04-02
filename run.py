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
from protocol import message_builder
import math

mbuilder = message_builder.MessageBuilder()
message = mbuilder.gen_header(0x0005, [0x00, 0x00], 0x11)
helpers.debug_print('MGMSG_IDENTIFICATION', message)

message = mbuilder.gen_header(0x0640, [0x01, 0x02], 0x21)
helpers.debug_print('PZ_SET_POSCONTROLMODE', message)

message = mbuilder.gen_header(0x0658, [0x01, 0x00], 0x21)
helpers.debug_print('PZ_SET_ZERO', message)

message = mbuilder.gen_header(0x0646, 0x04, 0x21)
message = mbuilder.add_word(0x0001, message)
message = mbuilder.add_word(math.floor(0.15 * 32767), message)
helpers.debug_print('PZ_SET_OUTPUTPOS', message)
