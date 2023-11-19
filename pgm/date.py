'''
Replacement for /bin/date

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
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent, wrap
        from color import t
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
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
        approximate this by inserting leap days, etc. into our times to
        keep the calendar days aligned with the astronomical events.

        The actual solar year (time for Earth to go around the sun) is
        365.2425 days.  In the Gregorian calendar, 97 out of 400 years
        (97/400 == 0.2425) must be leap years to keep the calendar
        synchronized with orbital workings of the Earth about the sun.

        The SI day is defined to be 24*3600 == 86400 seconds.
        https://en.wikipedia.org/wiki/Day_length_fluctuations shows
        interesting detail on how the measured length of a day varies over
        60 years starting in 1962, about 7 years after the invention of
        suitably-precise atomic clocks.  Note the vertical scale is 5 ms.
        The small flucuations are caused by the changes in mass
        distribution over the Earth by things like tides, crustal
        movements, atmospheric changes, core and mantle changes, and
        perhaps other things.

        Earth's rotation rate has changed over time (see
        https://en.wikipedia.org/wiki/Tidal_acceleration#Historical_evidence
        and
        https://en.wikipedia.org/wiki/Tidal_acceleration#Effects_of_Moon's_gravity).
        If we waited long enough, the length of Earth's day would
        synchronize with the Moon's orbital period (gravitational locking),
        but this won't happen before e.g. the Earth's oceans boil away in
        about 1 Gyr.  This slowdown is caused by tidal friction, causing
        gravitational energy to be dissipated in the Earth, resulting in
        the Earth-Moon system to lose energy (i.e., some gravitational
        energy is converted to heat, indicating gravitational energy isn't
        conserved).  This slowdown is so slow that it equal a month before
        the sun becomes a red giant in 4.5 Gyr and destroys both the Earth
        and Moon.


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
          -h      Print a manpage
          -n s    Define the current date/time
          -t s    Define the current time using the time format
          -u ltr  Output in these time units (first letter of seconds,
                  minutes, hours, days, weeks, months, years, and
                  centuries)
        Time format
            18Nov2023:10:52:59.123 
            - Case of the three month letters is ignored
            - Time is 24 hour form with hours:minutes:seconds
            - The seconds term can have arbitrary decimals
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 5         # Number of decimal digits in Julian days
        d["-f"] = 0         # Date/time format (integer)
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:f:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (0 <= d[o] <= 10):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 10")
                    Error(msg)
            elif o == "-f":
                low, high = 0, 4
                try:
                    d[o] = int(a)
                    if not (low <= d[o] <= high):
                        raise ValueError()
                except ValueError:
                    msg = ("-f option's argument must be an integer between "
                        "{low} and {high}")
                    Error(msg)
            elif o == "-h":
                Manpage()
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
