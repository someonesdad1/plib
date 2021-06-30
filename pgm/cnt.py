'''
Count 8-bit characters in a stream or file
    TODO
 
    * Change -r to turn on a report section that provides a number of
      statistical tests of randomness:  
 
        - Entropy
        - Chi-squared
        - Mean
        - Serial correlation test
 
    These statistical calculations should be done during the
    accumulation of the data from the files, but only if -r is used
    because they slow things down considerably.  Or, they would only
    need to acquire the counts[256] array; then the entropy,
    chi-squared, and mean could be calculated at report time.  The
    Serial correlation data adds to the calculation time, so it would
    only be printed if the -R option was used.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2012, 2019 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Count 8-bit characters in a stream or file
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import io
    import itertools
    import os
    import string
    import sys
    from collections import defaultdict
    from pprint import pprint as pp
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
    from fpformat import FPFormat
    from roundoff import RoundOff
    import color as C
if 1:   # Global variables
    # Colors
    C.max = C.lgreen
    C.median = C.lcyan
    C.min = C.lred
    C.filtered = C.yellow
def ProcessFile(file, d):
    ''' Read in the bytes from the file and add them to the
    d["counts"] dictionary.
    '''
    try:
        ifp = sys.stdin.buffer if file == "-" else open(file, "rb")
    except IsADirectoryError:
        return
    # Process in chunks to avoid running out of memory
    b = ifp.read(d["chunksize"])
    if d["-u"]:
        b = b.decode("UTF-8")
    while b:
        for byte in b:
            if d["-u"]:
                d["counts"][ord(byte)] += 1
            else:
                d["counts"][byte] += 1
        b = ifp.read(d["chunksize"])
        if d["-u"]:
            b = b.decode("UTF-8")
def GetCharacterClasses(d):
    'Set up the various character classes in d["char_classes"]'
    def F(s):
        'Convert the string s to a set of its ord numbers.'
        return set([ord(i) for i in s])
    cc = {
        "all": set(range(256)),
        "ctrl": set(range(32)),
        "7bit": set(range(128)),
        "8bit": set(range(128, 256)),
        "letters": F(string.ascii_letters),
        "lower": F(string.ascii_lowercase),
        "upper": F(string.ascii_uppercase),
        "digits": F(string.digits),
        "hex": F(string.hexdigits),
        "oct": F(string.octdigits),
        "punct": F(string.punctuation),
        "print": F(string.printable),
        "ws": F(string.whitespace),
    }
    d["char_classes"] = cc
def SetUpEncoding(d):
    '''The d["encoding"] dictionary is used to print out the
    characters for the given ord() value of a character.  This is done
    for two reasons:  1) The ASCII control characters are printed with 
    mnemonics and 2) certain 8-bit characters are replaced by a small 
    square because they don't print correctly in mintty under cygwin
    (which is where I'm currently working).  You'll want to change this
    encoding if you're working with a more sensible console program.
    '''
    # Set up the control character mnemonics
    e = d["encoding"] = {}
    for i, c in enumerate(("nul soh stx etx eot enq ack bel bs ht nl vt np "
            "cr so si dle dc1 dc2 dc3 dc4 nak syn etb can em sub esc fs gs "
            "rs us sp").split()):
        e[i] = c
    u = chr(0x25ab)     # White small square
    for i in range(33, 256):
        e[i] = u if 127 <= i <= 159 else chr(i)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] [file1 [file2 ...]]
      Construct a table of the counts of the bytes in one or more files
      (use '-' for stdin).  Directories on the command line are ignored.
    
      The display of some bytes with the 8th bit set are idiosyncratic and 
      depend on the console encoding used.  You can edit the function 
      SetUpEncoding() to customize the characters printed to the console
      for your environment.
    
      Caution:  files are read in as binary and the counts are with respect
      to byte ord() values.  A text file encoded in e.g. UTF-8 will read
      fine as a binary file, but you won't see the Unicode characters you
      expect in the output (unless they are 7-bit ASCII characters).  In
      such a case, use the -u option.
    Options:
      -C    Turn off ANSI-colored output.  This coloring is useful to show 
            when the data are filtered, the high and low counts and bytes,
            and the median value.
      -c char_class
            Restrict the output to the indicated character class(es):
              7bit     ord(c) < 128         | lower  string.ascii_lowercase
              8bit     ord(c) >= 128        | oct    string.octdigits
              ctrl     ord(c) < 32          | print  string.printable
              digits   string.digits        | punct  string.punctuation
              hex      string.hexdigits     | upper  string.ascii_uppercase
              letters  lower + upper        | ws     string.whitespace
            You can use more than one -c option or join them in a string
            separated by space characters; the resulting set is the union
            of the indicated sets.  To restrict the counts to a specified
            set of characters, use the -S option.
      -D    Include a list of the files that were processed.
      -d, -x, -o
            Instead of showing the characters in the table, show their
            ASCII decimal, hex, or octal value.
      -f    Fold letters into all lower case.  This lets you look at letter
            frequencies regardless of case.
      -l    Produce a long listing, one character per line, with counts
      -N    Suppress printing the statistics
      -n    Same as -l, but only show those characters with zero counts
            (i.e., those characters not in the file).
      -p    Instead of the counts, show the frequency in percent relative
            to the most-frequent character count.
      -S chars
            Add the characters is chars to the characters to be counted.
            set(chars) is added to those specified with -c.
      -s    Sort table by count rather than byte's ord() value.
      -r    Include the chi-squared statistic in the statistics.  This can be
            used to assess whether the bytes are uniformly randomly
            distributed (see the cnt.pdf file for details).
      -u    Read the files as UTF-8 encoded and print the data with respect 
            to the Unicode characters encountered.
      -X    Negate the sense of the -c and -S options by removing those
            specified characters from the counts.
    Statistics:
        character_classes   = Which classes used to filter
        count_nonzero       = Number of bytes with nonzero counts
        count_zero          = Number of bytes with zero count
        filtered            = True if one or more classes used to filter
        filtered_bytes_read = Count of bytes after filtering
        highest             = ord()'s of bytes with highest count
        highest_count       = Count of most frequent byte(s)
        lowest              = ord()'s of bytes with lowest nonzero count
        lowest_count        = Count of least frequent byte(s) (nonzero)
        median              = ord() at midpoint of ordered list of bytes
        total_bytes_read    = Number of bytes in input
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-C"] = True
    d["-c"] = []
    d["-D"] = False
    d["-d"] = False
    d["-f"] = False
    d["-l"] = False
    d["-N"] = False
    d["-n"] = False
    d["-o"] = False
    d["-P"] = False
    d["-p"] = False
    d["-r"] = False
    d["-R"] = False
    d["-s"] = False
    d["-S"] = set()
    d["-u"] = False
    d["-v"] = False
    d["-X"] = False
    d["-x"] = False
    if not sys.argv[1:]:
        Usage(d)
    try:
        s = "Cc:DdfLlNnoPpRrS:suvXx"
        optlist, args = getopt.getopt(sys.argv[1:], s)
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for o, a in optlist:
        if o[1] in "CDdfLlNnoPpRrsuvXx":
            d[o] = not d[o]
        elif o == "-c":
            # Specify character class
            def ProcessCharacterClass(cls):
                if cls not in d["char_classes"]:
                    s = (f"'{cls}' is an unrecognized character class.  "
                         f"Choose from:")
                    print(s)
                    s = "\n   ".join(list(d["char_classes"]))
                    print("  ", s)
                    exit(1)
                d["-c"].append(cls)
            if " " in a:
                for cls in a.strip().split():
                    ProcessCharacterClass(cls)
            else:
                ProcessCharacterClass(a)
        elif o == "-S":
            # Specify character set to count
            d["-S"] |= set([ord(i) for i in a])
    d["-c"] = set(d["-c"])
    if d["-u"]:
        others = [i for i, j in optlist]
        for i in "-C -c -d -x -o -f -l -n -r -R".split():
            if i in others:
                if i == "-c" and d["-X"]:
                    continue
                print(f"Warning:  option {i} not functional with -u",
                      file=sys.stderr)
    if d["-R"]:
        d["-r"] = True
    if d["-X"] and not (d["-c"] or d["-S"]):
        print("Must use -c or -S with -X", file=sys.stderr)
        exit(1)
    # Remove directories in args
    args = list(itertools.filterfalse(os.path.isdir, args))
    if not args:
        Usage(d)
    return args
def GetStatistics(d):
    ''' Calculate the counting statistics and put them in 
    d["statistics"].
    '''
    C = d["counts"]
    total_bytes_read = sum(C.values())
    if d["-u"]:
        d["statistics"] = {"total_bytes_read": total_bytes_read}
        return
    if d["-f"]:
        # Put uppercase counts into lowercase counts
        folded = True
        for i in range(ord('A'), ord('Z') + 1):
            C[i + 32] += C[i]
            del C[i]
    items = sorted(C.items())
    keys = [i for i, j in items]
    values = [j for i, j in items]
    # Filter by character classes if indicated
    filtered = bool(d["-c"] or d["-S"])
    if filtered:
        keep = set()
        character_classes = ' '.join(d["-c"])
        s = None
        for i in character_classes.split():
            s = d["char_classes"][i]
            keep |= s
        keep |= d["-S"]
        if d["-X"]:     # Get the complement
            keep = set(range(256)) - keep
        C1 = defaultdict(int)
        for i in C:
            if i in keep:
                C1[i] = C[i]
        d["counts"] = C = C1
        del s, keep, C1, i
        filtered_bytes_read = sum(C.values())
    if 1:   # Median
        midcount = filtered_bytes_read//2 if filtered else total_bytes_read//2
        # Find the location in values where the cumulative sum is closest
        # to midcount
        cumul = list(itertools.accumulate(values))
        diff = [abs(i - midcount) for i in cumul]
        median = None
        if d["-v"]:
            print(dedent(f'''
                Median data:
                  midcount = {midcount}'''))
            s = []
            for b, df in zip(keys, diff):
                s.append(f"{b:3d} {df:{max([len(str(i)) for i in diff])}d}")
            for i in Columnize(s, indent=" "*2):
                print(i)
        try:
            n = diff.index(min(diff))
            median = [keys[n]]
        except Exception:
            pass
        try:
            del midcount, cumul, diff, n, b, s, i, df
        except Exception:
            pass
    if d["-r"]:   # chi-squared
        e = total_bytes_read//256       # Expected value for each count
        terms = [RoundOff((i - e)**2/e, 3) for i in values]
        d["chi_square_terms"] = list(zip(keys, values, terms))
        chi_squared = round(sum(terms), 2)
        if chi_squared >= 1000:
            chi_squared = f"{chi_squared:.3e} (255 d.f.)"
        else:
            chi_squared = str(chi_squared) + " (255 d.f.)"
        expected_count = e
        mean = sum([i*j for i, j in d["counts"].items()])
        mean = mean/filtered_bytes_read if filtered else mean/total_bytes_read
        mean = round(mean, 2)
        del e, terms
    if d["-f"]:   # Upper case folded into lower case counts
        folded = True
    count_nonzero = len(C)
    count_zero = 256 - count_nonzero
    lowest_count = min(C.values()) if C.values() else 0
    lowest = tuple(sorted([i for i in C if C[i] == lowest_count]))
    highest_count = max(C.values()) if C.values() else 0
    highest = tuple(sorted([i for i in C if C[i] == highest_count]))
    del C, items, keys, values
    l = locals()
    del l["d"]
    d["statistics"] = l
    if 0:
        print("Variables in GetStatistics():")
        for i in l:
            print(f"   {i:20s}= {l[i]}")
def PrintFiles(d):
    ''
    if d["-D"]:
        n = len(d["files"])
        s = "s" if n > 1 else ""
        print(f"{n} file{s} processed:")
        for i in Columnize(d["files"], indent=" "*2):
            print(i)
def ReportLongForm(d):
    ''' Show the detailed long report.  The fields printed are:
        Byte decimal value
        Byte hex value
        Byte character form
        Count
        Relative percentage
        Histogram of relative percentage using '*' characters
    '''
    dec = C.Decorate()
    # Get needed data
    stats, counts, e = d["statistics"], d["counts"], d["encoding"]
    max_count = stats["highest_count"]
    median = stats["median"]
    highest, lowest = stats["highest"], stats["lowest"]
    filtered = stats["filtered"]
    numplaces = len(str(stats["highest_count"])) 
    used_dot = False
    lines = []
    # Sort data
    if d["-s"]: # Sort by count values
        t = sorted([(j, i) for i, j in counts.items()])
        items = [j for i, j in reversed(t)]
    else:       # Sort by byte value
        items = sorted(counts)
    # Get screen width
    c, E = "COLUMNS", os.environ
    w = int(E[c]) if c in E else 80
    # Print counts
    if d["-p"] or d["-P"]:
        print("Byte percentages:")
    else:
        print("Byte counts:")
    W = w - 3 - 1 - 2 - 1 - 3 - numplaces - 1 - 2 # Room left for *'s
    for i in items:
        a = "*"*int(W*counts[i]/max_count)
        printed_color = False
        if i in highest and d["-C"]:
            printed_color = True
            print(dec.fg(C.max), end="")
        elif i in lowest and d["-C"]:
            printed_color = True
            print(dec.fg(C.min), end="")
        elif i in median and d["-C"]:
            printed_color = True
            print(dec.fg(C.median), end="")
        print(f"{i:3d} {i:02x} {e[i]:^3s} {counts[i]:{numplaces}d} {a}", end="")
        if printed_color:
            print(dec.normal())
        else:
            print()
def PrintStatistics(d):
    ''
    dec = C.Decorate()
    def F(x, flag, name):
        # flag:  0 = normal, 1 = max, 2 = min, 3 = median
        if isinstance(x, (list, tuple)):
            if flag:
                s = [' '.join([str(i) for i in x])]
                s += [' '.join([e[i] for i in x])]
                if d["-x"]:
                    s += [' '.join([f"0x{i:02x}" for i in x])]
                elif d["-o"]:
                    s += [' '.join([f"0o{i:03o}" for i in x])]
                t = ' ≡ '.join(s)
                if d["-C"]:
                    c = C.max if flag == 1 else C.min if flag == 2 else C.median
                    t = dec.fg(c) + t + dec.normal()
                return t
            else:
                return ' '.join([str(i) for i in x])
        else:
            return str(x)
    print("Statistics:")
    stats, counts, e = d["statistics"], d["counts"], d["encoding"]
    max_count = stats["highest_count"] if stats["highest_count"] else None
    min_count = stats["lowest_count"] if stats["lowest_count"] else None
    median = stats["median"] if stats["median"] else None
    filtered = stats["filtered"]
    used_dot = False
    lines = []
    n = 23      # Width of statistics names
    trans = {
        "count_nonzero": "Used bytes",
        "count_zero": "Unused bytes",
        "highest": "Most frequent byte",
        "highest_count": "  Count",
        "lowest": "Least frequent byte(s)",
        "lowest_count": "  Count",
        "median": "Median",
        "total_bytes_read": "Total bytes read",
    }
    for i in sorted(stats):
        if i == "filtered":
            if not filtered:
                continue
            if d["-C"]:
                print(f"   {dec.fg(C.filtered)}{i:{n}s}= True{dec.normal()}")
            else:
                print(f"   {i:{n}s}= True")
            continue
        flag = 0
        if i == "highest":
            flag = 1
        elif i == "lowest":
            flag = 2
        elif i == "median":
            flag = 3
        if i == "character_classes" and d["-S"]:
            t = ''.join(sorted(list([chr(j) for j in d["-S"]])))
            if stats[i]:
                stats[i] += f" special('{t}')"
            else:
                stats[i] = f"special('{t}')"
        s = stats[i]
        j = trans[i]
        if i in set("lowest_count highest_count total_bytes_read "
                    "filtered_bytes_read".split()):
            print(f"   {j:{n}s}= {stats[i]:,}")
        else:
            print(f"   {j:{n}s}= {F(stats[i], flag, i)}")
def PrintReport(d):
    ''' Show the collected counts.
    '''
    dec = C.Decorate()
    PrintFiles(d)
    if d["-u"]:     # Interpret files as UTF-8 encoded text files
        # Used to align decimal points in percentage
        fp = FPFormat(num_digits=3)
        GetStatistics(d)
        total_characters = d["statistics"]["total_bytes_read"]
        if not d["-N"]:
            print(f"Total Unicode characters read = {total_characters:,}")
        counts, e = d["counts"], d["encoding"]
        max_count = max(len(str(max(counts.values()))), 5)
        # Sort data
        if d["-s"]: # Sort by count values
            t = sorted([(j, i) for i, j in counts.items()])
            items = [j for i, j in reversed(t)]
        else:       # Sort by byte value
            items = sorted(counts)
        # If -X option used, filter out the non-wanted characters
        if d["-X"]:
            keep = set()
            character_classes = ' '.join(d["-c"])
            s = None
            for i in character_classes.split():
                s = d["char_classes"][i]
                keep |= s
            keep |= d["-S"]
            items = [i for i in items if i not in keep]
            t = f"Bytes removed with -X = {character_classes} "
            if d["-S"]:
                t += 'with d["-S"] = ' + str(d["-S"])
            print(t)
        # Print counts
        p = "% of Total Count"
        print(f"Decimal   Hex   Char   {'Count':>{max_count}s}   {p}")
        for i in items:
            n = counts[i]
            c = chr(i)
            p = 100*n/total_characters
            try:
                pct = fp.dp(p, width=30, dpoint=4)
            except ValueError:
                # p is probably too small, so display in scientific notation
                pct = f"     {fp.sci(p):<30s}"
            try:
                c = e[i]
                hx = f"{i:02x}"
                print(f"{i:7d} {hx:^8s} {c:^3s}   {counts[i]:{max_count}d} "
                      f"{pct}")
            except KeyError:
                if i <= 0xffff:
                    s = f"U+{i:04x}"
                    print(f"{i:7d} {s:^8s} {c:^3s}   {counts[i]:{max_count}d}"
                          f" {pct}")
                        
                else:
                    print(f"{i:7d} U+{i:06x} {c:^3s}   {counts[i]:{max_count}d}"
                          f" {pct}")
        return
    else:
        GetStatistics(d)
        if not d["-N"]:
            PrintStatistics(d)
        if "chi_squared" in d["statistics"] and d["-R"] and not d["-N"]:
            # Print the terms in the chi-squared statistic.  keys are
            # the byte's ord() values, values are the counts, and terms
            # are the terms of the chi-squared sum.
            print("Chi-squared contributing terms (ord(), (obs-exp)^2/exp):")
            data = d["chi_square_terms"]
            if d["-s"]:
                # Sort the data by the size of the terms
                k = lambda x: x[2]
                data = sorted(data, key=k, reverse=True)
            s = []
            terms = [k for i, j, k in data]
            n = max([len(str(i)) for i in terms])
            e = d["encoding"]
            for key, value, term in data:
                t = str(term)
                if t.startswith("0."):
                    t = t.replace("0.", " .")
                if d["-d"]:
                    s.append(f"{key:3d} {t:{n}s}")
                elif d["-o"]:
                    s.append(f"{key:03o} {t:{n}s}")
                elif d["-x"]:
                    s.append(f"{key:02d} {t:{n}s}")
                else:
                    s.append(f"{e[key]:^3s} {t:{n}s}")
            for i in Columnize(s, indent=" "*2):
                print(i)
    # Get needed data
    stats, counts, e = d["statistics"], d["counts"], d["encoding"]
    max_count = stats["highest_count"] if stats["highest_count"] else None
    min_count = stats["lowest_count"] if stats["lowest_count"] else None
    median = stats["median"] if stats["median"] else None
    filtered = stats["filtered"]
    numplaces = len(str(stats["highest_count"])) + 1
    used_dot = False
    lines = []
    # Sort data
    if d["-s"]: # Sort by count values
        t = sorted([(j, i) for i, j in counts.items()])
        items = [j for i, j in reversed(t)]
    else:       # Sort by byte value
        items = sorted(counts)
    # Print counts
    for i in items:
        if d["-d"] or d["-x"] or d["-o"]:
            if d["-d"]:
                s1 = f"{i:3d} "
            elif d["-x"]:
                s1 = f"{i:02x} "
            else:
                s1 = f"{i:03o} "
        else:
            s1 = f"{e[i]:^3s}"
        if d["-p"] or d["-P"]:
            p = 100*counts[i]/stats["highest_count"]
            if p:
                if d["-P"]:
                    s2 = f"{p:7.3f}  "
                else:
                    p = int(p)
                    s2 = f"{p:4d}  " if p else "   ."
                    used_dot = "." in s2
            else:
                s2 = " "*4
        else:
            s2 = f"{counts[i]:{numplaces}}  "
        line = s1 + s2
        # Colorize min, max, median
        if max_count and counts[i] == max_count and d["-C"]:
            line = dec.fg(C.max) + line + dec.normal()
        if min_count and counts[i] == min_count and d["-C"]:
            line = dec.fg(C.min) + line + dec.normal()
        if median and i in median and d["-C"]:
            line = dec.fg(C.median) + line + dec.normal()
        lines.append(line)
    if d["-n"]:
        b = set(range(256)) - set(items)
        if d["-x"]:
            lines = [f"{i:02x}" for i in b]
            s = " (in hex)"
        elif d["-o"]:
            lines = [f"{i:03o}" for i in b]
            s = " (in octal)"
        elif d["-d"]:
            lines = [f"{i:3d}" for i in b]
            s = " (in decimal)"
        else:
            lines = [f"{e[i]:^3s}" for i in b]
            s = ""
        print(f"Bytes not present in data{s}:")
        for i in Columnize(lines, indent=" "*2):
            print(i)
        return
    if d["-l"]:   # Long form of report
        ReportLongForm(d)
    else:
        s = " (. means > 0 but rounds to 0)" if used_dot else ""
        p = " in % of highest count" if d["-p"] or d["-P"] else ""
        ho = "(hex) " if d["-x"] else "(octal) " if d["-o"] else ""
        if d["-p"] or d["-P"]:
            print(f"Byte percentages{p}{s}:")
        else:
            print(f"Byte {ho}counts:")
        for i in Columnize(lines, indent=" "*2):
            print(i)
if __name__ == "__main__":
    d = {   # Options dictionary
        "chunksize": int(1e6),          # How much to read into buffer
        "counts": defaultdict(int),     # Store counts
    }
    GetCharacterClasses(d)
    SetUpEncoding(d)
    d["files"] = ParseCommandLine(d)
    for file in d["files"]:
        ProcessFile(file, d)
    PrintReport(d)
