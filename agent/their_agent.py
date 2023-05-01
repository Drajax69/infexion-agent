# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

# from .min_max_strategy import MinMax
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexDir
from .board import *
from typing import List
from .min_max_strategy import *

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
        valid_moves = self._board.possible_moves_pruned(self._color)
        return valid_moves[0]
        # return min_max_strategy(self, 0) # Currently choosing the first valid move I can find

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
        # self._board.render(ansi=True) # THIS IS TO PRINT MY VERSION OF THE BOARD