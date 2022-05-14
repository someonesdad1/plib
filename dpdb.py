'''

This module is what I use to colorize parts of the python debugger output
using the color.py module.

    - The 'clr' command is used to turn colorizing on and off; it's
      argument is a boolean that, if true, turns colorizing on.

    - The three things I wanted were:
        - Colorize the current line in a list command
        - Colorize the current line, highlighting the file name, line
          number and function name
        - Make debugger error messages stand out

    My universal use of the debugger has always been to set the variable 
    xx to pdb.set_trace.  When inserted in a chunk of code as xx(), the
    code stops in the debugger at that point.  Later python 3 versions used
    the reserved word 'breakpoint' for this.

    In any code I want to debug, I insert the line
        from dpdb import set_trace as xx 
    and get the requisite behavior.
'''
from pdb import Pdb
import re
import sys
from wrap import dedent
from color import TRM as t
from pathlib import Path
if 1:   # Colorizing strings
    def Fancy():
        'Fancier set of colors'
        t.current_line = t("cynl")
        t.directory = t("brnl")
        t.filename = t("trq")
        t.linenum = t("yell")
        t.function = t("lavl")
        t.error = t("ornl")
    def Plain():
        'Minimal set of colors'
        t.current_line = t("cynl")
        t.directory = t("wht")
        t.filename = t("wht")
        t.linenum = t("grnl")
        t.function = t("wht")
        t.error = t("ornl")
    def NoColors():
        t.current_line = ""
        t.directory = ""
        t.filename = ""
        t.linenum = ""
        t.function = ""
        t.error = ""
    color_choice = Plain
    color_choice()
if 1:   # Regular expressions
    # Identify current line in list command
    t.list = re.compile(r"^(\d+)(\s->\s.*)$")
    # Identify current line when stepping
    t.curr = re.compile(r'''
        ^>\s        # Beginning of line is '> '
        ([^(]*?)    # Match up to parentheses for dir/filename
        \((.*?)\)   # Get text in parentheses for line number
        ([^\n]*)    # Get text up to newline for function name
        (\n.*)$     # String to end of line for current line
        ''', re.M|re.X)

class DPdb(Pdb):
    def current_stopped_line(self, file, linenum, func, remainder):
        print("> ", end="")
        # Only colorize the file name portion
        p = Path(file)
        print(f"{t.directory}{p.parent}/", end="")
        print(f"{t.filename}{p.name}{t.n} ", end="")
        print(f"{t.linenum}{linenum}{t.n} ", end="")
        print(f"{t.function}{func}{t.n}", end="")
        print(f"{remainder}")
    def current_listing_line(self, linenum, remainder):
        print(f"{t.linenum}{linenum}", end="")
        t.print(f"{t.current_line}{remainder}")
    def message(self, msg):
        # Look for a current line being printed with the list command.
        # This will be a line number followed by '->'.
        mo = t.list.match(msg)
        if mo:
            linenum, remainder = mo.groups()
            self.current_listing_line(linenum, remainder)
            return
        # Look for the current stopped line
        mo = t.curr.match(msg)
        if mo:
            file, linenum, func, remainder = mo.groups()
            self.current_stopped_line(file, linenum, func, remainder)
            return
        print(f"{msg}")
    def error(self, msg):
        print(f"{t.error}", end="")
        t.print('***', msg, file=self.stdout)
    def do_clr(self, var):
        'Toggle colorizing'
        color_choice() if var else NoColors()

def set_trace(*, header=None):
    pdb = DPdb()
    if header is not None:
        pdb.message(header)
    pdb.set_trace(sys._getframe().f_back)
