
import socket
import pickle
import os
import importlib
import time

READ_BUFF = 4096
ACTIONS_POINTS = 6

class Client :
  def __init__(self, IP, PORT) :
    # Se instancia un socket.
    self.server_socket = socket.socket()

    # El socket se conecta a un socket remoto según la IP y el puerto.
    self.server_socket.connect((IP,PORT))
    print("Te has unido a una partida.")

  def run(self, player) :
    sendPlayer(self.server_socket, player)
    oponent = recvOponent(self.server_socket)

    printStats(player, oponent)

    my_turn = False
    actions = 0

    while True :
      if my_turn :
        if actions >= ACTIONS_POINTS :
          my_turn = False
          actions = 0
          endTurn(self.server_socket)
          continue

        if oponent.getStats()["currentHp"] <= 0 :
          my_turn = False
          endTurn(self.server_socket)
          clearScreen()
          print("Has ganado!")
          break

        elif player.getStats()["currentHp"] <= 0 :
          my_turn = False
          endTurn(self.server_socket)
          clearScreen()
          print("Has sido derrotado!")
          break

        if player.getStats()["stunned"] :
          my_turn = False
          actions = 0
          player.setStat("stunned",False)
          sendCharacters(self.server_socket,(player,oponent))
          time.sleep(0.1)
          endTurn(self.server_socket)
          print("Estás aturdido.")
          continue

        update = player.combat(oponent)

        actions += update[2]

        player = update[0]
        oponent = update[1]

        characters = (player,oponent)

        sendCharacters(self.server_socket, characters)

        printStats(player,oponent)

      else :
        receive = self.server_socket.recv(READ_BUFF)

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
    self.server_socket.close()

def sendPlayer(server_socket, player) :
  encoded_obj = pickle.dumps(player)
  server_socket.send(encoded_obj)

def recvOponent(server_socket) :
  encoded_obj = server_socket.recv(READ_BUFF)
  oponent = pickle.loads(encoded_obj)
  return oponent

def sendCharacters(server_socket, characters) :
  encoded_obj = pickle.dumps(characters)
  server_socket.send(encoded_obj)

def clearScreen() :
  if os.name == "posix" :
    os.system("clear")
  elif os.name == "nt" :
    os.system("cls")

def printStats(player, oponent) :
  clearScreen()
  print("[Tú] " + player.getBaseStats()["name"] + " : HP[" + str(player.getStats()["currentHp"]) + "]")
  print("[Oponente] " + oponent.getBaseStats()["name"] + " : HP[" + str(oponent.getStats()["currentHp"]) + "]")

def endTurn(server_socket) :
  server_socket.send("done".encode())
