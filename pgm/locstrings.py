"""
Find and extract the localized strings from the files on the command line.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Find and extract i18n localization strings
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import re
    import getopt
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    r = re.compile(r'(_\(".*?"\))')
    # String counts for each file.  Each elements is (file, count).
    results = []
    # Keyed by file name.  Each value is a tuple of the strings found in order.
    strings = {}
    print_strings = False


def Usage():
    print(
        dedent(f"""
    Usage {sys.argv[0]} [-s] file1 [file2]
      Analyzes each file for localization strings '_("...")'.  Prints out a
      summary of the number of such strings in each file along with some
      statistics.  Use the -s option to print out each string found.
    """)
    )


def ParseCommandLine():
    if len(sys.argv) < 2:
        Usage()
        exit(1)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "hs")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-h":
            Usage()
            sys.exit(0)
        if opt[0] == "-s":
            global print_strings
            print_strings = True
    if len(args) < 1:
        Usage()
    return args


def ProcessLine(line, strings):
    done = False
    # print("line =", line)
    while not done:
        mo = r.search(line)
        if mo:
            # print("Found match; groups =", mo.groups())
            strings.append(mo.groups()[0])
            line = r.sub(" ", line, count=1)
            # print("Sub'd line is", line)
        else:
            done = True


def ProcessFile(file):
    lines = open(file).readlines()
    found_strings = []
    for line in lines:
        ProcessLine(line.strip(), found_strings)
    if found_strings:
        global strings
        strings[file] = found_strings
        global results
        results.append((file, len(found_strings)))


def Summary(file, list_of_strings):
    minlen = 10000
    maxlen = 0
    mean = 0
    for i in list_of_strings:
        n = len(i)
        if n < minlen:
            minlen = n
        if n > maxlen:
            maxlen = n
        mean += n
    s = "   %5.1f %6d %6d" % (mean / len(list_of_strings), maxlen, minlen)
    s += "    %s" % file
    return s


def PrintResults():
    if not len(results):
        print("No localization strings found")
        return
    print("Localization summary")
    print("--------------------")
    print("  Num strings   File")
    h = "  -----------   ---------------------------------"
    print(h)
    total = 0
    for file, count in results:
        print("%8d        %s" % (count, file))
        total += count
    print(h)
    print("%8d        %s" % (total, "TOTAL"))
    # Print detailed stats
    print("\nDetails:")
    print("    mean  maxlen  minlen  File")
    print("    ----  ------  ------  ---------------------------------")
    for file, count in results:
        print(Summary(file, strings[file]))
    if print_strings:  # Print actual strings
        for i in strings:
            print()
            print(i)
            for s in strings[i]:
                print("  ", s)


if __name__ == "__main__":
    for file in ParseCommandLine():
        ProcessFile(file)
    PrintResults()
