"""
Delete blank lines from files or stdin and fix docstrings.  This is intended to be used
to remove blank lines that are inserted by python formatters like ruff or black.
"""
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Delete blank lines from files or stdin
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        import re
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [file1 [file2 ...]]
          Delete blank lines from files.  Note a blank line is a line with no whitespace
          on it except for a newline.  Assumes stdin for no files.  If you include files
          on the command line, use '-' for stdin.
        Options:
            -1      Collapse multiple blank lines to one
        """)
        )
        exit(status)
    def ParseCommandLine(d):
        d["-1"] = False  # Multiple blank lines to one
        # if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, files = getopt.getopt(sys.argv[1:], "1")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("1"):
                d[o] = not d[o]
        return files
if 1:  # Core functionality
    def ProcessFileOrig(file):
        """Use regex matching to remove blank lines.
        
        A problem with this approach is that it will remove the blank lines inside of
        python multiline strings, which is almost certainly not wanted.
        ProcessFile2() was made to handle this case.  However, this function's approach
        is also concise and fast.
        """
        s = sys.stdin.read() if file == "-" else open(file).read()
        # Remove leading and trailing blank lines
        s = re.sub(r"^\n+", "", s)
        s = re.sub(r"\n+$", "", s)
        if d["-1"]:
            s = re.sub(r"\n\n\n+", "\n\n", s)
        else:
            s = re.sub(r"\n\n+", "\n", s)
        print(s)
    def ProcessFile(file):
        lines = sys.stdin.read() if file == "-" else open(file).read()
        for line in lines.split("\n"):
            ProcessLine(line)
    def IsComment(line):
        return line.strip()[0] == "#"
    def ProcessLine(line):
        """If we're in a multiline string, send the line to stdout.  Otherwise, if it's a
        blank line, ignore it; if not, print it.
        """
        single, double, empty = "'''", '"""', ""
        
        def GetSingleTriple(line):
            "Return any single triple quote in this line"
            nonlocal single, double, empty
            if IsComment(line):
                return empty
            elif single in line and double not in line:
                return single
            elif single not in line and double in line:
                return double
            elif single not in line and double not in line:
                return empty
            else:
                # Had both single & double on line; get their locations
                loc_single = line.find(single)
                loc_double = line.find(double)
                # If we're current in a single quote multiline, it's only ending if the
                # single triple comes after the double triple.  Analogously for the double
                # quote multiline.
                if ProcessLine.multiline == single and loc_single > loc_double:
                    return single
                elif ProcessLine.multiline == double and loc_double > loc_single:
                    return double
                else:
                    return double if loc_double > loc_single else single
                    
        def IsSingleMultiline(line):
            nonlocal single, double
            return line.count(single) == 1 or line.count(double) == 1
            
        def CountLeadingSpaces(string):
            lst, count = list(string), 0
            while lst:
                c = lst.pop(0)
                if c == " ":
                    count += 1
                else:
                    break
            return count
            
        # We'll use ProcessLine.previous_line to keep track of the previous line.  If we
        # encounter an empty line while in a multiline string, we'll add in the number
        # of spaces of indent on the previous line.
        if ProcessLine.multiline:  # We're currently in a multiline string
            if IsSingleMultiline(line):
                item = GetSingleTriple(line)
                if item == ProcessLine.multiline:  # Single or double triple is ended
                    ProcessLine.multiline = empty
            if not line:
                # Add indent of previous line
                line = " " * CountLeadingSpaces(ProcessLine.previous_line)
            print(line)
            ProcessLine.previous_line = line
        elif line == "":  # Don't print an empty line
            return
        elif line.count(single) == 1 or line.count(double) == 1:
            if ProcessLine.multiline:
                print(line)
                ProcessLine.previous_line = line
                # Exit the multiline state
                ProcessLine.multiline = empty
            else:
                print(line)
                ProcessLine.previous_line = line
                # Enter the multiline state
                if line.count(single) == 1:
                    ProcessLine.multiline = single
                elif line.count(double) == 1:
                    ProcessLine.multiline = double
                else:
                    print(f"---------- BUG ------------")
                    breakpoint()  # xx
        else:
            print(line)
            ProcessLine.previous_line = line
            
    def Reset():
        ProcessLine.previous_line = None
        ProcessLine.multiline = False
        
        
if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    if not files:
        Reset()
        ProcessFile("-")
    else:
        for file in files:
            Reset()
            ProcessFile(file)
            
