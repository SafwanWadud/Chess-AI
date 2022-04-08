import chess
from chess_ai import *

board = chess.Board()


def printStart():
    print("\n\nChess AI\n")
    print("White (player) pieces are in upper case")
    print("Black (AI) pieces are in lower case")


def printBoard():
    boardStr = str(board).split('\n')  # alphabetic characters for pieces
    # boardStr = str(chess.BaseBoard(board_fen=board.board_fen()).unicode()).split('\n')  # unicode characters for pieces
    print("\n    a b c d e f g h")
    print("  +-----------------+")
    for i in range(len(boardStr)):
        print(str(8-i)+" | "+boardStr[i] + " | " + str(8-i))
    print("  +-----------------+")
    print("    a b c d e f g h\n")


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
    printBoard()
    outcome = None
    while outcome == None:
        if(board.turn == chess.WHITE):
            move = get_player_move()
        elif(board.turn == chess.BLACK):
            move = get_agent_move(board)
        board.push(move)
        printBoard()
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
