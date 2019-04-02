from util import helpers


class MessageBuilder:
    def gen_header(self, message_type, params, destination):
        # Split message into 2 bytes because Python
        # Doesn't allow for values bigger than 256 to be put in byte arrays
        message_bytes = helpers.split_bytes_little_endian(message_type, 2)
        action = message_bytes[0]
        message = message_bytes[1]

        # If the params aren't a list it is the data size for the following data packet
        if type(params) != list:
            # Split data size into lo and hi bytes because Python
            # Doesn't allow for values bigger than 256 to be put in byte arrays
            data_size_bytes = helpers.split_bytes_little_endian(params, 2)
            data_size_lo = data_size_bytes[0]
            data_size_hi = data_size_bytes[1]

            # Destination bitwise OR'd with 0x80 to integer, flip MSB to 1 to indicate data packet.
            destination = destination | 0x80

            # Create byte array of all separate bytes, this is the header
            return bytearray([action, message, data_size_lo, data_size_hi, destination, 0x01])

        # Create byte array of all separate bytes, this is the header
        return bytearray([action, message, params[0], params[1], destination, 0x01])

    def add_word(self, value, header):
        word_bytes = helpers.split_bytes_little_endian(value, 2)
        word_byte_lo = word_bytes[0]
        word_byte_hi = word_bytes[1]

        header.append(word_byte_lo)
        header.append(word_byte_hi)

        return header

    def add_dword(self, value, header):
        dword_bytes = helpers.split_bytes_little_endian(value, 4)

        dword_byte_0 = dword_bytes[0]
        dword_byte_1 = dword_bytes[1]
        dword_byte_2 = dword_bytes[2]
        dword_byte_3 = dword_bytes[3]

        header.append(dword_byte_0)
        header.append(dword_byte_1)
        header.append(dword_byte_2)
        header.append(dword_byte_3)

        return header

    def add_short(self, value, header):
        if value < 0:
            byte1 = hex(255)
            byte2 = hex((256 + value))
        else:
            byte1 = hex(0)
            byte2 = hex(value)

        header.append(byte2)
        header.append(byte1)

        return header
