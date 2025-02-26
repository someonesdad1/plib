"""
Given two files of sha or md5 output (first token hash, second token
file name), compare the files and find any mismatches.
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
    # Compare two files with hash/file tokens to find differences
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    d = {}  # Options dictionary
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [-i] file1 file2
          Compares two files that contain two fields:
              1:  Hash of the file's data
              2:  The filename that was hashed
          Prints out any intersecting names that have different hashes
          and identifies files in one set but not in the other.
        Options
          -i    Ignore case in the file names
        """)
        )
        exit(status)

    def ParseCommandLine():
        d["-i"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hi")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("i"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        if len(args) != 2:
            Usage()
        return args


def ReadFile(file, ignore_case=False):
    "Return a dict of filename:hash pairs"
    lines = open(file).readlines()
    di = {}
    for line in lines:
        hash, name = line.split()
        if name[0] == "*":  # MD5 output includes asterisk
            name = name[1:]
        if d["-i"]:
            name = name.lower()
        if name in di:
            print(f"Collision for {file}:  {name}")
        else:
            di[name] = hash
    return di


def Compare(d1, d2):
    "Compare two dictionaries of hashes by keys"
    s1, s2 = set(d1), set(d2)
    common_keys = s1 & s2
    for key in common_keys:
        if key in d2:
            if d1[key] != d2[key]:
                print(f"{key}:")
                print("  ", d1[key])
                print("  ", d2[key])
    diff1 = s1 - s2
    diff2 = s2 - s1
    if diff1:
        print(f"Files in '{file1}' not in '{file2}':")
        for key in sorted(diff1):
            print(f"  {key}")
    if diff2:
        print(f"Files in '{file2}' not in '{file1}':")
        for key in sorted(diff2):
            print(f"  {key}")


if __name__ == "__main__":
    file1, file2 = ParseCommandLine()
    d1 = ReadFile(file1)
    d2 = ReadFile(file2)
    Compare(d1, d2)
