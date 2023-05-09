
from .board import Board
from referee.game.player import PlayerColor
from .commonutils import *
import time


def min_max_strat2(state:Board, current_depth: int, player: PlayerColor, alpha = float('-inf'), beta = float('inf'), initialCall=False, MAX_TIME=5):
    if current_depth == 0:
        return (state.util(), None)
    if ((state.game_won(player) or state.game_won(player.opponent)) and current_depth < 2):
        return (state.util(), None)
    ##############################################
    """To ensure we never cross the time limit"""
    global ELAPSED_TIME,START_TIME
    

    if initialCall:
        START_TIME = time.time()
        ELAPSED_TIME = 0

    ELAPSED_TIME = time.time() - START_TIME
    if(ELAPSED_TIME >= MAX_TIME):
        return (state.util(), None)

    ##############################################  
    if player == PlayerColor.RED :
        best_action = None
        best_score = float('-inf') 
        actions = state.possible_moves_pruned(player)
        for action in actions:
            new_state = state.apply_action(action, player)
            maximising_score, _action = min_max_strat2(new_state, current_depth-1, opponent(player), alpha, beta,MAX_TIME=MAX_TIME)
            if(maximising_score > best_score):
                best_score = maximising_score
                best_action = action
            alpha = max(alpha, best_score)
            if beta <= alpha or ELAPSED_TIME >= MAX_TIME:
                break
        return (best_score, best_action)
    else :
        best_action = None
        worst_score = float('inf') 
        actions = state.possible_moves_pruned(player)
        for action in actions :
            new_state = state.apply_action(action, player)
            minimising_score, _action = min_max_strat2(new_state, current_depth-1, opponent(player), alpha, beta,MAX_TIME=MAX_TIME)
            if(minimising_score < worst_score):
                worst_score = minimising_score
                best_action = action
            beta = min(beta, worst_score)
            if beta <= alpha or ELAPSED_TIME >= MAX_TIME:
                break
        return (worst_score, best_action)

# def iterative_deepening_search(state: Board, player: PlayerColor, MAX_TIME=5):
#     global START_TIME, ELAPSED_TIME
#     START_TIME = time.time()
#     depth = 1
#     best_action = None

#     while True:
#         try:
#             best_score, best_action = min_max_strat2(state, depth, player, MAX_TIME=MAX_TIME, initialCall=True)
#             depth += 1
#         except TimeoutError:
#             break

#         ELAPSED_TIME = time.time() - START_TIME
#         if ELAPSED_TIME >= MAX_TIME:
#             break

#     return best_action