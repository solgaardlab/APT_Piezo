from string import Template
from protocol.message import Message
import math


class Module:

    def __init__(self, controller, channel, max_travel):
        # Save reference to controller interface
        self.controller = controller

        # Create template string for channel, get channel value from controller interface's constant
        destination = Template('bay${channel}')
        self.destination = controller.SOURCE_DESTINATION[destination.substitute(channel=channel)]

        # Supported messages, not initialised yet, they're initialised as neededd
        self.closed_loop_enable_message = None
        self.closed_loop_disable_message = None
        self.zeropos_message = None
        self.move_message = None

        # Set maximum piezo travel
        self.max_travel = max_travel

        # Enable closed loop mode, set piezo to zero
        self.set_closed_loop(True)
        self.zero()

    def move(self, travel_micron):
        # Build a pz_set_outputpos message (0x0646), it has a data size of 4 (0x04)
        if self.move_message is None:
            self.move_message = Message(0x0646, 0x04, self.destination)

        # Clear previous message data
        self.move_message.clear_data()

        # limit movement between maximum movement and zero
        travel_micron = max(min(self.max_travel, travel_micron), 0)

        # output position is a 0 - 100% value based on 0 - 32767 decimal values
        # calculates the total movement value and creates a hex value from this
        travel_percentage = travel_micron / self.max_travel
        outputpos = math.floor(travel_percentage * 32767)

        # Add the channel indent to the message, 01 by default, 2 bytes in size
        self.move_message.add_word(0x0001)
        # Ad the output position to the message, as calculated, 2 bytes in size
        self.move_message.add_word(outputpos)

        self.controller.write_data(self.move_message.get_data())

    def zero(self):
        # Build a message that sets the Piezo to zero position if it doesn't yet exist
        if self.zeropos_message is None:
            self.zeropos_message = Message(0x0658, [0x01, 0x00], self.destination)

        self.controller.write_data(self.zeropos_message.get_data())

    def set_closed_loop(self, enable):
        if self.closed_loop_disable_message is None:
            # Build a message that sets the Piezo control mode to open loop mode
            self.closed_loop_disable_message = Message(0x0640, [0x01, 0x01], self.destination)
        if self.closed_loop_enable_message is None:
            # Build a message that sets the Piezo control mode to closed loop mode
            self.closed_loop_enable_message = Message(0x0640, [0x01, 0x02], self.destination)

        if enable:
            self.controller.write_data(self.closed_loop_enable_message.get_data())
        else:
            self.controller.write_data(self.closed_loop_disable_message.get_data())
