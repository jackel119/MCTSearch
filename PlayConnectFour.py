from ConnectFour import Board
from MonteCarlo import MonteCarlo

def main():
    print("Would you like to go 1st or 2nd?\n    Go 1st: 1\n    Go 2nd: 2")
    if int(input()) == 2:
        players = {2 : "Human", 1: 'AI'}
    else:
        players = {1 : "Human", 2 : 'AI'}
    board = Board()
    mc = MonteCarlo(board, seconds = 3)
    game_history = []
    game_state = board.start()
    game_history.append(game_state)
    mc.update(game_state)
    legals = board.legal_plays(game_history)
    winner = board.winner(game_history)
    print(board)
    while legals and winner == 0:
        current_player = board.current_player(game_state)
        #print(current_player)
        if players[current_player] == 'Human':
            print("Please enter the square you'd like to play: ") 
            print(board.legal_plays(game_history))
            pos = int(input())
            game_state = board.next_state(game_state, pos)
        elif players[board.current_player(game_state)] == 'AI':
            print("AI is thinking....")
            game_state = board.next_state(game_state, mc.get_play())
        mc.update(game_state)
        game_history.append(game_state)
        legals = board.legal_plays([game_state])
        winner = board.winner([game_state])
        print(board)

    print("The game is over!\n Plauer: ", winner, "has won")

if __name__ == '__main__':
    main()
