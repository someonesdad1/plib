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
Henrik H?rk?nen <radix@kortis.to>

Minor modifications by Don Peterson
'''

if 1:   # Imports
    import math
    import sys
    import time
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from months import months
class Sun:
    def __init__(self):
        # Some conversion factors between radians and degrees
        self.PI = 3.1415926535897932384
        self.RADEG = 180.0 / self.PI
        self.DEGRAD = self.PI / 180.0
        self.INV360 = 1.0 / 360.0
    def daysSince2000Jan0(self, y, m, d):
        '''A macro to compute the number of days elapsed since 2000 Jan 0.0
           (which is equal to 1999 Dec 31, 0h UT)'''
        return (367*(y)-((7*((y)+(((m)+9)/12)))/4)+((275*(m))/9)+(d)-730530)
    # The trigonometric functions in degrees
    def sind(self, x):
        '''Returns the sin in degrees'''
        return math.sin(x*self.DEGRAD)
    def cosd(self, x):
        '''Returns the cos in degrees'''
        return math.cos(x*self.DEGRAD)
    def acosd(self, x):
        '''Returns the acos in degrees'''
        return math.acos(x)*self.RADEG
    def atan2d(self, y, x):
        '''Returns the atan2 in degrees'''
        return math.atan2(y, x)*self.RADEG
    # Following are some macros around the "workhorse" function __daylen__
    # They mainly fill in the desired values for the reference altitude
    # below the horizon, and also selects whether this altitude should
    # refer to the Sun's center or its upper limb.
    def dayLength(self, year, month, day, lon, lat):
        '''
        This macro computes the length of the day, from sunrise to sunset.
        Sunrise/set is considered to occur when the Sun's upper limb is
        35 arc minutes below the horizon (this accounts for the refraction
        of the Earth's atmosphere).
        '''
        return self.__daylen__(year, month, day, lon, lat, -35.0/60.0, 1)
    def dayCivilTwilightLength(self, year, month, day, lon, lat):
        '''
        This macro computes the length of the day, including civil twilight.
        Civil twilight starts/ends when the Sun's center is 6 degrees below
        the horizon.
        '''
        return self.__daylen__(year, month, day, lon, lat, -6.0, 0)
    def dayNauticalTwilightLength(self, year, month, day, lon, lat):
        '''
        This macro computes the length of the day, incl. nautical twilight.
        Nautical twilight starts/ends when the Sun's center is 12 degrees
        below the horizon.
        '''
        return self.__daylen__(year, month, day, lon, lat, -12.0, 0)
    def dayAstronomicalTwilightLength(self, year, month, day, lon, lat):
        '''
        This macro computes the length of the day, incl. astronomical twilight.
        Astronomical twilight starts/ends when the Sun's center is 18 degrees
        below the horizon.
        '''
        return self.__daylen__(year, month, day, lon, lat, -18.0, 0)
    def sunRiseSet(self, year, month, day, lon, lat):
        '''
        This macro computes times for sunrise/sunset.
        Sunrise/set is considered to occur when the Sun's upper limb is
        35 arc minutes below the horizon (this accounts for the refraction
        of the Earth's atmosphere).
        '''
        return self.__sunriset__(year, month, day, lon, lat, -35.0/60.0, 1)
    def civilTwilight(self, year, month, day, lon, lat):
        '''
        This macro computes the start and end times of civil twilight.
        Civil twilight starts/ends when the Sun's center is 6 degrees below
        the horizon.
        '''
        return self.__sunriset__(year, month, day, lon, lat, -6.0, 0)
    def nauticalTwilight(self, year, month, day, lon, lat):
        '''
        This macro computes the start and end times of nautical twilight.
        Nautical twilight starts/ends when the Sun's center is 12 degrees
        below the horizon.
        '''
        return self.__sunriset__(year, month, day, lon, lat, -12.0, 0)
    def astronomicalTwilight(self, year, month, day, lon, lat):
        '''
        This macro computes the start and end times of astronomical twilight.
        Astronomical twilight starts/ends when the Sun's center is 18 degrees
        below the horizon.
        '''
        return self.__sunriset__(year, month, day, lon, lat, -18.0, 0)
    # The "workhorse" function for sun rise/set times
    def __sunriset__(self, year, month, day, lon, lat, altit, upper_limb):
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
        d = self.daysSince2000Jan0(year, month, day) + 0.5 - (lon/360.0)
        # Compute local sidereal time of this moment
        sidtime = self.revolution(self.GMST0(d) + 180.0 + lon)
        # Compute Sun's RA + Decl at this moment
        res = self.sunRADec(d)
        sRA = res[0]
        sdec = res[1]
        sr = res[2]
        # Compute time when Sun is at south - in hours UT
        tsouth = 12.0 - self.rev180(sidtime - sRA)/15.0
        # Compute the Sun's apparent radius, degrees
        sradius = 0.2666/sr
        # Do correction to upper limb, if necessary
        if upper_limb:
            altit = altit - sradius
        # Compute the diurnal arc that the Sun traverses to reach
        # the specified altitude altit:
        cost = ((self.sind(altit) - self.sind(lat) *
                self.sind(sdec))/(self.cosd(lat)*self.cosd(sdec)))
        if cost >= 1.0:
            rc = -1
            t = 0.0           # Sun always below altit
        elif cost <= -1.0:
            rc = +1
            t = 12.0          # Sun always above altit
        else:
            t = self.acosd(cost)/15.0   # The diurnal arc, hours
        # Store rise and set times - in hours UT
        return (tsouth-t, tsouth+t)
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
        d = self.daysSince2000Jan0(year, month, day) + 0.5 - (lon/360.0)
        # Compute obliquity of ecliptic (inclination of Earth's axis)
        obl_ecl = 23.4393 - 3.563E-7*d
        # Compute Sun's position
        res = self.sunpos(d)
        slon = res[0]
        sr = res[1]
        # Compute sine and cosine of Sun's declination
        sin_sdecl = self.sind(obl_ecl)*self.sind(slon)
        cos_sdecl = math.sqrt(1.0 - sin_sdecl*sin_sdecl)
        # Compute the Sun's apparent radius, degrees
        sradius = 0.2666 / sr
        # Do correction to upper limb, if necessary
        if upper_limb:
            altit = altit - sradius

        cost = ((self.sind(altit) - self.sind(lat)*sin_sdecl) /
                (self.cosd(lat)*cos_sdecl))
        if cost >= 1.0:
            t = 0.0             # Sun always below altit
        elif cost <= -1.0:
            t = 24.0      # Sun always above altit
        else:
            t = (2.0/15.0)*self.acosd(cost)      # The diurnal arc, hours
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
        w = 282.9404 + 4.70935E-5*d
        e = 0.016709 - 1.151E-9*d
        # Compute true longitude and radius vector
        E = M + e*self.RADEG*self.sind(M)*(1.0 + e*self.cosd(M))
        x = self.cosd(E) - e
        y = math.sqrt(1.0 - e*e)*self.sind(E)
        r = math.sqrt(x*x + y*y)              # Solar distance
        v = self.atan2d(y, x)                 # True anomaly
        lon = v + w                           # True solar longitude
        if lon >= 360.0:
            lon = lon - 360.0   # Make it 0..360 degrees
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
        obl_ecl = 23.4393 - 3.563E-7*d
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
        result is >= 0.0 and < 360.0
 
        Reduce angle to within 0..360 degrees
        '''
        return (x - 360.0*math.floor(x*self.INV360))
    def rev180(self, x):
        '''
        Reduce angle to within +180..+180 degrees
        '''
        return (x - 360.0*math.floor(x*self.INV360 + 0.5))
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
        sidtim0 = self.revolution((180.0 + 356.0470 + 282.9404) +
                                  (0.9856002585 + 4.70935E-5)*d)
        return sidtim0
if __name__ == "__main__":
    # Prints out today's sunrise/sunset.  If you include arguments on the
    # command line, they must be year, month, and day.
    k = Sun()
    # Boise, ID
    latitude = 43.64        # degrees
    longitude = -116.32     # degrees
    if len(sys.argv) > 1:
        if len(sys.argv) != 4:
            print(dedent(f'''
            sys.argv[0] [year month day]
              Prints sunrise and sunset for the given day.
            '''))
            exit(1)
        year, month, day = [int(i) for i in sys.argv[1:]]
        assert(1 <= month <= 12)
        T = "%s %s %s" % (day, months[month], year)
        t = "%s %s %s" % (year, month, day)
    else:
        t = time.strftime("%Y %m %d")
        T = time.strftime("%d %b %Y")
        year, month, day = [int(i) for i in t.split()]
    times = k.sunRiseSet(year, month, day, longitude, latitude)
    def Correct(decimal_hours):
        # Change UT to MST
        hr = int(decimal_hours) - 7  # Adjust UT to MST
        min = int((decimal_hours - hr)*60) % 60
        if hr > 12:
            hr -= 12
        # If daylight savings is on, add 1 hour.
        dst = False
        # DP:  I've disabled this feature
        if 0 and time.daylight:
            dst = True
            hr += 1
            if hr > 12:
                hr -= 12
        return "%2d:%02d" % (hr, min), dst
    def Print(s, times):
        ta, dst = Correct(times[0])
        tb, dst = Correct(times[1])
        is_dst = ""
        if dst:
            is_dst = "(DST)"
        diff = times[1] - times[0]
        #print("  %-25s %s am  %s pm %s (%.1f hr/%.1f hr)" % 
        #    (s, ta, tb, is_dst, diff, 24 - diff))
        print(f"  {s:25s} {ta} am  {tb} pm {is_dst}")
    print("For Boise, Idaho %s" % T)
    Print("Sunrise, sunset", times)
    times = k.civilTwilight(year, month, day, longitude, latitude)
    Print("Civil twilight", times)
    times = k.nauticalTwilight(year, month, day, longitude, latitude)
    Print("Nautical twilight", times)
    times = k.astronomicalTwilight(year, month, day, longitude, latitude)
    Print("Astronomical twilight", times)
    print("Add 1 hour if daylight saving time is in effect")
