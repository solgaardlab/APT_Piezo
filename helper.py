def debug_print(title, message):
    # Prepare printable versions of the message
    message_hex = message.hex()

    # Convert byte array message to hex
    # Convert hex to integer
    # Convert integer to binary
    # Strip the '0b' from the binary string, we don't need it
    message_bin = bin(int(message.hex(), 16))[2:].zfill(48)

    print('|--- ' + title + ' ' + ('-' * (53 - (len(title) + 5))) + '|')
    print('|                                                     |')
    print('| byte 1 | byte 2 | byte 3 | byte 4 | byte 5 | byte 6 |')
    print('|-----------------------------------------------------|')

    print('|', end='')
    for x in range(6):
        end = (x + 1) * 8
        indent = end - 8

        if x != 5:
            print(message_bin[indent:end] + '|', end='')
        else:
            print(message_bin[indent:end] + '|')
    print('|-----------------------------------------------------|')

    print('|', end='')
    for x in range(6):
        end = (x + 1) * 2
        indent = end - 2

        if x == 0:
            indent = 0
            end = 2

        if x != 5:
            print('  0x' + message_hex[indent:end] + '  |', end='')
        else:
            print('  0x' + message_hex[indent:end] + '  |')

    print('|-----------------------------------------------------|')


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
