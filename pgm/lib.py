__doc__ = '''
    Usage:  {name} [options] [name1 [name2...]]
      Tool to keep track of short snippets of code.  Prints to stdout the
      routines with the given names.  Enter no parameter to see an index of
      the routines in the data file (lib.dat in the same directory as the
      script by default).
    Data file structure:
      Separated into records by '{S}', which must be on its own line
      (arbitrary following characters allowed to end of line).  The first
      line after the separator is the name of the record and its category.
      The field separator is ';'.  The optional third field can be the
      language.  If there is a fourth field, it means this record should
      be ignored.  The following line must be a one-line description of
      the record for the printing of the index (call this script with no
      arguments).  The remaining lines to the next record separator are
      free-form.
    To try the script:
      Run it with the -c option and save the output in sample.data.  Then
      run the script as '{name} -f sample.data' and you should see an index
      listing of the topics in the datafile.  Run '{name} routine1' to get
      the snippet of code indexed by 'routine1'.
    Options:
      -c   Dump a template data file.
      -e   Edit the data file.
      -f   Specify an alternative data file.
      -l   Dump record names to stdout.
      -h   Show this help.
    '''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2005, 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Tool to keep track of code snippets
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import string
    import getopt
    import os
    import re
    from collections import defaultdict
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    # We'll try to import the color module to highlight the utilities by
    # their language.
    have_color = False
    try:
        import color as c
        have_color = True
    except ImportError:
        class C:    # Dummy object that will swallow calls to the color module
            def __setattr__(self, attr, x):
                pass
            def __getattr__(self, attr):
                return None
            def fg(self, *p):
                pass
            def normal(self):
                pass
        c = C()
if 1:   # Global variables
    sep = "@@"          # Separates datafile records
    nl = "\n"
    ff = "\n\x0c\n"      # Separates output records
    # Define colors for language types.  Languages not in this list won't
    # be highlighted.
    language_colors = {  # Color, name to display
        #"algorithm": ((c.lwhite, c.lblue), "Algorithm"),
        #"awk": (c.red, "awk"),
        "c": (c.yellow, "C"),
        #"c++": (c.lred, "C++"),
        #"java": (c.cyan, "Java"),
        "normal": ((c.white, c.black), ""),
        #"perl": (c.magenta, "Perl"),
        "python": (c.lcyan, "python"),
        "sh": (c.lgreen, "sh"),
        "text": (c.white, "text"),
    }
class Record(object):
    '''Holds the data from one record.
    '''
    def __init__(self):
        self.name = None
        self.category = None
        self.description = None
        self.lines = None
        self.language = None
        self.ignore = False
    def __cmp__(self, other):
        return self.name < other.name
def Error(msg):
    sys.stderr.write(msg + nl)
    sys.exit(1)
def Usage(d, status=1):
    name = d["name"]
    S = sep
    print(dedent(__doc__.format(**locals())))
    exit(status)
def DumpTemplateFile(d):
    print(dedent(f'''
    routine_name ; category ; language(optional)
    Put the one-line description on the second line
    The following lines are for the snippet's code
    ...
    @@
    findbaz ; utility
    Find the baz in a foo
    Line 1 for routine2's code
    Line 2 for routine2's code
    ...
    '''))
    exit(0)
def GetOptions(d):
    d["-l"] = False     # List record names
    # Get our default data file
    name, ext = os.path.splitext(d["name"])
    file = os.path.join(d["dir"], name + ".dat")
    d["-f"] = file.replace("\\", "/")   # Data file
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "cef:hl")
    except getopt.error as str:
        print("getopt error:  %s" % str)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-c":
            DumpTemplateFile(d)
        if opt[0] == "-e":
            # Edit the data file
            v = os.environ["EDITOR"]
            cmd = v + " " + d["-f"]
            print("command = ", repr(cmd))
            os.system(cmd)
            sys.exit(0)
        if opt[0] == "-f":
            d["-f"] = opt[1]
            if not os.path.isfile(d["-f"]):
                Error("'%s' isn't a readable file" % d["-f"])
        if opt[0] == "-h":
            Usage(d, status=0)
        if opt[0] == "-l":
            d["-l"] = True
    return args
def ReadDataFile(d):
    '''Read in the data file indicated in d["-f"].  Parse it into
    records and return a dictionary of records keyed by the names.
    '''
    # Build a regular expression to split the datafile into records.
    # This lets us use '@@' for the record separator, but you can
    # include e.g. a bunch of hyphens after it to the end of the line
    # to make it easier to visually separate records in your editor.
    t = "^%s.*$" % sep
    r = re.compile("\n%s.*\n" % sep)
    # Now read in and process the datafile
    s, records = open(d["-f"]).read(), {}
    for record in r.split(s):
        lines = record.strip().split(nl)
        # Must have at least three lines:
        # Line 0 is record name followed by optional category
        # Line 1 is one-line short description of record
        # Remainder is record's text
        if len(lines) < 3:
            Error("Not enough lines in record '%s'" % lines[0])
        # Process first line
        fields = [i.strip() for i in lines[0].split(";")]
        if len(fields) < 2:
            Error("Empty first record in record '%s'" % lines[0])
        record = Record()
        record.name = fields[0]
        record.category = fields[1]
        if len(fields) > 2:
            record.language = fields[2].lower()
        # If there was a fourth field, ignore this entry
        if len(fields) > 3:
            record.ignore = True
        record.description = lines[1]
        record.lines = lines[2:]
        if record.name in records:
            Error("'%s' used more than once for a record name" % record.name)
        records[record.name] = record
    return records
def DumpRecordNames(records, d):
    names = list(records.keys())
    names.sort()
    print("Record names in datafile '%s':" % d["-f"])
    for name in names:
        ignored = " (ignored)" if records[name].ignore else ""
        print(" "*4 + name + ignored)
    exit(0)
def ShowContents(records, d):
    '''records is a dictionary containing entries of the form:
        'name' : (category, description, lines, language)
    where name, category, description, and language are strings and
    lines is a sequence of strings.
    '''
    if have_color:
        # print the language names in their colors
        L = list(language_colors.keys())
        L.sort()
        for language in L:
            if language == "normal":
                continue
            else:
                color, name = language_colors[language]
                c.fg(color)
                print(name, end=" ")
                c.normal()
                print(" ")
        print()
    # Get maximum name length
    maxlen = max([len(name) for name in records])
    # Create a dictionary keyed by categories so we can list by
    # categories.
    by_category = defaultdict(list)
    for name in records:
        r = records[name]
        if not r.ignore:
            by_category[r.category].append(r)
    categories = list(by_category.keys())
    categories.sort()
    # List the contents by category
    fmt = "  %-*s %s%s"
    for category in categories:
        print("%s" % category)
        category_records = sorted(by_category[category], key=lambda x: x.name)
        for r in category_records:
            if have_color:
                try:
                    lang_color, lang_name = language_colors[r.language]
                except KeyError:
                    s = ["Language '%s' doesn't have an associated color"
                         % language]
                    s += ["  in record for '%s'" % r.name]
                    Error(nl.join(s))
                c.fg(lang_color)
                print("  %-*s " % (maxlen, r.name), end=" ")
                c.normal()
                print("%s" % r.description)
            else:
                print("  %-*s " % (maxlen, r.name), end=" ")
                print("%s" % r.description)
def GetKey(key, records):
    '''Search for key as a beginning string of record names.  If not
    unique or can't be found, print error message and stop.  Return
    the unique string.
    '''
    found = []
    for name, record in records.items():
        if not record.ignore and name.startswith(key):
            if key == name:
                return name  # Perfect match
            found.append(record)
    if len(found) == 1:
        return found[0].name
    else:
        if not found:
            Error("No matches for '%s'" % key)
        else:
            msg = ["Too many matches:"]
            msg += ["  " + i.name for i in found]
            Error("\n".join(msg))
if __name__ == "__main__": 
    d = {}
    d["dir"], d["name"] = os.path.split(sys.argv[0])
    args = GetOptions(d)
    records = ReadDataFile(d)
    if d["-l"]:
        DumpRecordNames(records, d)
    elif not args:
        # Show a listing of the entries
        ShowContents(records, d)
    else:
        # Show the requested records.  Each record entry in the
        # dictionary records is of the form (category, description,
        # sequence of text lines, language).
        output = []
        for key in args:
            Key = GetKey(key, records)
            if Key:
                output.append(nl.join(records[Key].lines))
        print(ff.join(output))
