import chess
from chess_ai import *

board = chess.Board()


def printStart():
    print("\n\nChess AI\n")
    print("White (player) pieces are in upper case")
    print("Black (AI) pieces are in lower case")


def get_player_move(turn):
    while True:
        move = input(str(board.fullmove_number) + ". "+turn + " move: ")
        try:
            san_move = board.parse_san(move)
        except:
            print("\nInvalid move\n")
        else:
            if (san_move not in board.legal_moves):
                print("\nInvalid move\n")
            else:
                return move


def main():

    printStart()
    print("\n" + str(board) + "\n")
    outcome = None
    while outcome == None:
        if(board.turn == chess.WHITE):
            move = get_player_move("White")
            board.push_san(move)
        elif(board.turn == chess.BLACK):
            # move = getMove("Black")
            move = get_agent_move(board)
            board.push(move)
        # print(move)
        # board.push(chess.Move.from_uci(move))
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
