from assignment05 import build_suffixtree

def test_suffixtree():
    T = "babacacb$"
    ST, leaves, inner_nodes = build_suffixtree(T)
    assert leaves == [1, 2, 2, 2, 5, 5, 5, 7, 9]
    assert inner_nodes == [0, 0, 0, 0, 2, 2, 2, 4, 5]