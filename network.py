import socket
import pickle


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 55557
        self.global_id = 0
        self.addr = (self.server, self.port)
        self.p = None
        self.games = {}

    def getP(self):
        return self.p

    def get_global_id(self):
        return self.global_id

    def connect(self, net_pack=None):
        try:
            self.client.connect(self.addr)
            if net_pack:
                net_pack_obj = pickle.dumps(net_pack)
                self.client.send(net_pack_obj)
                server_pack = pickle.loads(self.client.recv(2048))
                self.games = server_pack["games"]
                self.p = server_pack["p"]
                self.global_id = server_pack["global_id"]
        except socket.error as e:
            print(e)
            return -1

    def send(self, net_pack):
        try:
            net_pack_obj = pickle.dumps(net_pack)
            self.client.send(net_pack_obj)
            pickled_object = self.client.recv(2048)
            data = pickle.loads(pickled_object)
            if data == "game killed":
                return -1
            return data
        except socket.error as e:
            print(e)

