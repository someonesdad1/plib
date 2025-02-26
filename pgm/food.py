"""
Show food calorie content of foods

Motivation
    The Hacker's Diet by John Walker
    (Walker died in Feb 2024 from head injuries from a fall; he was 74)
    https://www.fourmilab.ch/hackdiet/
    https://www.fourmilab.ch/hackdiet/comptoolsExcel.html

food_mealplan.csv
    - This is a CSV version of Walker's Mealplan.xls file from the above comptoolsExcel page.
      Warning:  the encoding in Excel is screwed up, so first save the file as an Open Office
      spreadsheet, then open it in Open Office and save it as a CSV file using UTF-8 encoding.
    - After saving it, edit it to remove blank lines and the cruft at the bottom of the file.

"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Program description string
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        from pathlib import Path as P
        from pprint import pprint as pp
        import csv
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert

        if 0:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class G:
            pass

        g = G()
        g.dbg = False
        ii = isinstance
if 1:  # Food data (https://www.fatsecret.com/calories-nutrition)
    # kcal per 100 g
    raw_data = """

            almonds:578
            apple juice:47
            apple:52
            apricot:48
            asparagus:20
            avocado:160
            bacon:541
            banana:89
            bean curd:61
            beef, ground (10% fat):176
            beef, ground (20% fat):254
            beef, ground (5% fat):137
            beef, steak (top sirloin):188
            beets:43
            bell pepper:26
            black beans:92
            blackberry jam:250
            broccoli:34
            Brussel sprouts:43
            bun (hamburger/hotdog):282
            butter:717
            cabbage:24
            cantaloupe:34
            carrots:41
            cauliflower:25
            celery:14
            cheddar cheese:403
            cheese, swiss:380
            Cheetos:536
            Cheez-its:500
            chicken (canned):83
            chicken:195
            corn chips (Doritos):495
            corn on cob, ear:94
            corn, canned:81
            cornbread muffin:233
            cottage cheese 2%:106
            cottage cheese 4%:106
            cream cheese (fat free):96
            cream cheese:321
            cucumber:12
            egg:147
            fat:770
            Fritos:571
            garbanzo beans:92
            green beans:31
            half and half:133
            ham (11% fat):163
            honeydew:36
            hot dog (turkey):353
            kidney beans:82
            lima beans:113
            liverwurst:327
            mayonnaise:643
            milk 1%:43
            milk 2%:52
            milk 3.3% (whole):67
            mushrooms:22
            nectarine:44
            noodles, egg:138
            noodles:137
            oatmeal cereal:145
            olive oil:884
            onions:42
            onions:42
            orange juice:45
            orange:47
            pancake:227
            peach:39
            peanuts:599
            pear:58
            peas:77
            pickles, dill:18
            pineapple:48
            pinto beans:85
            plum:46
            popcorn:375
            pork tenderloin:136
            potato chips:547
            potato, sweet:86
            potato:104
            pretzels (Dot's):500
            prune:250
            raisins:300
            refried beans:94
            rice:135
            Ritz crackers:500
            sauerkraut:19
            scallops (battered & fried):230
            scallops (broiled):132
            sesame oil:884
            shrimp:106
            sour cream:214
            spaghetti sauce, canned:64
            spaghetti:157
            spam:321
            spinach:23
            spinach:23
            strawberry:32
            sugar:387
            sunflower seeds:633
            taco shell:500
            tomato juice:17
            tomato:18
            tortilla (Mission):300
            turkey:104
            V8 juice:19
            vinegar:18
            waffle:310
            watermelon:30
            wheat things:452
            whipping cream:345
            white bread:231
            yellow squash:16
            yogurt:131

        """
    data = []
    # Change the data to kcal/g
    ok = True
    for i in raw_data.strip().split("\n"):
        s, cal = i.strip().split(":")
        try:
            data.append((s.strip(), flt(cal) / 100))
        except ValueError:
            print(f"Missing number for {s}")
            ok = False
    if not ok:
        exit(0)
if 1:  # Utility

    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=0):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Need description
        d["-d"] = 2  # Number of significant digits
        # if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Usage()
        x = flt(0)
        x.N = d["-d"]
        return args


if 1:  # Core functionality

    def Report():
        w = max([len(i[0]) for i in data])
        # Alphabetical
        for item, cphg in data:
            print(f"{item:{w}s} {cphg!s:5s}")
        # Sorted by size
        t.print(f"\n{t('ornl')}Sorted by size")
        for item, cphg in sorted(data, key=lambda x: x[1]):
            print(f"{item:{w}s} {cphg!s:5s}")

    def HD():
        "Dump the Hacker's Diet data"
        data = []
        with open("food_mealplan.csv") as csvfile:
            f = csv.reader(csvfile)
            for i in f:
                data.append(i)
        # Find the largest category
        w = max([len(i[0]) for i in data])
        for i in data:
            print(f"{i[0]:{w}s} ", end="")
            print(" ".join(i[1:]))


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if 1:
        Report()
    else:
        HD()
