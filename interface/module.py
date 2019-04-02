from string import Template
import protocol.message_builder as message_builder
import math


class Module:

    def __init__(self, controller, channel):
        # Save reference to controller interface
        self.controller = controller

        # Create template string for channel, get channel value from controller interface's constant
        destination = Template('bay${channel}')
        self.destination = controller.SOURCE_DESTINATION[destination.substitute(channel=channel)]
        self.mbuilder = message_builder.MessageBuilder()

        # Build a message that sets the Piezo to zero position
        zeropos_message = self.mbuilder.gen_header(0x0658, [0x01, 0x00], self.destination)
        self.controller.write_data(zeropos_message)

        # Build a message that sets the Piezo control mode to closed loop mode
        poscontrol_message = self.mbuilder.gen_header(0x0640, [0x01, 0x02], self.destination)
        self.controller.write_data(poscontrol_message)

    def move(self, travel_percentage):
        # output position is a 0 - 100% value based on 0 - 32767 decimal values
        # calculates the total movement value and creates a hex value from this
        outputpos = math.floor(travel_percentage * 32767)

        # Build a pz_set_outputpos message (0x0646), it has a data size of 4 (0x04)
        message = self.mbuilder.gen_header(0x0646, 0x04, self.destination)
        # Add the channel indent to the message, 01 by default, 2 bytes in size
        message = self.mbuilder.add_word(0x0001, message)
        # Ad the output position to the message, as calculated, 2 bytes in size
        message = self.mbuilder.add_word(outputpos, message)
        self.controller.write_data(message)
