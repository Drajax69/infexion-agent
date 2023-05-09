# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

# from .min_max_strategy import MinMax
from referee.game import \
    PlayerColor, Action, SpawnAction, SpreadAction, HexDir
from .board import *
from typing import List
from .min_max_strat2 import *
from .commonutils import *
import time
# This is my red Agent playing
# The strategy used will be called by the action funciton
# The 


class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self.time_remaining = 180
        self.turn_count = 1
        self._board = Board()
        self._color = color
        match color:
            case PlayerColor.RED:
                print("-- MY AGENT IS RED")
            case PlayerColor.BLUE:
                print("-- MY AGENT IS BLUE")


    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        # Reset globals
        # START_TIME = None
        # ELAPSED_TIME = 0
        self.time_remaining = referee['time_remaining']
        self.turn_count += 1
    
        
        """ Dynamic time allocation for search """
        # max_time = self.time_remaining*(self.turn_count/170.0)
        if(self.time_remaining>15): # Calm mode
            max_time = self.turn_count/2.5
        else:
            max_time = self.time_remaining*(self.turn_count/170.0)

        actions = self._board.possible_moves_pruned(self._color)
        ''' Dynamic Deepening '''
        # depth = self.get_depth(len(actions))
        print(f'{self._color}::{max_time}::{self.time_remaining}|| turn: {self.turn_count} || {len(actions)}')

        return iterative_deepening_minmax(self._board, self._color, max_time, turn=self.turn_count) # Currently choosing the first valid move I can find

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        match action:
            case SpawnAction(cell):
                self._board.spawn(cell, color)
                pass
            case SpreadAction(cell, direction):
                self._board.spread(cell, direction, color)
                # update my board
                pass

    def get_depth(self,num_actions):
        if self.turn_count < 4:
            depth = 3
        elif self.turn_count <= 15 and num_actions < 70:
            depth = 4
        elif num_actions < 20:
            depth = 5
        elif num_actions < 70:
            depth = 4
        elif num_actions < 140:
            depth = 3
        else:
            depth = 2
        return depth