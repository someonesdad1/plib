if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Removes comments, includes, and blank lines from C/C++ files
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import string
    import re
    import os
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    start_C_comment = re.compile(r"^.*(/\*.*$)")
    end_C_comment = re.compile(r"^(.*\*/).*$")
    one_line_C_comment = re.compile(r".*(/\*.*\*/).*$")
    cpp_comment = re.compile(r".*(//.*$)")
    include = re.compile(r"^\s*#\s*include\s+.*$")


def Usage():
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} file1 [file2 ...]
      Removes comments, includes, and blank lines from C/C++ files and prints
      the resulting file to stdout.
    """)
    )
    exit(1)


def RemoveCComments(lines):
    # Any comments extending over multiple lines will be replaced with
    # blank lines to maintain line numbering.
    in_comment = 0
    for i in range(len(lines)):
        if in_comment:
            mo = end_C_comment.match(lines[i])
            if mo:
                in_comment = 0
                lines[i] = lines[i].replace(mo.group(1), "")
                continue
            lines[i] = ""
        else:
            mo = one_line_C_comment.match(lines[i])
            if mo:
                lines[i] = lines[i].replace(mo.group(1), "")
                continue
            mo = cpp_comment.match(lines[i])
            if mo:
                lines[i] = lines[i].replace(mo.group(1), "")
                continue
            mo = start_C_comment.match(lines[i])
            if mo:
                in_comment = 1
                lines[i] = lines[i].replace(mo.group(1), "")
                continue
            mo = include.match(lines[i])
            if mo:
                lines[i] = "\n"
                continue
    return lines


def RemoveBlankLines(lines):
    return [i for i in lines if i.strip()]
    # Remove all blank lines.  We go backwards so as not to mess the
    # counter i up.
    if len(lines) == 0:
        return
    for i in range(len(lines) - 1, -1, -1):
        line = string.strip(lines[i])
        if len(line) == 0:
            del lines[i]
    return lines


def DumpLines(lines, msg):
    print(msg)
    for line in lines:
        print(line)
    print()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        Usage()
    sep = "-" * 60
    for file in sys.argv[1:]:
        print(sep)
        lines = [i.rstrip() for i in open(file).readlines()]
        lines = RemoveCComments(lines)
        lines = [i for i in lines if i.strip()]
        DumpLines(lines, "File = " + file)
