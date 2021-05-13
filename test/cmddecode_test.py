import sys
from lwtest import run, assert_equal, raises
from cmddecode import CommandDecode

from pdb import set_trace as xx
if 1:
    import debug
    debug.SetDebugger()

def TestExceptions():
    commands = set(("a", "Aaa", "Aab", "aaa", "aab"))
    # Case-insensitive instantiation results in an exception ('Aaa' and
    # 'aaa' collide).
    raises(ValueError, CommandDecode, commands, ignore_case=True)
    # commands not a dict/set
    raises(ValueError, CommandDecode, 4)
    # Empty dict/set
    raises(ValueError, CommandDecode, {})
    raises(ValueError, CommandDecode, set())
    # Cannot contain empty string
    raises(ValueError, CommandDecode, set("",))
    # Call's argument must be a string
    cmd = CommandDecode(commands)
    raises(ValueError, cmd, 4)
    # Can't make empty call
    raises(TypeError, cmd)

def Test():
    commands = set(("a", "Aaa", "Aab", "aaa", "aab"))
    cmd = CommandDecode(commands, ignore_case=False)
    assert(set(cmd("a")) == set(["a"]))
    assert(set(cmd("ax")) == set([]))
    assert(set(cmd("aa")) == set(["aaa", "aab"]))
    assert(set(cmd("Aa")) == set(["Aaa", "Aab"]))
    assert(set(cmd("Aab")) == set(["Aab"]))
    # Case insensitive
    commands = set(("A", "AAA", "AAB"))
    cmd = CommandDecode(commands, ignore_case=True)
    assert(set(cmd("a")) == set(["a"]))
    assert(set(cmd("ax")) == set([]))
    assert(set(cmd("AX")) == set([]))
    assert(set(cmd("aa")) == set(["aaa", "aab"]))
    assert(set(cmd("Aa")) == set(["aaa", "aab"]))
    assert(set(cmd("Aab")) == set(["Aab"]))

if __name__ == "__main__":
    exit(run(globals())[0])
