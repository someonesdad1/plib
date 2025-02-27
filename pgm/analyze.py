"""
Print word statistics for each file
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Print word statistics for each file
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    import string
    import os
    from pdb import set_trace as xx
if 1:  # Custom imports
    from f import flt
    from wrap import dedent
if 1:  # Global variables
    # The following table is used in ''.translate() to convert all
    # punctuation characters to spaces.
    transtable = "".maketrans(string.punctuation, " " * len(string.punctuation))
    nl = "\n"
    discard_punctuation = True
    ignore_length = None
    columns = int(os.environ.get("COLUMNS", 80)) - 1
    # We'll use this to keep track of big words if -b option given.
    # big_word_length defines the length of a big word.
    big_word_length = None
    big_words = set()


def Usage(status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {name} [options] [file1 [file2 ...]]
      Analyzes a file (or stdin) for its word properties.  For each
      file, a word length histogram and summary statistics are printed.
      Use '-' for stdin.  Words are parsed on whitespace.
    Options:
      -b l      Defines the length of a big word.  If this option is used,
                the big words found in the input are printed after the report.
      -c        Ignore lines that start with '#'
      -h        Show this help statement
      -i l      Ignore words longer than l
      -p        Remove punctuation from input
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-c"] = False  # Ignore lines that start with '#'
    d["-p"] = False  # Remove punctuation
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "b:ci:hp")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-b":
            global big_word_length
            big_word_length = int(opt[1])
        elif opt[0] == "-c":
            d["-c"] = True
        elif opt[0] == "-h":
            Usage(0)
        elif opt[0] == "-i":
            global ignore_length
            try:
                ignore_length = int(opt[1])
                if ignore_length < 1:
                    raise ValueError()
            except ValueError:
                err("-i option must be an integer > 0")
        elif opt[0] == "-p":
            d["-p"] = True
    if not args:
        Usage()
    return args


def GetWord(stream):
    """This is a generator to get each word from the stream.  It uses the
    default behavior of ''.split(), which is to split words on whitespace.
    """
    for line in stream:
        if d["-p"]:
            line = line.translate(transtable)
        for word in line.split():
            yield word


def ProcessWord(word, stats):
    "Put histogram information into the dictionary stats"
    n = len(word)
    if ignore_length is not None and n >= ignore_length:
        return
    if big_word_length is not None and n >= big_word_length:
        global big_words
        big_words.add(word)
    if n in stats:
        stats[n] += 1
    else:
        stats[n] = 1
    stats["data"].append(n)


def PrintHistogram(numbers):
    # numbers is a dict of the form
    # {
    #   "data": [list of word lengths from file],
    #   1: count,       # Count of words of length 1
    #   2: count,       # Count of words of length 2
    #   ...
    # }
    wordlengths = numbers["data"]
    wordlengths.sort()
    del numbers["data"]  # Now all keys are integers
    n = len(wordlengths)
    if n < 3:
        print("  Not enough words in file")
        return
    largest_count = max(numbers.values())
    print("  Len   Count Percent")
    for i in range(1, 1 + max(numbers.keys())):
        value = numbers.get(i, 0)
        frac = flt(value / n)
        print(f"  {i:2d} {value:9d} {100 * frac:^8.3g}", end=" ")
        # Print a bar if we have room
        room = columns - 23
        bar_length = int(value / largest_count * room)
        if room > 5:
            print("*" * bar_length, end="")
        print()
    mean = flt(sum(wordlengths) / n)
    Min, Max = min(wordlengths), max(wordlengths)
    sx = flt(sum(wordlengths))
    sxx = flt(sum([i * i for i in wordlengths]))
    s = ((sxx - n * mean**2) / (n - 1)) ** 0.5
    A = (n - 1) // 2
    median = (
        flt((wordlengths[A] + wordlengths[A + 1]) / 2)
        if not (n % 2)
        else flt(wordlengths[A])
    )
    print(
        dedent(
            f"""
      Total words           = {n}
      Mean word length      = {mean}
      Word length std dev   = {s}
      Median word length    = {median}
      Range of word lengths = [{Min}, {Max}]
    """,
            n=4,
        )
    )
    if big_words:
        w = list(big_words)
        w.sort()
        print("Big words:" + nl)
        for word in w:
            print("  %s" % word + nl)


def PrintSummary(details):
    for file in details:
        print(f"{file}:")
        PrintHistogram(details[file])


def ProcessWord(word, stats):
    "Put histogram information into the dictionary stats"
    n = len(word)
    if ignore_length is not None and n >= ignore_length:
        return
    if big_word_length is not None and n >= big_word_length:
        global big_words
        big_words.add(word)
    if n in stats:
        stats[n] += 1
    else:
        stats[n] = 1
    stats["data"].append(n)


def ProcessFile(file, stream, details):
    """Read each word from the stream and cache its characteristics in the
    dictionary details.
    """
    if file in details:
        print(f"'{file}' given more than once on command line", file=sys.stderr)
        return
    details[file] = {"data": []}
    stats = details[file]
    for word in GetWord(stream):
        ProcessWord(word, stats)


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    details = {}
    for file in files:
        try:
            if file == "-":
                stream = sys.stdin
                file = "stdin"
            else:
                stream = open(file)
        except Exception:
            print(f"'{file}' cannot be read", file=sys.stderr)
        else:
            ProcessFile(file, stream, details)
    PrintSummary(details)
