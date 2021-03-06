import numpy as np


class Fonts:
    text_5px = 0x72  # Large letters only
    text_6px = 0x66
    text_7px = 0x65
    text_7px_bold = 0x64
    text_9px = 0x75
    text_9px_bold = 0x70
    text_9px_bolder = 0x62
    text_13px = 0x73
    text_13px_bold = 0x69
    text_13px_bolder = 0x61
    text_13px_boldest = 0x79
    text_15px = 0x71
    text_16px = 0x68
    text_16px_bold = 0x78
    text_16px_bolder = 0x74
    symbols = 0x67

class Text:
    def __init__(self, text, horizontal=0, vertical=0, font=Fonts.text_5px):
        self.text = text
        self.horizontal = horizontal
        self.vertical = vertical
        self.font = font

def get_header():
    header = bytearray()
    header.append(0xff)  # Header
    header.append(0x06)  # Address, can also be 0x06 and 0x07 OSOITE 0x06
    header.append(0xa2)  # Text node
    # Display width
    header.append(0xd0)
    header.append(160) #Nayto leveys
    # Display height
    header.append(0xd1)
    header.append(24) #Nayton korkeus

    return header


def add_trailer(msg):
    check_sum = 0
    for i in msg[1:]:
        check_sum = check_sum + i

    check_sum = check_sum & 0xff
    if check_sum == 0xfe:
        msg.append(0xfe)
        msg.append(0x00)
    elif check_sum == 0xff:
        msg.append(0xfe)
        msg.append(0x01)
    else:
        msg.append(check_sum)

    msg.append(0xff)
    return msg


def clear_display():
    pix_map = np.zeros([160, 24], dtype=np.bool)

    msg = get_header()

    lines = [5, 10, 15, 20, 25]

    for line in lines:
        # Horizontal offset:
        msg.append(0xd2)
        msg.append(0)

        # Vertical offset:
        msg.append(0xd3)
        msg.append(line-1)

        # Bitmap Font
        msg.append(0xd4)
        msg.append(0x77)

        for horisontal in range(160):
            bit_array = pix_map[horisontal, line-lines[0]:line]

            val = sum(bit_array[i] << i for i in range(len(bit_array)))
            val = val | 0x20
            msg.append(val)

    msg = add_trailer(msg)
    return msg


def set_pixels(pixels):
    pix_map = np.zeros([160, 24], dtype=np.bool)
    pix_map[pixels] = True

    mask = np.bitwise_or(pix_map, set_pixels.display_state)
    set_pixels.display_state = pix_map.copy()

    msg = get_header()
    lines = [5, 10, 15, 20, 25]
    for line in lines:
        # Vertical offset:
        msg.append(0xd3)
        msg.append(line-1)

        # Bitmap Font
        msg.append(0xd4)
        msg.append(0x77)

        horisontal_skip = True
        for horisontal in range(160):
            if mask[horisontal, line-lines[0]:line].any():
                # Horizontal offset:
                if horisontal_skip:
                    msg.append(0xd2)
                    msg.append(horisontal)
                    horisontal_skip = False

                bit_array = pix_map[horisontal, line-lines[0]:line]

                val = sum(bit_array[i] << i for i in range(len(bit_array)))
                val = val | 0x20
                msg.append(val)
            else:
                horisontal_skip = True

    msg = add_trailer(msg)
    return msg


set_pixels.display_state = np.zeros([160, 24], dtype=np.bool)


def set_text(text_str, horizontal_offset, vertical_offset, font):
    msg = get_header()

    # Horizontal offset:
    msg.append(0xd2)
    msg.append(horizontal_offset)

    # Vertical offset:
    msg.append(0xd3)
    msg.append(vertical_offset)

    # Font3
    msg.append(0xd4)
    msg.append(font)

    msg.extend(text_str.encode('utf-8'))

    msg = add_trailer(msg)
    return msg

def set_texts(text_list):
    msg = get_header()

    while len(text_list) > 0:
        text_object = text_list.pop(0)

        # Horizontal offset:
        msg.append(0xd2)
        msg.append(text_object.horizontal)

        # Vertical offset:
        msg.append(0xd3)
        msg.append(text_object.vertical)

        # Font3
        msg.append(0xd4)
        msg.append(text_object.font)

        msg.extend(text_object.text.encode('utf-8'))

    msg = add_trailer(msg)
    return msg

