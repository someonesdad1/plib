'''
Text formatter: Develop a mini-language for formatting strings.
 
    The main use case is to be able to get formatted output for the help
    strings used in scripts.
 
    A line containing a formatter command begins with a "." after
    stripping off whitespace.  If you want a line to begin with a
    period, escape it with a backslash.
 
    In the following, the leading '.' to the commands is not shown.
 
    Python code blocks and variables
 
        { and } delimit code blocks.  Common indentation is removed and the
        lines are executed one at a time with exec(line, globals(), vars)
        where vars is a maintained local variables dictionary.
  
            When a } is encountered, the code block is finished and it
            is executed.  stdout is trapped and becomes part of the
            formatted string.  stderr is also trapped, colorized, and
            printed to stderr.
 
            Colors:
                Code line               lcyan
                Source line in debug    brown
                Stuff sent to stdout    yellow
                Stuff sent to stderr    lred
 
        del x:  Delete the variable named x from vars.
 
        clear:  Clears the vars dictionary.  If you .pop, the old vars
        dictionary will be restored.
 
    State 
 
        The saved states are in a dictionary that is independent of the
        variables in vars and code.  This dictionary gets put onto a stack
        when you .push.
    
        debug x/on/off:  If True, print each line in color with its line
        number, followed by its formatted form.  Code lines are printed
        in a different color with no formatted form.
 
        format x/on/off:  If off, the output is not formatted; it is
        output as it is found in the line.  Otherwise, each line is
        formatted per the current state.  If the argument is x, it is
        bool(vars["x"]).
    
        out x/on/off:  Turn output on/off.  If it is off, no lines are
        output until the next '.output on' is seen.  This is a handy way to 
        comment out a chunk of text.  If the argument is x, it is
        bool(vars["x"]).
    
        push:  Save the current state.  Note vars is part of the state, so a
        subsequent '.clear' will be "forgotten" when you .pop or .restore an
        older state.  A shallow copy of vars is made for the new state.
    
        pop:  Restore the previously pushed state
    
        State variables:
    
            Left margin:        integer >= 0
            Right margin:       integer >= 0
            Width               integer >= 0
            Justification:      {left, right, center}
            wrap                bool
    
    Margins
    
        lm n:  Set left margin.  Set to 0 to have text start at column 1.
        Default 0.
    
        width n:  0 means wrap to width from COLUMNS.  'n' means to wrap to
        int(n) columns.  Default 0.
    
    Justification
        <:      Left justification
        >:      Right justification
        ^:      Center the lines
        wrap x/on/off:   Wrap paragraphs to current margins
    
    Other commands
        empty n:  A line with no whitespace is replaced by one with n space
        characters.
    
        #:  This line is a comment and won't make it to the output
    
    Commands with arguments:
        exec del verbatim out save load remove lm rm width prefix suffix
        emtpy
    
    Commands with no arguments:
        { } clear push pop 
    
    Commands with optional arguments
        < > ^ #
    
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
    from enum import Enum
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
class IdentifyCmd:
    def __init__(self):
        self.no_args = set("{ } clear push pop".split())
        self.opt_args = set("< > ^ #".split())
        self.args = set('''exec del verbatim out 
            lm width prefix suffix emtpy'''.split())
        self.all = self.no_args | self.opt_args | self.args
    def identify(self, line):
        '''Return None if not a command; otherwise return list of 
        [cmd, arg1, ...].
        '''
        s = line.strip()
        if not s.startswith("."):
            return None
        f = s[1:].split()
        candidate = f[0]
        if candidate not in self.all:
            return None
        elif candidate in self.no_args:
            return [candidate]
        elif candidate in self.opt_args or candidate in self.args:
            return f
class state(Enum):
    init = 0
    normal = 1
    code = 2
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
        lines = dedent('\n'.join(lines_of_code))
        if self.debug:
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
            print(f"{G.stderr}{err}{G.norm}, end=""", file=sys.stderr)
    def process(self):
        'Return the processed lines'
        self.state = state.normal
        self.stream = io.StringIO()
        for i, line in self.lines:
            cmd = self.idcmd.identify(line)
            if cmd is not None:
                if cmd[0] == "{":
                    self.state = state.code
                    cl = []
                elif cmd[0] == "}":
                    self.state = state.normal
                    self.execute(cl)
            else:
                if self.state == state.code:
                    cl.append(line)
                else:
                    print(line, file=self.stream)
        return self.stream.getvalue()

if 1:
    test = '''
        .{
            # Test code
            x = 0
            if x:
                print("hello from first code")
            x = 1
        .}
        .lm 0
        This is some text
        Here's the second line
        .{
            if x:
                print("Hello from second code")
        .}
        And a third line
    '''
    t = TF(test)
    t.debug = len(sys.argv) > 1
    s = t.process()
    print(s, end="")
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
    from lwtest import run, Assert
    import sys
    from pdb import set_trace as xx
    def Test1():
        pass
    if "--test" in sys.argv:
        exit(run(globals(), halt=1)[0])
if __name__ == "__main__": 
    # Run the demos
    def Example1():
        pass
    run(globals(), regexp=r"^Example\d\d?", quiet=True)
