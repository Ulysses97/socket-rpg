import random

class Potion :
  def __init__(self, name, attribute, amount) :
    self.name = name
    self.attribute = attribute
    self.amount = amount
    self.actionPts = 2

  def use(self, character) :
    if self.attribute == "currentHp" :
      if character.getStats()["currentHp"] + self.amount > character.getBaseStats()["maxHp"] :
        character.setStat("currentHp",character.getBaseStats()["maxHp"])

      else :
        character.setStat(self.attribute, character.getStats()[self.attribute] + self.amount)

    else :
      character.setStat(self.attribute, character.getStats()[self.attribute] + self.amount)

  def getName(self) :
    return self.name

  def getActionPts(self) :
    return self.actionPts

class HealthPotion(Potion) :
  def __init__(self) :
    Potion.__init__(self, "Poción de vitalidad", "currentHp", random.randint(20,25))

class ManaPotion(Potion) :
  def __init__(self) :
    Potion.__init__(self, "Poción de maná", "currentMana", random.randint(10,15))

class StrengthPotion(Potion) :
  def __init__(self) :
    Potion.__init__(self, "Poción de fuerza", "currentStrength", random.randint(10,15))

class IntelligencePotion(Potion) :
  def __init__(self) :
    Potion.__init__(self, "Poción de inteligencia", "currentIntelligence", random.randint(10,15))