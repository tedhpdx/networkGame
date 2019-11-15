import socket
from _thread import *
from player import Player
from game import Game
import pickle

server = "10.0.1.7"
port = 5550

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen()
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    while True:
        try:
            dice_roller = Player("", 0)
            data = conn.recv(4096)
            dice_roller = pickle.loads(data)
            if gameId in games:
                game = games[gameId]
                if not data:
                    break
                else:
                    if dice_roller.pickle_string == "reset":
                        game.resetWent()
                    elif dice_roller.pickle_string != "get":
                        if p == 0:
                            game.p1Name = dice_roller.name
                        elif p == 1:
                            game.p0Name = dice_roller.name
                        game.play(p, dice_roller)
                #this is where we can store data in the game class for each of our players
                #probs want to use a dictionary for each player with all their data inside
                if p == 0:
                    game.p0Name = dice_roller.name
                elif p == 1:
                    game.p1Name = dice_roller.name
                conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            print("error")
            break

    print("Lost Connection")
    try:
        del games[gameId]
        print("Closing game")
    except:
        pass
    idCount -= 1
    conn.close()


currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1
    start_new_thread(threaded_client, (conn, p, gameId))
