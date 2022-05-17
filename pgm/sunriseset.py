'''
SUNRISET.C - computes Sun rise/set times, start/end of twilight, and
    the length of the day at any date and latitude
 
    Written as DAYLEN.C, 1989-08-16
 
    Modified to SUNRISET.C, 1992-12-01
 
    (c) Paul Schlyter, 1989, 1992
 
    Released to the public domain by Paul Schlyter, December 1992
 
    Direct conversion to Java
    Sean Russell <ser@germane-software.com>
 
    Conversion to Python Class, 2002-03-21

    ---------------------------------------------------------------------
    DP Validation Sun 24 Apr 2022:  I downloaded the sunrise/sunset data
    for 2022 for my location from the USNO site https://aa.usno.navy.mil/;
    a number of spot checks over Apr to Oct 2022 gave agreements within one
    minute (i.e., the least significant figure). 
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
    # Imports
        from datetime import datetime, date, timedelta
        import getopt
        import os
        from pathlib import Path as P
        import math
        import sys
        import time
        from collections import deque
        from pdb import set_trace as xx
    # Custom imports
        from wrap import dedent
        from months import months
        from color import TRM as t
        if 0:
            import debug
            debug.SetDebugger()
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Colors
        t.rise = t("ornl")
        t.set = t("redl")
        t.civ = t("viob")
        t.naut = t("blub")
        t.astro = t("grnb")
        t.hyp = t("whtl")
if 1:   # Location data
        # Boise, ID
        latitude = 43.64        # degrees
        longitude = -116.32     # degrees
        GMT_offset = -7         # Hours, to correct GMT to local time
        # These two definitions are the approximate dates DST starts and
        # end.  Python's datetime class documentation is abstruse and I
        # just wanted something simple.  These numbers are correct for
        # 2022, but will be wrong otherwise.
        yr = 2022
        dst_start = datetime(yr, 3, 13)
        dst_end   = datetime(yr, 11, 6)
        today = datetime.today()
        if dst_start.year != today.year:
            raise ValueError(f"{sys.argv[0]}:  Year wrong for DST calculations")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [year month day]
          Print sunrise/sunset and twilight times.  The default settings
          print out 6 months of data.
        Options:
            -h      Print a manpage
            -n n    Print n lines from given date [{d['-n']}]
            -r      Reverse the order of the lines
            -s n    Use n days between dates [{d['-s']}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-n"] = 26        # Number of lines to print
        d["-r"] = False     # Reverse printout
        d["-s"] = 7         # Number of days to step by
        try:
            opts, args = getopt.getopt(sys.argv[1:], "n:hrs:", ["help"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("r"):
                d[o] = not d[o]
            elif o in ("-n", "-s"):
                try:
                    d[o] = n = int(a)
                    if n < 1:
                        raise ValueError()
                except ValueError:
                    Error(f"{o} must be > 0")
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    class Sun:
        def __init__(self):
            pass
        def daysSince2000Jan0(self, y, m, d):
            '''Return the number of days elapsed since 2000 Jan 0.0
            (which is equal to 1999 Dec 31, 0h UT)
            '''
            return (367*(y)-((7*((y)+(((m)+9)/12)))/4)+((275*(m))/9)+(d)-730530)
        'The trigonometric functions in degrees'
        def sind(self, x):
            return math.sin(math.radians(x))
        def cosd(self, x):
            return math.cos(math.radians(x))
        def acosd(self, x):
            return math.degrees(math.acos(x))
        def atan2d(self, y, x):
            return math.degrees(math.atan2(y, x))
        '''Following are some functions around the "workhorse" function __daylen__
        They mainly fill in the desired values for the reference altitude
        below the horizon, and also selects whether this altitude should
        refer to the Sun's center or its upper limb.
        '''
        def dayLength(self, year, month, day, lon, lat):
            '''Returns the length of the day, from sunrise to sunset.
            Sunrise/set is considered to occur when the Sun's upper limb is
            35 arc minutes below the horizon (this accounts for the refraction
            of the Earth's atmosphere).
            '''
            return self.__daylen__(year, month, day, lon, lat, -35/60, 1)
        def dayCivilTwilightLength(self, year, month, day, lon, lat):
            '''Returns the length of the day, including civil twilight.
            Civil twilight starts/ends when the Sun's center is 6 degrees below
            the horizon.
            '''
            return self.__daylen__(year, month, day, lon, lat, -6, 0)
        def dayNauticalTwilightLength(self, year, month, day, lon, lat):
            '''Returns the length of the day, incl. nautical twilight.
            Nautical twilight starts/ends when the Sun's center is 12 degrees
            below the horizon.
            '''
            return self.__daylen__(year, month, day, lon, lat, -12, 0)
        def dayAstronomicalTwilightLength(self, year, month, day, lon, lat):
            '''Returns the length of the day, incl. astronomical twilight.
            Astronomical twilight starts/ends when the Sun's center is 18 degrees
            below the horizon.
            '''
            return self.__daylen__(year, month, day, lon, lat, -18, 0)
        def sunRiseSet(self, year, month, day, lon, lat):
            '''Returns (sunrise, sunset) times.
            Sunrise/set is considered to occur when the Sun's upper limb is
            35 arc minutes below the horizon (this accounts for the refraction
            of the Earth's atmosphere).
            '''
            return self.__sunriset__(year, month, day, lon, lat, -35/60, 1)
        def civilTwilight(self, year, month, day, lon, lat):
            '''Returns (start_time, end_time) of civil twilight.
            Civil twilight starts/ends when the Sun's center is 6 degrees below
            the horizon.
            '''
            return self.__sunriset__(year, month, day, lon, lat, -6, 0)
        def nauticalTwilight(self, year, month, day, lon, lat):
            '''Returns (start_time, end_time) of nautical twilight.
            Nautical twilight starts/ends when the Sun's center is 12 degrees
            below the horizon.
            '''
            return self.__sunriset__(year, month, day, lon, lat, -12, 0)
        def astronomicalTwilight(self, year, month, day, lon, lat):
            '''Returns (start_time, end_time) of astronomical twilight.
            Astronomical twilight starts/ends when the Sun's center is 18 degrees
            below the horizon.
            '''
            return self.__sunriset__(year, month, day, lon, lat, -18, 0)
        def __sunriset__(self, year, month, day, lon, lat, altit, upper_limb):
            # The "workhorse" function for sun rise/set times
            '''
            Note: year,month,date = calendar date, 1801-2099 only.
                Eastern longitude positive, Western longitude negative
                Northern latitude positive, Southern latitude negative
                The longitude value IS critical in this function!
                altit = the altitude which the Sun should cross
                        Set to -35/60 degrees for rise/set, -6 degrees
                        for civil, -12 degrees for nautical and -18
                        degrees for astronomical twilight.
                    upper_limb: non-zero -> upper limb, zero -> center
                        Set to non-zero (e.g. 1) when computing rise/set
                        times, and to zero when computing start/end of
                        twilight.
                *rise = where to store the rise time
                *set  = where to store the set  time
                        Both times are relative to the specified altitude,
                        and thus this function can be used to compute
                        various twilight times, as well as rise/set times
            Return value:  0 = sun rises/sets this day, times stored at
                            *trise and *tset.
                        +1 = sun above the specified 'horizon' 24 hours.
                            *trise set to time when the sun is at south,
                            minus 12 hours while *tset is set to the south
                            time plus 12 hours. 'Day' length = 24 hours
                        -1 = sun is below the specified 'horizon' 24 hours
                            'Day' length = 0 hours, *trise and *tset are
                                both set to the time when the sun is at south.
            '''
            # Compute d of 12h local mean solar time
            d = self.daysSince2000Jan0(year, month, day) + 0.5 - (lon/360)
            # Compute local sidereal time of this moment
            sidtime = self.revolution(self.GMST0(d) + 180 + lon)
            # Compute Sun's RA + Decl at this moment
            res = self.sunRADec(d)
            sRA = res[0]
            sdec = res[1]
            sr = res[2]
            # Compute time when Sun is at south - in hours UT
            tsouth = 12 - self.rev180(sidtime - sRA)/15
            # Compute the Sun's apparent radius, degrees
            sradius = 0.2666/sr
            # Do correction to upper limb, if necessary
            if upper_limb:
                altit = altit - sradius
            # Compute the diurnal arc that the Sun traverses to reach
            # the specified altitude altit:
            cost = ((self.sind(altit) - self.sind(lat) *
                    self.sind(sdec))/(self.cosd(lat)*self.cosd(sdec)))
            if cost >= 1:
                rc = -1
                t = 0             # Sun always below altit
            elif cost <= -1:
                rc = +1
                t = 12            # Sun always above altit
            else:
                t = self.acosd(cost)/15     # The diurnal arc, hours
            # Store rise and set times - in hours UT
            return (tsouth - t, tsouth + t)
        def __daylen__(self, year, month, day, lon, lat, altit, upper_limb):
            '''
            Note: year,month,date = calendar date, 1801-2099 only.
                Eastern longitude positive, Western longitude negative
                Northern latitude positive, Southern latitude negative
                The longitude value is not critical. Set it to the correct
                longitude if you're picky, otherwise set to to, say, 0.0
                The latitude however IS critical - be sure to get it correct
                altit = the altitude which the Sun should cross
                        Set to -35/60 degrees for rise/set, -6 degrees
                        for civil, -12 degrees for nautical and -18
                        degrees for astronomical twilight.
                    upper_limb: non-zero -> upper limb, zero -> center
                        Set to non-zero (e.g. 1) when computing day length
                        and to zero when computing day+twilight length.
            '''
            assert(1800 < year < 2100)
            # Compute d of 12h local mean solar time
            d = self.daysSince2000Jan0(year, month, day) + 0.5 - (lon/360)
            # Compute obliquity of ecliptic (inclination of Earth's axis)
            obl_ecl = 23.4393 - 3.563e-7*d
            # Compute Sun's position
            res = self.sunpos(d)
            slon = res[0]
            sr = res[1]
            # Compute sine and cosine of Sun's declination
            sin_sdecl = self.sind(obl_ecl)*self.sind(slon)
            cos_sdecl = math.sqrt(1 - sin_sdecl*sin_sdecl)
            # Compute the Sun's apparent radius, degrees
            sradius = 0.2666 / sr
            # Do correction to upper limb, if necessary
            if upper_limb:
                altit = altit - sradius
            cost = ((self.sind(altit) - self.sind(lat)*sin_sdecl)/
                    (self.cosd(lat)*cos_sdecl))
            if cost >= 1:
                t = 0         # Sun always below altit
            elif cost <= -1:
                t = 24        # Sun always above altit
            else:
                t = 2/15*self.acosd(cost)      # The diurnal arc, hours
            return t
        def sunpos(self, d):
            '''
            Computes the Sun's ecliptic longitude and distance
            at an instant given in d, number of days since
            2000 Jan 0.0.  The Sun's ecliptic latitude is not
            computed, since it's always very near 0.
            '''
            # Compute mean elements
            M = self.revolution(356.0470 + 0.9856002585*d)
            w = 282.9404 + 4.70935e-5*d
            e = 0.016709 - 1.151e-9*d
            # Compute true longitude and radius vector
            E = M + e*180/math.pi*self.sind(M)*(1 + e*self.cosd(M))
            x = self.cosd(E) - e
            y = math.sqrt(1 - e*e)*self.sind(E)
            r = math.sqrt(x*x + y*y)              # Solar distance
            v = self.atan2d(y, x)                 # True anomaly
            lon = v + w                           # True solar longitude
            if lon >= 360:
                lon = lon - 360                   # Make it 0..360 degrees
            return (lon, r)
        def sunRADec(self, d):
            # Compute Sun's ecliptical coordinates
            res = self.sunpos(d)
            lon = res[0]
            r = res[1]
            #Compute ecliptic rectangular coordinates (z=0)
            x = r*self.cosd(lon)
            y = r*self.sind(lon)
            # Compute obliquity of ecliptic (inclination of Earth's axis)
            obl_ecl = 23.4393 - 3.563e-7*d
            # Convert to equatorial rectangular coordinates - x is unchanged
            z = y*self.sind(obl_ecl)
            y = y*self.cosd(obl_ecl)
            # Convert to spherical coordinates
            RA = self.atan2d(y, x)
            dec = self.atan2d(z, math.sqrt(x*x + y*y))
            return (RA, dec, r)
        def revolution(self, x):
            '''
            This function reduces any angle to within the first revolution
            by subtracting or adding even multiples of 360.0 until the
            result is >= 0.0 and < 360
    
            Reduce angle to within 0..360 degrees
            '''
            return (x - 360*math.floor(x/360))
        def rev180(self, x):
            '''
            Reduce angle to within +180..+180 degrees
            '''
            return (x - 360*math.floor(x/360 + 0.5))
        def GMST0(self, d):
            '''
            This function computes GMST0, the Greenwich Mean Sidereal Time
            at 0h UT (i.e. the sidereal time at the Greenwhich meridian at
            0h UT).  GMST is then the sidereal time at Greenwich at any
            time of the day.  I've generalized GMST0 as well, and define it
            as:  GMST0 = GMST - UT  --  this allows GMST0 to be computed at
            other times than 0h UT as well.  While this sounds somewhat
            contradictory, it is very practical:  instead of computing
            GMST like:
    
            GMST = (GMST0) + UT*(366.2422/365.2422)
    
            where (GMST0) is the GMST last time UT was 0 hours, one simply
            computes:
    
            GMST = GMST0 + UT
    
            where GMST0 is the GMST "at 0h UT" but at the current moment!
            Defined in this way, GMST0 will increase with about 4 min a
            day.  It also happens that GMST0 (in degrees, 1 hr = 15 degr)
            is equal to the Sun's mean longitude plus/minus 180 degrees!
            (if we neglect aberration, which amounts to 20 seconds of arc
            or 1.33 seconds of time)
            '''
            # Sidtime at 0h UT = L (Sun's mean longitude) + 180.0 degr
            # L = M + w, as defined in sunpos().  Since I'm too lazy to
            # add these numbers, I'll let the C compiler do it for me.
            # Any decent C compiler will add the constants at compile
            # time, imposing no runtime or code overhead.
            sidtim0 = self.revolution((180 + 356.0470 + 282.9404) +
                                    (0.9856002585 + 4.70935e-5)*d)
            return sidtim0
    def PrintSunriseSunset_orig(year, month, day):
        S = Sun()
        assert(1 <= month <= 12)
        T = "%s %s %s" % (day, months[month], year)
        t = "%s %s %s" % (year, month, day)
        times = S.sunRiseSet(year, month, day, longitude, latitude)
        print("For Boise, Idaho %s" % T)
        Print("Sunrise, sunset", times)
        times = S.civilTwilight(year, month, day, longitude, latitude)
        Print("Civil twilight", times)
        times = S.nauticalTwilight(year, month, day, longitude, latitude)
        Print("Nautical twilight", times)
        times = S.astronomicalTwilight(year, month, day, longitude, latitude)
        Print("Astronomical twilight", times)
        print("Add 1 hour if daylight saving time is in effect")
    def PrintHeader():
        print(dedent(f'''
        For Boise, ID
                                       {t.hyp}-------------- Twilight ---------------{t.n}
        '''))
        print(f"                  {t.rise}Rise  {t.set}Set{t.n}       ", end="")
        print(f"{t.civ}Civil{t.n}        {t.naut}Nautical{t.n}   {t.astro}Astronomical{t.n}")
        print(f"                 {t.hyp}-----------   -----------   -----------   -----------{t.n}")
    def DST(date):
        'Return True if DST is on'
        if dst_start < date < dst_end:
            return True
        return False
    def Correct(decimal_hours, date):
        # Change UT to local time
        hours = int(decimal_hours) + GMT_offset    # UT to local time
        minutes = int((decimal_hours - hours)*60) % 60
        if hours > 12:
            hours -= 12
        # If daylight savings is on, add 1 hour.
        if DST(date):
            hours += 1
            if hours > 12:
                hours -= 12
        return "%2d:%02d" % (hours, minutes)
    def Get(date, times, clr1="", clr2=""):
        rise = Correct(times[0], date)
        set = Correct(times[1], date)
        return f"{clr1}{rise:5s} {clr2}{set:5s}{t.n}   "
    def GetSunriseSunset(year, month, day):
        'Return a string for this day'
        S = Sun()
        dt = datetime(year, month, day, 12)
        dow = "Mon Tue Wed Thu Fri Sat Sun".split()[dt.weekday()]
        # Print the date
        today = date.today()
        s = ""
        if today.year == year and today.month == month and today.day == day:
            s = t("grnl")
        T = f"{day:2d} {months[month]} {year}"
        out = [f"{s}{dow} {T}{t.n} "]
        times = S.sunRiseSet(year, month, day, longitude, latitude)
        out.append(Get(dt, times, t.rise, t.set))
        times = S.civilTwilight(year, month, day, longitude, latitude)
        out.append(Get(dt, times, t.civ, t.civ))
        times = S.nauticalTwilight(year, month, day, longitude, latitude)
        out.append(Get(dt, times, t.naut, t.naut))
        times = S.astronomicalTwilight(year, month, day, longitude, latitude)
        out.append(Get(dt, times, t.astro, t.astro))
        # Need to correct for DST #xx
        return ''.join(out)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if args:
        year, month, day = [int(i) for i in sys.argv[1:]]
        target = date(year, month, date)
    else:
        target = date.today()
    incr = timedelta(days=d["-s"])
    target -= incr
    n = d["-n"]
    PrintHeader()
    out = deque()
    while n:
        n -= 1
        target += incr
        year, month, day = target.year, target.month, target.day
        out.append(GetSunriseSunset(year, month, day))
    # Print them so that the current day is the last printed
    while out:
        if d["-r"]:
            print(out.pop())
        else:
            print(out.popleft())
