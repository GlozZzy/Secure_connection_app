def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def ToHex(str):
    sf = ""
    hex = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f"]
    for i in range(len(str) // 4):
        s = str[:4]
        str = str[4:]
        s = list(s)
        num = 0

        for j in range(4):
            if (s[j] == "1"):
                num += 2 ** j
        sf += hex[num]
    return sf


def ToBin32(num):
    s = ""
    for i in range(31, -1, -1):
        if (num >= 2 ** i):
            num -= 2 ** i
            s += "1"
        else:
            s += "0"
    return s


def ToInt(str):
    s = list(str)
    num = 0
    for i in range(31, -1, -1):
        if (s[31 - i] == "1"):
            num += 2 ** i
    return num


def rightshift(str, l):
    str = str[l:]
    s = ""
    for i in range(l):
        s += "0"
    str = s + str
    return str


def rightrotate(str, l):
    s = str[len(str) - l:]
    str = str[:len(str) - l]
    str = s + str
    return str


def plus1(str, str1):
    m = ""
    s = list(str)
    s1 = list(str1)
    for i in range(len(str)):
        if (s[i] == s1[i] == "1"):
            m += "1"
        else:
            m += "0"
    return m


def plus(str, str1):
    m = ""
    s = ToInt(str)
    s1 = ToInt(str1)
    sf = (s + s1) % 2 ** 32

    return ToBin32(sf)


def xor1(str, str1):
    s = list(str)
    s1 = list(str1)
    sf = ""
    for i in range(len(s)):
        if (s[i] == s1[i]):
            sf += "0"
        else:
            sf += "1"
    return sf


def xor(str, str1):
    s = list(str)
    s1 = list(str1)
    sf = ""
    for i in range(len(s)):
        if (s[i] == s1[i]):
            sf += "1"
        else:
            sf += "0"
    return sf


def inver(str):
    s = list(str)
    m = ""
    for i in range(len(s)):
        if (s[i] == "0"):
            m += "1"
        else:
            m += "0"
    return m


def SHA(strr):
    h0 = 1779033703
    h1 = 3144134277
    h2 = 1013904242
    h3 = 2773480762
    h4 = 1359893119
    h5 = 2600822924
    h6 = 528734635
    h7 = 1541459225

    k = [1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221,
         3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580,
         3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986,
         2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895,
         666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, 2177026350, 2456956037,
         2730485921, 2820302411, 3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344,
         430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779,
         1955562222, 2024104815, 2227730452, 2361852424, 2428436474, 2756734187, 3204031479, 3329325298]
    w = []
    input1 = strr
    m = text_to_bits(input1)
    m += "1"
    while (len(m) % 512 != 448):
        m += "0"
    l = str(bin(len(input1))).replace("0b", "")
    while (len(m) % 512 != 512 - len(l)):
        m += "0"
    m += l
    m1 = m
    for j in range(len(m) // 512):
        for i in range(16):
            w.append(m1[:32])
            m1 = m1[32:]
        for i in range(16, 63):
            s = xor(xor(rightrotate(w[i - 15], 7), rightrotate(w[i - 15], 18)), rightshift(w[i - 15], 3))
            s1 = xor(xor(rightrotate(w[i - 2], 17), rightrotate(w[i - 2], 19)), rightshift(w[i - 2], 10))
            w.append(ToBin32(abs(ToInt(w[i - 16]) + ToInt(s) + ToInt(s1) + ToInt(w[i - 7]) % 2 ** 32)))
        a = ToBin32(h0)
        b = ToBin32(h1)
        c = ToBin32(h2)
        d = ToBin32(h3)
        e = ToBin32(h4)
        f = ToBin32(h5)
        g = ToBin32(h6)
        h = ToBin32(h7)

        for i in range(63):
            sum0 = xor(xor(rightrotate(a, 2), rightrotate(a, 13)), rightrotate(a, 22))
            ma = xor(xor(plus(a, b), plus(a, c)), plus(b, c))
            t2 = plus(sum0, ma)
            sum1 = xor(xor(rightrotate(e, 6), rightrotate(e, 11)), rightrotate(e, 25))
            ch = xor1(plus(e, f), plus(inver(e), g))
            t1 = ToBin32((ToInt(h) + ToInt(sum1) + ToInt(ch) + ToInt(w[i]) + k[i]) % 2 ** 32)

            h = g
            g = f
            f = e
            e = plus(d, t1)
            d = c
            c = b
            b = a
            a = plus(t1, t2)

        h0 = ToInt(plus(ToBin32(h0), a))
        h1 = ToInt(plus(ToBin32(h1), b))
        h2 = ToInt(plus(ToBin32(h2), c))
        h3 = ToInt(plus(ToBin32(h3), d))
        h4 = ToInt(plus(ToBin32(h4), e))
        h5 = ToInt(plus(ToBin32(h5), f))
        h6 = ToInt(plus(ToBin32(h6), g))
        h7 = ToInt(plus(ToBin32(h7), h))
    hashs = ToHex(
        ToBin32(h0) + ToBin32(h1) + ToBin32(h2) + ToBin32(h3) + ToBin32(h4) + ToBin32(h5) + ToBin32(h6) + ToBin32(h7))
    return hashs
