from math import inf

MAX_DEPTH = 4

num_evals = 0
explored_nodes = 0
transpo_lookups = 0

transpo_table = {}


def printStats():
    print("\nStats:")
    print("nodes explored: "+str(explored_nodes))
    print("states evaluated: " + str(num_evals))
    print("transposition table lookups: " + str(transpo_lookups))


def get_agent_move(board):
    global num_evals, transpo_lookups, explored_nodes, transpo_table
    num_evals = 0
    transpo_lookups = 0
    explored_nodes = 0
    transpo_table = {}
    print(str(board.fullmove_number) + ". Black move: ", end='', flush=True)
    move = minimax_search(board)
    print(move)
    printStats()
    return move


def minimax_search(board):
    best_move = None
    best_value = -inf
    alpha = -inf
    beta = inf
    for move in board.legal_moves:
        board.push(move)
        value = min_value(board, MAX_DEPTH - 1, alpha, beta)
        board.pop()
        if(value > best_value):
            best_value, best_move = value, move
            alpha = max(alpha, best_value)
    return best_move


def max_value(board, depth, alpha, beta):
    global transpo_lookups, explored_nodes
    explored_nodes += 1

    if(board.legal_moves.count() == 0 or depth == 0):
        return evaluation(board)

    if board.board_fen() in transpo_table:
        transpo_lookups += 1
        return transpo_table[board.board_fen()]

    value = -inf
    for move in board.legal_moves:
        board.push(move)
        value2 = min_value(board, depth-1, alpha, beta)
        board.pop()
        if(value2 > value):
            value, max_move = value2, move
            alpha = max(alpha, value)
        if (value >= beta):
            return value
    transpo_table[board.board_fen()] = value
    return value


def min_value(board, depth, alpha, beta):
    global transpo_lookups, explored_nodes
    explored_nodes += 1

    if(board.legal_moves.count() == 0 or depth == 0):
        return evaluation(board)

    if board.board_fen() in transpo_table:
        transpo_lookups += 1
        return transpo_table[board.board_fen()]

    value = inf
    for move in board.legal_moves:
        board.push(move)
        value2 = max_value(board, depth-1, alpha, beta)
        board.pop()
        if(value2 < value):
            value, min_move = value2, move
            beta = min(beta, value)
        if (value <= alpha):
            return value
    transpo_table[board.board_fen()] = value
    return value


PIECE_VALUES = {
    # Black (AI)
    'p': 1,      # pawn
    'n': 3,      # knight
    'b': 3,      # bishop
    'r': 5,      # rook
    'q': 9,      # queen
    'k': 1000,   # king
    # White (Player)
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
    is_white_turn = board.turn
    for char in fen:
        if char in PIECE_VALUES:
            eval += PIECE_VALUES[char]
    eval += MOBILITY_WEIGHT * board.legal_moves.count() * (-1 if is_white_turn else 1)
    return eval
