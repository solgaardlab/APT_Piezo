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
            data_size_lo = data_size_bytes[0]
            data_size_hi = data_size_bytes[1]

            # Destination bitwise OR'd with 0x80 to integer, flip MSB to 1 to indicate data packet.
            destination = self.model.destination | 0x80

            # Create byte array of all separate bytes, this is the header
            return bytearray([action, message, data_size_lo, data_size_hi, destination, self.model.source])

        # Create byte array of all separate bytes, this is the header
        return bytearray([action, message, params[0], params[1], self.model.destination, self.model.source])

    def add_word(self, value, header):
        word_bytes = helper.split_bytes_little_endian(value)
        word_byte_lo = word_bytes[0]
        word_byte_hi = word_bytes[1]

        header.append(word_byte_lo)
        header.append(word_byte_hi)

    def add_dword(self, value, header):
        dword_bytes = helper.split_bytes_little_endian(value)

        dword_byte_0 = dword_bytes[0]
        dword_byte_1 = dword_bytes[1]
        dword_byte_2 = dword_bytes[2]
        dword_byte_3 = dword_bytes[3]

        header.append(dword_byte_0)
        header.append(dword_byte_1)
        header.append(dword_byte_2)
        header.append(dword_byte_3)
