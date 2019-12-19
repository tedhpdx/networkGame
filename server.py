import socket
from _thread import *
import threading
from player import Player
from game import Game
import pickle

server = "localhost"
port = 55552

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    s.bind((server, port))
except socket.error as e:
    print (str(e))

s.listen()
print("Waiting for a connection, Server Started")

#connected = set()
games = {}
gameId = 0


def threaded_client(conn, p, gameId):

    while True:
        try:
            data = conn.recv(4096)
            client_data = pickle.loads(data)

            if gameId in games:
                game = games[gameId]
                if client_data.pickle_string == "reset":
                    game.reset_game()
                if client_data.pickle_string == "game":
                    game.update_game(client_data)
                    if client_data.in_progress:
                        game.in_progress = True
                if client_data.pickle_string == "player":
                    dice_player = client_data
                    game.update_object(dice_player)
                    if client_data.left_game is True:
                        if game.remove_player(dice_player) == -1:
                            break
                        conn.sendall(pickle.dumps(game))
                        return
                    if client_data.killed_game is True:
                        game.killed = True
                        pickle.dumps(game)
                        conn.sendall(pickle.dumps(game))
                        break
                conn.sendall(pickle.dumps(game))
            else:
                print("about to break in else because game deleted")
                game_killed = "game killed"
                conn.sendall(pickle.dumps(game_killed))
                break
        except socket.error as e:
            print(e)

    print("Lost Connection")
    try:
        if games[gameId]:
            del games[gameId]
            print("Closing game")
            #idCount -= 1
    except :
        print("delete game error")
    conn.close()


global_id = 1000
while True:
    try:
        p = 0
        global_id += 1
        conn, addr = s.accept()
        print("Connected to:", addr)
        data = conn.recv(4096)
        client_data = pickle.loads(data)
        client_pack = {"games": games, "p": None, "global_id": global_id}
        if client_data.pickle_string == "join" and client_data.gameId is None:
            client_pack["p"] = p
            conn.sendall(pickle.dumps(client_pack))
            data = conn.recv(4096)
            client_data = pickle.loads(data)
            if client_data.pickle_string == "unjoin":
                conn.close()
                continue
        if client_data.pickle_string == "join" and client_data.gameId is not None:
            client_pack["p"] = p
            conn.sendall(pickle.dumps(client_pack))
            print("Connecting to game")
            games[client_data.gameId].add_active_player()
            print("Client gameId:" + str(client_data.gameId))
            start_new_thread(threaded_client, (conn, p, client_data.gameId))
        elif client_data.pickle_string == "create":
            gameId += 1
            #gameId = idCount
            games[gameId] = Game(gameId)
            games[gameId].add_active_player()
            client_pack["games"] = games
            client_pack["p"] = p
            conn.sendall(pickle.dumps(client_pack))
            print("Creating a new Game")
            start_new_thread(threaded_client, (conn, p, gameId))
    except socket.error as e:
        print("error")
        print (e)
