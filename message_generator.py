from model import Model


class MessageGenerator:
    # Get model instance since it contains the current working source and destination
    model = Model.get_instance()

    def gen_header(self, message_type, params):
        # Split message into 2 bytes because Python
        # Doesn't allow for values bigger than 256 to be put in byte arrays
        message_bytes = self.split_bytes_little_endian(message_type)
        action = message_bytes[0]
        message = message_bytes[1]

        # If the params aren't a list it is the data size for the following data packet
        if type(params) != list:
            # Split data size into lo and hi bytes because Python
            # Doesn't allow for values bigger than 256 to be put in byte arrays
            data_size_bytes = self.split_bytes_little_endian(params)
            data_size_hi = data_size_bytes[1]
            data_size_lo = data_size_bytes[0]

            # Destination bitwise OR'd with 0x80 to integer, flip MSB to 1 to indicate data packet.
            destination = self.set_MSB_to_one(self.model.destination | 0x80)

            # Create byte array of all separate bytes, this is the header
            return bytearray([action, message, data_size_lo, data_size_hi, destination, self.model.source])

        # Create byte array of all separate bytes, this is the header
        return bytearray([action, message, params[0], params[1], self.model.destination, self.model.source])

    def gen_data(self, data_definitions):
        result = bytearray()

        for data_def in data_definitions:
            size = data_def[0]
            data = data_def[2]

    def set_MSB_to_one(self, value):
        # MSB is already set to 1, return original value
        if value >= (2 ** 7):
            return value

        # To set the MSB to 1 we add 2 to the power of 8 (one byte) - 1 as an integer value.
        return value + (2 ** 7)

    def split_bytes_little_endian(self, value):
        # Split value above 256 over two bytes
        # First byte 0 - 7 (as seen from the right) bitwise AND with the value and 11111111
        lo = value & 0x00ff
        # Second byte 7 - 15 (as seen from the right) bit shift to the right 8 times
        hi = value >> 8

        return lo, hi

    def hex_print(self, message):
        print('HEX:\n' + message.hex() + '')

    def bin_print(self, message):
        # Convert byte array message to hex
        # Convert hex to integer
        # Convert integer to binary
        # Strip the '0b' from the binary string, we don't need it
        print('BIN:')
        print('|-------|-------|-------|-------|-------|-------|')
        print('| byte1 | byte2 | byte3 | byte4 | byte5 | byte6 |')
        print('|-------|-------|-------|-------|-------|-------|')
        print('|' + bin(int(message.hex(), 16))[2:] + '|')
        print('|-------|-------|-------|-------|-------|-------|')

    def debug_print(self, title, message):
        print('=== ' + title + ': ========================')
        message_generator.hex_print(message)
        message_generator.bin_print(message)
        print('=================================================\n')


message_generator = MessageGenerator()
message_set = message_generator.gen_header(0x0646, 0x04)
message_req = message_generator.gen_header(0x0647, [0x01, 0x00])

message_generator.debug_print('SET OUTPUT POSITION', message_set)
message_generator.debug_print('REQ OUTPUT POSITION', message_req)
