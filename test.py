import usb_bridge as bridge
import message_generator
import helper

# usb = bridge.USBBridge()
# device = usb.get_device()

mgen = message_generator.MessageGenerator()
message_ident = mgen.gen_header(0x0005, [0x00, 0x00])

helper.debug_print('MSG_HW_REQ_INFO', message_ident)

# device.write_data(message_ident)

# helper.debug_print('RESPONSE', device.read_data(90))