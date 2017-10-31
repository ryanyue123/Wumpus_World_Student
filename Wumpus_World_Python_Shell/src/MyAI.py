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
import random

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

        self.numRow = 4
        self.numCol = 7

        self.worldMap = [[0]* self.numRow for _ in range(self.numCol)]
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
        self.backtraceIndex = 0

        # ======================================================================
        # YOUR CODE ENDS
        # ======================================================================

    def getAction( self, stench, breeze, glitter,  bump, scream ):
        # ======================================================================
        # YOUR CODE BEGINS
        # ======================================================================
        self.evaluateCurrentPosition(stench, breeze, bump, scream, glitter)
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
    def evaluateCurrentPosition(self, stench, breeze, bump, scream, glitter):
        if (bump):
            self.getOut = True
        if (not glitter):
            if (stench or breeze):
                self.getOut = True

    def chooseRandAdjMove(self):
            possible_moves = []
            r = self.currentRow
            c = self.currentCol
            if (r > 0 and (not (r-1, c) in self.locationHistory)):
                possible_moves.append((r-1, c))
            if (r < self.numRow - 1 and (not (r+1, c) in self.locationHistory)):
                possible_moves.append((r+1, c))
            if (c > 0 and (not (r, c-1) in self.locationHistory)):
                possible_moves.append((r, c-1))
            if (c < self.numCol - 1 and (not (r, c+1) in self.locationHistory)):
                possible_moves.append((r, c+1))

            if (len(possible_moves) == 0):
                return Agent.Action.TURN_LEFT
            else:
                selected = random.randint(0, len(possible_moves)-1)
                return self.processMove(possible_moves[selected][0], possible_moves[selected][1])



    def backtrace(self): #RETURN A MOVE, also call processMove()
        _ = self.locationHistory[-1]
        nextrow, nextcol = self.locationHistory[-2]
        action = self.processMove(nextrow, nextcol)
        if (action == Agent.Action.FORWARD):
            self.locationHistory = self.locationHistory[:-2]
        return action


    def processMove(self, row, col): #RETURNS A MOVE
        #based on currentx, currenty, and nextx, nexty -> change it into a move
        #already have the next location
        #preparing agent for step forward.
        #if moving forward, add
        deltaCol = col - self.currentCol
        deltaRow = row - self.currentRow

        if (deltaCol > 0):
            #north
            if (self.direction == MyAI.Direction.NORTH):
                self.locationHistory.append((row, col))
                self.currentRow = row
                self.currentCol = col
                return Agent.Action.FORWARD
            elif (self.direction == MyAI.Direction.EAST):
                self.direction = MyAI.Direction.NORTH
                return Agent.Action.TURN_LEFT
            elif (self.direction == MyAI.Direction.WEST):
                self.direction = MyAI.Direction.NORTH
                return Agent.Action.TURN_RIGHT
            else:
                self.direction = MyAI.Direction.EAST
                return Agent.Action.TURN_LEFT

        elif (deltaCol < 0):
            #south
            if (self.direction == MyAI.Direction.NORTH):
                self.direction = MyAI.Direction.WEST
                return Agent.Action.TURN_LEFT
            elif (self.direction == MyAI.Direction.EAST):
                self.direction = MyAI.Direction.SOUTH
                return Agent.Action.TURN_RIGHT
            elif (self.direction == MyAI.Direction.WEST):
                self.direction = MyAI.Direction.SOUTH
                return Agent.Action.TURN_LEFT
            else:
                self.locationHistory.append((row, col))
                self.currentRow = row
                self.currentCol = col
                return Agent.Action.FORWARD
        elif (deltaRow > 0):
            #east
            if (self.direction == MyAI.Direction.NORTH):
                self.direction = MyAI.Direction.EAST
                return Agent.Action.TURN_RIGHT
            elif (self.direction == MyAI.Direction.EAST):
                self.locationHistory.append((row, col))
                self.currentRow = row
                self.currentCol = col
                return Agent.Action.FORWARD
            elif (self.direction == MyAI.Direction.WEST):
                self.direction = MyAI.Direction.SOUTH
                return Agent.Action.TURN_LEFT
            else:
                self.direction = MyAI.Direction.EAST
                return Agent.Action.TURN_LEFT
        elif (deltaRow < 0):
            #west
            if (self.direction == MyAI.Direction.NORTH):
                self.direction = MyAI.Direction.WEST
                return Agent.Action.TURN_LEFT
            elif (self.direction == MyAI.Direction.EAST):
                self.direction = MyAI.Direction.NORTH
                return Agent.Action.TURN_LEFT
            elif (self.direction == MyAI.Direction.WEST):
                self.locationHistory.append((row, col))
                self.currentRow = row
                self.currentCol = col
                return Agent.Action.FORWARD
            else:
                self.direction = MyAI.Direction.WEST
                return Agent.Action.TURN_RIGHT
        else:
            return Agent.Action.FORWARD

    # ======================================================================
    # YOUR CODE ENDS
    # ======================================================================
