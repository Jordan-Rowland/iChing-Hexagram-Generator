from bs4 import BeautifulSoup as BSoup
from random import randint as r
from requests import get

# ['111',
# '001',
# '010',
# '100',
# '000',
# '110',
# '101',
# '011',]

hexagrams = {
 1: '111111',
 34: '001111',
 5: '010111',
 26: '100111',
 11: '000111',
 9: '110111',
 14: '101111',
 43: '011111',
 25: '111001',
 51: '001001',
 3: '010001',
 27: '100001',
 24: '000001',
 42: '110001',
 21: '101001',
 17: '011001',
 6: '111010',
 40: '001010',
 29: '010010',
 4: '100010',
 7: '000010',
 59: '110010',
 64: '101010',
 47: '011010',
 33: '111100',
 62: '001100',
 39: '010100',
 52: '100100',
 15: '000100',
 53: '110100',
 56: '101100',
 31: '011100',
 12: '111000',
 16: '001000',
 8: '010000',
 23: '100000',
 2: '000000',
 20: '110000',
 35: '101000',
 45: '011000',
 44: '111110',
 32: '001110',
 48: '010110',
 18: '100110',
 46: '000110',
 57: '110110',
 50: '101110',
 28: '011110',
 13: '111101',
 55: '001101',
 63: '010101',
 22: '100101',
 36: '000101',
 37: '110101',
 30: '101101',
 49: '011101',
 10: '111011',
 54: '001011',
 60: '010011',
 41: '100011',
 19: '000011',
 61: '110011',
 38: '101011',
 58: '011011'}


lines = {1: [0, True],
        2: [1, False],
        3: [1, False],
        4: [1, False],
        5: [1, False],
        6: [1, False],
        7: [0, False],
        8: [0, False],
        9: [0, False],
        10: [0, False],
        11: [0, False],
        12: [0, False],
        13: [0, False],
        14: [1, True],
        15: [1, True],
        16: [1, True],
}

hex1_lines = []
hex2_lines = []
hex1_url = None
hex2_url = None

def print_line(line):
    if line == '1':
        return '\t___'
    return '\t_ _'

def change(line):
    if line[0] == 0:
        return 1
    return 0

def return_reading(hexagram_number,hex_cast_number):
    global hex1_lines
    global hex2_lines
    global hex1_url
    global hex2_url
    res = get(f'https://divination.com/iching/lookup/{hexagram_number}-2/')
    soup = BSoup(res.text, 'html.parser')
    hex_name = soup.select('.entry-header > h1')[0].text
    text = soup.select('.entry-content > p')
    moving_lines_head = soup.select('.movinglines > h4')
    moving_lines_body= soup.select('.movinglines > p')
    for i in hexagrams[hexagram_number]:
        hex1_lines.append(print_line(line=i))
    if hex_cast_number == 1:
        hex1_url = res.url
        print(f'{hex_name} \n')
        for i in text:
            print(f'{i.text} \n\n')
        for head,body in list(zip(moving_lines_head, moving_lines_body))[::-1]:
            print(f'\t{head.text}')
            print(f'{body.text}')
        print('\n')
    else:
        print(f'{hex_name} \n')
        for i in text:
            print(f'{i.text} \n')
        hex2_url = res.url
        for i in hexagrams[hexagram_number]:
            hex2_lines.append(print_line(line=i))


def cast():
    hexagram_1 = []
    hexagram_2 = []
    for i in range(6):
        roll = r(1,16)
        line = lines[roll]
        changing = line[1]
        hexagram_1.append(str(line[0]))
        if changing:
            hexagram_2.append(str(change(line=line)))
        else:
            hexagram_2.append(str(line[0]))
    hexagram_1 = ''.join(hexagram_1[::-1])
    hexagram_2 = ''.join(hexagram_2[::-1])
    if hexagram_1 == hexagram_2:
        for key,value in hexagrams.items():
            if hexagram_1 == str(value):
                return_reading(hexagram_number=key,hex_cast_number=1)
        for i in hex1_lines:
            print(i)
        print('\n')
        print(hex1_url)
    else:
        for key,value in hexagrams.items():
            if hexagram_1 == str(value):
                return_reading(hexagram_number=key,hex_cast_number=1)
                print('========CHANGING TO========\n')
        for key,value in hexagrams.items():
            if hexagram_2 == str(value):
                return_reading(hexagram_number=key,hex_cast_number=2)
        for i,j in zip(hex1_lines, hex2_lines):
            print(f'{i}\t{j}')
        print('\n')
        print(hex1_url)
        print(hex2_url)

cast()