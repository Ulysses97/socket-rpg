import importlib

potion = importlib.import_module("src.potion")

class Character :
  def __init__(self, name, hp, mana, strength, intelligence, armor, magicResist) :
    self.baseStats = {
      "name" : name,
      "lvl" : 1,
      "maxHp" : hp,
      "maxMana" : mana,
      "strength" : strength,
      "intelligence" : intelligence,
      "armor" : armor,
      "magicResist" : magicResist
    }

    self.stats = {
      "dead" : False,
      "requiredExp" : 200,
      "currentExp" : 0,
      "currentHp" : hp,
      "currentMana" : mana,
      "currentStrength" : strength,
      "currentIntelligence" : intelligence,
      "currentArmor" : armor,
      "currentMagicResist" : magicResist,
      "stunned" : False
    }

    self.inventory = [potion.HealthPotion(), potion.HealthPotion(), potion.StrengthPotion(), potion.IntelligencePotion()]

  def getBaseStats(self) :
    return self.baseStats

  def getStats(self) :
    return self.stats

  def setBaseStat(self, key, value) :
    self.baseStats[key] = value

  def setStat(self, key, value) :
    self.stats[key] = value

  def getInventory(self) :
    return self.inventory

  def addToInventory(self, item) :
    self.inventory.append(item)

  def removeFromInventory(self, item) :
    self.inventory.remove(item)

  def takeDamage(self, dmgType, amount) :
    if dmgType == "physical" :
      dmgMult = 100.0 / (100 + self.stats["currentArmor"])
      self.setStat("currentHp",int(round(self.stats["currentHp"] - (amount * dmgMult))))
    elif dmgType == "magical" :
      dmgMult = 100.0 / (100 + self.stats["currentMagicResist"])
      self.setStat("currentHp",int(round(self.stats["currentHp"] - (amount * dmgMult))))
