"""
Prints out combinations & permutations of command line arguments.
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Prints comb/perm of command line arguments
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        from pathlib import Path as P
        import math
        import sys
        from itertools import combinations, permutations
        from pdb import set_trace as xx
    if 1:  # Custom imports
        from columnize import Columnize
        from wrap import wrap, dedent
        from color import t
        from f import flt

        try:
            import mpmath
            from mpmath.libmp import to_str

            have_mpmath = True
        except ImportError:
            have_mpmath = False
        if 0:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class G:
            pass

        g = G()
        ii = isinstance
        g.n = None  # number of objects
        g.k = None  # k at a time
if 1:  # Utility

    def Manpage():
        c = t("lill")
        print(
            dedent(f"""

        This script will compute permutations if it's named perm.py and will computer combinations
        if it's named comb.py.

        One use case of this script is to print out the permutations of a set of words that you 
        want to use as a password.  Suppose you run the script /plib/pgm/password.py with the
        arguments '-s 0 5 5 6 4', which means to print five lines of 5 words that contain 4 to 6
        characters.  You select the line 'many break girl market fate' and you want to see all the
        permutations of these words taken 3 at a time.  You use the command 

            python perm.py -c -k 3 -s " " many break girl market fate

        and you'll get 60 permutations.  One of the permutations was 'fate break market' and I
        might choose that as a password by changing it to 'fate breaks market'.  In 2024 this would
        be considered a barely acceptable password with 18 characters and 10 unique characters.  My
        password manager program KeePass2 says it has 64 bits of "quality".  KeePass2 generates a
        18 character password from ASCII letters and digits as 'raK076j8Vi5ljCDj37' and labels it
        as having 94 bits.  While I could probably memorize the latter, I can guarantee I'd have
        forgotten it in a month unless I used it a lot.  I'd stand a better chance of remembering
        'fate breaks market', as I'd just have to remind myself with the first word.

        Some other examples:

        Print the permutations of the letters 'rgb'
            python perm.py rgb
            prints 3! = 6 items
                {c}rgb rbg grb gbr brg bgr{t.n}
                6 permutations
        Print the permutations of the letters 'rgbhsv' taken 3 at a time
            python perm.py -k 3 rgbhsv
            prints 6!/3! = 6*5*4 = 120 items
                {c}rgb rbv rsh grh …{t.n}
                {c}rgh rhg rsv grs …{t.n}
                {c}⋮{t.n}
                120 permutations
        Print the combinations of the letters 'rgbhsv' taken 3 at a time
            python comb.py -k 3 rgbhsv
            prints 6!/(3!*3!) = 6*5*4/6 = 20
                {c}rgb rgh rgs rgv rbh rbs rbv rhs rhv rsv
                gbh gbs gbv ghs ghv gsv bhs bhv bsv hsv{t.n}
                20 combinations
        """)
        )
        exit(0)

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage():
        which = "combinations" if comb else "permutations"
        formula = "C(n, k)" if comb else "P(n, k)"
        k = None if comb else "n"
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] A [B...]
          Prints out {which} of command line arguments.  A is a string and if it's the only
          argument, then its letters are used as the elements.  Otherwise the set of n arguments
          (A, B, ...) is used.  If the number of the results is larger than 10! (~3.6e6), the
          calculation time is long, so just the numbers will be printed unless -f is used.
        Notation
          n = number of letters in A or number of arguments if > 1
          k = number of items to take for each subset
        """)
        )
        ex = "-k 2 -s '|' my dog has fleas"
        if comb:
            print(
                dedent(f"""
            C(n, k) = combinations of n objects taken k at a time
                    = n!/((n - k)!*k!)""")
            )
            print(
                dedent(f"""
            Example:  The arguments {ex!r} will print out all the combinations of
              the four words that contain two words.
            """)
            )
        else:
            print(
                dedent(f"""
            P(n, k) = all permutations of the size k subsets taken from all the n elements
                    = n!/(n - k)!
            P(n)    = P(n, n) = n!""")
            )
            print(
                dedent(f"""
            Example:  The arguments {ex!r} will print out all the permutations of
              the four words that contain two words.
            """)
            )
        print(
            dedent(f"""
        Options (default in square brackets):
          -c    Don't print in columns
          -f    Print output even if number of items is large (over 10!)
          -h    Print more help
          -k k  Number of objects in {formula} [{k}]
          -l    Just print the number of permutations or combinations
          -n n  Set the number of objects (implies -l also)
          -q    Quote the output strings
          -s x  Separator string for grouped items [""]
          --sum     The arguments are numbers; show all sums
          --prod    The arguments are numbers; show all products
        """)
        )
        exit(0)

    def ParseCommandLine(d):
        d["-c"] = True  # Print in columns
        d["-f"] = False  # Force output for large numbers
        d["-k"] = None  # Choose number
        d["-l"] = False  # Number only
        d["-n"] = None  # Set the number of objects (implies -l also)
        d["-q"] = False  # Quote output strings
        d["-s"] = ""  # Separator string
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(
                sys.argv[1:], "cfhk:ln:qs:", ["help", "sum", "prod"]
            )
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        g.n = len(args[0]) if len(args) == 1 else len(args)
        for o, a in opts:
            if o[1] in list("cflq"):
                d[o] = not d[o]
            elif o == "-k":
                # Allow g.n to be a float or an int if mpmath is present
                try:
                    d[o] = g.k = int(a)
                except ValueError:
                    if have_mpmath:
                        d[o] = g.k = float(a)
                    else:
                        raise
                if g.k < 1 or g.k > g.n:
                    Error(f"k must be between 1 and {g.n}")
            elif o == "-n":
                # Allow g.n to be a float or an int if mpmath is present
                try:
                    d[o] = g.n = int(a)
                except ValueError:
                    if have_mpmath:
                        d[o] = g.n = float(a)
                    else:
                        raise
                if g.n < 1:
                    Error(f"-n value must be > 0")
            elif o == "-s":
                d[o] = a
            elif o in ("-h", "--help"):
                Manpage()
            elif o == "--sum":
                Sums(args)
            elif o == "--prod":
                Sums(args, product=True)
        return args


if 1:  # Core functionality

    def Product(*args):
        product = flt(1)
        for i in args:
            product *= flt(i)
        return product

    def Sums(args, product=False):
        "Print a sorted list of all the possible sums/products of the numbers on the command line"
        print(
            f"All {'products' if product else 'sums'} of {' '.join(args)!r}:", end=" "
        )
        nums = [flt(i) for i in args]
        o = []
        for k in range(1, len(nums) + 1):
            for c in combinations(nums, k):
                if product:
                    o.append(Product(*c))
                else:
                    o.append(sum(c))
        o = set(o)
        print(f"({len(o)} combinations)")
        for i in Columnize(sorted(o), col_width=10, horiz=True):
            print(i)
        exit(0)

    def PrintOutput(func, name, objects):
        count = 0
        if g.k is None and func == combinations:
            Error(f"Must use -k option with {name}")
        out = []
        for i in func(objects, g.k):
            t = d["-s"].join(i)
            if d["-q"]:
                t = f"'{t}'"
            out.append(t)
            count += 1
        if d["-c"]:
            for i in Columnize(out):
                print(i)
        else:
            for i in out:
                print(i)
        print(f"{count} {name}")

    def GetHowMany(numobjects, k):
        """Calculate the number of combinations or permutations of numobjects taken k at
        a time.  This will return an integer, float, or mpmath.mpf.
        """
        n = numobjects
        if have_mpmath:
            f, F = mpmath.factorial, mpmath.fac
            try:
                if k is None:
                    p = f(n)
                else:
                    p = f(n) / f(n - k)
            except Exception:
                if k is None:
                    p = F(n)
                else:
                    p = F(n) / F(n - k)
            p = p / f(k) if comb else p
            assert ii(p, mpmath.mpf)
        else:
            if n > 9223372036854775807:
                raise ValueError(
                    "Number of objects must be no more than 9223372036854775807"
                )
            try:
                if k is None:
                    p = math.factorial(n)
                else:
                    p = math.factorial(n) // math.factorial(n - k)
            except Exception:
                print("{n} objects is too many to compute math.factorial()")
                exit(1)
            p = p // f(k) if comb else p
            assert ii(p, int)
        return p

    def Magnitude(n):
        assert ii(n, int) and n > 0
        s = str(n)
        m, e = s[0], len(s)
        e = len(s)
        return f"{m}e{e}"

    def JustPrintNumber():
        s = str(GetHowMany(g.n, g.k))
        if s.endswith(".0"):
            s = s[:-2]
        print(f"{s} {'combinations' if comb else 'permutations'}")


if __name__ == "__main__":
    # Options dictionary
    d = {"name": P(sys.argv[0]).name.replace(".py", "")}
    comb = True if d["name"] == "comb" else False
    args = ParseCommandLine(d)
    too_many = math.factorial(10)
    objects = list(args[0]) if len(args) == 1 else args
    g.k = g.n if g.k is None else g.k
    if d["-n"] is not None:
        g.n = d["-n"]
    else:
        g.n = GetHowMany(len(objects), g.k)
    if d["-l"] or d["-n"]:
        JustPrintNumber()
        exit(0)
    large = True if g.n >= too_many else False
    if d["-f"]:
        large = False  # Ignore the size
    if large:
        if ii(g.n, int):
            e = Magnitude(g.n)
        elif ii(g.n, (float, flt)):
            e = flt(g.n).sci
        elif have_mpmath and ii(g.n, mpmath.mpf):
            e = to_str(g.n._mpf_, 3, min_fixed=2, max_fixed=1, show_zero_exponent=True)
    l = f"Answer too large (limit is {Magnitude(too_many)}):  "
    # This script handles both combinations and permutations
    if d["name"] == "perm":
        if large:
            print(f"{l}number of permutations = {e}")
        else:
            PrintOutput(permutations, "permutations", objects)
    else:
        if large:
            print(f"{l}number of combinations = {e}")
        else:
            PrintOutput(combinations, "combinations", objects)
