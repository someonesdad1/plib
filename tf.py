'''
Text formatter:  format text for a script's printing to stdout
 
    The main use case is to be able to get formatted output for the help
    strings used in scripts.
 
    A line containing a formatter command begins with a "." after
    stripping off whitespace.  If you want a line to begin with a
    period, escape it with a backslash.
 
    { and }
        Begin and end a code block.

    fmt bool
        If off, the output is output verbatim.  Otherwise, each line
        is formatted per the current state.

    out bool
        Turn output on/off.  If it is off, no lines are output until
        the next '.out True' is seen.  This is a handy way to
        comment out a chunk of text.

    push
        Save the current state.  Note vars is part of the state, so
        a subsequent '.clear' will be "forgotten" when you .pop an
        older state.  A shallow copy of vars is made for the new
        state.

    pop
        Restore the previously pushed state.  Exception if stack is
        empty.

    lm int
        int >= 1.  Set left margin.  Set to 1 to have text start at
        column 1.

    width int
        int >= 0.  0 means wrap to width from COLUMNS; if no COLUMNS
        variable, then it's set to 80.

    hang int [str]
        Make first line a hanging indent.  Negative means outdented to
        left and positive is indented to right.  If str is given, a
        newline is substituted for it.

    bullet str1 [int [str2]]
        Use str1 as a bullet string and indent the block of text
        int to the right of the left margin.  If str2 is present, it's
        used the same as the str in the hanging indent command to
        provide line breaks.
        
    wrap bool
        Wrap paragraphs to current margins.  If off, then existing
        newlines are respected.

    <
        Left justification:  text aligned at left margin.
    >
        Right justification:  text aligned at right margin.
    ^
        Center the lines:  text centered at (lm + width//2) and wrapped
        if necessary.
    |
        Block justification:  use both left and right justification by
        inserting enough blanks between the words.

    #
        This line is a comment and won't make it to the output.
    
    del str
        Delete the variable named str from vars.

    clear
        Clears the vars dictionary.  If you .pop, the old vars
        dictionary will be restored.

    ----------------------------------------------------------------------
    State variables

        Left margin         integer >= 0
        Right margin        integer >= 0
        Width               integer >= 0
        Hanging             integer or None
        Bullet              str or None
        Bullet_hang         integer >= 0
        Justification       {left, right, center, block}
        wrap                bool

    
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
    # <programming> Provides a basic text formatting language for use in 
    # formatting text for python script output to a terminal.
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    from collections import deque
    import contextlib
    from enum import Enum, auto
    import io
    import os
    import pathlib
    import re
    import sys
    from pdb import set_trace as xx 
    from pprint import pprint as pp
if 1:   # Custom imports
    from wrap import dedent
    from color import C
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    class G: pass
    G.nl = "\n"
    G.code = C.cyn
    G.source = C.yel
    G.stdout = C.lyel
    G.stderr = C.lred
    G.norm = C.norm
    G.trigger = "."
class IdentifyCmd:
    def __init__(self):
        self.no_args = set("{ } push pop clear # < > ^ |".split())
        self.args = set('''fmt out lm width hang bullet wrap del'''.split())
        self.all = self.no_args | self.args
    def identify(self, line, vars):
        '''Return None if not a command; otherwise return list of 
        [cmd, arg1, ...].  vars is a dictionary of variables.
        '''
        self.vars = vars
        s = line.strip()
        if not s.startswith(G.trigger):
            return None
        f = s[len(G.trigger):].split()
        candidate = f[0]
        if candidate not in self.all:
            return None
        if candidate in self.no_args:
            if candidate == "#":
                cmd, args = candidate, [s[2:]]
            else:
                cmd, args = candidate, []
        else:
            cmd, args = candidate, f[1:]
        if cmd in self.args:
            self.check_syntax(cmd, args, s)
        return cmd, args
    def is_int_or_var(self, candidate):
        '''Return True if the candidate string can be converted to an
        integer, bool or is in self.vars.
        '''
        if candidate in self.vars:
            return True
        try:
            int(candidate)
            return True
        except Exception:
            try:
                bool(candidate)
                return True
            except Exception:
                return False
        else:
            return False
    def check_syntax(self, cmd, args, line):
        e = SyntaxError(f"'{line}' is incorrect syntax")
        if not args:
            raise SyntaxError(f"'{line}' is missing an argument")
        # First argument must be a bool, int, or variable
        if cmd in "fmt out lm width hang wrap".split():
            if not self.is_int_or_var(args[0]):
                raise e
        if cmd == "del":
            if args[0] not in self.vars:
                raise SyntaxError(f"'{line}' needs the name of a variable")
        elif cmd == "bullet":
            if len(args) not in (1, 2, 3):
                raise e
            if len(args) > 1:
                if not self.is_int_or_var(args[1]):
                    m = f"'{line}':  second argument needs to be int or variable"
                    raise SyntaxError(m)
class state(Enum):
    init = auto()
    normal = auto()
    code = auto()
class justification(Enum):
    left = auto()
    right = auto()
    center = auto()
    block = auto()
class TF:
    def __init__(self, s):
        lines = dedent(s).splitlines()
        self.debug = False
        self.lines = deque([(i, line) for i, line in enumerate(lines)])
        self.stack = deque()
        self.state = state.init
        self.idcmd = IdentifyCmd()
        self.state = {
            "left_margin": 0,
            "width": 0,
            "format": True,
            "out": True,
            "justification": "left",
            "empty": 0,
            "wrap": False,
        }
        self.vars = {}
        if 0:
            self.dump()
    def dump(self):
        for i, l in self.lines:
            print(f"[{i:3d}] {l}")
    def execute(self, lines_of_code):
        'Execute the lines of code from a code block'
        lines = dedent('\n'.join(lines_of_code))
        if self.debug:  # If debug on, print code in color
            print(f"{G.code}", end="", file=self.stream)
            for line in lines.splitlines():
                print(line, file=self.stream)
            print(f"{G.norm}", end="", file=self.stream)
        stdout, stderr = io.StringIO(), io.StringIO()
        co = compile(lines, "<src>", "exec")
        with contextlib.redirect_stdout(stdout):
            with contextlib.redirect_stderr(stderr):
                exec(co, globals(), self.vars)
        if self.debug:
            print(f"{G.stdout}{stdout.getvalue()}{G.norm}", end="", file=self.stream)
        else:
            print(f"{stdout.getvalue()}", end="", file=self.stream)
        err = stderr.getvalue()
        if err:     # Always print stderr in color
            print(f"{G.stderr}{err}{G.norm}", end="", file=sys.stderr)
    def process(self):
        'Return the processed lines'
        self.state = state.normal
        self.stream = io.StringIO()
        for i, line in self.lines:
            if self.state == state.code:
                cmd, args = None, []
                if line == f"{G.trigger}}}":
                    cmd = "}"
            else:
                c = self.idcmd.identify(line, self.vars)
                cmd = c[0]
                args = c[1:] if len(c) > 1 else []
            if cmd is None:
                if self.state == state.code:
                    codeblock.append(line)
                else:
                    print(line, file=self.stream)
            else:
                if cmd == "{":
                    self.state = state.code
                    codeblock = []
                elif cmd == "}":
                    self.state = state.normal
                    self.execute(codeblock)
                else:
                    pass
                    #xx()
        if self.state == state.code:
            m = f"Missing end of a code block '{G.trigger}}}'"
            raise SyntaxError(m)
        return self.stream.getvalue()

if 0:
    test = '''
        .{
            x = 1
        .}
    '''
    t = TF(test)
    t.process()
    exit()

if 0:
    c = IdentifyCmd()
    for i in test.split("\n"):
        t = c.identify(i)
        if t is not None:
            print(f"{i:20s}    command = {t}")
    exit()

if __name__ == "__main__": 
    # Run the selftests
    from lwtest import run, raises, assert_equal, Assert
    import sys
    from pdb import set_trace as xx
    def Test_cmd_syntax():
        '''These are all valid commands, so there should be no syntax
        error.
        '''
        test = '''
            .{
                x = 1
            .}
            .# Check reasonable bool values
            .fmt 0
            .fmt 1
            .fmt 2
            .fmt -1
            .fmt x
            .fmt True
            .fmt False
            .# Other commands
            .out 0
            .out 1
            .push
            .pop
            .lm 0
            .lm 1
            .lm 100
            .width 0
            .width 1
            .width 100
            .# hang
            .hang 0
            .hang 1
            .hang 2
            .hang -1
            .hang 0 *
            .hang 1 *
            .hang 2 *
            .hang -1 *
            .# bullet
            .bullet *
            .bullet * 0
            .bullet * 1
            .bullet * 2
            .bullet * 0 |
            .bullet * 1 |
            .bullet * 2 |
            .# Other stuff
            .>
            .<
            .^
            .|
            .clear
            .del x
        '''
        t = TF(test)
        t.process()
        # This should result in a syntax error because vars doesn't
        # contain 'x'.
        with raises(SyntaxError):
            t = TF(".del x")
            t.process()
        # This should result in a syntax error because of a missing end
        # of a code block.
        t = TF('''
            .{
                x = 3
        ''')
        raises(SyntaxError, t.process)
        #with raises(SyntaxError):
        #    t.process()
    if "--test" in sys.argv:
        exit(run(globals(), halt=1)[0])
    #xx
    exit(run(globals(), halt=1)[0]) #xx
if __name__ == "__main__": 
    # Run the demos
    def Example1():
        pass
    run(globals(), regexp=r"^Example\d\d?", quiet=True)
