'''
TODO

* Rewrite to use the trigger.py functionality.  I'd like to see it only
  replace the license portion with a short header statement.

* For each file, check that the trigger string only matches in two
  places.

* Write another script that lets you change the trigger string in all
  files on the command line with args 'old_trigger new_trigger files'.

----------------------------------------------------------------------
Replace license statements in files.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014, 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <utility> Replace license statements in files
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from pdb import set_trace as xx
    import getopt
    import os
    import pathlib
    import re
    import shutil
    import sys
    import time
if 1:   # Custom imports
    import color as C
    from wrap import dedent
    from license_data import licenses
if 1:   # Global variables
    P = pathlib.Path
    # Trigger string for replacements
    trigger = "#∞#"
    # Regexp used to identify the string to be replaced
    regexp = re.compile(r"%s(.*?)%s" % (trigger, trigger), re.S)
    # The following are too short to warrant a separate header file
    short_choices = ("bsd", "mit", "pd", "wol", "rem")
    backup_extension = ".bak"
    nl = "\n"
    descr = {
        "rem":     "  Remove any existing license text",
        "afl3":    "  Academic Free License 3.0",
        "apache2": "  Apache License 2.0",
        "bsd3":    "  BSD 3-clause license",
        "ccsa4":   "* Creative Commons Attribution-ShareAlike 4.0",
        "gpl2":    "* GNU Public License version 2",
        "gpl3":    "* GNU Public License version 3",
        "lgpl2":   "- Lesser GNU Public License version 2.1",
        "lgpl3":   "- Lesser GNU Public License version 3",
        "mit":     "  MIT License",
        "nposl3":  "* Non-Profit Open Software License 3.0",
        "osl3":    "* Open Software License 3.0",
        "pd":      "  Public domain release",
        "wol":     "  Wide-open License",
    }
    analysis = None
def eprint(*p, **kw):
    'Print to stderr'
    print(*p, **kw, file=sys.stderr)
def Error(msg, status=1):
    eprint(msg)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    choices = sorted(descr.keys())
    lic, fmt = [], "    %-8s %s"
    lic = nl.join(lic)
    bak = backup_extension
    cmnt = d["-c"]
    print(dedent(f'''
    Usage:  {name} [options] [license [file1 [file2...]]]
      Replace the license header in source code files.   Short licenses
      like BSD include the whole of the license text instead of a
      header.  The replacement is made between the first two lines that
      begin with a trigger string defined in the code.
    
      The license argument must be one of the strings (* = copyleft,
      - = non-strong copyleft):
    '''))
    for i in choices:
        print(f"    {i:8s} {descr[i]}")
    print()
    print(dedent(f'''
      Each source code file will be copied to a backup file with the
      appended extension "{bak}".  The script will first examine all the
      files to ensure they have the trigger string; if not, the program
      will exit with an error message and not change any of the files.
      Next, all of the backup files will then be constructed.  Finally,
      each of the files is processed.  Thus, if the script completes
      without an error message, all the substitutions were successful.
    
      If you only include the license string on the command line, the
      license's text is printed to stdout.
    
    Options:
      -a      Print my thoughts on licenses
      -c s    Change the comment string used for prepending to each
              source file's lines.  Default is '{cmnt}'.
      -n      Show which files don't have the requisite header
      -s      Substitute the license for the header
      -t s    Change the trigger string to s
    '''))
    exit(status)
def ParseCommandLine(d):
    global trigger
    d["-c"] = "# "      # Comment prepend string
    d["-f"] = False     # Force overwriting of backup files
    d["-n"] = False     # Show which files don't have header
    d["-s"] = False     # Substitute license text
    d["-t"] = trigger   # Trigger string
    d["missing"] = []
    # Get the analysis text, in the licenses subdirectory
    d["dir"] = GetDir()
    global analysis
    file = P("/pylib/licenses/analysis")
    analysis = file.read_text().strip()
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "ac:fnst:")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-a":
            print(analysis)
            exit(0)
        if opt[0] == "-c":
            d["-c"] = opt[1]
        if opt[0] == "-f":
            d["-f"] = True
        if opt[0] == "-n":
            d["-n"] = True
        if opt[0] == "-s":
            d["-s"] = True
        if opt[0] == "-t":
            trigger = d["-t"] = opt[1]
    if len(args) < 1:
        # Need choice and at least one file
        Usage(d)
    return args
def GetDir():
    'Return the directory of the script'
    return pathlib.Path(sys.argv[0]).resolve().parent
def PrintLicense(choice):
    if choice not in licenses:
        Error(f"'{choice}' license not recognized")
    print(dedent(f'''
        <statement about program's intent>
        Copyright (C) {time.strftime("%Y")} Don Peterson
        gmail.com at someonesdad1
    '''))
    print()
    print(licenses[choice].text)
def CheckFiles(files, d):
    '''For each file in files, ensure that it is readable and has the
    requisite string for substitution.
    '''
    bad, se = False, sys.stderr
    for file in files:
        p = P(file)
        if not p.isfile():
            eprint(f"'{file}' is not a file")
            bad = True
            continue
        try:
            s = p.read_text()
        except Exception:
            eprint(f"Could not read '{file}'")
            bad = True
            continue
        mo = regexp.search(s)
        if not mo:
            eprint(f"'{file}' does not have the trigger string '{trigger}'")
            bad = True
            continue
    if bad:
        if not d["-n"]:
            C.fg(C.lred)
            eprint("Cannot continue because of the above problems")
            C.normal()
        exit(1)
def MakeBackups(files, d):
    'For each file in files, make a backup file'
    for file in files:
        bu = P(file)/backup_extension
        if bu.exists() and not d["-f"]:
            eprint(dedent(f'''
            Backup file '{bu}' already exists
              Use the -f option to force overwriting of backup files.
            '''))
            exit(1)
        try:
            shutil.copyfile(file, bu)
        except Exception:
            eprint(f"Copy of '{file}' to '{bu}' failed")
            exit(1)
def ProcessFile(choice, file, d):
    if d["-s"] and choice not in short_choices:
        # Use license text rather than header
        s = licenses[choice]
    else:
        s = headers[choice]
    # Prepend comment string d["-c"] to each line.  Remember s is a
    # tuple of (short descr, license header).
    if choice is "rem":
        lines = s[1].split(nl)
    else:
        lines = [d["-c"] + i for i in s[1].split(nl)]
    try:
        u = "" if choice == "rem" else (nl.join(lines) + nl)
        t = "%s\n%s%s" % (trigger, u, trigger)
        s = open(file).read()
        open(file, "w").write(regexp.sub(t, s))
    except Exception as e:
        C.fg(C.lred)
        print('''File '%s' couldn't be changed
  '%s'
''' % (file, e))
        C.normal()
def ChangeFiles(choice, files, d):
    for file in files:
        ProcessFile(choice, file, d)
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    choice, files = args[0], args[1:]
    if not files:
        PrintLicense(choice)
    else:
        CheckFiles(files, d)
        if not d["-n"]:
            MakeBackups(files, d)
            ChangeFiles(choice, files, d)
