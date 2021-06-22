'''
TODO

    * Create classes:  wrapper, bulletter, numberer.  These can handle
      the various formatting tasks.  They all derive from a base class
      that has the methods input() and output().  You call input() an
      arbitrary number of times, then call output() to get the final
      formatted string to print.

        class Formatter:
            def input(self, s): raise SyntaxError("Abstract")
            def output(self): raise SyntaxError("Abstract")

    * I've investigated trying to build tools that process a line at a
      time, but this doesn't appear to be easy to implement,
      particularly for situations with wrapping like bullets or wrapped
      paragrams.  

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
 
    bullet str1 [str2]
        Use str1 as a bullet string; it is placed at the left margin.
        If str2 is present, it's used the same as the str in the hanging
        indent command to provide line breaks.

        Thus, ".bullet * ∞" in the following:

            It is a truth universally acknowledged, that a single man in
            possession of a good fortune, must be in want of a wife.∞ It
            was then disclosed in the following manner.  Observing his
            second daughter employed in trimming a hat, he suddenly
            addressed her with, "I hope Mr. Bingley will like it,
            Lizzy."

        results in

            * It is a truth universally acknowledged, that a single man
              in possession of a good fortune, must be in want of a
              wife.

              It was then disclosed in the following manner.  Observing
              his second daughter employed in trimming a hat, he
              suddenly addressed her with, "I hope Mr. Bingley will like
              it, Lizzy."
        
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
    from wrap import dedent, Wrap as WrapModule
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
        '''Return None if not a command; otherwise return tuple of 
        (cmd, arg1, ...).  vars is a dictionary of variables.
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
                cmd, args = candidate, tuple([s[2:]])
            else:
                cmd, args = candidate, tuple()
        else:
            cmd, args = candidate, tuple(f[1:])
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
                raise ValueError(f"'{args[0]}' not in vars dictionary")
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
    hang = auto()
    bullet = auto()
class TF:
    'Text formatter'
    def __init__(self, s):
        's is the string it initialize with'
        lines = dedent(s).splitlines()
        self.debug = False
        self.lines = deque([(i, line) for i, line in enumerate(lines)])
        self.stack = deque()
        self.cmdstate = state.init
        self.idcmd = IdentifyCmd()
        self.state = {
            "left_margin": 0,       # 0 or 1 means column 1
            "width": 0,             # Right margin is lm + width
            "format": True,         # If True, format line; if false,
                                    # pass through unchanged.
            "out": True,            # If True, output enabled
            # hang:  If negative, the body starts at the left margin and
            # the first line is to the right of the body.  If positive,
            # the first line is at the left margin and the body is to
            # the right.
            "hang": 0,
            "hang_nl": None,        # String to substitute a newline
            "bullet_str": 0,        # Used for bullet 'character'
            "bullet_nl": None,      # String to substitute a newline
            "wrap": False,
            "just": just.left,
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
    def bool(self, s):
        x = s.strip()
        if x in self.vars:
            return bool(self.vars[x])
        elif x in "on True".split():
            return True
        elif x in "off False".split():
            return False
        try:
            return(bool(int(x)))
        except Exception:
            return(bool(float(x)))
        else:
            try:
                return(bool(float(x)))
            except Exception:
                raise ValueError(f"Could not convert '{x}' to bool")
    def process_line(self, line, ln):
        print(line, file=self.stream)
    def process_cmd_line(self, cmd, args, line, ln):
        if cmd == "#":
            return
        elif cmd in "fmt out".split():
            self.state[cmd] = self.bool(args[0])
            self.cmdstate = state.normal
            return
        elif cmd == "wrap":
            self.state[cmd] = self.bool(args[0])
            self.cmdstate = state.wrap
            return
        elif cmd == "push":
            self.stack.append(self.state)
            return
        elif cmd == "pop":
            if not self.stack:
                raise ValueError("stack is empty")
            self.state = self.stack.pop()
            return
        elif cmd in "lm width".split():
            self.state[cmd] = int(args[0])
            return
        elif cmd == "hang":
            while len(args) < 2:
                args.append(None)
            self.state["hang"] = int(args[0])
            self.state["hang_str"] = args[1]
            self.cmdstate = state.hang
            return 
        elif cmd == "bullet":
            while len(args) < 2:
                args.append(None)
            self.state["bullet_str"] = args[0] if args[0] is not None else "*"
            self.state["bullet_nl"] = args[1]
            self.cmdstate = state.bullet
            return 
        elif cmd == ">":
            self.state["just"] = just.right
            self.cmdstate = state.normal
            return
        elif cmd == "<":
            self.state["just"] = just.left
            self.cmdstate = state.normal
            return
        elif cmd == "^":
            self.state["just"] = just.center
            self.cmdstate = state.normal
            return
        elif cmd == "|":
            self.state["just"] = just.block
            self.cmdstate = state.normal
            return
        elif cmd == "clear":
            self.vars.clear()
            return
        elif cmd == "del":
            if args[0] not in self.vars:
                raise KeyError(f"'{args[0]}' not in vars dictionary")
            del self.vars[args[0]]
            return
        else:
            raise SyntaxError(f"'{cmd}' is an unrecognized command")
        if self.debug:
            print(f"{C.yel}Need to process {cmd}, {args}{C.norm}")
    def process(self):
        'Return the processed lines'
        self.cmdstate = state.normal
        self.stream = io.StringIO()
        for i, line in self.lines:
            if self.cmdstate == state.code:
                cmd, args = None, deque()
                if line == f"{G.trigger}}}":
                    cmd = "}"
            else:
                c = self.idcmd.identify(line, self.vars)
                cmd = c[0]
                args = deque(c[1]) if len(c) > 1 else deque()
            if cmd is None:
                if self.cmdstate == state.code:
                    codeblock.append(line)
                else:
                    self.process_line(line, i)
            else:
                if cmd == "{":
                    self.cmdstate = state.code
                    codeblock = []
                elif cmd == "}":
                    self.cmdstate = state.normal
                    self.execute(codeblock)
                else:
                    self.process_cmd_line(cmd, args, line, i)
        if self.cmdstate == state.code:
            m = f"Missing an end of a code block '{G.trigger}}}'"
            raise SyntaxError(m)
        return self.stream.getvalue()

class fmtstate(Enum):
    normal = auto()     # Echo lines adj to margins, no wrapping, hang, etc.
    hang = auto()       # Hanging indent
    bullet = auto()     # Bullet form
    number = auto()     # Numbered items
    wrap = auto()       # Wrap to existing margins
class just(Enum):
    left = auto()
    right = auto()
    center = auto()
class Fmt:
    'Base class for formatters'
    state = fmtstate.normal     # State of formatter
    just = just.left            # Justification
    lm = 0                      # Left margin
    width = int(os.environ.get("COLUMNS", 80)) - 1
    def __init__(self):
        self.buffer = io.StringIO() 
    def input(self, s):
        '''s is a string, stream, or pathlib object.  Input the data
        from s and process it.
        '''
        if ii(s, P):
            t = dedent(open(s).read())
            self.process(t)
        elif ii(s, str):
            self.process(dedent(s))
        elif hasattr(s, "read"):
            self.process(dedent(s.read()))
        else:
            raise TypeError("s must be string, stream, or pathlib.Path")
    def output(self):
        return self.buffer.getvalue()
    def process(self, s):
        raise Exception("Abstract base class method")

class Normal(Fmt):
    'Echo the lines, adjusting for the left margin & justification'
    def __init__(self):
        super().__init__()
    def process(self, s):
        assert(Fmt.state == fmtstate.normal)
        for line in s.splitlines():
            lm = 1 if not Fmt.lm else Fmt.lm
            if lm > 1:
                line = ''.join([" "*(lm - 1), line])
            n = lm - 1 + self.width
            if Fmt.just == just.left:
                j = "<"
            elif Fmt.just == just.right:
                j = ">"
            elif Fmt.just == just.center:
                j = "^"
            print(f"{line:{j}{n}s}", file=self.buffer)
class Wrap(Fmt):
    def __init__(self):
        super().__init__()
    def process(self, s):
        assert(Fmt.state == fmtstate.wrap)
        w = WrapModule()
        w.i = " "*(Fmt.lm - 1) if Fmt.lm > 1 else ""
        w.width = Fmt.width
        t = w(s)
        print(t, file=self.buffer)
class Bullet(Fmt):
    def __init__(self, bullet="*", nltrigger=None):
        super().__init__()
        self.bullet = bullet
        self.nltrigger = nltrigger
    def first_paragraph(self, s):
        xx()
    def process(self, s):
        assert(Fmt.state == fmtstate.bullet)
        nlnl = "\n\n"
        w = WrapModule()
        w.i = " "*(Fmt.lm - 1) if Fmt.lm > 1 else ""
        # Allow for bullet string and space character in width
        w.width = Fmt.width - len(self.bullet) - 1
        n = len(self.bullet) + 1    # Bullet string and space character
        # Break into paragraphs and process each paragraph
        paragraphs = s.split(nlnl)
        for paragraph in paragraphs:
            paragraph.replace(self.nltrigger, nlnl)
            t = w(paragraph)
            plines = t.splitlines()
            plines[0] = self.bullet + " " + plines[0]
            for i in range(1, len(plines)):
                plines[i] = " "*n + plines[i]

        print(t, file=self.buffer)

if 1:
    ios = io.StringIO
    s = '''
        It is a truth universally acknowledged, that a single man in
        possession of a good fortune, must be in want of a wife.∞ 
        However little known the feelings or views of such a man may be
        on his first entering a neighbourhood, this truth is so well
        fixed in the minds of the surrounding families, that he is
        considered the rightful property of some one or other of their
        daughters.
    '''
    Fmt.lm = 5
    Fmt.state = fmtstate.bullet
    p = Bullet()
    p.input(ios(s))
    print(p.output(), end="")
    exit()

if __name__ == "__main__": 
    # Run the selftests
    from lwtest import run, raises, assert_equal, Assert
    import sys
    from pdb import set_trace as xx
    def Test_cmd_syntax():
        '''These are all valid commands, so there should be no syntax
        errors.
        '''
        test = '''
            .{
                x = 1
                y = 2
            .}
            .# Check reasonable bool values with IdentifyCmd.check_syntax
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
            .del x
            .clear
        '''
        t = TF(test)
        t.debug = True #xx
        t.process()
        # This should result in a syntax error because vars doesn't
        # contain 'x'.
        with raises(ValueError):
            t = TF(".del x")
            t.process()
        # This should result in a syntax error because of a missing end
        # of a code block.
        t = TF('''
            .{
                x = 3
        ''')
        with raises(SyntaxError):
            t.process()
    def Test_clear_and_del():
        # Works on empty dict
        t = TF(".clear")
        t.process()
        # Works on non-empty dict
        t = TF('''
            .{
                x = 8
            .}
            .clear
        ''')
        t.process()
        # del x works
        t = TF('''
            .{
                x = 8
            .}
            .del x
        ''')
        t.process()
    def Test_push():
        t = TF('''
            .lm 8
                x = 8
            .}
            .clear
        ''')
        t.process()
    if "--test" in sys.argv:
        exit(run(globals(), halt=1)[0])
    #xx
    exit(run(globals(), halt=1)[0]) #xx
if __name__ == "__main__": 
    # Run the demos
    def Example1(): pass
    run(globals(), regexp=r"^Example\d\d?", quiet=True)
