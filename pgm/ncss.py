'''
Counts lines of non-commented source code for C and C++
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2002 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Count lines of non-commented C/C++ source code
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import re
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from f import flt
if 1:   # Global variables
    class g: pass
    g.start_C_comment = re.compile("^.*(/\*.*$)")
    g.end_C_comment = re.compile("^(.*\*/).*$")
    g.one_line_C_comment = re.compile(".*(/\*.*\*/).*$")
    g.cpp_comment = re.compile(".*(//.*$)")
    g.total_lines = 0
def Usage():
    print(dedent(f'''
    Usage:  {sys.argv[0]} source_file1 [source_file2 ...]
      Counts lines of non-commented source code for C and C++.  Strips out
      comments, then counts non-empty lines.  Prints a report to stdout.
    '''))
    exit(1)
def RemoveCComments(lines):
    '''Any comments extending over multiple lines will be replaced with
    blank lines to maintain line numbering.
    '''
    in_comment = 0
    for i in range(len(lines)):
        if in_comment:
            mo = g.end_C_comment.match(lines[i])
            if mo:
                in_comment = 0
                lines[i] = lines[i].replace(mo.group(1), "")
                continue
            lines[i] = ""
        else:
            mo = g.one_line_C_comment.match(lines[i])
            if mo:
                lines[i] = lines[i].replace(mo.group(1), "")
                continue
            mo = g.cpp_comment.match(lines[i])
            if mo:
                lines[i] = lines[i].replace(mo.group(1), "")
                continue
            mo = g.start_C_comment.match(lines[i])
            if mo:
                in_comment = 1
                lines[i] = lines[i].replace(mo.group(1), "")
                continue
    return lines
def ProcessFile(file):
    try:
        lines = open(file).readlines()
    except Exception:
        print(f"Couldn't read '{file}'", file=sys.stderr)
        exit(1)
    RemoveCComments(lines)
    # Remove all blank lines.  We go backwards so as not to mess the
    # counter i up.
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if len(line) == 0:
            del lines[i]
    g.total_lines += len(lines)
    return len(lines)
if __name__ == "__main__":
    flt(0).n = 2
    if len(sys.argv) < 2:
        Usage()
    results = []
    for file in sys.argv[1:]:
        results.append((ProcessFile(file), file))
    print("  Lines  % of total   File")
    for lines, file in results:
        pct = flt(100*lines/g.total_lines)
        print(f"{lines:8d} {pct:6.1f} {file}")
    print(f"Total lines = {g.total_lines}")
