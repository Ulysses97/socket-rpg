import importlib
import os

def clearScreen() :
  if os.name == "posix" :
    os.system("clear")
  elif os.name == "nt" :
    os.system("cls")

character = importlib.import_module("src.character")
warrior = importlib.import_module("src.warrior")
mage = importlib.import_module("src.mage")
paladin = importlib.import_module("src.paladin")
potion = importlib.import_module("src.potion")
server = importlib.import_module("src.combat_server")
client = importlib.import_module("src.combat_client")

name = input("Cuál es tu nombre? : ")

choice = input("Escoge una clase ('guerrero', 'mago', 'paladin') : ").lower()

while not choice in ["guerrero","mago","paladin"] :
  choice = input("Ingresa una opción válida : ").lower()

if choice == "guerrero" :
  player = warrior.Warrior("[Guerrero] " + name)

elif choice == "mago" :
  player = mage.Mage("[Mago] " + name)

elif choice == "paladin" :
  player = paladin.Paladin("[Paladín] " + name)

clearScreen()

print(player.getBaseStats()["name"] + "\n")

choice = input("Ingresa 'd' para desafiar a alguien a combate o 'a' para aceptar un combate : ").lower()

while not choice in ["d","a"] :
  choice = input("Ingresa una opción válida : ")

if choice == "d" :
  ip = input("Ingresa tu IP local : ")
  port = int(input("Ingresa Puerto : "))

  game = server.Server(ip,port)
  game.run(player)
  game.closeConnection()

elif choice == "a" :
  ip = input("Ingresa la IP del Host : ")
  port = int(input("Ingresa Puerto : "))

  game = client.Client(ip,port)
  game.run(player)
  game.closeConnection()