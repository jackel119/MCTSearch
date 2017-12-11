from datetime import datetime

class MonteCarlo(object):

    def __init__(self, board, seconds=10, max_moves=100, **kwargs):
        self.board = board
        self.calc_time = seconds
        self.max_moves = max_moves
        self.states = []

    def update(self, state):
        self.states.append(state)

    def get_play(self):
        start = datetime.utcnow()
        while datetime.utcnow() - start < self.calc_time:
            self.run_simulation()

    def run_simulation(self):
        states_copy = states[:]
        curr_state = states_copy[-1]

        for t in xrange(1, self.max_moves + 1):
            legal = self.board.legal_plays(states_copy)
            
            play = choice(legal)
            curr_state = self.board.next_state(curr_state, play)
            states_copy.append(curr_state)
