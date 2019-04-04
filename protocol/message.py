from util import helpers


class Message:
    def __init__(self, message_type, params, destination):
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
            self.header = bytearray([action, message, data_size_lo, data_size_hi, destination, 0x01])
            self.data = bytearray()
        elif len(params) > 2:
            raise AssertionError("Too many parameters for header only communication (limit 2)")
        else:
            # Create byte array of all separate bytes, this is the header
            self.header = bytearray([action, message, params[0], params[1], destination, 0x01])

    def add_word(self, value):
        if not hasattr(self, "data"):
            raise AssertionError("Cannot add data to a header only communication")
        elif value > 65535:
            raise ValueError("Value for word too high (max 65535)")
        elif value < 0:
            raise ValueError("Value for word can't be negative")

        word_bytes = helpers.split_bytes_little_endian(value, 2)
        word_byte_lo = word_bytes[0]
        word_byte_hi = word_bytes[1]

        self.data.append(word_byte_lo)
        self.data.append(word_byte_hi)

    def add_dword(self, value):
        if not hasattr(self, "data"):
            raise AssertionError("Cannot add data to a header only communication")
        elif value > 4294967295:
            raise ValueError("Value for dword too high (max 4294967295)")
        elif value < 0:
            raise ValueError("Value for dword can't be negative")

        dword_bytes = helpers.split_bytes_little_endian(value, 4)

        dword_byte_0 = dword_bytes[0]
        dword_byte_1 = dword_bytes[1]
        dword_byte_2 = dword_bytes[2]
        dword_byte_3 = dword_bytes[3]

        self.data.append(dword_byte_0)
        self.data.append(dword_byte_1)
        self.data.append(dword_byte_2)
        self.data.append(dword_byte_3)

    def add_short(self, value):
        if not hasattr(self, "data"):
            raise AssertionError("Cannot add data to a header only communication")
        elif value < -32768 or value > 32768:
            raise ValueError("Value for short out of bounds (min -32768, max 32768")
        elif value < 0:
            byte1 = 255
            byte2 = 256 + value
        else:
            byte1 = 0
            byte2 = value

        self.data.append(byte2)
        self.data.append(byte1)

    def get_data(self):
        if not hasattr(self, "data"):
            return self.header
        else:
            message = bytearray(self.header)

            for x in range(len(self.data)):
                message.append(self.data[x])

            return message

    def clear_data(self):
        if not hasattr(self, "data"):
            raise AssertionError("Cannot clear data of header only communication")

        self.data = bytearray()
