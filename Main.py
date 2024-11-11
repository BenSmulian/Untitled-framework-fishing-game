
import copy
import random
import time

from torch import clamp, clone, tensor


class obtainable:
     def __init__(self,name : str, rarity : str,type : str,value : str, golden : bool, weightBounds : str):

          wieghtMin, weightMax = map(int,weightBounds.split(","))
          self.WeightBounds = {"Min" : wieghtMin, "Max" : weightMax}
          self.weight = self.WeightBounds["Min"]
          self.Name = name
          self.Type = type
          valueMin, valueMax = map(int,value.split(","))
          self.Value = {"Min" : valueMin, "Max" : valueMax}
          self.Golden = golden
          self.Rarity = rarity
class FishingRod:
     def __init__(self,name : str, catchTime : int, carizma : int, luck : int, goldLuck : int, Cost : int):
          self.Name = name
          self.CatchTime = catchTime
          self.Carizma = carizma
          self.Luck = luck
          self.GoldLuck = goldLuck
          self.Cost = Cost

obtainables = {
     "Salmon" : obtainable("Salmon", "Common", "Fish", "20,40", False, "1,2"),
     "Gun" : obtainable("Gun", "Common", "Hot", "1000,1000000", False, "1,3"),
     "Ultra super legendary fish" : obtainable("Ultra super legendary fish", "Common", "Fish", "1,2", False, "1,3"),

     "Salmonela" : obtainable("Salmonela", "Uncommon", "Fish", "5,40", False, "1,5"),
     "BroFish" : obtainable("BroFish", "Uncommon", "Fish", "200,300", False, "30,50"),
     "PlasticTresureChest" : obtainable("PlasticTresureChest", "Uncommon", "Loot", "1,10", False, "3,10"),
     "FoolsGoldFish" : obtainable("FoolsGoldFish", "Uncommon", "Fish", "50,100", False, "2,5"),

     "StickFish" : obtainable("StickFish", "MediumRare", "Fish", "150,200", False, "5,15"),
     "SpongeBob" : obtainable("SpongeBob", "MediumRare", "Fish", "-100,1000", False, "20,30"),
     "GoldGun" : obtainable("GoldGun","MediumRare","Fish","1,1000000",True,"5,10"),
}

rarityTable = {
     "Common" : 50,
     "Uncommon" : 40,
     "MediumRare" : 10,
}

fishingRods = {
     "Common" : FishingRod("Common",5,1,2,0,0),
     "Uncommon" : FishingRod("Uncommon",4,2,3,0,300),
     "Fishy" : FishingRod("Fishy",3,3,4,0,1000),
     "Yummers" : FishingRod("Yummers",2,4,5,0,5000),
}

class Player:
     def __init__(self,health : int, money : int, rod : FishingRod):
          self.Health = health
          self.Money = money
          self.rod = rod
          self.Collection : list[obtainable] = []
          self.Rods : list[FishingRod] = []
     
     def Sell(self):
          
          for i in self.Collection:
               ChosenNumber = round(random.randint(i.Value["Min"],i.Value["Max"]) * i.weight / i.WeightBounds["Max"])
               print(f"Sold {i.Name} for {ChosenNumber}!")
               self.Collection.pop(self.Collection.index(i))
               self.Money += ChosenNumber
                    
     def view(self):
          
          print("Your collection:")
          for i in self.Collection:
               print(f"Name: {i.Name}, Rarity: {i.Rarity}, Type: {i.Type}, Weight: {i.weight}")
               
          print("\nYour Money: " + str(self.Money))   
          
          print("\nYour Rods:")
          for i in self.Rods:
               print(f"Name: {i.Name}, CatchTime: {i.CatchTime}, Carizma: {i.Carizma}, Luck: {i.Luck}, GoldLuck: {i.GoldLuck}")
          
     def catch(self):
          print("Catching...")
          time.sleep(self.rod.CatchTime)
          
          ChosenNumber = random.randint(0,100)
          ChosenObtainable = None
          rarity = None
          
          aditive = 0
          
          for i,v in enumerate(rarityTable):
               aditive += rarityTable[v]
               
               if ChosenNumber <= aditive:
                    ChosenNumber = i
                    rarity = v
                    break
          
          ChoiceTabel = []
          for i in obtainables:
               if obtainables[i].Rarity == rarity:
                    ChoiceTabel.append(obtainables[i])
                    
          ChosenObtainable : obtainable = random.choice(ChoiceTabel)
          ChosenObtainable = copy.deepcopy(ChosenObtainable)
          ChosenObtainable.weight = random.randint(ChosenObtainable.WeightBounds["Min"],ChosenObtainable.WeightBounds["Max"])
          
          #Golden Chance
          if random.randint(1,100) <= self.rod.GoldLuck:
               ChosenObtainable.Golden = True
          
          ChosenObtainable.weight = random.randint(ChosenObtainable.WeightBounds["Min"],ChosenObtainable.WeightBounds["Max"])
          
          print(f"You caught a {ChosenObtainable.Name}.")
          print(f"{ChosenObtainable.Name} added to your collection!")
          self.Collection.append(ChosenObtainable)
          return ChosenObtainable
     
     def buy(self):
          print("Your Money: " + str(self.Money))
          print(f"Your Currently held Rod: {self.rod.Name}")
          
          print("Available Fishing Rods:")
          for i,v in enumerate(fishingRods):
               print(str(i) + " : " + v)
               printdetails = fishingRods[v]
               print(f"CatchTime: {printdetails.CatchTime}, Carizma: {printdetails.Carizma}, Luck: {printdetails.Luck}, GoldLuck: {printdetails.GoldLuck}\n")
          
          ChosenNumber = input("Choose a number: ")
          ChosenNumber = int(ChosenNumber)
          ChosenRod = list(fishingRods.keys())[ChosenNumber]
          ChosenRod = fishingRods[ChosenRod]
          
          PlayerOwnsRod = False
          for i in self.Rods:
               if i.Name == ChosenRod.Name:
                    PlayerOwnsRod = True
                    break
          
          if ChosenRod.Name == self.rod.Name:
               print("You state deeply into the object in your hand,\nand think to yourself:\nrod.\n")
               return
          
          if not PlayerOwnsRod:
               self.Rods.append(ChosenRod)
               print(f"Successfully bought a {ChosenRod.Name} rod.")
               print(f"{ChosenRod.Name} rod added to your rod collection!")
               self.rod = ChosenRod
          else:
               print(f"You take your {ChosenRod.Name} rod out of your bag and put the last one in.")
               self.rod = ChosenRod

def StartGame():
     print("You encounter a stranger.\n")
     print("Stanger: Hello and welcome to your new job!\n")
     Player1 = Player(100,0,fishingRods["Common"])
     print("You: Huh?")
     
     print("In this game you will catch fish and sell them for money.")
     print("You can also buy rods to catch fish with.")
     print("You a start with a common rod.")
     
     print("To desplay your stats including of:\n- Your Collection\n- Your Money\nand your Rods\nat start of a turn, type 'view'.\n")
     print("To catch a fish, type 'catch'.\n")
     print("To buy or rquip a rod, type 'buy'.\n")
     
     print("You: who said that?")
     print("Stranger: said what?\n")
     
     FirstTimeHearingInvalidInput = True
     
     while True:
          Input = input("\nYou decide to type: ")
          Input = Input.lower()
          
          print("\n")
          
          if Input == "view":
               Player1.view()
          elif Input == "catch":
               Player1.catch()
          elif Input == "buy":
               Player1.buy()
          elif Input == "sell":
               Player1.Sell()
          else:
               print("Invalid choice.")
               if FirstTimeHearingInvalidInput:
                    print("You: Invalid choice? don't I have free will?\nand it's coming from nowhere,\nI left the stranger to go fish like a preety long time ago...\nwhy am I here?...")
                    FirstTimeHearingInvalidInput = False

StartGame()
# Cat

