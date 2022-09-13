IP = [58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6, 64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1, 59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5, 63, 55, 47, 39, 31, 23, 15, 7]
FP = [40, 8, 48, 16, 56, 24, 64, 32, 39, 7, 47, 15, 55, 23, 63, 31,
      38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29,
      36, 4, 44, 12, 52, 20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27,
      34, 2, 42, 10, 50, 18, 58, 26, 33, 1, 41, 9, 49, 17, 57, 25]
EP = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7, 8, 9,
      8, 9, 10, 11, 12, 13, 12, 13, 14, 15, 16, 17,
      16, 17, 18, 19, 20, 21, 20, 21, 22, 23, 24, 25,
      24, 25, 26, 27, 28, 29, 28, 29, 30, 31, 32, 1]
PP = [16, 7, 20, 21, 29, 12, 28, 17, 1, 15, 23, 26, 5, 18, 31, 10,
      2, 8, 24, 14, 32, 27, 3, 9, 19, 13, 30, 6, 22, 11, 4, 25]
KP = [57, 49, 41, 33, 25, 17, 9, 1, 58, 50, 42, 34, 26, 18,
      10, 2, 59, 51, 43, 35, 27, 19, 11, 3, 60, 52, 44, 36,
      63, 55, 47, 39, 31, 23, 15, 7, 62, 54, 46, 38, 30, 22,
      14, 6, 61, 53, 45, 37, 29, 21, 13, 5, 28, 20, 12, 4]
CP = [14, 17, 11, 24, 1, 5, 3, 28, 15, 6, 21, 10,
      23, 19, 12, 4, 26, 8, 16, 7, 27, 20, 13, 2,
      41, 52, 31, 37, 47, 55, 30, 40, 51, 45, 33, 48,
      44, 49, 39, 56, 34, 53, 46, 42, 50, 36, 29, 32]
shifts = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
sbox = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]


def BinToDec(mas):
    dec = 0
    leng = len(mas)
    for i in range(leng):
        dec += mas[i] * 2 ** (leng - 1 - i)
    return dec


def DecToBin(a):
    b = []
    if a == 0:
        b.insert(0, 0)
    while a != 0:
        b.insert(0, a % 2)
        a = a // 2
    return b


def addTo56(mas):
    while (len(mas) != 56):
        mas.insert(0, 0)


def addTo4(mas):
    while (len(mas) != 4):
        mas.insert(0, 0)


def StrToMas(str):
    a = []
    for ch in str:
        asc = ord(ch)
        ch_mas = DecToBin(asc)
        while len(ch_mas) % 8:
            ch_mas.insert(0, 0)
        a += ch_mas
    return a


def KeyGenerator(key):
    key_copy = key
    key = DecToBin(key_copy)
    addTo56(key)
    new_key = [0] * 64
    for i in range(8):
        new_key[8 * i:8 * i + 7] = key[7 * i:7 * i + 7]
        new_key[8 * i + 7] = (sum(key[7 * i:7 * i + 7]) + 1) % 2
    C, D = key_permutation(new_key)
    key_mas = []
    for i, sh in enumerate(shifts):
        C = C.copy()
        D = D.copy()
        shift(C, sh)
        shift(D, sh)
        mas = C + D
        # print(C, D, sep='  ')
        r_key = key_compression_permutation(mas)
        key_mas.append(r_key)
    return key_mas


def key_compression_permutation(c):
    N = [0] * 56
    for i in range(48):
        N[i] = c[CP[i] - 1]
    return N


def shift(lst, steps):
    for i in range(steps):
        lst.insert(0, lst.pop())


def key_permutation(key):
    D = [0] * 28
    C = [0] * 28
    for i in range(28):
        C[i] = key[KP[i] - 1]
        D[i] = key[KP[i + 28] - 1]
    return C, D


def initial_permutation(word):
    new_word = [0] * 64
    for i in range(64):
        new_word[i] = word[IP[i] - 1]
    return new_word


def final_permutation(word):
    new_word = [0] * 64
    for i in range(64):
        new_word[i] = word[FP[i] - 1]
    return new_word


def expansion_permutation(block32):
    block48 = [0] * 48
    for i in range(48):
        block48[i] = block32[EP[i] - 1]
    return block48


def substitutions(block48):
    block6 = [[block48[i * 6 + j] for j in range(6)] for i in range(8)]
    block4 = []
    for i in range(8):
        block4 += substitutions6bits_to_4bits(block6[i], i)
    return block4


def substitutions6bits_to_4bits(block6, i):
    row = BinToDec([block6[0], block6[-1]])
    column = BinToDec(block6[1:-1])
    block4 = DecToBin(sbox[i][row][column])
    addTo4(block4)
    return block4


def F(block32, key):
    block48 = expansion_permutation(block32)
    block48 = list(map(lambda x, y: x ^ y, block48, key))
    block32 = substitutions(block48)
    new_block32 = [0] * 32
    for i in range(32):
        new_block32[i] = block32[PP[i] - 1]
    return new_block32


def round_feistel_cipher(side1, side2, key):
    temp = side2
    res_F = F(side2, key)
    side2 = list(map(lambda x, y: x ^ y, side1, res_F))
    side1 = temp
    return side1, side2


def feistel_cipher(mode, side1, side2, keys):
    if mode == "E":
        for rd in range(16):
            side1, side2 = round_feistel_cipher(side1, side2, keys[rd])
        side1, side2 = side2, side1
    if mode == "D":
        for rd in reversed(range(16)):
            side1, side2 = round_feistel_cipher(side1, side2, keys[rd])
        side1, side2 = side2, side1
    return side1 + side2


def AddSYmbolsTo8(word):
    while len(word) < 8:
        word += ""
    return word


def DeleteTempSYmbols(word):
    str = ""
    for i in word:
        if i != "":
            str += i
    return str


def DecToStr(dec):
    str = ""
    for i in dec:
        str += chr(i)
    return str


def DES(word, mode, key):
    if mode == "E":
        word = AddSYmbolsTo8(word)
    word = StrToMas(word)
    keys = KeyGenerator(key)

    new_word = initial_permutation(word)
    side1 = new_word[:32]
    side2 = new_word[32:]
    word = feistel_cipher(mode, side1, side2, keys)

    new_word = final_permutation(word)
    new_word = [BinToDec(new_word[i * 8:i * 8 + 8]) for i in range(8)]
    new_word = DecToStr(new_word)
    if mode == "D":
        new_word = DeleteTempSYmbols(new_word)
    return new_word
