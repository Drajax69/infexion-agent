# COMP30024 Artificial Intelligence, Semester 1 2023
# Project Part B: Game Playing Agent

from referee.game import \
    Board, PlayerColor, Action, SpawnAction, SpreadAction, HexPos, HexDir


# This is the entry point for your game playing agent. Currently the agent
# simply spawns a token at the centre of the board if playing as RED, and
# spreads a token at the centre of the board if playing as BLUE. This is
# intended to serve as an example of how to use the referee API -- obviously
# this is not a valid strategy for actually playing the game!

def evaluate(state, color):
    total = 0
    me = 0
    opponent = 0
    for key, value in state._state.items():
        if value.player != None:
            total += value.power
            if value.player == color:
                me += value.power
            elif value.player == color.opponent:
                opponent += value.power
    return (me - opponent) / total
    
def final_state(state: Board):
    bluecount = 0
    redcount = 0
    for key, value in state._state.items():
        if value.player == PlayerColor.BLUE:
            bluecount += 1
        elif value.player == PlayerColor.RED:
            redcount += 1
    if (redcount == 0 or bluecount == 0):
        if (redcount != 0 or bluecount != 0):
            return True
    return False
    
def find_actions(state: Board, color: PlayerColor):
    actions = []
    for key, value in state._state.items():
        if value.player == None:
            if state._color_power(color) + state._color_power(color.opponent) < 49:
                action = SpawnAction(key)
                actions.append(action)
        elif value.player == color:
            action = SpreadAction(key, HexDir.Up)
            actions.append(action)
            action = SpreadAction(key, HexDir.DownRight)
            actions.append(action)
            action = SpreadAction(key, HexDir.DownLeft)
            actions.append(action)
            action = SpreadAction(key, HexDir.UpLeft)
            actions.append(action)
            action = SpreadAction(key, HexDir.UpRight)
            actions.append(action)
            action = SpreadAction(key, HexDir.Down)
            actions.append(action)
    #print(actions)
    actions.sort(key = lambda action: evaluate(nxt_state(state, action, color), color))
    return actions

def nxt_state(state: Board, action: Action, color):
    new_state = Board(state._state)
    #print(new_state.render())
    new_state._turn_color = color
    new_state.apply_action(action)
    return new_state
    
def minimax1(state: Board, turn, depth, color):
    #print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEE\n", state.render(), "DDDDDDDDDDDDDDDDDDDDDDDDDDDDD\n")
    if (depth == 0):
        return (evaluate(state, color), None)
    if (final_state(state) and depth < 2):
        return (evaluate(state, color), None)
        
    
    if (turn == "max"):
        max_value = float("-inf")
        chosed_action = None
        #print(find_actions(state, color))
        for action in find_actions(state, color): #find acitons 出错空空
            #print(find_actions(state, color))
            new_state = Board(state._state)
            if (new_state._turn_color != color):
                new_state._turn_color = color
            new_state.apply_action(action)
            value, _ = minimax(new_state, "min", depth - 1, color)
            if (value > max_value):
                max_value = value
                chosed_action = action
        
        return (max_value, chosed_action)
    
    elif (turn == "min"):
        min_value = float("inf")
        chosed_action = None
 
        for action in find_actions(state, color.opponent):
            new_state = Board(state._state)
            if (new_state._turn_color != color.opponent):
                new_state._turn_color = color.opponent
            new_state.apply_action(action)
            value, _= minimax(new_state, "max", depth - 1, color)
            if (value < min_value):
                min_value = value
                chosed_action = action
        return (min_value, chosed_action)

def minimax(state: Board, turn, depth, color, alpha=float("-inf"), beta=float("inf")):
    #print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEE\n", state.render(), "DDDDDDDDDDDDDDDDDDDDDDDDDDDDD\n")
    if (depth == 0):
        return (evaluate(state, color), None)
    if (final_state(state) and depth < 2):
        return (evaluate(state, color), None)
        
    
    if (turn == "max"):
        max_value = float("-inf")
        chosed_action = None
        #print(find_actions(state, color))
        for action in find_actions(state, color): #find acitons 出错空空
            #print(find_actions(state, color))
            new_state = Board(state._state)
            if (new_state._turn_color != color):
                new_state._turn_color = color
            new_state.apply_action(action)
            value, _ = minimax(new_state, "min", depth - 1, color)
            if (value > max_value):
                max_value = value
                chosed_action = action
            alpha = max(max_value, alpha)
            if (alpha >= beta):
                break
        
        return (max_value, chosed_action)
    
    elif (turn == "min"):
        min_value = float("inf")
        chosed_action = None
 
        for action in find_actions(state, color.opponent):
            new_state = Board(state._state)
            if (new_state._turn_color != color.opponent):
                new_state._turn_color = color.opponent
            new_state.apply_action(action)
            value, _= minimax(new_state, "max", depth - 1, color)
            if (value < min_value):
                min_value = value
                chosed_action = action
            beta = min(beta, min_value)
            if (beta <= alpha):
                break

        return (min_value, chosed_action)


class Agent:
    def __init__(self, color: PlayerColor, **referee: dict):
        """
        Initialise the agent.
        """
        self._color = color
        self._state = Board()
        self._state.render()
        match color:
            case PlayerColor.RED:
                print("Testing: I am playing as red")
            case PlayerColor.BLUE:
                print("Testing: I am playing as blue")

    def action(self, **referee: dict) -> Action:
        """
        Return the next action to take.
        """
        match self._color:
            case PlayerColor.RED:
                t = minimax(self._state, "max", 2, PlayerColor.RED)
                return t[1]
            case PlayerColor.BLUE:
                #print("CCCCCCCCCCCCCCCCCCCCCCCCCCC\n", self._state.render(), "CCCCCCCCCCCCCCCCCCCCCCCCCCC\n")
                #print(self._state._state)
                t = minimax(self._state, "max", 2, PlayerColor.BLUE)
                print(t, t[1])
                return t[1]
            

    def turn(self, color: PlayerColor, action: Action, **referee: dict):
        """
        Update the agent with the last player's action.
        """
        self._state.apply_action(action)
        #print(self._state.render())
        match action:
            case SpawnAction(cell):
                print(f"Testing: {color} SPAWN at {cell}")
                pass
            case SpreadAction(cell, direction):
                print(f"Testing: {color} SPREAD from {cell}, {direction}")
                pass
    

    

