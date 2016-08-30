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


def gen_next_states(board):
    os, xs, _ = board
    return (new_move(board, i) for i in '123456789' if i not in (os | xs))


def is_terminal(board):
    os, xs, _ = board
    return (set('123456789') == (os | xs)) or winner(os) or winner(xs)


def score(board, depth=0):
    os, xs, current = board
    if winner(os):
        return -1, depth
    if winner(xs):
        return 1, depth
    if is_terminal(board):
        return 0, depth
    best = min if current == 'x' else max
    return best(score(b, -1*(abs(depth)+1)) for b in gen_next_states(board))


def next_move(board):
    _, _, current = board
    best = min if current == 'x' else max
    moves = gen_next_states(board)
    return best(moves, key=score)


def print_b(board, file=sys.stdout):
    os, xs, who = board

    def val_at(i):
        if i in os: return ' O'
        if i in xs: return ' X'
        return '  '
    turn = 'x' if who == 'o' else 'o'
    print("it is {turn}'s turn".format(turn=turn.upper()), file=file)
    print('', file=file)
    for row, cols in enumerate(['123', '456', '789']):
        if row in (1, 2):
            print('---------', file=file)
        line = '|'.join([val_at(i) for i in cols])
        print(line, end=' \n', file=file)


def game(start=True):
    if not start:
        pos = yield mk_board()
        current_state = mk_board(xs=str(pos))
    else:
        current_state = mk_board(xs=random.choice('123456789'))

    while not is_terminal(current_state):
        state = next_move(current_state)
        next_pos = yield state
        current_state = new_move(state, next_pos)


def play_game():
    y_n = raw_input('X starts first do you want to start ? [y,n]')
    if y_n in ['y', 'Y']:
        play = game(state, start=False)
    else:
        play = game()
    b = next(play)
    print_b(b)
    while True:
        pos = raw_input('select position for your move')
        board = play.send(pos)
        print_b(board)


def test_score():
    assert -100 == score(mk_board(xs='23', os='14', turn='x'))
    assert 3 == score(mk_board(xs='23', os='14', turn='o'))
    assert 0 == score(mk_board())


def test_gen_plays():
    next_states = set(gen_plays(mk_board(turn='x')))
    assert all(s.turn == 'o' for s in next_states)
    assert next_states == {mk_board(os=p, turn='o') for p in '123456789'}


def run_tests():
    tests = [(name, func) for name, func in globals().items()
             if name.startswith('test_')]
    passed = failed = 0
    while tests:
        name, func = tests.pop()
        try:
            res = func()
        except Exception as e:
            failed += 1
            print (name, '...', repr(E))
        else:
            passed += 1
            print (name, '...', 'passed')
    print('ran {count} test(s) with {failed} failures'.format(count=(passed+failed), failed=failed))

