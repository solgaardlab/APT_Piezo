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

    # Prepare strings to print
    header_str = ''
    bytes_str = ''
    hex_str = ''

    # Print the header title
    print('|--- ' + title + ' ' + ('-' * trailing) + '|')

    # Parse message to bytes and hex and add to proper strings
    for x in range(amount_bytes):
        byte_indent = x * 8
        byte_end = byte_indent + 8

        hex_indent = x * 2
        hex_end = hex_indent + 2

        if x >= 9:
            header_str += ' byte' + str(x + 1) + ' |'
        else:
            header_str += ' byte ' + str(x + 1) + ' |'

        bytes_str += message_bin[byte_indent:byte_end] + '|'
        hex_str += '  0x' + message_hex[hex_indent:hex_end].upper() + '  |'

    # Print the final strings
    print('|' + header_str)
    print('|' + '-' * (length_of_line - 1) + '|')
    print('|' + bytes_str)
    print('|' + '-' * (length_of_line - 1) + '|')
    print('|' + hex_str)
    print('|' + '-' * (length_of_line - 1) + '|\n\n')


def split_bytes_little_endian(value, size):
    if size == 2:
        index0 = value & 0x00ff
        index1 = value >> 8

        return index0, index1
    elif size == 4:
        index0 = value & 0x000000ff
        index1 = value & 0x0000ff00
        index2 = value & 0x00ff0000
        index3 = value >> 24

        return index0, index1, index2, index3
