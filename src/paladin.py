import random
import importlib
import collections
character = importlib.import_module('src.character')

class Paladin(character.Character) :
  def __init__(self, name) :
    character.Character.__init__(self, name, 300, 200, 15, 15, 20, 20)

    self.attacks = [
      ("golpeElec", (2,"Golpe Eléctrico","Ataque físico, escala con fuerza, inteligencia, y un porcentaje de tu armadura")),
      ("inspiracion", (2,"Inspiración","Incrementas tu armadura y resistencia mágica")),
      ("curacion", (3,"Curación","Te curas 20 puntos de vitalidad, puedes sobrepasar tu vida máxima")),
      ("carga", (4,"Carga con Escudo","Gran ataque físico y mágico, con una pequeña probabilidad del x0.25 de cancelar el sig. turno de tu oponente"))
    ]

    self.attacks = collections.OrderedDict(self.attacks)

  def attack(self, name, oponent) :
    if name == "golpeElec" :
      oponent.takeDamage("physical",(self.stats["currentStrength"] + self.stats["currentArmor"])/2)
      oponent.takeDamage("magical",self.stats["currentIntelligence"])

    elif name == "inspiracion" :
      self.stats["currentArmor"] += 3
      self.stats["currentMagicResist"] += 2

    elif name == "curacion" :
      self.stats["currentHp"] += 20

    elif name == "carga" :
      oponent.takeDamage("physical",self.stats["currentStrength"] + 10)
      oponent.takeDamage("magical",self.stats["currentIntelligence"] + 10)
      prob = random.choice([True,False,False,False])
      oponent.setStat("stunned",prob)

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
        oponent = self.attack("golpeElec",oponent)
        action_pts = 2

      elif option == "2" :
        oponent = self.attack("inspiracion",oponent)
        action_pts = 3

      elif option == "3" :
        oponent = self.attack("curacion",oponent)
        action_pts = 3

      elif option == "4" :
        oponent = self.attack("carga",oponent)
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
