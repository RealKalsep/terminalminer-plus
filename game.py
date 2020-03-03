import gridEngine as ge
import keyboard as kb 
from time import sleep
from random import choice, randint
from os import system
from pynput.keyboard import Key, Controller

flagToggle = True

keyboard = Controller()

creationTabRecipes = []

playerPosition = 5
gridSize = 2001

rock = ge.Object("o", ge.gray, "rock", None)
wood = ge.Object("w", ge.red, "wood", rock)
stone_wall = ge.Object("█", ge.white, "stone_wall", rock, 0, True)
player = ge.Player()
player.standingOn = rock

grid = ge.Grid()
#grid.monoGenerate(rock, gridSize)
grid.multiGenerate(gridSize, rock, stone_wall)
grid.markup(100)
grid.setProperties()
grid.grid[playerPosition] = player

currentGrid = grid
changes = []

player.inv.append(rock)
player.inv.append(rock)
player.inv.append(wood)

class Recipe:

    required = []

    def __init__(self, name, result, *required):
        self.name = name
        self.result = result
        for i in required:
            self.required.append(i)

    def craft(self):
        for k in range(0, len(self.required)):
            player.inv.remove(self.required[k])

        player.inv.append(self.result)



class Tool:
    def __init__(self, name, toolID):
        self.name = name
        self.toolID = toolID

wooden_pickaxe = Tool("wooden_pickaxe", 1)
woodpickRecipe = Recipe("wooden_pickaxe", wooden_pickaxe, wood, rock)
creationTabRecipes.append(woodpickRecipe)

def userInputDefine(plrInput):
    if plrInput.startswith("eq"):
        splitted = plrInput.split()
        for i in range(0, len(player.inv)):
            if player.inv[i].name == splitted[1]:
                player.eq = player.inv[i]
                print(player.inv[i].name + " equipped")
                break

def inventoryTab():
    userInput = None
    reservedObjects = []
   

    system("cls")
    print("YOUR INVENTORY. <HELP> FOR A LIST OF COMMANDS")

    for i in range(0, len(player.inv)):
        if player.inv.count(player.inv[i]) > 1 and not (player.inv[i] in reservedObjects):
            print(player.inv[i].name + " x" + str( player.inv.count( player.inv[i] ) ))
            reservedObjects.append(player.inv[i])
        elif player.inv.count(player.inv[i]) == 1:
            print(player.inv[i].name + " x1")

    #keyboard.press(Key.enter)
    userInput = input()
    #keyboard.release(Key.enter)
    while userInput != "e":
        userInputDefine(userInput)
        userInput = input()
    currentGrid.draw(0)

def creationTab():
    system('cls')


    isPossibleToCraft = []
    availableRecipes = []

    print("CREATION MENU. \n AVAILABLE BLUEPRINTS:")

    for i in range(0, len(creationTabRecipes)):
        for j in creationTabRecipes[i].required:
            if j in player.inv:
                isPossibleToCraft.append(True)
            else:
                isPossibleToCraft.append(False)

        if not (False in isPossibleToCraft):
            print(creationTabRecipes[i].name)
            availableRecipes.append(creationTabRecipes[i])

    userInput = input()
    while userInput != "q":
        if userInput.startswith("craft"):
            splitted = userInput.split()
            for i in range(0, len(availableRecipes)):
                if splitted[1] == availableRecipes[i].name:
                    availableRecipes[i].craft()
                    print("you crafted {0}!".format(availableRecipes[i].name))

        userInput = input()
    currentGrid.draw(0)

def key_listen():
    global playerPosition
    global changes
    oldPlayerPosition = playerPosition

    #Sorry for big comparing lines. But i think this is the only way, excluding if-else stairs.
    #First condition - if key is pressed
    #Second condition - if player stays near one of 4 borders
    #Third condition - checking if "destination point" haven't any collision

    #The reason why 1 is being added in <S> and <W> movements is preventing player's offset. 

    if kb.is_pressed("s") and not (playerPosition in range( (gridSize - currentGrid.gridWidth), gridSize) ) and (currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1) * player.velocity].collision ==False): 
        changes.append(True)
        newPlayerPosition = playerPosition + (currentGrid.gridWidth + 1) * player.velocity

        currentGrid.grid[oldPlayerPosition] = player.standingOn
        player.standingOn = currentGrid.grid[newPlayerPosition]
        currentGrid.grid[newPlayerPosition] = player
        playerPosition = newPlayerPosition
        sleep(0.1)

    elif kb.is_pressed("w") and not (playerPosition in range(0, currentGrid.gridWidth)) and (currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1) * player.velocity) ].collision == False): 
        changes.append(True)
        newPlayerPosition = playerPosition - (currentGrid.gridWidth + 1) * player.velocity 

        currentGrid.grid[oldPlayerPosition] = player.standingOn
        player.standingOn = currentGrid.grid[newPlayerPosition]
        currentGrid.grid[newPlayerPosition] = player
        playerPosition = newPlayerPosition
        sleep(0.1)

    elif kb.is_pressed("d") and ( (playerPosition + 2) % 100 != 0) and (currentGrid.grid[ playerPosition + 1 * player.velocity ].collision == False): 
        changes.append(True)

        newPlayerPosition = playerPosition + 1 * player.velocity

        currentGrid.grid[oldPlayerPosition] = player.standingOn #===================================================================================#
        player.standingOn = currentGrid.grid[newPlayerPosition] #                                                                                   #
        currentGrid.grid[newPlayerPosition] = player            # COPY+PASTE IN ALL MOVEMENT CHECKS. PURPOSE: UPDATING PLAYER'S POSITION ON SCREEN  #
        playerPosition = newPlayerPosition                      #                                                                                   #
        sleep(0.1)                                              #===================================================================================#

    elif kb.is_pressed("a") and ( playerPosition % 100 != 0 ) and (currentGrid.grid[ playerPosition - 1 * player.velocity ].collision == False):
        changes.append(True)

        newPlayerPosition = playerPosition - 1 * player.velocity

        currentGrid.grid[oldPlayerPosition] = player.standingOn
        player.standingOn = currentGrid.grid[newPlayerPosition]
        currentGrid.grid[newPlayerPosition] = player
        playerPosition = newPlayerPosition
        sleep(0.1)

    #TABS OPENING

    elif kb.is_pressed("e"):
        inventoryTab()

    elif kb.is_pressed('q'):
        creationTab()

    #BLOCK BREAKING USING ARROWS
    try:
        if kb.is_pressed("right arrow") and currentGrid.grid[ playerPosition + 1 ].collision and player.eq.toolID == 1 and ( (playerPosition + 2) % 100 != 0):
                currentGrid.grid[playerPosition + 1] = currentGrid.grid[playerPosition + 1].bottomTile
                player.inv.append(currentGrid.grid[playerPosition + 1])
                currentGrid.draw(0)

        elif kb.is_pressed("left arrow") and ( playerPosition % 100 != 0 ) and (currentGrid.grid[ playerPosition - 1 ].collision) and player.eq.toolID == 1:
            currentGrid.grid[playerPosition - 1] = currentGrid.grid[playerPosition - 1].bottomTile
            player.inv.append(currentGrid.grid[playerPosition - 1])
            currentGrid.draw(0)

        elif kb.is_pressed("up arrow") and not (playerPosition in range(0, currentGrid.gridWidth)) and (currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ].collision):
            currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ] = currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ].bottomTile
            player.inv.append(currentGrid.grid[ (playerPosition - (currentGrid.gridWidth + 1)) ])
            currentGrid.draw(0)

        elif kb.is_pressed("down arrow")  and not (playerPosition in range( (gridSize - currentGrid.gridWidth), gridSize) ) and (currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].collision):
            currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)] = currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)].bottomTile
            player.inv.append(currentGrid.grid[playerPosition + (currentGrid.gridWidth + 1)])
            currentGrid.draw(0)
    except AttributeError:
        pass

        

def physicsCalculate():
    pass


currentGrid.draw(0)
while True:
    previousGrid = currentGrid.grid
    key_listen()
    physicsCalculate()
    #if previousGrid != currentGrid.grid:
    if True in changes:
        currentGrid.draw(0)
        changes = []
