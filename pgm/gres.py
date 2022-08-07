'''
This script is similar to the MKS gres command that was typical on MKS
CDs in the early 1990's.  However, instead of using grep-type regular
expressions, it's aimed at replacing symbol tokens in programming files.
Each file on the command line will first be copied to a backup version
with a tilde appended to the filename.  Then the files will be
transformed using the symbol transformation(s) indicated.
 
The two typical uses are:
 
    gres.py old_sym new_sym file1 [file2...]
    gres.py -@ symfile file1 [file2...]
 
The second form allows you to have multiple symbol replacements.
symfile must be a text file with two symbol tokens on each line
separated by whitespace.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Replace symbol tokens in programming text files.  Similar to the
    # MKS gres command.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import pathlib
    import os
    import re
if 1:   # Custom imports
    from wrap import dedent
def ParseCommandLine(d):
    d["-i"] = False     # Compile regexp with re.I
    d["-@"] = []        # Read regex's from file
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "@:i")
    except getopt.error as e:
        print(f"Option error:  {e}")
        exit(1)
    for o, a in optlist:
        if o[1] in list("i"):
            d[o] = not d[o]
        if o == "-@":
            d["-@"] = a
    if not args:
        Usage(d)
    return args
def Usage(d, status=1):
    name = sys.argv[0]
    r = d["backup_symbol"]
    print(dedent(f'''
    {name}  old_sym  new_sym  [file1  [file2...]]
      Replaces symbol tokens in programming text files.  The original
      files are copied to backup files with '{r}' added to the file
      name.  If the backup copy for any of the files exist, no
      substitutions or changes will be made.  
      
      If one of the files is '-', then the string is read from stdin and
      written to stdout.
    Options
      -i        Make substitutions case-insensitive
      -@ file   Read (old_sym, new_sym) pairs from file, one pair per line.
                Use '-' to read from stdin.
    '''))
    exit(status)
def ReadFile(file):
    if file == "-":
        lines = sys.stdin.readlines()
    else:
        try:
            lines = open(file).readlines()
        except Exception:
            print(f"Could not read file '{file}'", file=sys.stderr)
            exit(1)
    return [line.rstrip("\n") for line in lines]
def ReadSubstitutions(d):
    'Read the substitutions to be made from the indicated file'
    for i, line in enumerate(ReadFile(d["-@"])):
        fields = line.split()
        if len(fields) != 2:
            raise ValueError(f"Symbol file has error on line {i + 1}")
        d["substitutions"].append(fields)
def ConstructRegexps(d):
    '''In the substitutions array, take each pair of symbols and
    construct a regular expression that will match the first expression
    when it is used as a programming symbol.  Put them into the global
    regexps list.
    '''
    for oldsym, newsym in d["substitutions"]:
        try:
            if d["-i"]:
                r = re.compile(r"\b" + oldsym + r"\b", re.I)
            else:
                r = re.compile(r"\b" + oldsym + r"\b")
            d["regexps"].append((r, newsym))
        except Exception:
            print(f"'{oldsym}' is an invalid regular expression")
            exit(1)
def CheckFiles(files, d):
    'Make sure no backup files exist'
    for file in files:
        f = file + d["backup_symbol"]
        p = pathlib.Path(f)
        if p.exists():
            print(f"Backup file {f} already exists.  Program stopped.",
                  file=sys.stderr)
            exit(1)
def ProcessFile(file, d):
    '''Read the file in and immediately write out an exact copy.
    Then overwrite the existing one with a new file with the
    substitutions made.
    '''
    if file == "-":
        s = sys.stdin.read()
        for regexp, newsym in d["regexps"]:
            s = regexp.sub(newsym, s)
        sys.stdout.write(s)
        return
    try:
        s = open(file, "r").read()
    except Exception:
        print(f"Couldn't read '{file}'")
        return
    try:
        newfile = file + d["backup_symbol"]
        open(newfile, "w").write(s)
    except Exception:
        print(f"Couldn't make backup copy '{newfile}'")
        return
    for regexp, newsym in d["regexps"]:
        s = regexp.sub(newsym, s)
    try:
        # Write out new file
        open(file, "w").write(s)
    except Exception:
        print(f"Couldn't write changed file '{file}'")
        return
if __name__ == "__main__":
    d = {   # Options dictionary
        "backup_symbol": "~",
        "regexps": [],
        "substitutions": [],
    }
    files = ParseCommandLine(d)
    if d["-@"]:
        if len(files) < 1:
            Usage(d)
        ReadSubstitutions(d)
    else:
        if len(files) < 3:
            Usage(d)
        d["substitutions"] = [(files[0], files[1])]
        files = files[2:]
    CheckFiles(files, d)
    ConstructRegexps(d)
    for file in files:
        ProcessFile(file, d)
