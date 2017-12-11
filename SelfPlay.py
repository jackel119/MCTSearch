from datetime import datetime, timedelta
from Board import Board
from MonteCarlo import MonteCarlo

def main():
    begin = datetime.utcnow()
    timelimit = timedelta(seconds=60)
    b = Board()
    mc = MonteCarlo(b, seconds=4)
    player_one_wins = 0
    player_two_wins = 0
    draws = 0
    while (datetime.utcnow() - begin < timelimit):
        winner, _ = self_play(mc, b)
        if winner == 1:
            player_one_wins += 1
        elif winner == -1:
            player_two_wins += 1
        elif winner == 0:
            draws += 1
        else:
            print("Error, unknown winner returned:", winner)
    total_played = player_one_wins + player_two_wins + draws
    print("Total games played:", total_played)
    print("Player one wins:", player_one_wins, " or ", (player_one_wins / total_played) * 100, "%")
    print("Player two wins:", player_two_wins, " or ", (player_two_wins / total_played) * 100, "%")
    print("Draws:", draws, " or ", (draws / total_played) * 100, "%")

def main2():
    b = Board()
    mc = MonteCarlo(b, seconds=20)
    game_state = b.start()
    mc.update(game_state)
    mc.get_play()

def self_play(mc, b):
    game_history = []
    game_state = b.start()
    game_history.append(game_state)
    #print(b.start())
    mc.update(game_state)
    legals = b.legal_plays([game_state])
    winner = b.winner([game_state])
    while legals and winner == 0:
        game_state = b.next_state(game_state, mc.get_play())
        mc.update(game_state)
        game_history.append(game_state)
        legals = b.legal_plays([game_state])
        winner = b.winner([game_state])
   
    return winner, game_history


if __name__ == '__main__':
    b = Board()
    mc = MonteCarlo(b, seconds = 3)
    winner, hist = self_play(mc, b)
    for state in hist:
        print("")
        Board().show(state)
    print("\nWinner: ", winner)
