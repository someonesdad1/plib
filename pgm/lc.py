"""
Count the number of lines
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Count the number of lines
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    import color as c


def Usage(status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [file1 [file2...]]
      Prints the line counts for the indicated files.  stdin is read if there
      are no files given.  The total number of lines is sent to stderr.
      The smallest and largest line counts are highlighted.
    Options
        -c  Colorize output to show high and low counts
        -h  Print this help
        -n  Sort by file name
        -z  Sort by file size, smallest to largest
        -Z  Sort by file size, largest to smallest
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-c"] = False
    d["-n"] = False
    d["-z"] = False
    d["-Z"] = False
    try:
        optlist, files = getopt.getopt(sys.argv[1:], "chnzZ")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "cnzZ":
            d[o] = not d[o]
        if o == "-h":
            Usage(0)
    if not case1 and not files:
        Usage()
    return files


def CountLines(stream, filename):
    try:
        lines = stream.readlines()
        return (len(lines), filename)
    except Exception as e:
        # print(f"Couldn't read '{file}':\n  {e}", file=sys.stderr)
        # Unable to read the file, so open it as binary and read the number
        # of newline characters
        bytes = open(filename, "rb").read()
        return (bytes.count(0x0A), filename)


def PrintReport(results):
    """results is [(linecount, filename), ...].  The output order will
    be as the files were given on the command line.
    """
    if d["-z"]:
        results = list(sorted(results))
    elif d["-Z"]:
        results = list(reversed(sorted(results)))
    elif d["-n"]:

        def f(x):
            return x[1]

        results = list(sorted(results, key=f))
    # Get largest number in results array
    counts = [i[0] for i in results]
    maxsize = max(counts)
    minsize = min(counts)
    total = sum(counts)
    w = len(str(total))
    # Print results array
    for linecount, filename in results:
        already_colored = False
        if linecount == maxsize:
            if d["-c"]:
                c.fg(c.lred)
                already_colored = True
        elif linecount == minsize:
            if d["-c"]:
                c.fg(c.lgreen)
                already_colored = True
        if not already_colored and filename == d["stdin"]:
            if d["-c"]:
                c.fg(c.lcyan)
        print(f"{linecount:{w}d}  {filename}")
        if d["-c"]:
            c.normal()
    # Print total
    if d["-c"]:
        c.fg(c.yellow)
    print(f"{total:{w}d}  Total")
    if d["-c"]:
        c.normal()


if __name__ == "__main__":
    # NOTE:  there are two behaviors:  1) read from stdin if there are no
    # arguments or 2) you must use '-' as a file to read from stdin.  Set
    # case1 to True if you want 1).
    case1 = True
    d = {  # Options dictionary
        "stdin": "<stdin>",
    }
    files = ParseCommandLine(d)
    results = []
    if not files and case1:
        result = CountLines(sys.stdin, "<stdin>")
        if result is not None:
            results.append(result)
    else:
        for file in files:
            try:
                filename = "<stdin>" if file == "-" else file
                s = sys.stdin if file == "-" else open(file)
            except FileNotFoundError:
                print(f"Couldn't open '{filename}'", file=sys.stderr)
                if len(files) == 1:
                    exit(1)
            result = CountLines(s, filename)
            if result is not None:
                results.append(result)
    PrintReport(results)
    c.normal()
