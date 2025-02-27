"""
Finds duplicate lines in one or more files
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2008 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Finds duplicate lines in one or more files
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
    import re
    import random
    from hashlib import sha256 as hash
    from math import log10 as log
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    out = sys.stdout.write
    nl = "\n"
    return_status = {
        "no duplicates": 0,
        "duplicates": 1,
        "bad command": 2,
    }
    # Set these to True if you want them enabled by default; False for off by
    # default.
    ignore_case = False
    ignore_whitespace = False
    ignore_blank_lines = True
    # Maps integer to file name on the command line
    filenames = {}
    # The matches dictionary will contain all the matches.  The format is:
    #   {
    #       processed_line: [original_line, (fn, ln), (fn, ln), ...],
    #       processed_line: [original_line, (fn, ln), (fn, ln), ...],
    #       ...
    #   }
    # There were duplicate lines for any list with 3 or more elements.
    # Processed lines are the lines that have been changed to comply with
    # the command line options.  For example, if ignore_case is on, the
    # processed string will be converted to all lower case.  If whitespace
    # is being ignored, all whitespace will have been removed from the
    # processed string.
    matches = {}
    # Compiled regular expressions we will ignore
    regular_expressions = []
    canned_expressions = {
        "float": re.compile(
            r"""
            [+-]?               # Optional sign
            \d*\.\d+            # Mandatory decimal point and following digit
            ([eE][+-]?\d+)?     # Optional exponent
            |                   # or
            [+-]?               # Optional sign
            \d+\.\d*            # Mandatory leading digits and decimal point
            ([eE][+-]?\d+)?     # Optional exponent
            |                   # or
            [+-]?               # Optional sign
            \d+                 # Leading digits, but no decimal point
            [eE][+-]?\d+        # Mandatory exponent
        """,
            re.VERBOSE,
        ),
        "integer": re.compile(r"[+-]?\d+(?!\.)"),
        "hex": re.compile(r"0x[\da-f]+", re.IGNORECASE),
    }
    whitespace = re.compile(r"\s+")


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {name} [options] file1 [file2...]
      Finds duplicate lines in one or more files.  Each duplicate line
      will be printed along with the file it occurs in and the line number.
     
      Options (default value in brackets; the option toggles this value):
          -b      Ignore blank lines [%(ignore_blank_lines)s]
          -i      Ignore case [%(ignore_case)s]
          -r re   Ignore the python regular expression re.  More than one
                  -r option is allowed.
          -R ex   Ignore some common expressions.  The string ex can have the
                  following values:
                     float     Floating point numbers
                     integer   Integers
                     hex       Hex numbers that begin with 0x
                  Note that an integer followed by a '.' at the end of a sentence
                  will be considered a floating point number, not an integer.
          -t n    Generate n files for testing.  There are 1e4 lines in each
                  file and the first line is the same as the last.
          -w      Ignore whitespace [%(ignore_whitespace)s]
    """)
    )
    exit(status)


def Test(number_of_files=100):
    """Generate lots of files with lots of lines.

    29Mar2008 (dual Celeron process running XP):  generated 100 files with
    1e4 lines each.  Made the last line of the last file the same as the
    first line.  It took 30 seconds for this script to find and print the
    duplicates.  That's 33 klines/sec.  Changing the script's hash to MD5
    knocked 1 second off that time.  Using sha512 added 5 seconds.  sha256
    seems like a good compromise.

    Note:  I changed from using a hash from hashlib to just putting the
    text string itself in the dictionary.  This took 5 seconds less and
    should guarantee there won't be any collisions.

    24Apr2011 (quad core Intel processor running XP):  Took 10.8 s to find
    the duplicates for 100 files for 92 klines/s (note these lines were
    probably cached, so that's not a realistic number).

    3Jul2021 (quad core processor running cygwin under Windows 10 with
    python 3.7.10):  took 2.7 s for 100 files produced with 'dupfiles -t
    100'.
    """
    random.seed()
    digits = int(log(number_of_files) - 1e-9) + 1
    number_of_lines = 10000

    def FillFile(file):
        f = open(file, "w")
        for i in range(number_of_lines - 1):
            r = random.random()
            s = hash(f"{r:.15f}".encode())
            line = s.hexdigest() + "\n"
            if i == 0:
                firstline = line
            f.write(line)
        f.write(firstline)

    for i in range(number_of_files):
        FillFile(f"dupfiles.test.{i}")
    exit(0)


def ParseCommandLine():
    global regular_expressions
    global ignore_blank_lines
    global ignore_case
    global ignore_whitespace
    if len(sys.argv) < 2:
        Usage()
    try:
        optlist, files = getopt.getopt(sys.argv[1:], "bir:R:t:w")
    except getopt.error as str:
        print(str)
        exit(return_status["bad command"])
    for o, a in optlist:
        if o == "-b":
            ignore_blank_lines = not ignore_blank_lines
        elif o == "-i":
            ignore_case = not ignore_case
        elif o == "-r":
            regular_expressions.append(re.compile(a))
        elif o == "-R":
            try:
                regular_expressions.append(canned_expressions[a])
            except KeyError:
                Error("'{a}' is not a recognized expression for -R")
        elif o == "-t":
            Test(int(a))
        elif o == "-w":
            ignore_whitespace = not ignore_whitespace
    if len(files) < 1:
        Usage()
    return files


def ProcessLine(line):
    """Transform the line to satisfy the constraints of the things that
    must be ignored.
    """
    if ignore_case:
        line = line.lower()
    if ignore_whitespace:
        line = whitespace.sub("", line)
    # Remove any text that matches the compiled regular expressions
    for expression in regular_expressions:
        line = expression.sub("", line)
    return line


def ProcessFile(file):
    """Add (file_number, line_number) pairs to the matches map for each
    line.
    """
    global matches
    global filenames
    lines = open(file).readlines()
    file_number = len(filenames)  # Index into filenames map
    filenames[file_number] = file
    for i in range(len(lines)):  # Process each line
        line_number = i + 1
        line = ProcessLine(lines[i][:-1])  # Strip trailing newline
        if ignore_blank_lines and line == "":
            continue
        if line in matches:
            # This is a duplicate line
            matches[line].append((file_number, line_number))
        else:
            # Not in map yet; create a new entry.  Note the string for
            # the original line is the first element.
            matches[line] = [lines[i][:-1], (file_number, line_number)]


def GetDetails(items):
    """Change from (file_number, line_number) pairs to a string of the
    form
        file1:  linenum1, linenum2, ...
        file2:  linenum1, linenum2, ...
        ...
    """
    data = {}
    for file_number, line_number in items:
        if file_number in data:
            data[file_number].append(line_number)
        else:
            data[file_number] = [line_number]
    files = [(i, data[i]) for i in data]
    files.sort()
    s = ""
    for file_number, line_numbers in files:
        s += "  %s: " % filenames[file_number]
        nums = ["%d" % i for i in line_numbers]
        s += " ".join(nums)
        s += nl
    return s


def PrintReport():
    data = []  # Build a structure that we can sort on the lines
    status = return_status["no duplicates"]
    for match in matches:
        item = matches[match]
        if len(item) > 2:
            status = return_status["duplicates"]
            line = item[0]
            if line.strip() == "":
                line = repr(line)  # Add apostrophes if all whitespace
            data.append((line, GetDetails(item[1:])))
    data.sort()  # Now output will be in terms of the sorted lines
    for line, info in data:
        print(line)
        print(info, end="")
    return status


if __name__ == "__main__":
    files = ParseCommandLine()
    for file in files:
        ProcessFile(file)
    status = PrintReport()
    exit(status)
