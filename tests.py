
def test_score():
    assert -1 == score(mk_board(xs='23', os='147', turn='o'))
    assert 0 == score(mk_board())
    assert -100 == score(mk_board(xs='23', os='14', turn='x'))


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
