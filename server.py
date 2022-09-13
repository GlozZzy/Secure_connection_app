import json
import socket
from random import randint

from DES import DES
from SHA import SHA


def GeneratePrime():
    while True:
        k = randint(2, 2 ** 56)
        b = 0
        p = (k - 1) / 2
        for i in [2, 3, 5, 7, 11, 13]:
            if k % i == 0:
                b = 1
                break
            if p % i == 0:
                b = 1
                break
        if b == 1:
            continue
        p = int(p)
        if MillerRabin(p) and MillerRabin(k):
            return k
        else:
            continue


def MillerRabin(a, k=3):
    n = a - 1
    s = 0
    d = n
    while d % 2 == 0:
        d = d // 2
        s += 1
    for rnd in range(k):
        t = randint(2, n)
        if pow(t, d, a) == 1:
            continue
        for i in range(1, s):
            if pow(t, d, a) == n:
                continue
        return 0
    return a


def getKey(g, key, p):
    return pow(g, key, p)


def EncryptMessage(text, key):
    Encryptedtext = ""
    EPart = ""
    for i in text:
        EPart += i
        if len(EPart) == 8:
            Encryptedtext += DES(EPart, "E", key)
            EPart = ""
    if len(EPart) > 0:
        Encryptedtext += DES(EPart, "E", key)
    return Encryptedtext


def DecryptMessage(text, key):
    Dencryptedtext = ""
    DPart = ""
    for i in text:
        DPart += i
        if len(DPart) == 8:
            Dencryptedtext += DES(DPart, "D", key)
            DPart = ""
    if len(DPart) > 0:
        Dencryptedtext += DES(DPart, "D", key)
    return Dencryptedtext


if __name__ == '__main__':
    HOST = 'localhost'
    PORT = 50006
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((HOST, PORT))

    predefined_p = GeneratePrime()
    predefined_g = 2

    print('Server started!')
    sock.listen(5)

    while True:
        conn, addr = sock.accept()  # Establish connection with client.
        print('Connected by', addr)

        # Generate Session key by Diffie–Hellman alg
        private_key = randint(2, predefined_p - 1)

        g = predefined_g
        p = predefined_p
        A = getKey(g, private_key, p)

        data = {"A": A, "g": g, "p": p}
        data = json.dumps(data)
        conn.sendall(bytes(data, encoding="utf-8"))

        jsonReceived = conn.recv(4096)
        if not jsonReceived:
            break
        jsonReceived = json.loads(jsonReceived)
        public_key = jsonReceived["B"]

        # Session key
        Session_key = getKey(public_key, private_key, p)
        print("Session key on server:", Session_key)

        # receive message from client
        while True:
            jsonReceived = conn.recv(4096)
            if not jsonReceived:
                break
            jsonReceived = json.loads(jsonReceived)

            receivedEMessage = jsonReceived["EMessage"]
            receivedHash = jsonReceived["Hash"]

            DMessage = DecryptMessage(receivedEMessage, Session_key)
            if SHA(DMessage) == receivedHash:
                sendMessage = "Answer: " + DMessage.upper()
            else:
                sendMessage = "Text damaged on server"

            # send uppercase message with Answer to client
            EMessage = EncryptMessage(sendMessage, Session_key)
            hash_ = SHA(sendMessage)

            data = {"EMessage": EMessage, "Hash": hash_}
            data = json.dumps(data)
            conn.sendall(bytes(data, encoding="utf-8"))

    conn.close()
