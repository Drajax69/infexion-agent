
from .board import Board
from referee.game.player import PlayerColor
from .commonutils import *


def min_max_strat2(state:Board, current_depth: int, player: PlayerColor, alpha = float('-inf'), beta = float('inf')):
    if current_depth == 0:
        return (util(state), None)
    if ((state.game_won(player) or state.game_won(player.opponent)) and current_depth < 2):
        return (util(state), None)

    if player == PlayerColor.RED :
        best_action = None
        best_score = float('-inf') 
        actions = state.possible_moves_pruned(player)
        for action in actions :
            new_state = state.apply_action(action, player)
            maximising_score, _action = min_max_strat2(new_state, current_depth-1, opponent(player), alpha, beta)
            if(maximising_score > best_score):
                best_score = maximising_score
                best_action = action
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return (best_score, best_action)
    else :
        best_action = None
        worst_score = float('inf') 
        actions = state.possible_moves_pruned(player)
        for action in actions :
            new_state = state.apply_action(action, player)
            minimising_score, _action = min_max_strat2(new_state, current_depth-1, opponent(player), alpha, beta)
            if(minimising_score < worst_score):
                worst_score = minimising_score
                best_action = action
            beta = min(beta, worst_score)
            if beta <= alpha:
                break
        return (worst_score, best_action)

        
def util(state:Board): # Catered assuming RED is maxing and blue is minimising 
    powers = state.calculate_power()
    util_func = (powers[PlayerColor.RED] - powers[PlayerColor.BLUE])
    return util_func
