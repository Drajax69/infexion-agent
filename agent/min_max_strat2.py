
from .board import Board
from referee.game.player import PlayerColor
from .commonutils import *

def min_max_strat2(state:Board, depth: int, color: PlayerColor, isMaximizingPlayer:bool, alpha = float('-inf'), beta = float('inf')):

    if depth == 0:
        return (util(state, color), None)
    if ((state.game_won(color) or state.game_won(color.opponent)) and depth < 2):
        return (util(state, color), None)

    bestAction = None
    if isMaximizingPlayer :
        bestVal = float('-inf') 
        actions = state.possible_moves_pruned(color)
        for action in actions :
            value, _action = min_max_strat2(state, depth-1, color.opponent, False, alpha, beta)
            print(f'Max: {value}')
            if(bestVal < value):
                bestVal = value
                bestAction = action
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return (bestVal, bestAction)
    else :
        bestVal = float('-inf') 
        actions = state.possible_moves_pruned(color)
        for action in actions :
            value, _action = min_max_strat2(state, depth-1, color.opponent, True, alpha, beta)
            print(f'Min: {value}')
            if(bestVal > value):
                bestVal = value
                bestAction = action
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return (bestVal, bestAction)

def util(state:Board, color:PlayerColor): # Catered assuming RED is maxing and blue is minimising 
    powers = state.calculate_power()
    util_func = (powers[color] - powers[color.opponent])
    return util_func
