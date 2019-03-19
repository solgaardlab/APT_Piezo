from model import Model
import helper


class MessageGenerator:
    # Get model instance since it contains the current working source and destination
    model = Model.get_instance()

    def gen_header(self, message_type, params):
        # Split message into 2 bytes because Python
        # Doesn't allow for values bigger than 256 to be put in byte arrays
        message_bytes = helper.split_bytes_little_endian(message_type)
        action = message_bytes[0]
        message = message_bytes[1]

        # If the params aren't a list it is the data size for the following data packet
        if type(params) != list:
            # Split data size into lo and hi bytes because Python
            # Doesn't allow for values bigger than 256 to be put in byte arrays
            data_size_bytes = helper.split_bytes_little_endian(params)
            data_size_hi = data_size_bytes[1]
            data_size_lo = data_size_bytes[0]

            # Destination bitwise OR'd with 0x80 to integer, flip MSB to 1 to indicate data packet.
            destination = helper.MSB_to_one(self.model.destination | 0x80)

            # Create byte array of all separate bytes, this is the header
            return bytearray([action, message, data_size_lo, data_size_hi, destination, self.model.source])

        # Create byte array of all separate bytes, this is the header
        return bytearray([action, message, params[0], params[1], self.model.destination, self.model.source])

    def gen_data(self, data_definitions):
        result = bytearray()

        for data_def in data_definitions:
            size = data_def[0]
            data = data_def[2]


message_generator = MessageGenerator()
message_ident = message_generator.gen_header(0x0223, [0x00, 0x00])

helper.debug_print('MSG_MOD_IDENTIFY', message_ident)
