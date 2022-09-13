import json
import socket
from random import randint

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QGridLayout, QPlainTextEdit, QVBoxLayout

from DES import DES
from SHA import SHA


class WellcomeWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.mainwindow = None
        self.setGeometry(200, 50, 800, 500)
        self.setMinimumSize(450, 225)
        self.setMaximumSize(450, 225)

        self.label = QLabel()
        self.button = QPushButton()
        self.layout = QVBoxLayout()

        self.private_key = None
        self.public_p = None
        self.public_g = None
        self.public_key = None
        self.public_key_from_server = None
        self.Session_key = None

        self.sock = socket.socket()

        self.UIcomponents()
        self.show()

    def UIcomponents(self):
        # Label
        self.label.setText("Wellcome!")
        self.label.setFont(QFont("Arial", 20))
        self.label.setAlignment(Qt.AlignCenter)

        # Button
        self.button.setText("Connect")
        self.button.setFont(QFont("Arial", 14))
        self.button.clicked.connect(self.Connect)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

    def Connect(self):
        if self.ConnetToServer():
            boo = True
            try:
                self.private_key = randint(2, self.public_p - 1)
                self.public_key = self.getPublicKey()
                data = {"B": self.public_key}
                data = json.dumps(data)
                self.sock.sendall(bytes(data, encoding="utf-8"))
            except:
                boo = False

            if boo:
                self.Session_key = self.getSessionKey()
                print("Session key on client:", self.Session_key)
                self.mainwindow = MainWindow(self.sock, self.Session_key)
                self.mainwindow.show()
                self.mainwindow.setWindowTitle("Client interface")
                self.hide()
            else:
                self.label.setText("Something went wrong\nPlease try again later")
        else:
            self.label.setText("Something went wrong\nPlease try again later")

    def ConnetToServer(self):
        boo = True
        try:
            self.sock.connect(('localhost', 50006))
            jsonReceived = self.sock.recv(4096)
            jsonReceived = json.loads(jsonReceived)
            self.public_p = jsonReceived["p"]
            self.public_g = jsonReceived["g"]
            self.public_key_from_server = jsonReceived["A"]
        except:
            boo = False
        return boo

    def getPublicKey(self):
        return pow(self.public_g, self.private_key, self.public_p)

    def getSessionKey(self):
        return pow(self.public_key_from_server, self.private_key, self.public_p)


class MainWindow(QWidget):
    def __init__(self, sock, session_key):
        super().__init__()
        self.sock = sock
        self.Session_key = session_key

        self.setGeometry(200, 50, 800, 500)
        self.setMinimumSize(600, 300)

        self.textbox_client = QPlainTextEdit()
        self.textbox_server = QPlainTextEdit()
        self.label = QLabel()
        self.label_client = QLabel()
        self.label_server = QLabel()
        self.button_send = QPushButton()
        self.button_clear = QPushButton()

        self.spacing = 5
        self.grid = QGridLayout()

        self.UIcomponents()
        self.show()

    def UIcomponents(self):
        self.grid.setSpacing(self.spacing)

        # Labels
        self.label.setText("Successful server connection!")
        self.label.setFont(QFont("Arial", 20))

        self.label_client.setText("Your message")
        self.label_client.setFont(QFont("Arial", 14))

        self.label_server.setText("Message from server")
        self.label_server.setFont(QFont("Arial", 14))

        # TextBoxs
        self.textbox_client.setFont(QFont("Arial", 14))
        self.textbox_client.textChanged.connect(self.texthandler)
        self.textbox_server.setFont(QFont("Arial", 14))
        self.textbox_server.setReadOnly(True)

        # Buttons
        self.button_send.setText("Send")
        self.button_send.setFont(QFont("Arial", 14))
        self.button_send.clicked.connect(self.SendMessage)

        self.button_clear.setText("Clear")
        self.button_clear.setFont(QFont("Arial", 14))
        self.button_clear.clicked.connect(self.Clear)

        # Positioning objects
        self.grid.addWidget(self.label, 0, 0, 1, 0)
        self.grid.addWidget(self.label_client, 1, 0)
        self.grid.addWidget(self.label_server, 1, 1)
        self.grid.addWidget(self.textbox_client, 2, 0)
        self.grid.addWidget(self.textbox_server, 2, 1)
        self.grid.addWidget(self.button_send, 10, 0)
        self.grid.addWidget(self.button_clear, 10, 1)
        self.setLayout(self.grid)

    def SendMessage(self):
        self.textbox_server.clear()

        sendMessage = self.textbox_client.toPlainText()
        EMessage = self.EncryptMessage(sendMessage)
        hash_ = SHA(sendMessage)

        data = {"EMessage": EMessage, "Hash": hash_}
        data = json.dumps(data)
        self.sock.sendall(bytes(data, encoding="utf-8"))

        # Receive message from server
        jsonReceived = self.sock.recv(4096)
        jsonReceived = json.loads(jsonReceived)

        receivedEMessage = jsonReceived["EMessage"]
        receivedHash = jsonReceived["Hash"]

        DMessage = self.DecryptMessage(receivedEMessage)
        if SHA(DMessage) == receivedHash:
            self.textbox_server.insertPlainText(DMessage)
        else:
            self.textbox_server.insertPlainText("Text damaged on client")

    def Clear(self):
        self.textbox_client.clear()
        self.textbox_server.clear()

    def EncryptMessage(self, text):
        Encryptedtext = ""
        EPart = ""
        for i in text:
            EPart += i
            if len(EPart) == 8:
                Encryptedtext += DES(EPart, "E", self.Session_key)
                EPart = ""
        if len(EPart) > 0:
            Encryptedtext += DES(EPart, "E", self.Session_key)
        return Encryptedtext

    def DecryptMessage(self, text):
        Decryptedtext = ""
        DPart = ""
        for i in text:
            DPart += i
            if len(DPart) == 8:
                Decryptedtext += DES(DPart, "D", self.Session_key)
                DPart = ""
        if len(DPart) > 0:
            Decryptedtext += DES(DPart, "D", self.Session_key)
        return Decryptedtext

    def texthandler(self):
        a = self.textbox_client.toPlainText()
        if len(a) > 0:
            if ord(a[-1]) > 255:
                a = a[:-1]
                self.textbox_client.clear()
                self.textbox_client.insertPlainText(a)


if __name__ == '__main__':
    app = QApplication([])
    wind = WellcomeWindow()
    wind.setWindowTitle("Client wellcome")
    app.exec_()
