import math

def debug_print(title, message):
    # Prepare printable versions of the message
    message_hex = message.hex()

    # Convert byte array message to hex
    # Convert hex to integer
    # Convert integer to binary
    # Strip the '0b' from the binary string, we don't need it
    message_bin = bin(int(message_hex, 16))[2:]

    # Calculate the byte size of the message for proper printing later
    amount_bytes = math.ceil(len(message_bin) / 8)
    message_bin = message_bin.zfill(amount_bytes * 8)

    # Calculate the total length of the table line
    length_of_line = 2 + (amount_bytes * 8) + (amount_bytes - 2)
    # Calculate the amount of trailing '-' after the title
    trailing = length_of_line - (6 + len(title))

    # Print the header including title and byte indicators
    print('|--- ' + title + ' ' + ('-' * trailing) + '|')
    print('|', end='')
    for x in range(amount_bytes):
        if x != amount_bytes - 1:
            print(' byte ' + str(x + 1) + ' |', end='')
        else:
            print(' byte ' + str(x + 1) + ' |')
    print('|' + '-' * (length_of_line - 1) + '|')

    # Print the message per byte in binary format
    print('|', end='')
    for x in range(amount_bytes):
        indent = x * 8
        end = indent + 8

        if x != amount_bytes - 1:
            print(message_bin[indent:end] + '|', end='')
        else:
            print(message_bin[indent:end] + '|')
    print('|' + '-' * (length_of_line - 1) + '|')

    # Print the message per byte in hex format
    print('|', end='')
    for x in range(amount_bytes):
        indent = x * 2
        end = indent + 2

        if x != amount_bytes - 1:
            print('  0x' + message_hex[indent:end] + '  |', end='')
        else:
            print('  0x' + message_hex[indent:end] + '  |')
    print('|' + '-' * (length_of_line - 1) + '|')

def MSB_to_one(value):
    # MSB is already set to 1, return original value
    if value >= (2 ** 7):
        return value

    # To set the MSB to 1 we add 2 to the power of 8 (one byte) - 1 as an integer value.
    return value + (2 ** 7)


def split_bytes_little_endian(value):
    # Split value above 256 over two bytes
    # First byte 0 - 7 (as seen from the right) bitwise AND with the value and 11111111
    lo = value & 0x00ff
    # Second byte 7 - 15 (as seen from the right) bit shift to the right 8 times
    hi = value >> 8

    return lo, hi
