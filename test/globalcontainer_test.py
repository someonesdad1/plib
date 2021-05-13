from globalcontainer import Global, Variable, Constant, ReadOnlyError
from lwtest import run, assert_equal, raises

one, two, three, four, five = 1, 2.0, "3", 4+0j, 5
g = Global()
g.one = one
g.two = two
g.three = three
g.ro = Constant()
g.ro.x = four
g.rw = Variable()
g.rw.y = five

def Test():
    'This exercises the simple globals that are read/write'
    assert(isinstance(g.one, int))
    assert(isinstance(g.two, float))
    assert(isinstance(g.three, str))
    assert_equal(g.one, one)
    assert_equal(g.two, two)
    assert_equal(g.three, three)
def Test_more():
    'Tests using Constant and Variable classes'
    # Read only feature
    assert(isinstance(g.ro.x, complex))
    assert(g.ro.x == four)
    with raises(ReadOnlyError):
        g.ro.x = 1
    # Variable is read/write
    assert(isinstance(g.rw.y, int))
    assert(g.rw.y == five)
    g.rw.y = five + 1
    assert(g.rw.y == five + 1)

if __name__ == "__main__":
    exit(run(globals())[0])
