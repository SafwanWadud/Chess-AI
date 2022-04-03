from math import inf


MAX_DEPTH = 4
MOBILITY_WEIGHT = 0.1
EXACT = 0
UPPER = 1
LOWER = 2
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


num_evals = 0
explored_nodes = 0
transpo_lookups = 0
# key = board part of fen string; value = tuple (state value, depth at which value was computed, type of value (EXACT, UPPER, or LOWER))
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
        entry = transpo_table[board.board_fen()]
        if (entry[1] >= depth):
            if(entry[2] == EXACT):
                transpo_lookups += 1
                return entry[0]
            elif(entry[2] == UPPER):
                beta = min(beta, entry[0])
            elif(entry[2] == LOWER):
                alpha = max(alpha, entry[0])
            if (alpha >= beta):
                transpo_lookups += 1
                return entry[0]

    value = -inf
    for move in board.legal_moves:
        board.push(move)
        value2 = min_value(board, depth-1, alpha, beta)
        board.pop()
        if(value2 > value):
            value, max_move = value2, move
            alpha = max(alpha, value)
        if (value >= beta):
            # value is lower bounded by beta
            transpo_table[board.board_fen()] = (value, depth, LOWER)
            return value
    # found exact value
    transpo_table[board.board_fen()] = (value, depth, EXACT)
    return value


def min_value(board, depth, alpha, beta):
    global transpo_lookups, explored_nodes
    explored_nodes += 1

    if(board.legal_moves.count() == 0 or depth == 0):
        return evaluation(board)

    if board.board_fen() in transpo_table:
        entry = transpo_table[board.board_fen()]
        if (entry[1] >= depth):
            transpo_lookups += 1
            if(entry[2] == EXACT):
                return entry[0]
            elif(entry[2] == UPPER):
                beta = min(beta, entry[0])
            elif(entry[2] == LOWER):
                alpha = max(alpha, entry[0])
            if (alpha >= beta):
                return entry[0]

    value = inf
    for move in board.legal_moves:
        board.push(move)
        value2 = max_value(board, depth-1, alpha, beta)
        board.pop()
        if(value2 < value):
            value, min_move = value2, move
            beta = min(beta, value)
        if (value <= alpha):
            # value is upper bounded by alpha
            transpo_table[board.board_fen()] = (value, depth, UPPER)
            return value
    # found exact value
    transpo_table[board.board_fen()] = (value, depth, EXACT)
    return value


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
