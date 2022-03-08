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
    # formatting text for python script output to a terminal.  Warning:
    # not ready for production use yet.
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
    from abbreviations import IsAbbreviation
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
def dedent(s, empty=True):
    '''For the string s, trim leading and trailing lines of whitespace,
    then remove any common leading space characters from each line.  If
    empty is True, then empty lines are considered to have the common
    indent number of spaces.
 
    Example:  For s = "   \n    Line 1\n      Line 2  \n    ", dedent(s)
    will return 'Line 1\n  Line 2  '.
    '''
    def LeadingSpaces(s):
        'Return the number of space characters at the beginning of s'
        i = 0
        while len(s) > i and s[i] == " ":
            i += 1
        return i
    if not ii(s, str):
        raise TypeError("s must be a string")
    if not s.strip():
        return ""
    lines = s.split("\n")   # Splitting on a newline always returns a list
    if len(lines) == 1:
        return lines[0].strip()
    # Delete first & last lines if only whitespace
    for i in (0, -1):
        if not lines[i].strip():
            del lines[i]
    # Get sequence of the number of beginning spaces on each line
    o = [LeadingSpaces(i) for i in lines]
    if empty:   # Make the empty lines have "infinite" spaces
        m = max(o)
        o = [i if i else m + 1 for i in o]  
    if min(o):
        lines = [line[min(o):] for line in lines]
    return "\n".join(lines)
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
    block = auto()      # Left and right justified
class just(Enum):
    left = auto()
    right = auto()
    center = auto()
class Fmt:
    '''Base class for formatters.  Does basic left/center/right
    formatting of lines.
    '''
    def __init__(self):
        self.state = fmtstate.normal
        self._left = 0      # Left margin
        self.width = int(os.environ.get("COLUMNS", 80)) - 1
        self.just = just.left
    def __call__(self, s):
        '''s is a string, stream, or pathlib object.  Input the data
        from s and process it.
        '''
        # Get the string to process
        if ii(s, P):
            t = dedent(open(s).read())
        elif ii(s, str):
            t = dedent(s)
        elif hasattr(s, "read"):
            t = dedent(s.read())
        else:
            raise TypeError("s must be string, stream, or pathlib.Path")
        # Format the lines
        lines = t.split("\n")
        if self.just == just.left:
            j = "<"
        elif self.just == just.right:
            j = ">"
        elif self.just == just.center:
            j = "^"
        i = " "*self.left
        lines = [f"{i}{line:{j}{self.width}s}" for line in lines]
        return '\n'.join(lines)
    @property
    def left(self):
        '''This 'left margin' property is equivalent to the number of
        space characters that must be appended to a line to get the
        first character at the desired 1-based column number.  Thus, you
        can consider this left margin number the 0-based python
        numbering of the columns.
        '''
        assert(self._left >= 0)
        return self._left - 1 if self._left else 0
    @left.setter
    def left(self, value):
        if not ii(value, int):
            raise TypeError("left must be an integer")
        self._left = max(0, int(value))
class Block(Fmt):
    def __init__(self):
        super().__init__()
    def justify_paragraph(self, s):
        'Block justify string s into width self.width = L and return it'  
        # Modified by DP; the original algorithm had a couple of bugs that
        # show up when you test at corner cases like L == 1.  Also added
        # extra stuff for end of sentence and colon.
        # From https://medium.com/@dimko1/text-justification-63f4cda29375
        f = lambda x, y: x.endswith(y)
        L = self.width
        indent = " "*self.left
        out, line, num_of_letters = [], [], 0
        for w in s.split():
            if (not IsAbbreviation(w) and 
                    (f(w, ".") or f(w, "!") or f(w, "?") or f(w, ":"))):
                w = w + " "
            if num_of_letters + len(w) + len(line) > L:
                spaces_to_add = max(L - num_of_letters, 0)
                # The following avoids a divide by zero when L is small
                ws_amount = max(len(line) - 1, 1)
                for i in range(spaces_to_add):
                    # When L is small, line can be empty and the
                    # mod results in an exception
                    if line:
                        line[i % ws_amount] += ' '
                out.append(indent + ''.join(line))
                line, num_of_letters = [], 0
            line.append(w)
            num_of_letters += len(w)
        # I don't want the last line to have trailing spaces
        out.append(indent + ' '.join(line))
        return '\n'.join(out)
    def __call__(self, s):
        brk="\n\n"
        paragraphs = [self.justify_paragraph(p) for p in s.split(brk)]
        return brk.join(paragraphs)
class Wrap(Fmt):
    # Independently generated wrap class, simpler than wrap.py.
    def __init__(self):
        super().__init__()
        self.sentence_sep = " "
    def __call__(self, s, sep="\n\n"):
        '''Return the wrapped string from paragraphs of s.  paragraphs
        are separated by the string sep.
        '''
        out = []
        for i in s.split(sep):
            out.append(self.wrap(i))
        return sep.join(out)
    def is_sentence_end(self, t):
        'Return True if string t ends a sentence'
        # Note we call 'word:' a sentence end too.
        f = lambda x, y:  x.endswith(y)
        if f(t, ".") and not IsAbbreviation(t):
            return True
        elif f(t, "?") or f(t, "!") or f(t, ":"):
            return True
        return False
    def wrap_line(self, s):
        '''Wrap s to get it to fit a line of width self.width and return 
        (first_line_string, remaining_string).
        '''
        #raise Exception("xx Not needed") #xx
        def get(s, count):
            if s[count] == " ":
                first_line_string = s[:count].rstrip()
                remaining_string = s[count:].strip()
                return first_line_string, remaining_string
            else:
                return None
        count = self.width - 1
        while count and get(s, count) is None:
            count -= 1
        if not count:
            raise ValueError("No space characters in first line")
        return get(s, count)
    def wrap(self, s, indent=True):
        'Wrap the string s to self.width'
        out, line, tokens = deque(), deque(), deque(s.split())
        LEN = lambda x:  len(' '.join(x))
        while tokens:
            token = tokens.popleft()
            if self.is_sentence_end(token):
                token += self.sentence_sep
            line.append(token)
            next_token_length = len(tokens[0]) if tokens else 0
            if LEN(line) + next_token_length + 1 >= abs(int(self.width)):
                out.append(' '.join(line).rstrip())
                line.clear()
        if line:
            out.append(' '.join(line))
        if indent:      # Apply indent to each line
            t = " "*self.left
            u = [t + i for i in out]
            return '\n'.join(u)
        else:
            return '\n'.join(out)
class Bullet(Fmt):
    def __init__(self, bullet="*", internalnl=None):
        '''Format with the indicated bullet string.  internalnl is the
        string to use to break on to continue a bullet with a pair of
        newline characters.
 
        Example:  If s = "This is a bullet.XA follow-on paragraph." then
        using 'X' as the internalnl, the bulleted form would be
 
            * This is a bullet.
 
              A follow-on paragraph.
        '''
        super().__init__()
        self.bullet = bullet
        self.internalnl = internalnl
    def paragraph(self, s, outsep="\n\n"):
        n = len(self.bullet) + 1
        lines, wrap = deque(), Wrap()
        for i, p in enumerate(s.split(self.internalnl)):
            if i:
                wrap.width -= n
                lines.append(wrap(p))
                wrap.width += n
            else:
                # First line
                first, remainder = wrap.wrap_line(p)
                lines.append(first)
                wrap.width -= n
                lines.append(wrap(remainder))
                wrap.width += n
        return outsep.join(lines)
    def __call__(self, s, insep="\n\n", outsep="\n\n"):
        '''Break the string s into paragraphs separated at insep, then
        format each paragraph as a bulleted item.  Separate the out
        paragraphs with outsep.
        '''
        out = deque()
        for paragraph in s.split(insep):
            paragraph = self.bullet + " " + paragraph
            out.append(self.paragraph(paragraph, outsep=outsep))
        pp(out);exit() #xx
        return outsep.join(out)
if 1:
    s = dedent('''
        Mrs. Gardiner's caution to Elizabeth was punctually and kindly given on
        the first favourable opportunity of speaking to her alone; after
        honestly telling her what she thought, she thus went on:

        "You are too sensible a girl, Lizzy, to fall in love merely because you
        are warned against it; and, therefore, I am not afraid of speaking
        openly.  Seriously, I would have you be on your guard.
    ''')
    w = Bullet()
    w.internalnl = "∞"
    w.width = 60
    w.left = 5
    print(w(s))
    exit()
if 0:
    s = '''
        It is a truth universally acknowledged, that a single man in
        possession of a good fortune, must be in want of a wife.

        However little known the feelings or views of such a man may be
        on his first entering a neighbourhood, this truth is so well
        fixed in the minds of the surrounding families, that he is
        considered the rightful property of some one or other of their
        daughters.
    '''
    p = Block()
    p.left = 5
    p.width = 60
    print(p(s))
    print("-"*70)
    p = Wrap()
    p.left = 5
    p.width = 60
    print(p(s))
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
if __name__ == "__main__": 
    # Run the demos
    def Example1(): pass
    run(globals(), regexp=r"^Example\d\d?", quiet=True)
