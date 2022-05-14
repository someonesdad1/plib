'''

This module is what I use to colorize parts of the python debugger output
using the color.py module.  Features:

    - The 'clr' command can be used to choose the colorizing colors or turn
      them off.
    - The three colorizations are:
        - The current line in a list command
        - Colorize the current line, highlighting the file name, line
          number and function name
        - Error messages 

    My universal use of the debugger has always been to set the variable 
    xx to pdb.set_trace.  When inserted in a chunk of code as xx(), the
    code stops in the debugger at that point.  Later python 3 versions used
    the reserved word 'breakpoint' for this.

    In any code I want to debug, I insert the line
        from dpdb import set_trace as xx 
    and get the requisite behavior.
'''
from pdb import Pdb
import linecache
import re
import sys
from wrap import dedent
from color import TRM as t
from pathlib import Path
if 1:   # Functions to set up colorizing strings
    def All():
        'Fancier set of colors'
        t.current_line = t("cynl")
        t.directory = t("brnl")
        t.filename = t("trq")
        t.linenum = t("yell")
        t.function = t("lavl")
        t.error = t("ornl")
    def LineNumOnly():
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
    color_choice = LineNumOnly
    color_choice()
if 1:   # Regular expressions
    # Identify current line in list command
    t.list = re.compile(r"^(\d+)(\s+->\s.*)$")
    # Identify current line when stepping
    t.curr = re.compile(r'''
        ^>\s        # Beginning of line is '> '
        ([^(]*?)    # Match up to parentheses for dir/filename
        \((.*?)\)   # Get text in parentheses for line number
        ([^\n]*)    # Get text up to newline for function name
        (\n.*)$     # String to end of line for current line
        ''', re.M|re.X)
class DPdb(Pdb):
    if 1:   # Overridden Pdb methods
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
        # This method is changed to allow more than 11 lines to be shown
        def do_list(self, arg):
            '''l(ist) [first [,last] | .]

            List source code for the current file.  Without arguments,
            list 11 lines around the current line or continue the previous
            listing.  With . as argument, list 11 lines around the current
            line.  With one argument, list 11 lines starting at that line.
            With two arguments, list the given range; if the second
            argument is less than the first, it is a count.

            The current line in the current frame is indicated by "->".
            If an exception is being debugged, the line where the
            exception was originally raised or propagated is indicated by
            ">>", if it differs from the current line.
            '''
            numlines = 30       # DP
            half = numlines//2  # DP
            self.lastcmd = 'list'
            last = None
            if arg and arg != '.':
                try:
                    if ',' in arg:
                        first, last = arg.split(',')
                        first = int(first.strip())
                        last = int(last.strip())
                        if last < first:
                            # assume it's a count
                            last = first + last
                    else:
                        first = int(arg.strip())
                        #first = max(1, first - 5)
                        first = max(1, first - half)   # DP
                except ValueError:
                    self.error('Error in argument: %r' % arg)
                    return
            elif self.lineno is None or arg == '.':
                #first = max(1, self.curframe.f_lineno - 5)
                first = max(1, self.curframe.f_lineno - half)  # DP
            else:
                first = self.lineno + 1
            if last is None:
                #last = first + 10
                last = first + numlines     # DP
            filename = self.curframe.f_code.co_filename
            breaklist = self.get_file_breaks(filename)
            try:
                lines = linecache.getlines(filename, self.curframe.f_globals)
                self._print_lines(lines[first-1:last], first, breaklist,
                                self.curframe)
                self.lineno = min(last, len(lines))
                if len(lines) < last:
                    self.message('[EOF]')
            except KeyboardInterrupt:
                pass
        do_l = do_list
    if 1:   # New methods
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
        def do_clr(self, var):
            'Set colorizing:  0 = None, 1 = line number, 2 = all'
            try:
                value = int(var)
            except Exception:
                value = 1
            if value == 0:
                NoColors()
            elif value == 1:
                LineNumOnly()
            elif value == 2:
                All()
            else:
                print("value must be 0 (no color), 1 (line number), or 2 (all)")
def set_trace(*, header=None):
    pdb = DPdb()
    if header is not None:
        pdb.message(header)
    pdb.set_trace(sys._getframe().f_back)
