'''
Count the number of lines
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Count the number of lines
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    import color as c
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [file1 [file2...]]
      Prints the line counts for the indicated files.  stdin is read if there
      are no files given.  The total number of lines is sent to stderr.
      The smallest and largest line counts are highlighted.
    Options
        -c  Colorize output to show high and low counts
        -n  Sort by file name
        -z  Sort by file size, smallest to largest
        -Z  Sort by file size, largest to smallest
    '''))
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
    if not files:
        Usage()
    return files
def CountLines(stream, file):
    try:
        lines = stream.readlines()
        return (len(lines), file)
    except Exception:
        print("Couldn't read '{file}'", file=sys.stderr)
        return None
def PrintReport(results):
    '''results is [(linecount, filename), ...].  The output order will
    be as the files were given on the command line.
    '''
    if d["-z"]:
        results = list(sorted(results))
    elif d["-Z"]:
        results = list(reversed(sorted(results)))
    elif d["-n"]:
        f = lambda x: x[1]
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
    d = {   # Options dictionary
        "stdin": "<stdin>",
    }
    files = ParseCommandLine(d)
    results = []
    for file in files:
        try:
            s = sys.stdin if file == "-" else open(file)
            name = "<stdin>" if file == "-" else file
        except Exception:
            print("Couldn't open '{name}'", file=sys.stderr) 
        result = CountLines(s, name)
        if result is not None:
            results.append(result)
    PrintReport(results)
    c.normal()
