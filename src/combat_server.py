
import socket
import pickle
import os
import importlib
import time

ACTION_POINTS = 6
READ_BUFF = 4096

class Server :
  def __init__(self, IP, PORT) :
    # AF_INET especifíca que el tipo de direcciones utilizadas serán IPv4.
    # SOCK_STREAM especifíca que el socket será TCP.
    self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # "Enlaza" el socket con la dirección IP y puerto.
    self.server_socket.bind((IP,PORT))

    # El socket "escuchará" a una conexión entrante.
    print("Esperando jugador...")
    self.server_socket.listen(1)

    # Cuando se encuentra una conexión, se recibe un socket que se
    # utilizará para enviar datos al equipo conectado + su dirección.
    self.client_socket, self.addr =  self.server_socket.accept()
    print("Un oponente se ha unido a la partida.")

  def run(self, player) :
    oponent = recvOponent(self.client_socket)
    sendPlayer(self.client_socket, player)

    printStats(player, oponent)

    my_turn = True
    actions = 0

    while True :
      if my_turn :
        if actions >= ACTION_POINTS :
          my_turn = False
          actions = 0
          endTurn(self.client_socket)
          continue

        if oponent.getStats()["currentHp"] <= 0 :
          my_turn = False
          endTurn(self.client_socket)
          clearScreen()
          print("Has ganado!")
          break

        elif player.getStats()["currentHp"] <= 0 :
          my_turn = False
          endTurn(self.client_socket)
          clearScreen()
          print("Has sido derrotado!")
          break

        if player.getStats()["stunned"] :
          my_turn = False
          actions = 0
          player.setStat("stunned",False)
          sendCharacters(self.client_socket,(player,oponent))
          time.sleep(0.1)
          endTurn(self.client_socket)
          print("Estás aturdido.")
          continue

        update = player.combat(oponent)

        actions += update[2]

        player = update[0]
        oponent = update[1]

        characters = (player,oponent)

        sendCharacters(self.client_socket, characters)

        printStats(player,oponent)

      else :
        receive = self.client_socket.recv(READ_BUFF)

        try :
          decoded = receive.decode()

        except UnicodeDecodeError :
          decoded = pickle.loads(receive)

        if decoded == "done" :
          my_turn = True
          continue

        else :
          player = decoded[1]
          oponent = decoded[0]

          printStats(player, oponent)

  def closeConnection(self) :
    self.client_socket.close()

def sendPlayer(client_socket, player_obj) :
  encoded_obj = pickle.dumps(player_obj)
  client_socket.send(encoded_obj)

def recvOponent(client_socket) :
  encoded_obj = client_socket.recv(READ_BUFF)
  oponent_obj = pickle.loads(encoded_obj)
  return oponent_obj

def sendCharacters(client_socket, characters) :
  encoded_obj = pickle.dumps(characters)
  client_socket.send(encoded_obj)

def clearScreen() :
  if os.name == "posix" :
    os.system("clear")
  elif os.name == "nt" :
    os.system("cls")

def printStats(player, oponent) :
  clearScreen()
  print("[Tú] " + player.getBaseStats()["name"] + " : HP[" + str(player.getStats()["currentHp"]) + "]")
  print("[Oponente] " + oponent.getBaseStats()["name"] + " : HP[" + str(oponent.getStats()["currentHp"]) + "]")

def endTurn(client_socket) :
  client_socket.send("done".encode())
