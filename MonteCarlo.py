from datetime import datetime, timedelta
from random import choice
from Board import Board
from math import log, sqrt

class MonteCarlo(object):

    def __init__(self, board, seconds=10, max_moves=100, c=1.4, **kwargs):
        self.board = board
        self.calc_time = timedelta(seconds=seconds)
        self.max_moves = max_moves
        self.states = []
        self.wins = {}
        self.plays = {}
        self.C = c

    def update(self, state):
        self.states.append(state)

    def get_play(self):
        self.max_depth = 0
        state = self.states[-1]
        player = self.board.current_player(state)
        legal = self.board.legal_plays(self.states[:])

        if not legal:
            for i in [1,-1]:
                for i, curr_state in visited_states:
                    if (player, curr_state) not in self.plays:
                        continue
                    self.plays[player,curr_state] +=2
                    if player == winner:
                        self.wins[(player, curr_state)] += 1
            return
        if len(legal) == 1:
            return legal[0]

        start = datetime.utcnow()
        games = 0
        while (datetime.utcnow() - start) < self.calc_time:
            print(datetime.utcnow() - start, "||| ", self.calc_time)
            self.run_simulation()
            games += 1
        
        moves_states = [(p, self.board.next_state(state, p)) for p in legal]
        
        print("Games played:", games, "\nTime Elapsed: ", datetime.utcnow() - start)
        percent_wins, move = max(
            (self.wins.get((player, S), 0) /
             self.plays.get((player, S), 1),
             p)
            for p, S in moves_states
        )

        # Display the stats for each possible play.
        for x in sorted(
            ((100 * self.wins.get((player, S), 0) /
              self.plays.get((player, S), 1),
              self.wins.get((player, S), 0),
              self.plays.get((player, S), 0), p)
             for p, S in moves_states),
            reverse=True
        ):
            print("{3}: {0:.2f}% ({1} / {2})".format(*x))

        print("Maximum depth searched:", self.max_depth)

        return move


    def run_simulation(self):
        states_copy = self.states[:]
        curr_state = states_copy[-1]
        visited_states = set()
        player = self.board.current_player(curr_state)
        plays, wins = self.plays, self.wins

        expand = True

        draw = False

        for t in range(1, self.max_moves + 1):
            legal = self.board.legal_plays(states_copy)
            
            if not legal:
                print(curr_state)
                draw = True
                break

            moves_states = [(p, self.board.next_state(curr_state, p)) for p in legal]
            if all(plays.get((player, S)) for p, S in moves_states):
                # If we have stats on all of the legal moves here, use them.
                log_total = log(
                    sum(plays[(player, S)] for p, S in moves_states))
                value, play, curr_state = max(
                    ((wins[(player, S)] / plays[(player, S)]) +
                     self.C * sqrt(log_total / plays[(player, S)]), p, S)
                    for p, S in moves_states
                )
            else:
                # Otherwise, just make an arbitrary decision.
                play, curr_state = choice(moves_states)

            #print(curr_state)
            states_copy.append(curr_state)
            
            if expand and (player, curr_state) not in self.plays:
                expand = False
                self.plays[(player,curr_state)] = 0
                self.wins[(player, curr_state)] = 0
                if t > self.max_depth:
                    self.max_depth = t

            visited_states.add((player,curr_state))
            player = self.board.current_player(curr_state)
            winner = self.board.winner(states_copy)
            if winner != 0:
                break
        
        if not draw:
            for player, curr_state in visited_states:
                if (player, curr_state) not in self.plays:
                    continue
                self.plays[player,curr_state] +=1
                if player == winner:
                    self.wins[(player, curr_state)] += 1
        else:
            for i in [1,-1]:
                for i, curr_state in visited_states:
                    if (player, curr_state) not in self.plays:
                        continue
                    self.plays[player,curr_state] +=2
                    if player == winner:
                        self.wins[(player, curr_state)] += 1


# b = Board()
# m = MonteCarlo(b)
# m.update((
#     (1,0,0),
#     (0,0,0),
#     (0,0,0)
#     ))
# print(m.get_play())
