'''
Get daily text form of weather forecast
    - Parse contents and convert to very short output
    - Use color to flag important stuff like winds, rain, thunderstorms,
      snow
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright © 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print out text-based weather information
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import re
        import sys
        from pdb import set_trace as xx
        from collections import deque
        from pprint import pprint as pp
    # Custom imports
        import requests
        import julian
        import months
        from wrap import dedent
        from color import TRM as t
        from lwtest import Assert
    # Global variables
        ii = isinstance
        w = int(os.environ.get("COLUMNS", "80")) - 5
        # Location
        lat, lon = "43.5", "-116.4"
        # Turn on debugging to avoid loading from web
        dbg = 1
        class g: 
            # Global variable holder
            pass
        g.update = ""
if 1:   # Utility
    def Error(*msg, stasus=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [s]
          Print NOAA weather forecast as plain text.  If s is not empty, a 
          one-line report for each period is given unless it's 'd', in
          which case the raw NOAA text is printed.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-b"] = True            # Brief output (one line)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "bh", ["help"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("b"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        # One or more command line arguments toggles the -b setting
        if not args:
            d["-b"] = not d["-b"]
        return args
if 0:   # Functions to return string describing the weather feature
    def AnalyzeRain(line):
        'Return empty string if nothing of interest'
        return ""
    def AnalyzeWind(line):
        'Return empty string if nothing of interest'
        return ""
    def AnalyzeThun(line):
        'Return empty string if nothing of interest'
        return ""
    def AnalyzeSnow(line):
        'Return empty string if nothing of interest'
        return ""
class Weather:
    def __init__(self, lines, brief_report=True):
        self.lines = lines
        self.brief_report = brief_report
        # Build a list of the days' data:  elements are [day, details]
        self.lst = lst = []
        for line in self.lines:
            day, details = line.split(":")
            lst.append([day, details])
        self.today, self.first_day_count = self.FixTodaysName()
        Assert(len(self.lst) in (12, 13))
        Assert(self.first_day_count in (1, 2))
    def FixTodaysName(self):
        # Get a set of the day's names
        a = set()
        for day, details in self.lst:
            if "Night" in day or "Today" in day or "Tonight" in day:
                continue
            a.add(day)
        days = set("Monday Tuesday Wednesday Thursday Friday Saturday Sunday".split())
        # Find the missing name
        b = days - a
        Assert(len(b) == 1)
        today = b.pop()
        # Change first two elements to today's day name
        count = 0
        if self.lst[0][0] == "Today":
            self.lst[0][0] = today
            count += 1
        if self.lst[1][0] == "Tonight":
            self.lst[1][0] = f"{today} Night"
            count += 1
        return today, count
    def __str__(self):
        o = []
        for day, details in self.lst:
            o.append(day)
        return '\n'.join(o)

if 1:   # Core functionality
    def Wrap(line):
        'Print the line wrapped as needed'
        n, used = 4, 0
        print(f"{' '*n}", end="")
        used += n
        for word in line.split():
            l = len(word) + 1
            if l + used > w:
                print(f"\n{' '*n}", end="")
                used = n
            print(word, end=" ")
            used += l
        print()
    def Get():
        file = "/plib/pgm/weather.data"
        if dbg:
            t.print(f"{t.dbg}weather.py is in debug mode")
            s = open(file).read()
        else:
            url = (f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}&"
                   f"unit=0&lg=english&FcstType=text&TextType=1")
            url = "https://forecast.weather.gov/MapClick.php?lat=43.6339&lon=-116.3256&unit=0&lg=english&FcstType=text&TextType=1"
            u = requests.get(url)
            s = u.content.decode()
            s = s.replace("<br>", "\n")
            s = s.replace("<b>", "\n")
            s = s.replace("</b>", "")
            open(file, "w").write(s)
        q = s.split("\n")
        # Do some preliminary processing to remove the header stuff
        if 0:
            ln = q.popleft()
            while ln.strip() != "</style>":
                ln = q.popleft()
        else:
            # Use regexps to keep only lines with data we want
            s = ["^" + i for i in '''Last Today Tonight Monday Tuesday Wednesday 
                   Thursday Friday Saturday Sunday'''.split()]
            r = re.compile('|'.join(s))
            o = []
            while q:
                ln = q.pop(0)
                if r.search(ln):
                    o.append(ln)
            q = deque(o)
            if 0:
                for i in q:
                    print(i)
                exit()
        return q
    def SetColors():
        if 0:
            t.dbg = t("purl")
            t.title = t("orn")
            t.rain = t("grnl")
            t.snow = t("magl")
            t.thun = t("redl")
            t.wind = t("cynl")
            t.sun = t("yell")
            t.cloud = t("vio")
            t.low = t("wht", "royd")
            t.high = t("wht", "lipd")
            t.low = t("sky")
            t.high = t("lipl")
        else:
            t.dbg = t("purl")
            t.title = t("brnl")
            t.rain = t("grnl")
            t.snow = t("magl")
            t.thun = t("magl")
            t.wind = t("cynl")
            t.sun = t("yell")
            t.cloud = t("viol")
            t.low = t("wht", "royd")
            t.high = t("wht", "lipd")
            t.low = t("sky")
            t.high = t("redl")
    def PrintTitle(title, line):
        '''Print the title with color coding.  To do this, search line
        text for keywords.
        '''
        r = line.lower()
        rain = True if "rain" in r or "shower" in r else False
        snow = True if "snow" in r else False
        thund = True if "thunderstorm" in r else False
        windy = True if "wind" in r or "gust" in r else False
        sunny = True if "sunny" in r else False
        cloudy = True if "cloudy" in r else False
        # Get high and low temperatures
        mo = re.search(r"high near (-?\d{1,3})", line, re.I)
        high = mo.groups()[0] if mo else ""
        mo = re.search(r"low around (-?\d{1,3})", line, re.I)
        low = mo.groups()[0] if mo else ""
        temp = f"{t.low}{low}{t.n}{t.high}{high}{t.n}"
        # Print title to 16 characters wide
        n = 16 - len(title)
        #Assert(n >= 0)
        print(f"{t.title}{title:s}{t.n}", end=" "*n)
        print(f"{temp}", end=" "*4)
        if thund:
            print(f"{t.thun}thund{t.n} ", end="")
        if snow:
            print(f"{t.snow}snow{t.n} ", end="")
        if rain:
            print(f"{t.rain}rain{t.n} ", end="")
        if windy:
            print(f"{t.wind}wind{t.n} ", end="")
        if sunny:
            print(f"{t.sun}sun{t.n} ", end="")
        if cloudy:
            print(f"{t.cloud}cloudy{t.n} ", end="")
        print()
    def Select(q):
        'Return a list of the lines to be printed'
        Assert(ii(q, deque))
        found, lines = False, []
        show = 0    # Set to True to see all of the lines and then exit
        while q:
            u = q.popleft()
            u = u.strip()
            if show:
                # Just print to see what's going on
                print(u)
                continue 
            if not u:
                continue
            if u.startswith("Last Update:"):
                loc = u.find("</td>")
                s = u[:loc]
                g.update = s.replace("</a>", "")
                continue
            if (u.startswith("Today") or u.startswith("This ") or
                u.startswith("Tonight")):
                found = True
            if not found:
                continue
            if u.startswith("<hr>"):
                break
            lines.append(u)
        if show:
            exit()
        Assert(lines)
        return lines
    def GetLastUpdate():
        'Return number of hours since last update'
        s = g.update.replace("Last Update: ", "")
        f = s.split()
        tm, ampm, tz, month, day, year = f
        hr, minute = [int(i) for i in tm.split(":")]
        hrs = hr + minute/60
        if ampm == "am":
            hrs += 12
            day


        print(f)
        month = months.months(month)
        print(month)
        exit()

    def Report(lines):
        for line in lines:
            loc = line.find(":")
            title = line[:loc]
            details = line[loc + 1:].strip()
            PrintTitle(title, details)
            if d["-b"]:
                Wrap(details)
        num_hours = GetLastUpdate()
        print(g.update, "\nNow: ", end="")
        os.system("date")
if __name__ == "__main__": 
    d = {}      # Options dictionary
    SetColors()
    args = ParseCommandLine(d)
    q = Get()
    if args and args[0] == "d":
        # Show raw html
        for line in q:
            l = line.rstrip()
            if l:
                print(l)
        exit(0)
    lines = Select(q)
    if 0:
        w = Weather(lines)
        print(w)
    else:
        Report(lines)
