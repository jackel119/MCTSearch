import numpy as np

class Board(object):
    def __init__(self):
        pass

    def start(self):
        self.current_state = ((0,0,0), (0,0,0), (0,0,0))
        return self.current_state

    def current_player(self, state):
        # Takes the game state and returns the current player's
        # number.
        curr_state = list(map(list, state))
        count = sum(map(sum, state))
        if count == 0:
            return 1
        elif count == 1:
            return -1

    def next_state(self, state, play):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        position, piece = play
        state = list(map(list, state))
        ret = state[:]
        if self.current_player(state) == piece:
           ret[(position - 1) // 3][(position - 1) % 3] = piece
           return tuple(map(tuple,ret))
        else:
            print(ret)
            print(play)

    def legal_plays(self, state_history):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        curr_state = state_history[-1]
        curr_state = list(map(list, curr_state))
        curr_player = self.current_player(curr_state)
        legal_plays = []
        for p in range(1,10):
            if curr_state[(p-1) // 3][(p-1) % 3] == 0:
                legal_plays.append((p, curr_player))
        return legal_plays



    def winner(self, state_history):
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        curr_state = state_history[-1]
        curr_state = list(map(list, curr_state))
        curr_state_t = np.transpose(curr_state)
        for i in range(0,3):
            if sum(curr_state[i]) == 3:
                return 1
            elif sum(curr_state[i]) == -3:
                return -1
            elif sum(curr_state_t[i]) == 3:
                return 1
            elif sum(curr_state_t[i]) == -3:
                return -1
        if (curr_state[0][0] + curr_state[1][1] + curr_state[2][2]) == 3:
            return 1
        elif (curr_state[0][0] + curr_state[1][1] + curr_state[2][2]) == -3:
            return -1
        elif (curr_state[0][2] + curr_state[1][1] + curr_state[2][0]) == -3:
            return -1 
        elif (curr_state[0][2] + curr_state[1][1] + curr_state[2][0]) == 3:
            return 1
        else:
            for i in range(0,9):
                if curr_state[i // 3][i % 3] == 0:
                    return 0
            return None

    def show(self, state):
        for i in state:
            print(i)

# b = Board()
# state = ((1,1,-1),
#          (1,1,0),
#          (0,0,1))
# b.show(state)
# sh = [state]
# print(b.winner(sh))
