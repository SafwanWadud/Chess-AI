# import chess
# board = chess.Board()
from math import inf

MAX_DEPTH = 3


def get_agent_move(board):
    # def get_agent_move():
    print("Agent choosing move...")
    return minimax_search(board)


def minimax_search(board):
    value, move = max_value(board, MAX_DEPTH)
    return move


def max_value(board, depth):
    if(board.legal_moves.count() == 0 or depth == 0):
        return evaluation(board), None
    value = -inf
    for move in board.legal_moves:
        board.push(move)
        value2, move2 = min_value(board, depth-1)
        board.pop()
        if (value2 > value):
            value, max_move = value2, move
    return value, max_move


def min_value(board, depth):
    if(board.legal_moves.count() == 0 or depth == 0):
        return evaluation(board), None
    value = inf
    for move in board.legal_moves:
        board.push(move)
        value2, move2 = min_value(board, depth-1)
        board.pop()
        if (value2 < value):
            value, min_move = value2, move
    return value, min_move


def evaluation(board):
    return 1
