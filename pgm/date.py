'''
Replacement for /bin/date.  This script is aware of time zones and will
handle calculations involving DST correctly (well, as long as python's 
datetime module does them correctly).

Note:  if you use this for your own use, you'll want to make sure the
code uses the proper datetime.tzinfo object for your location.  This is
done by providing the location in a constructor call to ZoneInfo().

- Command line not needed for current time
- Command line arithmetic
    - 'x - 42u'
        - x or now is the current date/time
        - u == time unit:  s, m, h, d, w, m, y
        - Default unit is d
            - Use -s for sec, -m for min, etc. for default unit
        - Allows aliases like
            - day to be 'date -d'
            - week to be 'date -w'
                - 'week x+6' gives 6 weeks from today
            - month to be 'date -m'
            - year to be 'date -y'
- Options
    - -u x is default time unit:  s, m, h, d, w, m, y
    - -f num is format
        - 0:  Long          18Nov2023 10:52:59 am Sat
        - 1:  Short         18Nov2023
        - 2:  Zulu          18Nov2023 10:52:59 GMT
        - 3:  24 hr long    18Nov2023 14:52:59 Sat
        - 4:  Julian        2460267.4570023147 JD

'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from datetime import datetime, timedelta
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from zoneinfo import ZoneInfo
    if 1:   # Custom imports
        from wrap import dedent, wrap
        from color import t
        from lwtest import Assert
        import months 
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        zi = ZoneInfo("America/Boise")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        wrap.width = W
        print(wrap(dedent(f'''

        Times and dates are not simple and have different standards,
        conventions, etc.  This results from the fact that the tropical
        year in astronomy is not a whole number of days.  This comes about
        because the Earth's orbital period is not an integer number of
        Earth's rotation period about its axis.  Because it's easy for us
        to count the number of e.g. mornings, humans want the astronomical
        year to be an integer number of days.  We've evolved rules for
        intercalation
        (https://en.wikipedia.org/wiki/Intercalation_(timekeeping)) that
        approximate this by inserting e.g. leap times to keep the calendar
        days aligned with the astronomical events.

        The actual solar year (time for Earth to go around the sun) is
        365.2425 days.  In the Gregorian calendar, 97 out of 400 years
        (97/400 == 0.2425) must be leap years to keep the calendar
        synchronized with orbital period of the Earth about the sun with
        respect to the "fixed" stars.

        The SI day is defined to be 24*3600 == 86400 seconds.
        https://en.wikipedia.org/wiki/Day_length_fluctuations shows
        interesting detail on how the measured length of a day varies over
        60 years starting in 1962, about 7 years after the invention of
        atomic clocks with the precision to make such measurements.  Note
        the vertical scale is 5 ms.  The small flucuations are caused by
        the changes in mass distribution over the Earth by things like
        tides, crustal movements, atmospheric changes, core and mantle
        changes, and perhaps other things.

        Earth's rotation rate has changed over time (see
        https://en.wikipedia.org/wiki/Tidal_acceleration#Historical_evidence
        and
        https://en.wikipedia.org/wiki/Tidal_acceleration#Effects_of_Moon's_gravity).
        If we waited long enough, the length of Earth's day would
        synchronize with the Moon's orbital period (gravitational locking),
        but this won't happen before the Earth and Moon are destroyed by
        the sun in about 4.5 Gyr when the sun becomes a red giant.  This
        slowdown is caused by tidal friction, meaning some of the
        Earth-Moon gravitational energy is dissipated in the Earth as heat
        (i.e., the system's gravitational energy isn't conserved). 

        ''')))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [expr]

          Show the current date/time.  If expr is given, it allows addition
          and subtraction of times from 'now', the current date/time.  Time
          unit abbreviations are the first letters of the words seconds,
          minutes, hours, days, weeks, months, years, and centuries.

          Allowed forms of expr:  +nu and -nu where n is a number and u is
          an optional cuddled time unit leter.

        Examples:
          '-3y' 
            Shows the date/time 3 years ago

          '-t 1Jun1950 +70y'

            Shows 70 years after 1 Jun 1950.  You know the result should be
            about in the year 2020, but the actual result is controlled by
            the underlying time calculational library.  Here, it's the
            python datetime library.

        Options:
          -d num  Number of decimals in Julian day numbers [{d["-d"]}]
          -f num  Select date/time format
                  0   Long    18Nov2023 10:52:59 am Sat
                  1   Short   18Nov2023
                  2   Zulu    18Nov2023 10:52:59 GMT
                  3   24 hr   18Nov2023 14:52:59 Sat
                  4   Julian  2460267.4570023147 JD
          -H      Print a manpage
          -h      Print usage
          -n s    Define the current date/time
          -u ltr  Output in these time units (first letter of seconds,
                  minutes, hours, days, weeks, months, years, and
                  centuries)
        Time format
            18Nov2023:10:52:59.123 
            - Case of the three month letters is ignored
            - Time is 24 hour form with hours:minutes:seconds
            - The seconds term can have arbitrary decimals
            - If the time portion is omitted, it is set to midnight
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 5         # Number of decimal digits in Julian days (5
                            # gives about 1 s resolution).
        d["-f"] = 0         # Date/time format (integer)
        d["-n"] = None      # Current date/time
        d["-u"] = None      # Time units for output (None means use default)
        d["-z"] = -7        # Hours offset from UTC
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:f:hn:u:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":     # Number of decimal places in Julian day
                try:
                    d[o] = int(a)
                    if not (0 <= d[o] <= 10):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 10")
                    Error(msg)
            elif o == "-f":     # Chose the date/time format
                low, high = 0, 4
                try:
                    d[o] = int(a)
                    if not (low <= d[o] <= high):
                        raise ValueError()
                except ValueError:
                    msg = ("-f option's argument must be an integer between "
                        "{low} and {high}")
                    Error(msg)
            elif o == "-H":     # Show the manpage
                Manpage()
            elif o == "-h":     # Show the manpage
                Usage(status=0)
            elif o == "-n":     # Define current date/time
                print("Missing code!")
                breakpoint() #xx
        return args
if 1:   # Core functionality
    def PrintDate(dt):
        'Print the date in the selected format'
        Assert(ii(dt, datetime))
        if d["-f"] == 0:        # 18Nov2023 10:52:59 am Sat
            pass
        elif d["-f"] == 1:      # 18Nov2023
            pass
        elif d["-f"] == 2:      # 18Nov2023 10:52:59 UTC
            pass
        elif d["-f"] == 3:      # 18Nov2023 14:52:59 Sat
            pass
        elif d["-f"] == 4:      # 2460267.4570023147 JD
        else:
            raise RuntimeError(f"Bad d['-f'] value of {d['-f']}")

    def ShowCurrentTime():
        '''Print the current time in the selected format to stdout.
        Note this ignores the -n option.
        '''
        PrintDate(datetime.now(zi))


if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if not args:
        ShowCurrentTime()
