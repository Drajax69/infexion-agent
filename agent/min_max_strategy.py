from .board import Board
from referee.game.player import PlayerColor
from .commonutils import *

def evaluate_state(state: Board, player: PlayerColor, current_depth: int, alpha=float('-inf'), beta=float('inf')) -> int:
    if current_depth == 0:
        return util(state, player)
    if ((state.game_won(player) or state.game_won(player.opponent)) and current_depth < 2):
        return util(state, player)
    # MinMax algorithm
    if player == PlayerColor.RED:  # maximizing player
        best_score = float('-inf')
        actions = state.possible_moves_pruned(player)
        sorted_actions = sorted(actions, key=lambda action: util(state.apply_action(action, player), player.opponent), reverse=True)
        for action in sorted_actions:
            new_state = state.apply_action(action, player)
            score = evaluate_state(new_state, opponent(player), current_depth-1, alpha, beta)
            best_score = max(best_score, score)
            alpha = max(alpha, best_score)
            if beta <= alpha:
                break
        return best_score
    else:  # minimizing player
        worst_score = float('inf')
        actions = state.possible_moves_pruned(player)
        sorted_actions = sorted(actions, key=lambda action: util(state.apply_action(action, player), player.opponent), reverse=False)
        for action in sorted_actions:
            new_state = state.apply_action(action, player)
            score = evaluate_state(new_state, opponent(player), current_depth-1, alpha, beta)
            worst_score = min(worst_score, score)
            beta = min(beta, worst_score)
            if beta <= alpha:
                break
        return worst_score


def min_max_strategy(agent, depth = 3):
    """
    Implements the MinMax algorithm to select the next action.
    """
    # Choose the best action according to the MinMax algorithm
    best_action = None
    best_score = float('inf') if agent._color == PlayerColor.BLUE else float('-inf')

    actions: List[Action] = agent._board.possible_moves_pruned(agent._color)
    print(f'Number of moves : {len(actions)}')

    sorted_actions = sorted(actions, key=lambda action: util(agent._board.apply_action(action, agent._color), agent._color.opponent), reverse=agent._color == PlayerColor.RED)
    """Sorting it helps with the alpha-beta pruning -> Show why so (ADD REFERENCE)
        Idea is if we somehow greedily sort it beforehand, it should likely make the game much faster
    """
    # print(actions)

    for action in sorted_actions:
        new_state:Board = agent._board.apply_action(action, agent._color)
        if(new_state.game_won(agent._color)): # Case next move is game end - no point searching
            return action
        score = evaluate_state(new_state, agent._color.opponent, depth-1)
        if agent._color == PlayerColor.RED:
            if score > best_score:
                best_score = score
                best_action = action
        elif agent._color == PlayerColor.BLUE:
            if score < best_score:
                best_score = score
                best_action = action
    return best_action

def util(state:Board, player: PlayerColor): # Catered assuming RED is maxing and blue is minimising 
    powers = state.calculate_power()
    # print(powers)
    util_func = (powers[PlayerColor.RED] - powers[PlayerColor.BLUE])/(powers[PlayerColor.RED] + powers[PlayerColor.BLUE])
    # print(powers)
    # print(util_func)
    return util_func
