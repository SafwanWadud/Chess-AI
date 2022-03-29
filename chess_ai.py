from math import inf

MAX_DEPTH = 4

num_evals = 0


def get_agent_move(board):
    global num_evals
    num_evals = 0
    print(str(board.fullmove_number) + ". Black move: ", end='', flush=True)
    move = minimax_search(board)
    print(move)
    print("Number of evaluations: "+str(num_evals))
    return move


def minimax_search(board):
    value, move = max_value(board, MAX_DEPTH, -inf, inf)
    return move


def max_value(board, depth, alpha, beta):
    if(board.legal_moves.count() == 0 or depth == 0):
        return evaluation(board), None
    value = -inf
    for move in board.legal_moves:
        board.push(move)
        value2, move2 = min_value(board, depth-1, alpha, beta)
        board.pop()
        if(value2 > alpha):
            alpha = value2
        if(value2 > value):
            value, max_move = value2, move
        if (value >= beta):
            break
    return value, max_move


def min_value(board, depth, alpha, beta):
    if(board.legal_moves.count() == 0 or depth == 0):
        return evaluation(board), None
    value = inf
    for move in board.legal_moves:
        board.push(move)
        value2, move2 = max_value(board, depth-1, alpha, beta)
        board.pop()
        if(value2 < beta):
            beta = value2
        if(value2 < value):
            value, min_move = value2, move
        if (value <= alpha):
            break
    return value, min_move


PIECE_VALUES = {
    #Black (AI)
    'p': 1,      # pawn
    'n': 3,      # knight
    'b': 3,      # bishop
    'r': 5,      # rook
    'q': 9,      # queen
    'k': 1000,   # king
    #White (Player)
    'P': -1,
    'N': -3,
    'B': -3,
    'R': -5,
    'Q': -9,
    'K': -1000,
}

MOBILITY_WEIGHT = 0.1


def evaluation(board):
    global num_evals
    num_evals += 1
    eval = 0
    fen = board.board_fen()
    turn = board.turn
    for char in fen:
        if char in PIECE_VALUES:
            eval += PIECE_VALUES[char]
    eval += MOBILITY_WEIGHT * board.legal_moves.count() * (1 if turn == 'b' else -1)
    return eval
