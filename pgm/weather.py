'''
Get daily text form of weather forecast
    Vision:
        - Parse contents and convert to very short output
        - Use color to flag important stuff like winds, rain,
          thunderstorms, snow
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
    # Custom imports
        import requests
        from wrap import dedent
        from color import TRM as t
    # Global variables
        ii = isinstance
        w = int(os.environ.get("COLUMNS", "80")) - 5
        # Location
        lat, lon = "43.5", "-116.4"
        # Turn on debugging to avoid loading from web
        dbg = False
if 1:   # Utility
    def Error(*msg, stasus=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [s]
          Print NOAA weather forecast as plain text.  If s is not empty, a 
          one-line report for each period is given.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dh", ["help"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("d"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if not args:
            d["-d"] = True
        return args
if 1:   # Core functionality
    def Get():
        file = "/plib/pgm/weather.data"
        if dbg:
            s = open(file).read()
        else:
            url = (f"https://forecast.weather.gov/MapClick.php?lat={lat}&lon={lon}&"
                   f"unit=0&lg=english&FcstType=text&TextType=1")
            u = requests.get(url)
            s = u.content.decode()
            s = s.replace("<br>", "\n")
            s = s.replace("<b>", "\n")
            s = s.replace("</b>", "")
            if 0:
                open(file, "w").write(s)
                exit()
        q = deque(s.split("\n"))
        return q
    def Select(q):
        'Return a list of the lines to be printed'
        assert(ii(q, deque))
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
        assert(lines)
        return lines
        xx()
    def PrintTitle(title, line):
        '''Print the title with color coding.  To do this, search line
        text for keywords.
        '''
        def SetColors():
            t.title = t("orn")
            t.rain = t("lgrn")
            t.snow = t("lblu")
            t.thun = t("lred")
            t.wind = t("lcyn")
            t.sun  = t("lyel")
            t.cloud = t("gry")
        SetColors()
        r = line.lower()
        rain   = True if "rain" in r or "shower" in r else False
        snow   = True if "snow" in r else False
        thund  = True if "thunderstorm" in r else False
        windy  = True if "wind" in r or "gust" in r else False
        sunny  = True if "sunny" in r else False
        cloudy = True if "cloudy" in r else False
        # Print title to 16 characters wide
        n = 16 - len(title)
        assert(n >= 0)
        print(f"{t.title}{title:s}{t.n}", end=" "*n)
        if thund:
            print(f"{t.thun}thunderstorm{t.n} ", end="")
        if snow:
            print(f"{t.snow}snow{t.n} ", end="")
        if rain:
            print(f"{t.rain}rain{t.n} ", end="")
        if windy:
            print(f"{t.wind}wind{t.n} ", end="")
        if sunny:
            print(f"{t.sun}sunny{t.n} ", end="")
        if cloudy:
            print(f"{t.cloud}cloudy{t.n} ", end="")
        print()
    if 1:   # Functions to return string describing the weather feature
        # Return empty string if nothing of interest
        def AnalyzeRain(line):
            return ""
        def AnalyzeWind(line):
            return ""
        def AnalyzeThun(line):
            return ""
        def AnalyzeSnow(line):
            return ""
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
            print(word, end = " ")
            used += l
        print()
    def Report(lines):
        for line in lines:
            loc = line.find(":")
            title = line[:loc]
            details = line[loc + 1:].strip()
            PrintTitle(title, details)
            if d["-d"]:
                Wrap(details)

if __name__ == "__main__": 
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    q = Get()
    lines = Select(q)
    Report(lines)