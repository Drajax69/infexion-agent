from copy import deepcopy
from agent.commonutils import *
from referee.game.actions import *
from referee.game.player import PlayerColor
from referee.game.hex import HexDir, HexPos
from typing import List


class Board:
    def __init__(self):
        self.board = {}
        self.maxrq = 7
        # Example:

        #     >>> board = {
        #     ...     (5, 6): ("r", 2),
        #     ...     (1, 0): ("b", 2),
        #     ...     (1, 1): ("b", 1),
        #     ...     (3, 2): ("b", 1),
        #     ...     (1, 3): ("b", 3),
        #     ... }

    def get_empty_cells(self) -> List:
        empty_cells = []
        for r in range(7):
            for q in range(7):
                if (r, q) not in self.board:
                    empty_cells.append(HexPos(r, q))
        return empty_cells

    def get_player_tiles(self, color:PlayerColor):
        tiles = []
        for pos, value in self.board.items():
            if value[0] == color:
                tiles.append(HexPos(pos[0], pos[1]))
        return tiles

    def apply_action(self, action:Action, color: PlayerColor):
        board_copy = deepcopy(self)
        match action:
            case SpawnAction(cell):
                board_copy.spawn(cell, color)
            case SpreadAction(cell, direction):
                board_copy.spread(cell, direction, color)
        return board_copy
             
        
    def spawn(self, pos: HexPos, color:PlayerColor):
        self.board[(pos.r, pos.q)] = (color, 1)

    def spread(self, cell: HexPos, dir: HexDir, color: PlayerColor): # NEEDS EDITING
        r = cell.r
        q = cell.q
        value = self.board[(r,q)][1]
        self.board.pop((r,q)) 
        for i in range(1,value+1):
            r_new = (r+dir.r*i)%7
            q_new = (q+dir.q*i)%7
            if not ((r_new,q_new) in self.board): # Case empty cell
                self.board[(r_new,q_new)] = (color,1)
            else: # Case it is occupied
                if(self.board[(r_new,q_new)][1]+1 <= 6):
                    self.board[(r_new,q_new)] = (color, self.board[(r_new,q_new)][1]+1)
                else:
                    self.board.pop((r_new,q_new), None)
        return self.board
        
    def verify_legal(self, action):
        # If total power < 49 return true
        if(self.get_total_power() < 49):
            return True
        return False

    def get_total_power(self):
        powers = self.calculate_power() 
        return powers[PlayerColor.RED] + powers[PlayerColor.BLUE]

    def render(self, ansi=False): 
        # This function has been copied from Infexion Part A 
        # - 2023 Artificial Intelligence Semester 2
        dim = 7
        output = ""
        for row in range(dim * 2 - 1):
            output += "    " * abs((dim - 1) - row)
            for col in range(dim - abs(row - (dim - 1))):
                r = max((dim - 1) - row, 0) + col
                q = max(row - (dim - 1), 0) + col
                if (r, q) in self.board:
                    color, power = self.board[(r, q)]
                    text = f"{map_color(color)}{power}".center(4)
                    if ansi:
                        output += apply_ansi(text, color=map_color(color), bold=False)
                    else:
                        output += text
                else:
                    output += " .. "
                output += "    "
            output += "\n"
        print(output)
    
    def calculate_power(self):
        power_dict ={PlayerColor.RED: 0, PlayerColor.BLUE: 0}
        for pos, value in self.board.items():
            if(value[0] == PlayerColor.RED):
                power_dict[PlayerColor.RED] += value[1]
            elif(value[0] == PlayerColor.BLUE):
                power_dict[PlayerColor.BLUE] += value[1]
        return power_dict
    
    def find_cells(self, colour:PlayerColor):
        """Returns a list of all the red cells in state in format -> (r, q, power)"""
        
        pos = []
        for key,value in self.items():
            if value[0] == colour:
                pos.append(((key[0],key[1],value[1])))
        return pos

    def possible_moves(self, color: PlayerColor) -> List[Action]:
        """
        Return a list of all valid moves for the current player.
        """
        valid_moves = []
        for cell in self.get_empty_cells(): 
            if(self.verify_legal(SpawnAction(cell))): # Create verify legal function
                valid_moves.append(SpawnAction(cell))

        for cell in self.get_player_tiles(color): 
            for direction in HexDir:
                valid_moves.append(SpreadAction(cell, direction))

        return valid_moves

    def possible_moves_pruned(self, color: PlayerColor) -> List[Action]:
            """
            Return a list of pruned moves for a Player
            Pruning Strategies:
            - Symmetry of board
            - Unnecessary Spawns
            - Unnecessary Spread (Careful)
            - Spread operations first
            """

            valid_moves = []
            empty_cells = self.get_empty_cells()

            # First move returns Spawn in middle
            if(len(empty_cells) == 49):
                return [SpawnAction(HexPos(3,3))]

            for cell in self.get_player_tiles(color): 
                for direction in HexDir:
                    if(self.pruned_valid(SpreadAction(cell, direction), valid_moves, color)):
                        valid_moves.append(SpreadAction(cell, direction))

            for cell in empty_cells: 
                if(self.verify_legal(SpawnAction(cell))): # Create verify legal function
                    if(self.pruned_valid(SpawnAction(cell), valid_moves, color)):
                        valid_moves.append(SpawnAction(cell))


            return valid_moves


    def pruned_valid(self, action: Action, valid_moves: List[Action], color: PlayerColor):
        match action:
            case SpreadAction(cell, direction):
            
                pass
            case SpawnAction(cell): # Spawning Strategy
                neighbours = self.neighbouring_colors(cell)
                if(opponent(color) in neighbours): # Don't spawn if opponent is right next to you
                    return False
                if(color not in neighbours and len(self.get_player_tiles(color)) > 0): # Spawn next to ur tiles if they exist
                    return False
                
                # if() : # Doesn't really matter where you spawn, so choose one at random
                pass

        return True

    def neighbouring_colors(self, cell:HexPos) -> List: # Returns a list of neighbouring colours
        colors: List[PlayerColor] = []
        dirs = [(0,1),(-1,1),(-1,0),(0,-1),(1,-1),(1,0)]
        r = cell.r
        q = cell.q
        for dir in dirs:
            if(((r + dir[0])%7,(q + dir[1])%7) in self.board):
                colors.append(self.board[(r + dir[0],q + dir[1])][0])

        return colors


    def game_won(self, player: PlayerColor):
        """
        Returns 0 if opponent has no tiles
        """
        return not len(self.get_player_tiles(opponent(player)))

