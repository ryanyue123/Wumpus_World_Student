# ======================================================================
# FILE:        MyAI.py
#
# AUTHOR:      Abdullah Younis
#
# DESCRIPTION: This file contains your agent class, which you will
#              implement. You are responsible for implementing the
#              'getAction' function and any helper methods you feel you
#              need.
#
# NOTES:       - If you are having trouble understanding how the shell
#                works, look at the other parts of the code, as well as
#                the documentation.
#
#              - You are only allowed to make changes to this portion of
#                the code. Any changes to other portions of the code will
#                be lost when the tournament runs your code.
# ======================================================================

from Agent import Agent
from enum import Enum
from random import random

class MyAI ( Agent ):
    class Direction(Enum):
        NORTH = 1
        EAST = 2
        SOUTH = 3
        WEST = 4

    class CellEvaluation:
        def __init__(self, x, y , score):
            self.x = x
            self.y = y
            self.score = score



    def __init__ ( self ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================

        self.numRow = numRow
        self.numCol = numCol

        self.worldMap = [[0]* numRow] * numCol
        self.worldMap[0][0] = 1

        self.currentRow = 0
        self.currentCol = 0

        self.getOut = False
        self.hasGold = False
        self.hasArrow = True
        self.direction = MyAI.Direction.EAST

        self.wumpusKilled = False

        self.locationHistory = []
        self.locationHistory.append((0, 0))

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter,  bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.evaluateCurrentPosition(stench, breeze, bump, scream)
        if (not self.hasGold and not self.getOut):
            if (glitter):
                self.hasGold = True
                return Agent.Action.GRAB
            else:
                return self.chooseRandAdjMove()

        else:
            if (self.currentRow == 0 and self.currentCol == 0):
                return Agent.Action.CLIMB
            else:
                return self.backtrace()



        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================



    # ======================================================================
    # YOUR CODE BEGINS
    # ======================================================================
    def evaluateCurrentPosition(self, stench, breeze, bump, scream):
        if (bump):
            self.locationHistory.pop()
            resetLocation = locationHistory[-1]
            self.currentRow = resetLocation.first
            self.currentCol = resetLocation.second
            if (self.direction == MyAI.direction.EAST):
                if (self.currentCol > 0):
                    self.numCol = self.currentCol + 1
            elif (self.direction == MyAI.direction.NORTH):
                if (self.currentRow > 0):
                    self.numRow = self.currentRow + 1

        if (stench or breeze):
            self.getOut = True

    def chooseRandAdjMove(self):
        possible_moves = []
        if (currentRow > 0):
            possible_moves.append((currentRow - 1, currentCol))
        if (currentRow < numRow - 1):
            possible_moves.append((currentRow + 1, currentCol))
        if (currentCol > 0):
            possible_moves.append((currentRow, currentCol - 1))
        if (currentCol < numCol - 1):
            possible_moves.append((currentRow, currentCol + 1))

        for i in range(len(possible_moves)):
            x,y = possible_moves[i]
            if (self.worldMap[x][y] == 1):
                del possible_moves[i]

        selected = randomint(0, len(possible_moves))
        return self.processMove(possible_moves[selected].first, possible_moves[selected].second)



    def backtrace(self): #RETURN A MOVE, also call processMove()
        #location history, move back to square (1,1) or (0,0)
        deltaX = self.locationHistory[-1][1] - self.currentCol
        deltaY = self.locationHistory[-1][0] - self.currentRow

        if(deltaX > 0 and deltaY == 0):
            #go east
            if(self.direction == MyAI.Direction.NORTH):
                self.direction = MyAI.Direction.EAST
                return Agent.Action.TURN_RIGHT
            elif(self.direction == MyAI.Direction.SOUTH):

                self.direction = MyAI.Direction.EAST
                return Agent.Action.TURN_LEFT
            elif(self.direction == MyAI.Direction.WEST):

                self.direction = MyAI.Direction.NORTH
                return Agent.Action.TURN_RIGHT
            else:
                self.locationHistory.pop()
                return Agent.Action.FORWARD
        elif(deltaX < 0 and deltaY == 0):
            #go west
            if(self.direction == MyAI.Direction.NORTH):
                self.direction = MyAI.Direction.WEST
                return Agent.Action.TURN_LEFT
            elif(self.direction == MyAI.Direction.SOUTH):
                self.direction = MyAI.Direction.WEST
                return Agent.Action.TURN_RIGHT
            elif(self.direction == MyAI.Direction.EAST):
                self.direction= MyAI.Direction.SOUTH
                return Agent.Action.TURN_RIGHT
            elif(self.direction == MyAI.Direction.WEST):
                self.locationHistory.pop()
                return Agent.Action.FORWARD

        elif(deltaX == 0 and deltaY > 0):
            #go north
            if(self.direction == MyAI.Direction.NORTH):
                self.locationHistory.pop()
                return Agent.Action.FORWARD
            elif(self.direction == MyAI.Direction.SOUTH):
                self.direction = MyAI.Direction.WEST
                return Agent.Action.TURN_RIGHT
            elif(self.direction == MyAI.Direction.EAST):
                self.direction = MyAI.Direction.NORTH
                return Agent.Action.TURN_LEFT
            else:
                self.direction = MyAI.Direction.NORTH
                return Agent.Action.TURN_RIGHT


        elif(deltaX == 0 and deltaY < 0):
            #go south
            if(self.direction == MyAI.Direction.NORTH):
                self.direction = MyAI.Direction.EAST
                return Agent.Action.TURN_LEFT
            elif(self.direction == MyAI.Direction.SOUTH):
                self.locationHistory.pop()
                return Agent.Action.FORWARD
            elif(self.direction == MyAI.Direction.EAST):
                self.direction = MyAI.Direction.SOUTH
                return Agent.Action.TURN_RIGHT
            else:
                self.direction = MyAI.Direction.SOUTH
                return Agent.Action.TURN_LEFT


    def processMove(self, nextX, nextY): #RETURNS A MOVE
        #based on currentx, currenty, and nextx, nexty -> change it into a move
        #already have the next location
        #preparing agent for step forward.
        #if moving forward, add
        deltaX = nextX - self.currentCol
        deltaY = nextY - self.currentRow

        if(deltaX > 0 and deltaY == 0):
            #go east
            if(self.direction == MyAI.Direction.NORTH):
                self.direction = MyAI.Direction.EAST
                return Agent.Action.TURN_RIGHT

            elif(self.direction == MyAI.Direction.SOUTH):
                self.direction = MyAI.Direction.EAST
                return Agent.Action.TURN_LEFT

            elif(self.direction == MyAI.Direction.WEST):
                self.direction = MyAI.Direction.NORTH
                return Agent.Action.TURN_RIGHT
            else:
                self.locationHistory.append((nextY, nextX))
                self.currentRow = nextY
                self.currentCol = nextX
                self.direction = MyAI.Direction.EAST
                return Agent.Action.FORWARD
        elif(deltaX < 0 and deltaY == 0):
            #go west
            if(self.direction == MyAI.Direction.NORTH):
                self.direction = MyAI.Direction.WEST
                return Agent.Action.TURN_LEFT
            elif(self.direction == MyAI.Direction.SOUTH):
                self.direction = MyAI.Direction.WEST
                return Agent.Action.TURN_RIGHT
            elif (self.direction == MyAI.Direction.EAST):
                self.direction = MyAI.Direction.SOUTH
                return Agent.Action.TURN_RIGHT
            else:
                self.locationHistory.append((nextY, nextX))
                self.currentRow = nextY
                self.currentCol = nextX
                self.direction = MyAI.Direction.WEST
                return Agent.Action.FORWARD
        elif(deltaX == 0 and deltaY > 0):
            #go up
            if(self.direction == MyAI.Direction.NORTH):
                self.locationHistory.append((nextY, nextX))
                self.currentRow = nextY
                self.currentCol = nextX
                return Agent.Action.FORWARD
            elif(self.direction == MyAI.Direction.SOUTH):
                self.direction = MyAI.Direction.WEST
                return Agent.Action.TURN_RIGHT
            elif(self.direction == MyAI.Direction.WEST):
                self.direction = MyAI.Direction.NORTH
                return Agent.Action.TURN_RIGHT
            else:
                self.direction = MyAI.Direction.NORTH
                return Agent.Action.TURN_LEFT

        elif(deltaX == 0 and deltaY < 0):
            #go down
            if(self.direction == MyAI.Direction.NORTH):
                self.direction = MyAI.Direction.EAST
                return Agent.Action.TURN_RIGHT
            elif(self.direction == MyAI.Direction.SOUTH):
                self.locationHistory.append((nextY, nextX))
                self.currentRow = nextY
                self.currentCol = nextX
                return Agent.Action.FORWARD
            elif(self.direction == MyAI.Direction.WEST):
                self.direction = MyAI.Direction.SOUTH
                return Agent.Action.TURN_LEFT
            else:
                self.direction = MyAI.Direction.SOUTH
                return Agent.Action.TURN_RIGHT
    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
