'''
Container for global variables
    This module provides the class Global which provides a container for
    global variables.

        import globalcontainer

        G = globalcontainer.Global()

        # Define our global variables
        G.operation_name = "Check status"
        G.number_of_units = 17

    The __str__ and __repr__ methods are defined so that print(G) will
    list the global variable names and their values to stdout.

    If you instead use the line

        G = globalcontainer.GlobalContainer

    the variables defined will be class variables rather than instance
    variables.  For printing, you can use the Global.str() and
    Global.repr() methods.

    There are two auxiliary classes Variable and Constant that can be
    used if you wish.  Constant is defined so that you can assign to it
    once; later attempts to assign to a Constant attribute will result
    in an exception (the idea is due to A. Martelli, given on page 192
    of the Python Cookbook, 2002 edition).  These two classes let you
    define "blocks" in the Global's set of attributes:

        G.display = Constant()
        G.display.lines = 51        # This variable is readonly
        G.display.columns = 80      # This variable is readonly
        G.display.colors = [red, blue]      # This variable is readonly
        G.keyboard = Variable()
        G.keyboard.keys = 26
        G.keyboard.leds = [1, 2, 3]
        
    The naming of the blocks can help with remembering where things are.

    Note the assignment to G.display.colors is a list, which is a
    mutable object.  The list's contents can be changed, but you won't
    be able to bind a different list to the object without getting an
    exception.  If you want it to be immutable, use e.g. a tuple,
    frozenset, etc.

    Run the module as a script to get examples of use.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Container for global variables
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
class ReadOnlyError(Exception):
    pass
class Descr:
    'Provide str() and repr() methods'
    def __init__(self, indent=" "*2):
        self.__indent__ = indent
    def __str__(self):
        name = type(self).__name__
        s, d = [f"{name}({hex(id(self))}):"], self.__dict__
        for i in sorted(d):
            if not i.startswith("__") and not i.endswith("__"):
                s.append("{}{} = {}".format(self.__indent__, i, repr(d[i])))
        return '\n'.join(s)
    def __repr__(self):
        return self.__str__()
class Variable(Descr):
    def __init__(self, indent=" "*4):
        super().__init__(indent)
class Constant(Descr):
    def __init__(self, indent=" "*4):
        super().__init__(indent)
    def __setattr__(self, name, value):
        if name in self.__dict__:
            msg = f"The constant '{name}' is read-only"
            raise ReadOnlyError(msg)
        self.__dict__[name] = value
    def __delattr__(self, name):
        if name in self.__dict__:
            msg = f"The constant '{name}' is read-only"
            raise ReadOnlyError(msg)
class Global:
    'Container for global variables as instance attributes'
    @staticmethod
    def str():
        s, d = [f"Global class variables:"], Global.__dict__
        for i in sorted(d):
            if i in ("str", "repr"):
                continue
            if not i.startswith("__") and not i.endswith("__"):
                s.append("{}{} = {}".format(" "*2, i, repr(d[i])))
        return '\n'.join(s)
    @staticmethod
    def repr():
        return Global.str()
if __name__ == "__main__": 
    # Standard library modules
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
    # Custom modules
    from lwtest import run, assert_equal, raises, Assert
    from wrap import wrap, dedent
    try:
        from lwtest import run, raises, assert_equal
        _have_lwtest = True
    except ImportError:
        # Get it from
        # https://someonesdad1.github.io/hobbyutil/prog/lwtest.zip
        _have_lwtest = False
    if 1:   # Script base code
        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)
        def Usage(d, status=1):
            name = sys.argv[0]
            s = dedent(f'''
        Usage:  {name}
          Show example of use.  Use --test option to run tests.''')
            print(s)
            exit(status)
        def ParseCommandLine(d):
            d["--test"] = False
            try:
                opts, args = getopt.getopt(sys.argv[1:], "h", "test")
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o in ("-h", "--help"):
                    Usage(d, status=0)
                elif o == "--test":
                    d["--test"] = True
            wrap.indent = " "*4
            return args
    if 1:   # Test code 
        one, two, three, four, five = 1, 2.0, "3", 4+0j, 5
        g = Global()
        g.one = one
        g.two = two
        g.three = three
        g.ro = Constant()
        g.ro.x = four
        g.rw = Variable()
        g.rw.y = five
        def Test_read_write():
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
    if 1:   # Example code 
        def Example_Instance():
            print("Example 1:  Using an Instance")
            s = dedent('''
                g1 = Global()
                g1.rw = Variable()
                g1.rw.a = 33
                g1.rw.b = "a string"
                g1.ro1 = Constant()
                g1.ro1.x = -44.3
                g1.ro1.y = [0.1, "xy"]
                g1.ro2 = Constant()
                g1.ro2.w = 395375
                g1.ro2.z = (-1e17, "blithering")''')
            print("  Code:")
            for line in s.split("\n"):
                print(f"    {line}")
            # Execute the code
            g1 = Global()
            g1.rw = Variable()
            g1.rw.a = 33
            g1.rw.b = "a string"
            g1.ro1 = Constant()
            g1.ro1.x = -44.3
            g1.ro1.y = [0.1, "xy"]
            g1.ro2 = Constant()
            g1.ro2.w = 395375
            g1.ro2.z = (-1e17, "blithering")
            print(g1)
            # We get an exception trying to change a readonly attribute
            s = dedent('''
            with raises(ReadOnlyError):
                g1.ro1.x = 48
                print("Didn't get expected exception")''')
            print("Using the following code to check readonly:")
            for line in s.split("\n"):
                print(f"    {line}")
            msg = "Didn't get expected exception"
            with raises(ReadOnlyError):
                g1.ro1.x = 48
                print(msg)
            print(f"You shouldn't see '{msg}'")
            print("End of Example 1")
            print("-"*70)
        def Example_UsingClassVariables():
            print("Example 2:  Using Class Variables")
            s = dedent('''
                g2 = Global
                g2.rw = Variable()
                g2.rw.a = 33
                g2.rw.b = "a string"
                g2.ro = Constant()
                g2.ro.x = -44.3
                g2.ro.y = [0.1, "xy"]
                print(f"str(g2) doesn't produce a dump (no __str__ method):")
                print(f"  {str(g2)}")
                print(f"Instead, use Global's staticmethod str():")
                print(f"{Global.str()}")
            ''')
            print("  Code:")
            for line in s.split("\n"):
                print(f"    {line}")
            # Execute the code
            g2 = Global
            g2.rw = Variable()
            g2.rw.a = 33
            g2.rw.b = "a string"
            g2.ro = Constant()
            g2.ro.x = -44.3
            g2.ro.y = [0.1, "xy"]
            print(f"str(g2) doesn't produce a dump (no __str__ method):")
            print(f"  {str(g2)}")
            print(f"Instead, use Global's staticmethod str():")
            print(f"{Global.str()}")
            # We get an exception trying to change a readonly attribute
            s = dedent('''
                with raises(ReadOnlyError):
                    g2.ro.x = 48
                    print("Didn't get expected exception")''')
            print("Using the following code to check readonly:")
            for line in s.split("\n"):
                print(f"    {line}")
            msg = "Didn't get expected exception"
            with raises(ReadOnlyError):
                g2.ro.x = 48
                print("Didn't get expected exception")
            print(f"You shouldn't see '{msg}'")
            print("End of Example 2")
    # ----------------------------------------------------------------------
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["--test"]:
        exit(run(globals(), halt=True)[0])
    else:
        Example_Instance()
        Example_UsingClassVariables()
