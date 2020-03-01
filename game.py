import gridEngine as ge
import keyboard as kb 
from time import sleep
from random import choice, randint

playerPosition = 5

rock = ge.Object("o", ge.gray, "rock")
player = ge.Player()

grid = ge.Grid()
grid.monoGenerate(rock, 2001)
grid.setProperties()
grid.markup(100)
grid.grid[playerPosition] = player

currentGrid = grid 

def key_listen():
    global playerPosition
    oldPlayerPosition = playerPosition

    if kb.is_pressed("s"):
        newPlayerPosition = playerPosition + currentGrid.gridWidth * player.velocity

    currentGrid.grid[oldPlayerPosition] = player.standingOn
    player.standingOn = currentGrid.grid[newPlayerPosition]
    currentGrid.grid[newPlayerPosition] = player

def physicsCalculate():
    pass


currentGrid.draw(0)
while True:
    previousGrid = currentGrid.grid
    key_listen()
    physicsCalculate()
    if previousGrid != currentGrid.grid:
        currentGrid.draw(0)
