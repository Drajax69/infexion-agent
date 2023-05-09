# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

# from .min_max_strategy import MinMax
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexDir
from .board import *
from typing import List
from .min_max_strat2 import *
from .commonutils import START_TIME
# This is my red Agent playing
# The strategy used will be called by the action funciton
# The 


class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        

        self._board = Board()
        self._color = color
        match color:
            case PlayerColor.RED:
                print(" -- MY AGENT IS RED")
            case PlayerColor.BLUE:
                print(" -- MY AGENT IS BLUE")


    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """

        return min_max_strat2(self._board, 3, self._color,initialCall=True)[1]# Currently choosing the first valid move I can find

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                self._board.spawn(cell, color)
                # update my board
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                self._board.spread(cell, direction, color)
                # update my board
                pass
