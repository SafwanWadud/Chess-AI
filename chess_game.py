import chess
from chess_ai import *

board = chess.Board()


def printStart():
    print("\n\nChess AI\n")
    print("White (player) pieces are in upper case")
    print("Black (AI) pieces are in lower case")


def get_player_move():
    while True:
        uci_move = input(str(board.fullmove_number) + ". White move: ")
        try:
            move = chess.Move.from_uci(uci_move)
        except:
            print("\nInvalid move\n")
        else:
            if (move not in board.legal_moves):
                print("\nInvalid move\n")
            else:
                return move


def main():
    printStart()
    print("\n" + str(board) + "\n")
    outcome = None
    while outcome == None:
        if(board.turn == chess.WHITE):
            move = get_player_move()
        elif(board.turn == chess.BLACK):
            move = get_agent_move(board)
        board.push(move)
        print("\n" + str(board) + "\n")
        outcome = board.outcome()

    # fix
    result = "Tie game"
    if outcome.winner == chess.WHITE:
        result = "White wins"
    elif outcome.winner == chess.BLACK:
        result = "Black wins"
    print("Game Over:", result, "\n")


if __name__ == "__main__":
    main()
