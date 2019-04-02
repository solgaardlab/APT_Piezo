import apt


APT = apt.APT()

controller = APT.controller
module1 = APT.module1
module2 = APT.module2
module3 = APT.module3
mbuilder = APT.mbuilder

message = mbuilder.gen_header(0x0005, [0x00, 0x00], 0x11)

controller.write_data(message)
controller.read_data(90, 1)
