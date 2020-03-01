import gridEngine as ge
import keyboard as kb 
from time import sleep
from random import choice, randint

playerPosition = 5
gridSize = 2001

rock = ge.Object("o", ge.gray, "rock")
player = ge.Player()
player.standingOn = rock

grid = ge.Grid()
grid.monoGenerate(rock, gridSize)
grid.markup(100)
grid.setProperties()
grid.grid[playerPosition] = player

currentGrid = grid
changes = []

def key_listen():
    global playerPosition
    global changes
    oldPlayerPosition = playerPosition

    if kb.is_pressed("s") and not (playerPosition in range( (gridSize - currentGrid.gridWidth), gridSize) ): #checking if player standing at the bottom. If he is, don't move him.
        changes.append(True)
        newPlayerPosition = playerPosition + (currentGrid.gridWidth + 1) * player.velocity #Calculating new player position. Adding 1 to prevent player offset to left.

        currentGrid.grid[oldPlayerPosition] = player.standingOn
        player.standingOn = currentGrid.grid[newPlayerPosition]
        currentGrid.grid[newPlayerPosition] = player
        playerPosition = newPlayerPosition
        sleep(0.1)

    elif kb.is_pressed("w") and not (playerPosition in range(0, currentGrid.gridWidth)): #checking is player standing at the top. If he is, don't move him
        changes.append(True)
        newPlayerPosition = playerPosition - (currentGrid.gridWidth + 1) * player.velocity #Calculating new player position. Adding 1 to prevent player offset to left.

        currentGrid.grid[oldPlayerPosition] = player.standingOn
        player.standingOn = currentGrid.grid[newPlayerPosition]
        currentGrid.grid[newPlayerPosition] = player
        playerPosition = newPlayerPosition
        sleep(0.1)

    elif kb.is_pressed("d") and ( (playerPosition + 2) % 100 != 0): #checking right border
        changes.append(True)

        newPlayerPosition = playerPosition + 1 * player.velocity

        currentGrid.grid[oldPlayerPosition] = player.standingOn #===================================================================================#
        player.standingOn = currentGrid.grid[newPlayerPosition] #                                                                                   #
        currentGrid.grid[newPlayerPosition] = player            # COPY+PASTE IN ALL MOVEMENT CHECKS. PURPOSE: UPDATING PLAYER'S POSITION ON SCREEN  #
        playerPosition = newPlayerPosition                      #                                                                                   #
        sleep(0.1)                                              #===================================================================================#

    elif kb.is_pressed("a") and ( playerPosition % 100 != 0 ):
        changes.append(True)

        newPlayerPosition = playerPosition - 1 * player.velocity

        currentGrid.grid[oldPlayerPosition] = player.standingOn
        player.standingOn = currentGrid.grid[newPlayerPosition]
        currentGrid.grid[newPlayerPosition] = player
        playerPosition = newPlayerPosition
        sleep(0.1)

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
