'''
Treat lines of a file like a set
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2005, 2009 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Treat lines of a file like a set
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import sys
        import getopt
        import re
        from pdb import set_trace as xx
    if 1:  # Custom imports
        from wrap import dedent
        from get import GetWordlist
        if 0:
            import debug       
            debug.SetDebugger()
    if 1:  # Global variables
        element_string = None  # For el operation
if 1:  # Utility
    def Error(msg):
        print(msg, file=sys.stderr)
        exit(1)
    def Manpage():
        print(dedent(f'''
        There are two use cases for this script:
            - Compare the lines in two files
            - Convert files to sets of words and compare them

        In the first case, the lines making up the file are regarded as elements of a
        set.  In fact, this is what is done internally, as python lets you construct
        sets of hashable objects like strings.

        The second use case uses the same basic set operations, but first parses the
        input file into tokens by splitting on whitespace.

        Here are two example files that will illustrate the behaviors:

        file1:
            This is file1
            One common line
            One uncommon line
        file2:
            This is file2
            Another uncommon line
            One common line

        Running the script with the various operands (op) gives the following results:

            ne  -> True
            eq  -> False
            el  -> False
            di  ->
                One uncommon line
                This is file1
            sd  ->
                Another uncommon line
                One uncommon line
                This is file1
                This is file2
            in  ->
                One uncommon line
            is  -> False
            un  -> 
                Another uncommon line
                One common line
                One uncommon line
                This is file1
                This is file2

        Running the script with the various operands (op) gives the following results
        when the -w option is used:
            ne  -> True
            eq  -> False
            el  -> False
            di  ->
                file1
            sd  ->
                Another
                file1
                file2
            in  ->
                One
                This
                common
                is
                line
                uncommon
            is  -> False
            un  -> 
                Another
                One
                This
                common
                file1
                file2
                is
                line
                uncommon
        '''))
        exit(0)
    def ParseCommandLine():
        d["-H"] = False  # Print manpage
        d["-i"] = []  # Regexps of lines to ignore
        d["-l"] = False  # Convert all lines to lowercase
        d["-s"] = True  # Sort output
        d["-W"] = False  # Same as -w except convert all punctuation to space characters
        d["-w"] = False  # Convert all file contents to a list of words, splitting on whitespace
        d["--ws"] = False  # Ignore leading and trailing whitespace
        if len(sys.argv) < 2:
            Usage()
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "Hhi:lsWw", "--ws")
        except getopt.GetoptError as e:
            msg, option = e
            print(msg)
            sys.exit(1)
        for o, a in optlist:
            if o[1] in list("Hlsw"):
                d[o] = not d[o]
            elif o == "-h":
                Usage(0)
            elif o == "-i":
                r = re.compile(opt[1])
                d["-i"].append(r)
            elif o == "--ws":
                d[o] = not d[o]
        if d["-H"]:
            Manpage()
        if len(args) < 2:
            Usage()
        CheckArgs(args)
        return args
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] op file1 file2 [file3 ...]
          where op is the operation:
            ne        B      Lines in file1 are != to the lines in following files
            eq        B      Lines in file1 are == to the lines in following files
            el        B      file1 contains the string given as file2 as an element
            di        L      Lines in file1 that are not in the following files
            sd       +L      Lines that are in file1 or the remaining files, but
                                not both (symmetric difference)
            in        L      Lines that are common to all files (intersection)
            is       +B      Determine whether file1 is a proper subset of
                                remaining files
            un        L      Lines that are in any of the files (union)
          Performs operations on the lines of a file as if they were members of a set.  In
          the operations marked with '+', file2 and subsequent files will be collapsed into
          one set of lines.  
        
          ne, eq, el, and is return Boolean values (B) and also indicate the state by
          returning 0 for true and 1 for false (i.e., their exit codes).  The other
          operations return the resulting lines (L).  They will be stripped of leading
          and trailing whitespace if you use the -w option.
        
          Output is sent to stdout and is sorted; use the -s option if you don't
          want the lines sorted (they will be in an indeterminate order, however,
          as a set has no notion of ordering).
        
          If a filename starts with ':', then it is a list of filenames to read, one file
          per line.
        Options
          -H            Print a manpage
          -i regexp     Ignore lines that contain the regexp.  More than one of
                        these options may be given.
          -l            Convert all lines to lowercase
          -s            Do not sort the output lines
          -W            Same as -w except convert all punctuation to space characters
          -w            Convert all file contents to a list of words, splitting on
                        whitespace
          --ws          Ignore leading and trailing whitespace
        '''))
        exit(status)
if 1:  # Core functionality
    def CheckArgs(args):
        if len(args) < 3:
            Usage()
        try:
            op = args[0][:2]
            if op not in "ne eq el di sd in is un".split():
                Error(f"{args[0]!r} is not a recognized operation")
        except Exception:
            Usage(1)
        args[0] = op
        if op in "sd is el".split():
            if len(args) != 3:
                Usage(1)
    def GetLines(file):
        '''Return a list of the lines from file.  If file is a string beginning with ':',
        then it's a file whose lines are filenames to be read.
        '''
        if file.startswith(":"):
            lines = []
            for _file in open(file[1:]).read().split("\n"):
                f = _file.strip()
                if f:
                    lines.extend(open(f).read().split("\n"))
        else:
            lines = open(file).read().split("\n")
        return lines 
    def GetData(op, files):
        '''Read in the lines from the files and return (lines1, lines2)
        where lines1 and lines2 are the sets of lines.  The returned lines do not
        include the newline.
          op:       one of the strings ne eq el di sd in is un
          files:    List of files to get lines from
          d:        Command line options dictionary
        '''
        def do_not_ignore(line, r):
            return not r.search(line)
        lines1 = GetLines(files[0])
        lines2 = []
        if op == "el":
            lines2 = []
            global element_string
            element_string = files[1] + "\n"
        else:
            for file in files[1:]:
                lines2 += GetLines(file)
            if d["-i"]:  # Ignore lines with given regular expressions
                for r in d["-i"]:
                    lines1 = [line for line in lines1 if do_not_ignore(line, r)]
                    lines2 = [line for line in lines2 if do_not_ignore(line, r)]
            if d["--ws"]:  # Strip leading and trailing whitespace
                lines1 = [line.strip() for line in lines1]
                lines2 = [line.strip() for line in lines2]
            if d["-l"]:  # Convert lines to lowercase
                lines1 = [line.lower() for line in lines1]
                lines2 = [line.lower() for line in lines2]
        if d["-W"] or d["-w"]:
            # Convert the lines to sets of words
            lines1 = GetWordlist(' '.join(lines1), remove_punc=d["-W"])
            lines2 = GetWordlist(' '.join(lines2), remove_punc=d["-W"])
        return frozenset(lines1), frozenset(lines2)

if __name__ == "__main__":
    d = {}
    args = ParseCommandLine()
    op = args[0]
    del args[0]
    files = args
    lines1, lines2 = GetData(op, files)
    status = 0
    if op == "di":
        results = lines1 - lines2
    elif op == "sd":
        results = lines1 ^ lines2
    elif op == "in":
        results = lines1 & lines2
    elif op == "un":
        results = lines1 | lines2
    elif op == "ne":
        print(str(lines1 != lines2))
        if lines1 == lines2:
            status = 1
    elif op == "eq":
        print(str(lines1 == lines2))
        if lines1 != lines2:
            status = 1
    elif op == "el":
        if element_string in lines1:
            print(str(True))
        else:
            print(str(False))
            status = 1
    elif op == "is":
        print(str(lines1 < lines2))
        if not lines1 < lines2:
            status = 1
    if op in ("di", "sd", "in", "un"):
        results = list(results)
        if d["-s"]:
            results = sorted(results)
        for line in results:
            if line:
                if line[-1] == "\n":
                    print(line, end="")
                else:
                    print(line)
