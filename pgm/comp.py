'''
Search for text in the components database
'''
if 1:  # Data
    Todo = '''
    comp.py ToDo list
    
    - Boxes
        - Color code the box numbers
            - yel My existing plastic boxes
            - cyn The Plano box
            - orn Cardboard boxes devoted to e.g. MPJA or Proto Supply parts
    - Inventory
        - Quantities
        - Symbols:  M = many, F = few, * = few or none and need to order
    - Data structure
        - Data lines with two nonbreaking spaces to give 3 fields
            - Box, compartment, etc. data
            - Description
            - Keywords
        - Code can find missing lines by compartment numbering interruptions
    - Plano box
        - Use for Arduino/prototyping stuff
        - Move things around to get this
        - Put spares of multiples in a cardboard box on the rolling cart
            - Spares have box:compartment pointer in their description
    - Look at getting some locking heavy duty plastic boxes for storage that will stack in a
      compact fashion
    '''
if 1:  # Header
    if 1:  # Imports
        from collections import defaultdict
        from functools import cmp_to_key
        from pprint import pprint as pp
        import csv
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:  # Custom imports
        from columnize import Columnize
        from wrap import dedent
        import dpseq
        import trm
        t = trm.TrmDP()
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        beginning_lines_to_ignore = 3
        box_data = None
if 1:  # Classes
    class Entry:
        def __init__(self, line_number, info, description, keywords):
            '''Attributes:
            line_number     i Line number in data string
            box             i Box number
            compartment     i Compartment number
            quantity        s Count, M for many, * for 0 or needs ordering, ? for unknown
            description     s Item's description
            keywords        l List of keywords
            start           i Start of regex match
            end             i End of regex match
            empty           b If description string is empty
            '''
            self.line_number = line_number  # 1-based number
            # info will be two integers and a string separated by colons
            self.box, self.compartment, self.quantity = info.split(":")
            self.box = int(self.box)
            self.compartment = int(self.compartment)
            self.description = description.strip()
            self.keywords = keywords.strip().split()
            # Attributes to indicate a regex match in the self.description string
            self.start = None
            self.end = None
            # Other attributes
            self.empty = True if not self.description else False
        def __str__(self):
            k = "/".join(self.keywords)
            i = " " * 1
            s = f"{t.box}{self.box:2d}:{t.compartment}{self.compartment:2d}:"
            q = "" if self.quantity == "?" else str(self.quantity)
            s += f"{t.quantity}{q:3s}{t.n}{i}{self.description}"
            # s = f"{t.box}{self.box:2d}:{t.compartment}{self.compartment:2d}{t.n}{i}{self.description}"
            if k:
                s += f" {t.keyword}[{k}]{t.n}"
            return s
        def __repr__(self):
            return str(self)
        def __lt__(self, other):
            '''Comparison for sorting.  The primary key is the box number and the secondary key is
            the compartment number.
            '''
            if int(self.box) < int(other.box):
                return True
            elif int(self.box) > int(other.box):
                return False
            else:
                return int(self.compartment) < int(other.compartment)
if 1:  # Utility
    def Error(*msg, status=1):
        print(f"{t.err}", end="")
        print(*msg, end="")
        print(f"{t.n}")
        exit(status)
    def SetColors(on=True):
        # Colors
        t.match = t("royl") if on else ""
        t.box = t("yel") if on else ""
        t.compartment = t("grn") if on else ""
        t.quantity = t("viol") if on else ""
        t.keyword = t("gry") if on else ""
        t.warn = t("orn") if on else ""  # Color for a missing category warning
        t.err = t("red") if on else "" 
    def Usage(status=0):
        print(dedent(f'''
            {sys.argv[0]} [options] [regex [regex2...]]
                Searches the components database for the indicated regular expressions AND'd
                together.  The search is case-insensitive.  Prefix a regex with '-' and anything
                that matches this with the '-' removed will not appear in the output.  The numbers
                separated by ':' are:  box, compartment, quantity.  Quantity is not shown unless
                it is known (i.e., not '?' in the data).
            Single letter commands
                a   Dump all records
                b n Show contents of box number n
                d   Inspect the data, showing problem areas
                D   Dump raw data to stdout
                e   Edit the source file
                k, l  List keywords
                m   Show empty compartments
                n   Show box numbers in use
                t   Dump the todo list
                v   Print out color code and numbering key
            Example
                python '{sys.argv[0]}' diode -zener
                    shows diodes that don't contain 'zener'.
            Options
                -a        Dump all records
                -b N      Show contents of box number N
                -C        Do not use color highlighting
                -c        Show category
                -D        Dump the raw data to stdout
                -d        Inspect the data, looking for problems
                -e        Show empty compartments
                -i        Do not ignore case in searches
                -k kwd    Show items with keyword kwd (not case-sensitive)
                -l        List the keywords
                -o        OR the regexes instead of AND
                -t        Dump the ToDo list
                -v        Print out color code and numbering key 
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False  # Dump all records
        d["-b"] = None   # Specifies box number to list
        d["-C"] = False  # Turn off color highlighting
        d["-c"] = False  # Show category
        d["-d"] = False  # Inspection
        d["-e"] = False  # Show empty compartments
        d["-i"] = True   # Ignore case
        d["-k"] = ""     # Show this keyword
        d["-l"] = False  # List the keywords
        d["-o"] = False  # OR the regexes on the command line
        d["-t"] = False  # Print the ToDo list
        d["-v"] = False  # Print color coding & numbering key
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "ab:CcDdehik:lotv")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        if len(sys.argv) < 2:
            Usage()
        GetBoxData()
        for o, a in optlist:
            if o[1] in "aCcdeilotv":
                d[o] = not d[o]
            elif o in ("-b",):
                d["-b"] = int(a)
            elif o in ("-D",):
                print(box_data)
                exit(0)
            elif o in ("-h",):
                Usage()
            elif o in ("-k",):
                d["-k"] = a
            elif o in ("-m",):
                ShowEmptyCompartments()
            elif o in ("-n",):
                ShowBoxNumbersInUse()
        SetColors(False) if d["-C"] else SetColors()
        return args
if 1:  # Core functionality
    def GetBoxData():
        'Fill the global box_data with the data lines'
        global box_data
        with open("/plib/pgm/comp.txt", "r") as f:
            box_data = f.read()
    def PrintToDo():
        print(dedent(Todo))
    def EditDataFile(box_number=""):
        'Edit the data file'
        file = "/plib/pgm/comp.txt"
        if box_number:
            cmd = ["vi", f"-c /Box {box_number}", file]
            #print(cmd)
            subprocess.call(cmd)
        else:
            subprocess.call(["vi", file])
    def GetData():
        "Return a list of Entry items"
        items = []
        # This regex should find lines beginning with two integers, each with a colon after
        # them, then a string.
        r = re.compile(r"^(\s*\d+\s*:\s*\d+\s*:)")
        for i, line in enumerate(box_data.split("\n")):
            line = line.strip()
            mo = r.search(line)
            if mo:
                if 0:  # Show the line
                    t.print(f"{t.magl}{line}")
                f = line.split()
                if len(f) == 1:
                    # Empty line after matched location stuff
                    e = Entry(i + 1, f[0], "", "")
                else:
                    location, remainder = line.split(" ", 1)
                    # location is of the form 'n:m:s' where n and m are integers and s is a
                    # string.  remainder is the description followed by a non-breaking space,
                    # followed by optional keyword(s).
                    separator = "🟦"  # Large blue square U+1F7E6
                    if separator in remainder:  # Has one or more keywords
                        description, keywords = remainder.split(separator)
                    else:  # Has no keywords
                        description = remainder.strip()
                        keywords = ""
                    e = Entry(i + 1, location, description, keywords)
                items.append(e)
        if 0:  # Debug dump items
            t.print(f"{t.orn}Debug dump of items:")
            for i in items:
                print(i)
            exit(0)
        items = list(sorted(items))
        if not items:
            print(f"{t.orn}items is empty")
            exit()
        return items
    def TextSearch(args, items):
        '''found will hold the Entry items that matched; pos holds the start and
        end position of the first match and is keyed by the line.
        
        args        List of regexes to search for
        items       List of Entry instances; when printed, an Entry will result in a string like
                    "1:1 Component pins".
        '''
        if 1:  # regexps is a list of the regular expressions made from args
            regexps = []
            remove = []  # Hold those that begin with "-"
            for i in args:
                i = i.strip()
                if not i:
                    continue
                if i.startswith("-"):
                    remove.append(i[1:])
                else:
                    regexps.append(re.compile(i, re.I) if d["-i"] else re.compile(i))
        if 1:  # Search all the items (Entry instances) for regex matches in their descr attribute
            found = []  # List containing the Entry instances that had a regex match
            if d["-o"]:  # OR the regexes
                for i in items:
                    s = i.description
                    for r in regexps:
                        mo = r.search(s)
                        if mo:
                            i.start, i.end = mo.start(), mo.end()
                            found.append(i)
                            break
            else:  # AND the regexes
                for i in items:
                    s = i.description
                    matched_all = True  # Assume we'll match all
                    # Since this is reversed, the only regex that will be color-coded is the first
                    for r in reversed(regexps):
                        mo = r.search(s)
                        if mo:
                            i.start, i.end = mo.start(), mo.end()
                        else:
                            matched_all = False
                    if matched_all:
                        found.append(i)
        if 1 and remove:  # Remove any specified regexes
            keep = []
            # Compile the regexes
            remove = [
                re.compile(regex, re.I) if d["-i"] else re.compile(regex)
                for regex in remove
            ]
            for item in found:
                not_found = True
                for r in remove:
                    if r.search(item.description):
                        # Had a match, so ignore this item
                        not_found = False
                        break
                if not_found:
                    keep.append(item)
            found = keep
        if 1:  # Print results
            # We can't just print the string of the Entry because we want to highlight the search
            # match in the description
            for item in sorted(found):
                # Box, compartment, quantity.  If quantity is ?, meaning it hasn't been
                # inventoried, then print it in black so that it won't be visible.
                q = t.blk if item.quantity == "?" else t.quantity
                print(
                    f"{t.box}{item.box:>2d}:"
                    f"{t.compartment}{item.compartment:>2d}:"
                    f"{q}{item.quantity:3s}{t.n}",
                    end="",
                )
                # Description
                if 1:
                    print(
                        "", end=" " * 1
                    )  # Spacing between box:compartment and description
                    s = item.description
                    print(s[: item.start], end="")
                    # Colorized match
                    print(f"{t.match}{s[item.start : item.end]}{t.n}", end="")
                    # Remainder
                    print(s[item.end :], end="")
                # Keywords
                k = "/".join(item.keywords)
                print(f" {t.keyword}[{k}]{t.n}") if k else print()
            if found:
                PrintColorCoding()
    def PrintColorCoding(qty=True):
        if not d["-v"]:
            return
        if not d["-C"]:
            t.print(
                f"Color coding:  {t.box}box "
                f"{t.compartment}compartment "
                f"{t.quantity}quantity "
                f"{t.keyword}keyword")
        # Quantity coding
        if qty:
            print(dedent('''
                Letters for quantity:
                    ?   Not inventoried yet
                    f   A few
                    m   Too many to count
            '''))
    def Keywords(items):
        "Returns a set of the keywords"
        kw = []
        for item in items:
            kw.extend(item.keywords)
        return set(kw)
    def Inspection():
        '''Look for problems in the data:
        - No keyword
        - Misspelled (not important yet)
        - Needs inventory taken
        '''
        # No keyword
        if 1:
            no_kwd = []
            for item in items:
                if item.empty:
                    continue
                if not item.keywords:
                    no_kwd.append(item)
            if no_kwd:
                t.print(f"{t.orn}Items with no keyword:")
                for item in no_kwd:
                    print(item)
        # Need inventory:  print boxes that still need their parts counted
        if 1:
            needs_counting = defaultdict(int)  # key: box, value: number of ?
            box = 0
            for item in items:
                if item.box != box:
                    box = item.box
                if item.quantity == "?":
                    needs_counting[box] += 1
            if needs_counting:
                o = []
                t.print(f"{t.orn}Box:(number of compartments) that still need parts counting:")
                for box in needs_counting:
                    o.append(f"{box:2d}: ({needs_counting[box]})")
                for i in Columnize(o, columns=5, sep=" " * 5):
                    print(i)
    def PrintKeywords():
        # Put each keyword into a dict with its count
        KW = defaultdict(int)
        for item in items:
            for kw in item.keywords:
                KW[kw] += 1
        # Get maximum count
        max_count = max(KW.values())
        w = len(str(max_count))  # Needed printing width
        # Print sorted alphabetically
        o, o1, max_count = [], [], 0
        #t.print(f"{t.orn}Keywords sorted alphabetically (number is count):")
        t.print(f"{t.orn}Keywords sorted alphabetically:")
        for name in sorted(KW, key=str.lower):
            count = KW[name]
            #o.append(f"{count:{w}d} {name}")
            o.append(f"{name}")
            o1.append((count, name))
        for item in Columnize(o):
            print(item)
        # Print sorted numerically
        t.print(f"\n{t.orn}Keywords sorted by count:")
        o = []
        for count, name in sorted(o1):
            o.append(f"{count:{w}d} {name}")
        for item in Columnize(o):
            print(item)
    def ShowEmptyCompartments():
        u = defaultdict(list)
        for item in items:
            if item.empty:
                u[item.box].append(item.compartment)
        t.print(f"{t.orn}Empty compartments:")
        for i in u:
            b = list(sorted(set(u[i])))
            t.print(f"{t.box}{i:2d}: {t.compartment}{' '.join(str(j) for j in b)}")
    def ShowBoxNumbersInUse():
        o = []
        for line in data.split("\n"):
            line = line.strip()
            if not line.startswith("Box "):
                continue
            num = int(line.split()[1])
            o.append(num)
        print("Box numbers in use: ", dpseq.Hyphenate(o))

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if args and len(args[0]) == 1:   # One letter command
        allowed, letter = "abdDeklmntv", args[0]
        if letter in allowed:
            if letter == "a":
                d["-a"] = True
            elif letter == "b":
                try:
                    d["-b"] = args[1]
                except Exception:
                    Error("Need box number")
            elif letter == "d":
                d["-d"] = True
            elif letter == "D":
                print(data)
                exit(0)
            elif letter == "e":
                if len(args) > 1:
                    EditDataFile(args[1])
                else:
                    EditDataFile()
                exit(0)
            elif letter in "kl":
                d["-l"] = True
            elif letter == "m":
                d["-e"] = True
            elif letter == "n":
                ShowBoxNumbersInUse()
                exit(0)
            elif letter == "t":
                d["-t"] = True
            elif letter == "v":
                d["-v"] = True
                PrintColorCoding()
                exit(0)
    if not d["-C"]:
        t.cat = t.hl = t.N = ""
    items = GetData()
    if d["-a"]:  # Show all items
        for item in items:
            if item.description:
                print(item)
        PrintColorCoding()
    elif d["-b"] is not None:  # Show items in box number -b
        n = int(d["-b"])
        for item in items:
            if item.box == n:
                print(item)
    elif d["-d"]:
        Inspection()
    elif d["-e"]:  # Show empty compartments
        ShowEmptyCompartments()
    elif d["-l"]:  # Show allowed keywords
        PrintKeywords()
    elif d["-k"]:  # Show all the items with the given keyword
        kw = d["-k"].lower()
        for item in items:
            ikw = [j.lower() for j in item.keywords]
            if kw in ikw:
                print(item)
        PrintColorCoding()
    elif d["-t"]:  # Print the ToDo list
        PrintToDo()
    elif not args:
        Usage()
    else:
        TextSearch(args, items)
