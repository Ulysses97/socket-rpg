import random
import importlib
import collections
character = importlib.import_module('src.character')

class Mage(character.Character) :
  def __init__(self, name) :
    character.Character.__init__(self, name, 250, 250, 5, 20, 15, 20)

    self.attacks = [
      ("atArc", (2,"Ataque Arcano","Ataque mágico, escala con inteligencia")),
      ("hipnotizar", (3,"Hipnotizar","Cancelas el sig. turno de tu oponente con una probabilidad de x0.5")),
      ("interEq", (3,"Intercambio Equivalente","Ataque mágico, te curas la misma cantidad que el daño que haces.")),
      ("tormentFuego", (4,"Tormenta de Fuego","Gran ataque mágico, escala con inteligencia + x0.02 de la vida máxima de tu oponente"))
    ]

    self.attacks = collections.OrderedDict(self.attacks)

  def attack(self, name, oponent) :
    if name == "atArc" :
      oponent.takeDamage("magical", self.stats["currentIntelligence"])

    elif name == "hipnotizar" :
      prob = random.choice([True,False])
      oponent.setStat("stunned",prob)

    elif name == "interEq" :
      heal = int(round(self.stats["currentIntelligence"] / 2 * (100.0 / (100 + oponent.getStats()["currentMagicResist"]))))
      oponent.takeDamage("magical",self.stats["currentIntelligence"]/2)
      self.stats["currentHp"] += heal

    elif name == "tormentFuego" :
      oponent.takeDamage("magical",60 + (oponent.getBaseStats()["maxHp"] * 0.02))

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
        oponent = self.attack("atArc",oponent)
        action_pts = 2

      elif option == "2" :
        oponent = self.attack("hipnotizar",oponent)
        action_pts = 3

      elif option == "3" :
        oponent = self.attack("interEq",oponent)
        action_pts = 3

      elif option == "4" :
        oponent = self.attack("tormentFuego",oponent)
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
