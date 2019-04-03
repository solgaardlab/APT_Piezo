from string import Template
from protocol.message import Message
import math


class Module:

    def __init__(self, controller, channel):
        # Save reference to controller interface
        self.controller = controller

        # Create template string for channel, get channel value from controller interface's constant
        destination = Template('bay${channel}')
        self.destination = controller.SOURCE_DESTINATION[destination.substitute(channel=channel)]

        # Build a message that sets the Piezo to zero position
        self.zero()

        # Build a message that sets the Piezo control mode to closed loop mode
        poscontrol_message = Message(0x0640, [0x01, 0x02], self.destination)
        self.controller.write_data(poscontrol_message.get_data())

    def move(self, travel_percentage):
        # Build a pz_set_outputpos message (0x0646), it has a data size of 4 (0x04)
        if not self.move_message:
            self.move_message = Message(0x0646, 0x04, self.destination)

        # Clear previous message data
        self.move_message.clear_data()

        # output position is a 0 - 100% value based on 0 - 32767 decimal values
        # calculates the total movement value and creates a hex value from this
        outputpos = math.floor(travel_percentage * 32767)

        # Add the channel indent to the message, 01 by default, 2 bytes in size
        self.move_message.add_word(0x0001)
        # Ad the output position to the message, as calculated, 2 bytes in size
        self.move_message.add_word(outputpos)

        self.controller.write_data(self.move_message.get_data())

    def zero(self):
        # Build a message that sets the Piezo to zero position if it doesn't yet exist
        if not self.zeropos_message:
            self.zeropos_message = Message(0x0658, [0x01, 0x00], self.destination)

        self.controller.write_data(self.zeropos_message.get_data())
