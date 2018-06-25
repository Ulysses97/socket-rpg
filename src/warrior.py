import importlib
import collections
character = importlib.import_module('src.character')

class Warrior(character.Character) :
  def __init__(self, name) :
    character.Character.__init__(self, name, 400, 100, 20, 0, 30, 20)

    self.attacks = [
      ("embate", (2,"Embate","Ataque físico, escala con la fuerza")),
      ("posDef", (3,"Posición Defensiva","Incrementa tu armadura en 5 puntos")),
      ("golpePen", (3,"Golpe Penetrante","Reduce la armadura de tu oponente en 3 puntos")),
      ("golpeDeSangre", (4,"Golpe de Sangre","Gran ataque físico, a coste de x0.05 de tu vida actual"))
    ]

    self.attacks = collections.OrderedDict(self.attacks)

  def attack(self, name, oponent) :
    if name == "embate" :
      oponent.takeDamage("physical",self.stats["currentStrength"])

    elif name == "posDef" :
      self.stats["currentArmor"] += 5

    elif name == "golpePen" :
      oponent.setStat("currentArmor",oponent.getStats()["currentArmor"] - 3)

    elif name == "golpeDeSangre" :
      oponent.takeDamage("physical",self.stats["currentStrength"] + 50)
      self.stats["currentHp"] -= (self.stats["currentHp"] * 0.05)

    return oponent

  def combat(self, oponent) :
    print("Ataques / Hechizos :\n")

    for key in self.attacks :
      print("[" + str(self.attacks[key][0]) + " pts de acción] " + self.attacks[key][1] + " : " + self.attacks[key][2])

    if len(self.getInventory()) != 0 :
      print("\nPociones :\n")

      for potion in self.getInventory() :
        print("[" + str(potion.getActionPts()) + " pts de acción] " + potion.getName())

    else :
      print("\nTu inventorio de pociones está vacío.")

    choice = input("\nIngresa 'atacar' para seleccionar un Ataque/Hechizo o 'pocion' para consumir una poción : ")

    while not choice.lower() in ["atacar","pocion"] :
      choice = input("Ingresa una opción válida : ")

    if choice.lower() == "pocion" and len(self.getInventory()) == 0 :
      print("Tu inventorio de pociones está vacío.")
      choice = "atacar"

    if choice.lower() == "atacar" :
      i = 1
      for key in self.attacks :
        print("[" + str(i) + "] [" + str(self.attacks[key][0]) + " pts de acción] " + self.attacks[key][1] + " : " + self.attacks[key][2])
        i += 1

      option = input("Selecciona un ataque : ")

      while not option in ["1","2","3","4"] :
        option = input("Ingresa una opción válida : ")

      if option == "1" :
        oponent = self.attack("embate",oponent)
        action_pts = 2

      elif option == "2" :
        oponent = self.attack("posDef",oponent)
        action_pts = 3

      elif option == "3" :
        oponent = self.attack("golpePen",oponent)
        action_pts = 3

      elif option == "4" :
        oponent = self.attack("golpeDeSangre",oponent)
        action_pts = 4

    elif choice.lower() == "pocion" :
      i = 1
      for potion in self.getInventory() :
        print("[" + str(i) + "] [" + str(potion.getActionPts()) + " pts de acción] " + potion.getName())
        i += 1

      option = input("Selecciona una poción para utilizarla : ")

      potions = list()

      for n in range(i - 1) :
        potions.append(n + 1)

      options = list()

      for nums in potions :
        options.append(str(nums))

      while not option in options :
        option = input("Ingresa una opción válida : ")

      self.getInventory()[int(option) - 1].use(self)
      self.getInventory().remove(self.getInventory()[int(option) - 1])
      action_pts = 2

    return (self, oponent, action_pts)
