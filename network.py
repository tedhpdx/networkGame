import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 5550
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def send(self, data):
        try:
            dice_player = pickle.dumps(data)
            self.client.send(dice_player)
            something = pickle.loads(self.client.recv(2048))
            return something
        except socket.error as e:
            print(e)

