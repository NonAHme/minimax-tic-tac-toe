import math
import sys
import random
from collections import namedtuple

Board = namedtuple('Board', 'os xs who')

WINNING_LINES = {frozenset(s) for s in ['123', '456', '789', '147', '258',
                                        '369', '159', '357']}


def mk_board(os='', xs='', who='x'):
    "return a board with os contaiing position o and xs postions of x"
    return Board(os=frozenset(os), xs=frozenset(xs), who=who)


def new_move(board, pos):
    pos = str(pos)
    os, xs, _ = board
    who = 'x' if board.who == 'o' else 'o'
    if who == 'x':
        return mk_board(os, (xs | set(pos)), who=who)
    else:
        return mk_board((os | set(pos)), xs=xs, who=who)


def winner(pos):
    return any(win.issubset(pos) for win in WINNING_LINES)


def moves(board):
    "Board -> [Board] all valid moves"
    os, xs, _ = board
    return (new_move(board, i) for i in '123456789' if i not in (os | xs))


def is_terminal(board):
    os, xs, _ = board
    return (set('123456789') == (os | xs)) or winner(os) or winner(xs)


def score(board, alpha=-math.inf, beta=math.inf):
    os, xs, current = board
    if winner(os):
        return -1
    if winner(xs):
        return 1
    if is_terminal(board):
        return 0

    def best_choice(rank, state):
        alpha, beta, best = rank
        if alpha >= beta:
            return rank
        current_score = score(state, alpha, beta)
        if state.turn == 'o':
            best = max(best, current_score)
            alpha = max(best, alpha)
        else:
            best = min(best, current_score)
            beta = min(best, beta)
        return alpha, beta, best

    #_, _, best = reduce(best_choice, moves(board))

    if current == 'o':
        best = -math.inf
        for m in moves(board):
            best = max(best, score(m, alpha, beta))
            alpha = max(best, alpha)
            if alpha >= beta:
                break
        return best
    else:
        best = math.inf
        for m in moves(board):
            best = min(best, score(m, alpha, beta))
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best


def next_move(board):
    _, _, current = board
    best = min if current == 'x' else max
    next_states = moves(board)
    return best(next_states, key=score)


def print_b(board, file=sys.stdout):
    os, xs, who = board
    
    def val_at(i):
        if i in os: return ' O'
        if i in xs: return ' X'
        return '  '
    turn = 'X'.upper() if who == 'o' else 'O'
    description = "game over !" if is_terminal(board) else "it is {turn}'s turn".format(turn=turn)
    print(description, file=file)
    print('', file=file)
    for row, cols in enumerate(['123', '456', '789']):
        if row in (1, 2):
            print('---------', file=file)
        line = '|'.join([val_at(i) for i in cols])
        print(line, end=' \n', file=file)


def game(start=True, state=None):
    current_state = state or mk_board(who='o')
    while not is_terminal(current_state):
        ai_move = next_move(current_state)
        next_pos = yield ai_move
        current_state = new_move(ai_move, next_pos)
        yield current_state


def play_game(file=sys.stdout):
    y_n = input('X starts first do you want to start ? [y,n]')
    if y_n in ['y', 'Y']:
        print_b(mk_board(who='o'), file=file)
        pos = input('select position for your move \n')
        plays = game(start=False, state=mk_board(xs=str(pos)))
    else:
        plays = game()
    for board in plays:
        print_b(board, file=file)
        if is_terminal(board):
            break
        pos = input('select position for your move \n')
        board = plays.send(pos)
        print_b(board, file=file)
    print("game over ", file=file)
