import os

sbox = [[0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0,
            0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc,
            0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a,
            0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0,
            0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b,
            0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85,
            0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5,
            0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17,
            0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88,
            0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c,
            0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9,
            0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6,
            0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e,
            0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94,
            0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]]

RCON = [0x00000000, 0x01000000, 0x02000000,
        0x04000000, 0x08000000, 0x10000000,
        0x20000000, 0x40000000, 0x80000000,
        0x1b000000, 0x36000000]

'''
Code for key expansion
'''

def generate_key():
    '''
    generate random key,  not perfect but good enough for cryptography
    '''
    key = os.urandom(32)
    return key


def key_expansion(key):
    '''
    expand key to be 15x128 (aes-256)
    '''
    w = [()]*44

    for i in range(4):
        w[i] = key[i*4:(i+1)*4]

    for i in range(4, 44):
        prev = w[i-1]

        if i % 4 == 0:
            prev = Rotword_Function(prev)
            prev = Subword_Function(prev)

            rcon = RCON[i // 4]
            prev_int = int(''.join(prev), 16)
            prev_int ^= rcon

        prev_int ^= int(''.join(w[i-4]), 16)

        prev_hex = format(prev_int, '08x')

        prev_list = [prev_hex[j:j+2] for j in range(0, len(prev_hex), 2)]

        w[i] = prev_list

    return w


def convert_to_binary(text):
    binary_words = []
    for word in text:
        binary_word = ''.join(format(int(byte, 16), '04b') for byte in word)
        binary_words.append(binary_word)
    return binary_words


def binary_to_hex(binary_words):
    hex_words = []
    for binary_word in binary_words:
        hex_word = ""
        for i in range(0, len(binary_word), 8):
            byte = binary_word[i:i+8]
            hex_byte = format(int(byte, 2), '02x')
            hex_word += hex_byte
        hex_words.append(hex_word)
    return hex_words


def Rotword_Function(word):
    return word[1:] + word[:1]


def Subword_Function(word):
    for i in range(len(word)):
        curr = [c for c in word[i]]
        x, y = curr
        x = int(x, 16)
        y = int(y, 16)
        word[i] = format(sbox[x][y], '02x')
    return word


def add_padding(plaintext, block_size=16):
    pad_length = block_size - (len(plaintext) % block_size)
    padding = bytes([pad_length] * pad_length)
    return plaintext + padding


def convert_text_to_blocks(text):
    text = text.encode('utf-8')
    text = add_padding(text)
    text_blocks = [text[i:i+16] for i in range(0, len(text), 16)]
    formatted_blocks = []

    for block in text_blocks:
        formatted_block = []
        for i in range(0, len(block), 4):
            formatted_word = []
            for j in range(4):
                formatted_word.append(format(block[i+j], '02x'))
            formatted_block.append(formatted_word)
        formatted_blocks.append(formatted_block)

    return formatted_blocks


def sub_bytes(block):
    for i in range(4):
        block[i] = Subword_Function(block[i])
    return block


def shift_rows(block):
    b = block
    b[1][0], b[1][1], b[1][2], b[1][3] = b[1][1], b[1][2], b[1][3], b[1][0]
    b[2][0], b[2][1], b[2][2], b[2][3] = b[2][2], b[2][3], b[2][0], b[2][1]
    b[3][0], b[3][1], b[3][2], b[3][3] = b[3][3], b[3][0], b[3][1], b[3][2]
    return b

# this code is a modified version of boppreh function to performt he galois multiplication,  who took it from somewhere else. original source not known,  link: https://github.com/boppreh/aes/blob/master/aes.py
def xtime(a): return (((a << 1) ^ 0x1B) & 0xFF) if (a & 0x80) else (a << 1)


def mix_single_column(a):

    t = int(a[0], 16) ^ int(a[1], 16) ^ int(a[2], 16) ^ int(a[3], 16)
    u = int(a[0], 16)

    a0, a1, a2, a3 = int(a[0], 16), int(a[1], 16), int(a[2], 16), int(a[3], 16)

    a0 ^= t ^ xtime(int(a[0], 16) ^ int(a[1], 16))
    a1 ^= t ^ xtime(int(a[1], 16) ^ int(a[2], 16))
    a2 ^= t ^ xtime(int(a[2], 16) ^ int(a[3], 16))
    a3 ^= t ^ xtime(int(a[3], 16) ^ u)

    return [hex(a0)[2:], hex(a1)[2:], hex(a2)[2:], hex(a3)[2:]]


def mix_columns(block):
    for i in range(4):
        block[i] = mix_single_column(block[i])
    return block


def add_round_key(blocked_text, key):
    for i in range(len(blocked_text)):
        working_block = blocked_text[i]
        complete_bytes = []
        for byte in working_block:
            byte = int(''.join(byte), 16)
            byte ^= int(''.join(key), 16)
            hex_c = format(byte, '08x')
            hex_c = [hex_c[j:j+2]
                     for j in range(0, len(hex_c), 2)]
            complete_bytes.append(hex_c)
        blocked_text[i] = complete_bytes
    return blocked_text


def encrypt_text(text, key):
    key_list = key_expansion(key)
    blocked_text = convert_text_to_blocks(text)

    # setup round
    key = key_list[0]
    blocked_text = add_round_key(blocked_text, key)

    # main_rounds
    for key in key_list[1:-1]:
        blocked_text = [sub_bytes(block) for block in blocked_text]
        blocked_text = [shift_rows(block) for block in blocked_text]
        blocked_text = [mix_columns(block) for block in blocked_text]
        blocked_text = add_round_key(blocked_text, key)
    # final round

    key = key_list[-1]
    blocked_text = [sub_bytes(block) for block in blocked_text]
    blocked_text = [shift_rows(block) for block in blocked_text]
    blocked_text = add_round_key(blocked_text, key)

    # format data
    encrypted_string = []
    for block in blocked_text:
        block_text = []
        for row in block:
            block_text.append(''.join(row))
        encrypted_string.append(''.join(block_text))

    return ''.join(encrypted_string)


key = ["0f", "15", "71", "c9", "47", "d9", "e8", "59",
       "0c", "b7", "ad", "d6", "af", "7f", "67", "98"]

text = 'Text to be encrypted'  

print(encrypt_text(text, key))
