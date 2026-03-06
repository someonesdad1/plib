'''

ToDo
    - Collapse things into a more sensible set of functions

Various astronomical routines
        
'''
if 1:  # Header
    if 1:   # Standard imports
        import collections
        import datetime
        import enum
        import functools
        import getopt
        import math
        import operator
        import os
        import pathlib
        import re
        import sys
        import time
    if 1:   # Custom imports
        import columnize
        import dpstr
        import dpmath
        import dptime
        import dptypes
        import f
        import lwtest
        import trm
        import wrap
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Import symbols
        Path = pathlib.Path
        defaultdict = collections.defaultdict
        deque = collections.deque
        reduce = functools.reduce
        namedtuple = collections.namedtuple
        #
        Assert = lwtest.Assert
        Columnize = columnize.Columnize
        dedent = wrap.dedent
        flt = f.flt
        t = trm.Trm()
    if 1:   # Global variables
        g = dptypes.Constant()
        g.dbg = False
        g.earth_equatorial_radius_km = 6378.14
        g.earth_flattening = 1/298.257
        g.earth_meridian_eccentricity = math.sqrt(2/298.257 - 1/298.257**2)
        g.minimum_year = -4712
        g.max_iterations = 120
if 1:  # Julian day 
    def JD(year, month, day, hour=0, minute=0, second=0):
        '''Return astronomical Julian Day, a float.
        All arguments are integers except day and second can also be floats.
        '''
        # Algorithm from pg 62 of Meeus, "Astronomical Algorithms", 2nd ed., 1998
        if 1:   # Check parameter types
            for i in (year, month, hour, minute):
                if not isinstance(i, int):
                    msg = "year, month, day, hour, and minute must be int"
                    raise TypeError(msg)
            if not isinstance(second, (int, float)):
                raise TypeError("second must be an int or float")
            if not isinstance(day, (int, float)):
                raise TypeError("day must be an int or float")
        floor = math.floor
        # Convert time of day to fractional day
        frac_day = (hour + minute/60 + second/3600)/24.0
        # Adjust month/year so March = 3 ... February = 14 of previous year
        if month <= 2:
            year -= 1
            month += 12
        # Determine if Gregorian calendar correction applies
        if (year > 1582) or (year == 1582 and (month > 10 or (month == 10 and day >= 15))):
            A = floor(year/100)
            B = 2 - A + floor(A/4)
        elif (year < 1582) or (year == 1582 and (month < 10 or (month == 10 and day <= 4))):
            B = 0
        else:
            raise ValueError("Date falls within the Gregorian calendar transition gap (1582-10-05 to 1582-10-14).")
        jd = (floor(365.25*(year + 4716)) + floor(30.6001*(month + 1)) + day + B - 1524.5)
        return jd + frac_day
    def DT2JD(datetime_instance):
        '''Return astronomical Julian Day, a float.
        The date/time is a datetime.datetime instance.
        '''
        dt = datetime_instance
        year, month, day, hour, minute, second, microsecond = (dt.year, dt.month,
            dt.day, dt.hour, dt.minute, dt.second, dt.microsecond)
        second += microsecond/1e6
        return JD(year, month, day, hour, minute, second)
    def JD2DT(julian_day):  # Meeus pg 63
        'Return a datetime.datetime instance for a Julian day'
        if julian_day < 0:
            raise ValueError("Bad input value")
        jd = julian_day + 0.5
        Z = int(jd)
        F = jd - Z
        A = Z
        if Z >= 2299161:
            alpha = int((Z - 1867216.26)/36254.25)
            A = Z + 1 + alpha - alpha//4
        B = A + 1524
        C = int((B - 122.1)/365.25)
        D = int(365.25*C)
        E = int((B - D)/30.6001)
        day_ = B - D - int(30.6001*E) + F
        if E < 13.5:
            month = int(E - 1)
        else:
            month = int(E - 13)
        if month > 2.5:
            year = int(C - 4716)
        else:
            year = int(C - 4715)
        day_int = int(day_)
        day_fp = day_ - day_int
        days, hr, min, sec_ = DaysToHMS(day_fp)
        sec = math.floor(sec_)
        usec = int((sec_ - sec)*1e6)
        dt = datetime.datetime(year, month, day_int, hr, min, sec, usec)
        return dt
    def JD2MonthDayYear(jd):    # Meeus pg 63
        '''Returns (month, day, year) given the Julian day jd.  month and year are
        integers; day may be an integer or float.
        '''
        Assert(jd >= 0, "Julian day must be >= 0")
        jd += 0.5
        Z = int(jd)
        F = jd - Z
        A = Z
        if Z >= 2299161:
            alpha = int((Z - 1867216.25) / 36524.25)
            A = Z + 1 + alpha - int(alpha / 4)
        B = A + 1524
        C = int((B - 122.1) / 365.25)
        D = int(365.25 * C)
        E = int((B - D) / 30.6001)
        day = B - D - int(30.6001 * E) + F
        if E < 14:
            month = int(E - 1)
        else:
            month = int(E - 13)
        if month > 2:
            year = int(C - 4716)
        else:
            year = int(C - 4715)
        return month, day, year  # month, year are integers
    def NumDaysInMonth(month, year):
        if month == 2:
            return 29 if IsLeapYear(year) else 28
        elif month in set((4, 6, 9, 11)):
            return 30
        elif month in set((1, 3, 5, 7, 8, 10, 12)):
            return 31
        else:
            raise ValueError("Bad month")
    def IsLeapYear(year):   # Meeus pg 62
        return True if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0) else False
    def DaysToHMS(numdays):
        '''Return a tuple of (days, hours, minutes, seconds) given a number of days.
        days, hours, and minutes are integers; seconds is a float or an integer.
        '''
        if numdays < 0:
            raise ValueError("numdays should be >= 0")
        day_int = math.floor(numdays)
        frac_part = numdays - math.floor(numdays)
        hours = int(24*frac_part)
        frac_part -= hours/24
        minutes = int(24*60*frac_part)
        frac_part -= minutes/(24*60)
        seconds = 24*3600*frac_part
        return (day_int, hours, minutes, seconds)
    def DayOfYear(month, day, year):    # Meeus pg 65
        'Return the integer day of the year on [1, 366]'
        k = 1 if IsLeapYear(year) else 2
        n = int(275*month/9) - k*int((month + 9)/12) + int(day) - 30
        assert 1 <= n <= 366, "month, day, year inappropriate"
        return n
    def DayOfWeek(month, day, year):    # Meeus pg 65
        'Return day of the week (0 == Sunday, 1 == Monday, etc.)'
        julian = int(JD(year, month, int(day)) + 1.5)
        return julian % 7
    def IsValidDate(month, day, year):
        '''Returns True if the year is later than 1752 and the month and day
        numbers are valid.
        '''
        if (month < 1 or month > 12) or (int(month) != month) or (year < 1753) or (day < 1):
            return False
        if isinstance(day, float):
            if month == 2:
                if IsLeapYear(year):
                    if day >= 30:
                        return False
                else:
                    if day >= 29:
                        return False
            elif month in (4, 6, 9, 11):
                if day >= 31:
                    return False
            else:
                if day >= 32:
                    return False
        else:
            assert isinstance(day, int), "day must be int or float"
            if month == 2:
                if IsLeapYear(year):
                    if day > 29:
                        return False
                else:
                    if day > 28:
                        return False
            elif month in (4, 6, 9, 11):
                if day > 30:
                    return False
            else:
                if day > 31:
                    return False
        return True
if 1:  # Utility
    def hms2rad(hours, minutes, seconds):
        'Converts angular measure in hours, minutes, seconds to radians'
        # One hour = 360/24 = 15 degrees
        assert isinstance(hours, int), "hours must be an integer"
        assert isinstance(minutes, int), "minutes must be an integer"
        assert hours >= 0, "hours must be >= 0"
        assert minutes >= 0, "minutes must be >= 0"
        assert seconds >= 0, "seconds must be >= 0"
        decimal_hours = hours + minutes/60 + seconds/3600
        return math.radians(decimal_hours*15)
    def dms2rad(d, m, s):
        '''Converts angular measure in degrees, minutes, seconds to radians.
        The result will have the sign of d.
        '''
        assert isinstance(d, int), "d must be an integer"
        assert isinstance(m, int), "m must be an integer"
        assert m >= 0, "m must be >= 0"
        assert s >= 0, "s must be >= 0"
        deg = abs(d) + abs(m)/60 + abs(s)/3600
        return math.radians(dpmath.signum(d)*deg)
    def hr2hms(hr):
        '''Return a tuple (hours, minutes, seconds) of a decimal hour value hr.  hours will have
        the sign of hr.
        '''
        h = int(abs(hr))
        m = 60*(abs(hr) - h)
        s = 60*(m - int(m))
        return dpmath.signum(hr)*h, int(m), s
    def rad2dms(x):
        '''Return a tuple (degrees, minutes, seconds) of a radian value.  The degrees value will
        have the sign of x.
        '''
        sig = dpmath.signum(x)
        x = math.fabs(x)
        d = math.degrees(x)
        deg = int(d)
        min = 60*(d - deg)
        sec = 60*(min - int(min))
        return sig*deg, int(min), sec
    def rad2hms(x):
        "Return a tuple (hour, minutes, seconds) of a radian value"
        return rad2dms(x/15)
    def product(x):
        "Returns the product of the components of the iterable x"
        return reduce(operator.mul, x)
    def LinearRegression(X, Y):     # Meeus pg 36
        '''Returns a tuple (slope, intercept, correlation) from the linear regression of
        Y against X.  X and Y are sequences of the abscissas and ordinates,
        respectively; they must be of the same size.
        '''
        def sq(x):
            return x*x
        def prod(x, y):
            return x*y
        assert len(X) == len(Y), "X and Y must be sequences of the same size"
        N, sx, sy = len(X), sum(X), sum(Y)
        sxx, syy, sxy = sum(map(sq, X)), sum(map(sq, Y)), sum(map(prod, X, Y))
        denomx, denomy = N*sxx - sx*sx, N*syy - sy*sy
        if not denomx or not denomy:
            raise ValueError("Regression equation denominator is zero")
        slope = (N*sxy - sx*sy)/denomx
        intercept = (sy*sxx - sx*sxy)/denomx
        R = (N*sxy - sx*sy)/math.sqrt(denomx*denomy)
        assert -1 <= R <= 1, "Correlation coefficient out of range"
        return (slope, intercept, R)
    def AngularSeparation(ra1, dec1, ra2, dec2):    # Meeus pg 109
        '''Returns the angular separation in radians between two bodies at (ra1, dec1)
        and (ra2, dec2).  ra is right ascension and dec is declination, both in radians.
        '''
        d = math.acos(math.sin(dec1)*math.sin(dec2) + math.cos(dec1)*math.cos(dec2)*math.cos(ra1 - ra2))
        if d < 1/60:
            # Use an approximation for small angles
            a = (ra1 - ra2)*math.cos((dec1 + dec2)/2)
            b = dec1 - dec2
            d = math.sqrt(a*a + b*b)
        return d
    def NormalizeAngle(angle, degrees=False):
        "Normalize an angle to between 0 and 2*pi radians (0 and 360 degrees if degrees is true)"
        rotation = 360 if degrees else 2*math.pi
        new_angle = math.fmod(angle, rotation)
        if new_angle < 0:
            new_angle += rotation
        return new_angle
if 1:  # Time 
    def MDY2ISO(month, day, year):
        '''Returns an integer in the ISO form YYYYMMDD.  month and year must be integers.  day can
        be a float; it is truncated to an integer.
        '''
        assert isinstance(month, int), "month must be an integer"
        assert isinstance(year, int), "year must be an integer"
        day = int(day)
        if not IsValidGregorianDate(month, day, year):
            raise ValueError("Not a valid Gregorian calendar date")
        return int("%d%02d%02d" % (year, month, day))
    def CheckIntegerDate(month, day, year, decimal_day=False):
        '''Raises a ValueError if month, day, and year aren't integers and properly bounded.  If
        decimal_day is True, then day can be a floating point number.
        '''
        if decimal_day:
            day = int(day)
        e = ValueError("Year, month, or day are bad")
        try:
            datetime.date(year, month, day)
        except ValueError:
            # Year can be less than 1, which is the datetime module's
            # least allowed year.
            if year < 1:
                # Check month and day by using the year 2000.
                try:
                    datetime.date(2000, month, day)
                except ValueError:
                    raise e
                if year < g.minimum_year:
                    raise e
            else:
                raise e
    def IsDST(year, month, day):
        '''Return True if daylight savings time (DST) is in effect.  Assumes a location in the US
        that utilizes DST.  Note the rules can change at any time.
        '''
        assert isinstance(month, int), "month must be an integer"
        assert isinstance(day, int), "day must be an integer"
        assert isinstance(year, int), "year must be an integer"
        # Algorithm from
        # http://stackoverflow.com/questions/5590429/calculating-daylight-savings-time-from-only-date
        dow = DayOfWeek(month, day, year)
        # Jan, Feb, Dec are not DST
        if month in (1, 2, 12):
            return False
        if month in range(4, 11):
            return True
        previous_sunday = day - dow
        # In Mar, we are in DST if our previous Sunday was on or after the
        # 8th.
        if month == 3:
            return previous_sunday >= 8
        # In Nov we must be before the first Sunday to be DST.  That means
        # the previous Sunday must be before the first.
        return previous_sunday <= 0
    def IsValidGregorianDate(month, day, year):
        '''Returns True if the year is a valid Gregorian calendar date (i.e., year is 1583 or
        greater) and the month and day numbers are valid.  The maximum year allowed is
        datetime.MAXYEAR.
        '''
        assert isinstance(month, int), "month must be an integer"
        assert isinstance(day, int), "day must be an integer"
        assert isinstance(year, int), "year must be an integer"
        if year < 1583:
            return False
        try:
            CheckIntegerDate(month, day, year)
            return True
        except ValueError:
            return False
    def UT2DT(year):    # Meeus pg 78
        'Returns the correction in seconds to add to Universal Time to get dynamical time'
        t = (year - 2000)/100.0
        if year < 948:
            return 2177 + 497*t + 44.1*t*t
        if 948 <= year <= 1600 or year >= 2000:
            correction = 0
            if 2000 <= year <= 2100:
                correction = 0.37*(year - 2100)
            return 102 + 102*t + 25.3*t*t + correction
        if 1800 <= year <= 1997:
            # Maximum error <= 2.3 seconds
            t = (year - 1900)/100.0
            dt = -1.02 + t*(91.02 + t*(265.90 + t*(-839.16 + t*(-1545.20 + t*(3603.62 
                     + t*(4385.98 + t*(-6993.23 + t*(-6090.04 + t*(6298.12 + t*(4102.86
                     + t*(-2137.64 + t*(-1081.51))))))))))))
            return dt
        if int(year + 0.5) == 1998:
            return 63.0
        if int(year + 0.5) == 1999:
            return 64.0
        raise ValueError("Year is out of bounds")
    def MeanSiderealTime(year, month, day):     # Meeus pg 87
        'Returns the mean sidereal time in decimal hours for 0 UT on the given day'
        jd = JD(year, month, day)
        T = (jd - 2451545.0)/36525  # Julian centuries
        # Calculate mst = mean sidereal time in degrees using eq. 12.4
        mst = (280.46061837 + 360.98564736629*(jd - 2451545) + 0.000387933*T*T - T*T*T/38710000)
        mst = math.fmod(mst, 360)
        if mst < 0:
            mst += 360
        return mst/15
    def ApparentSiderealTime(year, month, day):     # Meeus pg 88
        'Returns the apparent sidereal time in decimal hours for 0 UT on the given day'
        jd = JD(year, month, day)
        T = (jd - 2451545.0)/36525  # Julian centuries
        # Calculate mst = mean sidereal time in degrees using eq. 12.4
        mst = (280.46061837 + 360.98564736629*(jd - 2451545) + 0.000387933*T*T - T*T*T/38710000)
        mst = math.fmod(mst, 360)
        while mst < 0:
            mst += 360
        # mst is in decimal degrees.  Get the correction for nutation.
        d_psi, d_eps = Nutation(jd)
        d_psi = math.degrees(d_psi)
        eps = EclipticObliquity(jd)  # Leave in radians
        mst += d_psi*math.cos(eps)  # Correction to apparent sid. time
        return mst/15  # Convert to decimal hours
if 1:  # Earth
    def EarthSurfaceDistance(lat1, long1, lat2, long2):
        '''Page 85.  Returns the distance in km between two points on the Earth's surface.  The
        latitudes and longitudes must be in radians.  The returned value is in km.  The relative
        error of the result is on the order of 1e-5.
        '''
        lwtest.Assert(abs(lat1) <= math.pi/2, "abs(lat1) must be <= pi/2")
        lwtest.Assert(abs(lat2) <= math.pi/2, "abs(lat2) must be <= pi/2")
        lwtest.Assert(abs(long1) <= math.pi/2, "abs(long1) must be <= pi/2")
        lwtest.Assert(abs(long2) <= math.pi/2, "abs(long2) must be <= pi/2")
        a = g.earth_equatorial_radius_km
        f = g.earth_flattening
        F = (lat1 + lat2)/2
        G1 = (lat1 - lat2)/2
        L = (long1 - long2)/2
        S = math.sin(G1)*math.sin(G1)*math.cos(L)*math.cos(L) + math.cos(F)*math.cos(F)*math.sin(L)*math.sin(L)
        C = math.cos(G1)*math.cos(G1)*math.cos(L)*math.cos(L) + math.sin(F)*math.sin(F)*math.sin(L)*math.sin(L)
        omega = math.atan(math.sqrt(S/C))
        R = math.sqrt(S*C)/omega
        D = 2*omega*a
        H1 = (3*R - 1)/(2*C)
        H2 = (3*R + 1)/(2*S)
        return D*(
            1
            + f*H1*math.sin(F)*math.sin(F)*math.cos(G1)*math.cos(G1)
            - f*H2*math.cos(F)*math.cos(F)*math.sin(G1)*math.sin(G1)
        )
    def LongitudinalDistance(latitude, angle):
        '''Page 83.  Returns the distance in km along a circle of constant latitude for Earth for
        an angular longitude distance of angle.  Both angles must be in radians.
        '''
        lwtest.Assert(abs(latitude) <= math.pi/2, "abs(latitude) must be <= pi/2")
        angle = math.fmod(angle, 2*math.pi)
        if angle < 0:
            angle += 2*math.pi
        a = g.earth_equatorial_radius_km
        e = g.earth_meridian_eccentricity
        return (
            angle*a*math.cos(latitude)/math.sqrt(1 - e*e*math.sin(latitude)*math.sin(latitude))
        )
    def LatitudinalDistance(latitude, angle):
        '''Page 84.  Returns the distance in km along a circle of constant longitude for Earth for
        an angular distance of angle along the latitude.  Both angles must be in radians.
        '''
        lwtest.Assert(abs(latitude) <= math.pi/2, "abs(latitude) must be <= pi/2")
        angle = math.fmod(angle, 2*math.pi)
        if angle < 0:
            angle += 2*math.pi
        a = g.earth_equatorial_radius_km
        e = g.earth_meridian_eccentricity
        d = 1 - e*e*math.sin(latitude)*math.sin(latitude)
        return angle*a*(1 - e*e)/pow(d, 3/2.0)
    def EclipticObliquity(jd):
        '''Page 147.  Returns the obliquity of the ecliptic in radians given the Julian day jd.
        This is the angle between the Earth's axis of rotation and the ecliptic.  This is the mean
        obliquity, meaning nutation isn't taken into account.
        '''
        # Convert Julian day to units of 1e4 years
        u = (jd - 2451545.0)/(36525*100)
        lwtest.Assert(abs(u) <= 1)  # Only to be used for +/- 1e4 years from 2000
        c = dms2rad(23, 26, 21.448)  # Major component constant
        e=u*(-4680.93+u*(-1.55+u*(1999.25+u*(-51.38+u*(-249.67+u*(-39.05+u*(7.12+u*(27.87+u*(5.79+u*(2.45))))))))))
        # e is in arcseconds; convert to radians and add the constant
        e = c + math.radians(e/3600)
        return e
    def Nutation(jd):
        '''Page 143.  Returns the tuple (d_psi, d_eps) in radians where d_psi is the nutation in
        longitude and d_eps is the nutation in obliquity.  jd is the Julian astronomical day.
        Accuracy is 2.4 μrad for psi and 0.48 μrad for eps.
        '''
        T = (jd - 2451545.0)/36525  # Julian centuries
        # Mean elongation of the moon from the sun
        # D = 297.85036 + 445267.111480*T - 0.0019142*T*T + T*T*T/189474
        # Mean anomaly of the sun (earth)
        # M = 357.52772 + 35999.050340*T - 0.0001603*T*T - T*T*T/300000
        # Mean anomaly of the moon
        # m = 134.96298 + 477198.867398*T + 0.0086972*T*T + T*T*T/56250
        # Moon's argument of latitude
        # F = 93.27191 + 483202.017538*T - 0.0036825*T*T + T*T*T/327270
        # Longitude of ascending node of moon's mean orbit on ecliptic
        Omega = 125.04452 - 1934.136261*T + 0.0020708*T*T + T*T*T/450000
        # Mean longitude of sun
        L = 280.4665 + 36000.7698*T
        # Mean longitude of moon
        Lm = 218.3165 + 481267.8813*T
        # Note:  I use the formulas on page 144 which give 0.5" accuracy
        # in d_psi and 0.1" accuracy in d_eps.
        d_psi = (
            -17.20*math.sin(math.radians(Omega))
            - 1.32*math.sin(math.radians(2*L))
            - 0.23*math.sin(math.radians(2*Lm))
            + 0.21*math.sin(math.radians(2*Omega))
        )
        d_eps = (
            9.20*math.cos(math.radians(Omega))
            + 0.57*math.cos(math.radians(2*L))
            + 0.10*math.cos(math.radians(2*L))
            - 0.09*math.cos(math.radians(2*Omega))
        )
        return (math.radians(d_psi)/3600, math.radians(d_eps)/3600)
    def EarthOrbitEccentricity(T):
        '''Returns Earth's orbit eccentricity (dimensionless) for the time T in Julian centuries
        from 1 Jan 2000.  Equation 25.4 on page 163.
        '''
        return 0.016708634 - 0.000042037*T - 0.0000001267*T*T
    def LocalCoordinates(latitude, longitude, ra, dec, jd):
        '''Page 93.  Calculate the local horizontal coordinates for an object with right ascension
        ra and declination dec.  The current time is specified in the Julian day jd.  The latitude
        and longitude are of the observer on the surface of the Earth.  The tuple (azimuth,
        altitude) in degrees are returned.  Meeus' convention is that longitude is positive when it
        is west of Greenwich.  Units are:
            latitude, longitude, dec:  radians
            ra:  decimal hours
        '''
        # Get the sidereal time at Greenwich
        month, day, year = JD2MonthDayYear(jd)
        sidereal_time_in_hours = MeanSiderealTime(year, month, day)
        theta0 = math.radians(sidereal_time_in_hours*15)
        H = theta0 - longitude - ra  # Hour angle in radians
        H = math.fmod(H, 2*math.pi)
        if H < 0:
            H += 2*math.pi
        lwtest.Assert(0 <= H <= 2*math.pi)
        A = math.degrees(math.atan(math.sin(H)/(math.cos(H)*math.sin(latitude) 
                         - math.tan(dec)*math.cos(latitude))))
        h = math.degrees(math.asin(math.sin(latitude)*math.sin(dec) 
                         + math.cos(latitude)*math.cos(dec)*math.cos(H)))
        # Convert A to an attitude reckoned from north
        A = math.fmod(A + 180, 360)
        lwtest.Assert(0 <= A <= 360)
        lwtest.Assert(-90 <= h <= 90)
        return (A, h)
    def Precession(jd, jd0, ra0, dec0, pm_ra=0, pm_dec=0):
        '''Page 134.  Returns (ra, dec) representing a position in equatorial coordinates at time
        Julian day jd for a position (ra0, dec0) given at time jd0.  ra and dec mean right
        ascension and declination angles.  This function corrects for the precession of the Earth's
        axis of rotation over time.  (ra and dec) are in radians.  pm_ra and pm_dec, if given, are
        the proper motions of the object in radians/year.
        '''
        T = (jd0 - 2451545.0)/36525
        t = (jd - jd0)/36525
        # The following are in seconds of arc
        zeta = (
            (2306.2181 + 1.39656*T - 0.000139*T*T)*t
            + (0.30188 - 0.000344*T)*t*t
            + 0.017998*t*t*t
        )
        z = (
            (2306.2181 + 1.39656*T - 0.000139*T*T)*t
            + (1.09468 + 0.000066*T)*t*t
            + 0.018203*t*t*t
        )
        theta = (
            (2004.3109 - 0.85330*T - 0.000217*T*T)*t
            - (0.42665 + 0.000217*T)*t*t
            - 0.041833*t*t*t
        )
        zeta = math.radians(zeta/3600)
        z = math.radians(z/3600)
        theta = math.radians(theta/3600)
        # Adjust for the proper motion
        years = (jd - jd0)/365.25
        ra = ra0 + pm_ra*years
        dec = dec0 + pm_dec*years
        # Now calculate the new position
        A = math.cos(dec)*math.sin(ra + zeta)
        B = math.cos(theta)*math.cos(dec)*math.cos(ra + zeta) - math.sin(theta)*math.sin(dec)
        C = math.sin(theta)*math.cos(dec)*math.cos(ra + zeta) + math.cos(theta)*math.sin(dec)
        ra = math.atan2(A, B) + z
        if math.fabs(C - 1) < 0.001:
            # It's within a degree or so to the celestial pole, so use a
            # different formula
            dec = math.acos(math.sqrt(A*A + B*B))
        else:
            dec = math.asin(C)
        return (ra, dec)
if 1:  # Sun
    def SunMeanAnomaly(T):
        "Return the Sun's mean anomaly in radians, equation 25.3 pg 163"
        return NormalizeAngle(math.radians(357.52911 + 35999.05029*T + 0.0001537*T*T))
    def SunPosition(jd, apparent=0):
        '''Page 163.  Returns equatorial coordinates (ra, dec) in radians for the true position of
        the sun at the specified Julian day.  If apparent is true, then the position returned is
        the apparent position.
        '''
        T = (jd - 2451545.0)/36525  # Centuries from 2000 Jan 1.5 TD
        # Geometric mean longitude in radians
        L0 = NormalizeAngle(math.radians(280.46646 + 36000.76983*T + 0.0003032*T*T))
        # Mean anomaly of sun in radians
        M = NormalizeAngle(math.radians(357.52911 + 35999.05029*T + 0.0001537*T*T))
        # Eccentricity of earth's orbit
        # e = 0.016708634 - 0.000042037*T - 0.0000001267*T*T
        # Sun's equation of center in radians
        C = math.radians(
            (1.914602 - 0.004817*T - 0.000014*T*T)*math.sin(M)
            + (0.019993 - 0.000101*T)*math.sin(2*M)
            + 0.000289*math.sin(3*M)
        )
        C = NormalizeAngle(C)
        # Sun's true geometric longitude in radians referred to the mean
        # equinox of the date
        L = NormalizeAngle(L0 + C)
        # Sun's true anomaly in radians
        # nu = NormalizeAngle(M + C)
        # Sun's radius vector in AU
        # R = 1.000001018*(1 - e*e)/(1 + e*math.cos(math.radians(nu)))
        # Calculate the sun's apparent longitude in radians, referred to
        # the true equinox of the date, correcting for nutation and
        # aberration.
        Omega = NormalizeAngle(math.radians(125.04 - 1934.136*T))
        Lambda = NormalizeAngle(L - math.radians(0.00569 - 0.00478*math.sin(Omega)))
        # Mean obliquity of the ecliptic
        eps = EclipticObliquity(jd)  # In radians
        if apparent:
            eps += math.radians(0.00256*math.cos(Omega))
            ra = NormalizeAngle(math.atan2(math.cos(eps)*math.sin(Lambda), math.cos(Lambda)))
            dec = math.asin(math.sin(eps)*math.sin(Lambda))
        else:
            ra = NormalizeAngle(math.atan2(math.cos(eps)*math.sin(L), math.cos(L)))
            dec = math.asin(math.sin(eps)*math.sin(L))
        return (ra, dec)
    def SunriseSunset(month, day, year, latitude, longitude):
        '''Returns a tuple (t_UT_sunrise, t_UT_sunset) of the UT times in decimal hours for sunrise
        and sunset on the indicated day.  latitude and longitude must be in radians.  If you
        convert the returned times to your local time zone and get a negative time, add 24 hours.
        '''
        jd = JD(year, month, day)
        # Convert apparent sidereal time from decimal hours to radians
        ast = math.radians(ApparentSiderealTime(year, month, day)*15)
        h0 = math.radians(-0.8333)  # Geometric altitude of center at rising
        ra, dec = SunPosition(jd)
        s = math.sin(latitude)*math.sin(dec)
        if s < -1 or s > 1:
            raise "Object doesn't go below horizon"
        H0 = math.acos((math.sin(h0) - s)/(math.cos(latitude)*math.cos(dec)))
        m0 = (ra + longitude - ast)/(2*math.pi)
        m1 = m0 - H0/(2*math.pi)
        m2 = m0 + H0/(2*math.pi)
        while m1 > 1:
            m1 -= 1
        while m1 < 0:
            m1 += 1
        return 24*m1, 24*m2
    def SunMeanLongitude(T):
        '''Returns sun's mean longitude in radians for time T in Julian centuries.  Equation 28.2
        pg 183.
        '''
        tau = T/10  # Julian millenia
        L0 = (
            280.4664567
            + 360007.6982779*tau
            + 0.03032028*tau*tau
            + tau*tau*tau/49931
            - tau**4/15300
            - tau**5/2000000
        )
        L0 = math.fmod(L0, 360)  # In degrees
        if L0 < 0:
            L0 += 360
        return math.radians(L0)
    def EquationOfTime(jd):     # Meeus pg 183
        '''Returns the Equation of Time in radians given the Julian day; see equation 28.1 pg 183.
        The equation of time is the time difference between a sundial and the "mean" sun.
        
        To use month, day, year, calculate Julian day by JD(year, month, day).  To convert
        radians to e.g. minutes use 15*degrees(EOT)/60.
        
        This is Smart's formula 28.3 pg 185.
        '''
        T = (jd - 2451545)/36525  # Time in Julian centuries
        epsilon = EclipticObliquity(jd)  # In radians
        L0 = SunMeanLongitude(T)  # In radians
        y = math.tan(epsilon/2) ** 2
        e = EarthOrbitEccentricity(T)
        M = SunMeanAnomaly(T)
        E = (y*math.sin(2*L0) - 2*e*math.sin(M) + 4*e*y*math.sin(M)*math.cos(2*L0)
             - y*y/2*math.sin(4*L0) - 5/4*e*e*math.sin(2*M))
        return E
if 1:  # Moon
    def TimeOfMoonPhase(year, quarter=0):
        '''Returns the time in JDE (Julian Day Ephemeris, which is equivalent to Dynamical Time
        TD).  Note if you want the time in UT, you'll have to correct it using the equation of
        time.  See Chapter 49 starting on page 349.
        
        year should be a floating point number; quarter should be 0 for new moon, 1 for first
        quarter, 2 for full moon, and 3 for last quarter.  k = 0 corresponds to the new moon of 6
        Jan 2000.  Use negative values of k for phases before 2000.
        
        Maximum error for years between 1980-2020 is less than 18 seconds with mean error of 3.7 s.
        '''
        def norm(x):
            '''Normalize x to a number in [0, 360).'''
            while x < 0:
                x += 360
            while x >= 360:
                x -= 360
            return x
        if quarter not in range(4):
            raise ValueError("quarter must be 0, 1, 2, or 3")
        # Calculate the needed value of k
        k = math.floor((year - 2000)*12.3685) + quarter/4.0
        # T is time in Julian centuries since year 2000
        T = k/1236.85  # Eq 49.3, p 350
        # Time of mean phase of moon in Julian days
        jde = (
            2451550.09766
            + k*29.530588861
            + T*T*(0.00015437 + T*(-0.000000150 + T*0.00000000073))
        )  # Eq 49.1, p 349
        E = 1 - 0.002516*T - 0.0000074*T*T  # Eq 47.6, pg 338
        # The following four items are in degrees
        M = (
            2.5534 + 29.10535670*k - 1.4e-6*T*T - 1.1e-7*T*T*T
        )  # Sun mean anomaly
        M1 = (
            201.5643
            + 385.81693528*k
            + 0.0107582*T*T
            + 1.238e-5*T*T*T
            - 5.8e-8*T*T*T*T
        )  # Moon's mean anomaly
        F = (
            160.7108
            + 390.67050284*k
            - 0.0016118*T*T
            - 2.27e-6*T*T*T
            + 1.1e-8*T*T*T*T
        )  # Moon's argument of latitude
        # Longitude of the ascending node of the lunar orbit
        OO = 124.7746 - 1.56375588*k + 0.0020672*T*T + 2.15e-6*T*T*T
        # Normalize
        M, M1, F, OO = [norm(i) for i in (M, M1, F, OO)]
        # Convert to radians
        M, M1, F, OO = [math.radians(i) for i in (M, M1, F, OO)]
        A = (
            # Planetary arguments in radians p 351
            math.radians(299.77 + 0.107408*k - 0.009173*T*T),
            math.radians(251.88 + 0.016321*k),
            math.radians(251.83 + 26.651886*k),
            math.radians(349.42 + 36.412478*k),
            math.radians(84.66 + 18.206239*k),
            math.radians(141.74 + 53.303771*k),
            math.radians(207.14 + 2.453732*k),
            math.radians(154.84 + 7.306860*k),
            math.radians(34.52 + 27.261239*k),
            math.radians(207.19 + 0.121824*k),
            math.radians(291.34 + 1.844379*k),
            math.radians(161.72 + 24.198154*k),
            math.radians(239.56 + 25.513099*k),
            math.radians(331.55 + 3.592518*k),
        )
        # Get correction to true (apparent phase) p 351
        if not quarter:
            # New moon
            corr = (
                -0.40720*math.sin(M1),
                +0.17241*E*math.sin(M),
                +0.01608*math.sin(2*M1),
                +0.01039*math.sin(2*F),
                +0.00739*E*math.sin(M1 - M),
                -0.00514*E*math.sin(M1 + M),
                +0.00208*E*E*math.sin(2*M),
                -0.00111*math.sin(M1 - 2*F),
                -0.00057*math.sin(M1 + 2*F),
                +0.00056*E*math.sin(2*M1 + M),
                -0.00042*math.sin(3*M1),
                +0.00042*E*math.sin(M + 2*F),
                +0.00038*E*math.sin(M - 2*F),
                -0.00024*E*math.sin(2*M1 - M),
                -0.00017*math.sin(OO),
                -0.00007*math.sin(M1 + 2*M),
                +0.00004*math.sin(2*M1 - 2*F),
                +0.00004*math.sin(3*M),
                +0.00003*math.sin(M1 + M - 2*F),
                +0.00003*math.sin(2*M1 + 2*F),
                -0.00003*math.sin(M1 + M + 2*F),
                +0.00003*math.sin(M1 - M + 2*F),
                -0.00002*math.sin(M1 - M - 2*F),
                -0.00002*math.sin(3*M1 + M),
                +0.00002*math.sin(4*M1),
            )
        elif quarter == 2:
            # Full moon
            corr = (
                -0.40614*math.sin(M1),
                +0.17302*E*math.sin(M),
                +0.01614*math.sin(2*M1),
                +0.01043*math.sin(2*F),
                +0.00734*E*math.sin(M1 - M),
                -0.00515*E*math.sin(M1 + M),
                +0.00209*E*E*math.sin(2*M),
                -0.00111*math.sin(M1 - 2*F),
                -0.00057*math.sin(M1 + 2*F),
                +0.00056*E*math.sin(2*M1 + M),
                -0.00042*math.sin(3*M1),
                +0.00042*E*math.sin(M + 2*F),
                +0.00038*E*math.sin(M - 2*F),
                -0.00024*E*math.sin(2*M1 - M),
                -0.00017*math.sin(OO),
                -0.00007*math.sin(M1 + 2*M),
                +0.00004*math.sin(2*M1 - 2*F),
                +0.00004*math.sin(3*M),
                +0.00003*math.sin(M1 + M - 2*F),
                +0.00003*math.sin(2*M1 + 2*F),
                -0.00003*math.sin(M1 + M + 2*F),
                +0.00003*math.sin(M1 - M + 2*F),
                -0.00002*math.sin(M1 - M - 2*F),
                -0.00002*math.sin(3*M1 + M),
                +0.00002*math.sin(4*M1),
            )
        else:
            # First or last quarter
            pass
            corr = (  # p 352
                -0.62801*math.sin(M1),
                +0.17172*E*math.sin(M),
                -0.01183*E*math.sin(M1 + M),
                +0.00862*math.sin(2*M1),
                +0.00804*math.sin(2*F),
                +0.00454*E*math.sin(M1 - M),
                +0.00204*E*E*math.sin(2*M),
                -0.00180*math.sin(M1 - 2*F),
                -0.00070*math.sin(M1 + 2*F),
                -0.00040*math.sin(3*M1),
                -0.00034*E*math.sin(2*M1 - M),
                +0.00032*E*math.sin(M + 2*F),
                +0.00032*E*math.sin(M - 2*F),
                -0.00028*E*E*math.sin(M1 + 2*M),
                +0.00027*E*math.sin(2*M1 + M),
                -0.00017*math.sin(OO),
                -0.00005*math.sin(M1 - M - 2*F),
                +0.00004*math.sin(2*M1 + 2*F),
                -0.00004*math.sin(M1 + M + 2*F),
                +0.00004*math.sin(M1 - 2*M),
                +0.00003*math.sin(M1 + M - 2*F),
                +0.00003*math.sin(3*M),
                +0.00002*math.sin(2*M1 - 2*F),
                +0.00002*math.sin(M1 - M + 2*F),
                -0.00002*math.sin(3*M1 + M),
            )
        periodic1 = sum(corr)
        A1 = [
            0.000325,
            0.000165,
            0.000164,
            0.000126,
            0.000110,
            0.000062,
            0.000060,
            0.000056,
            0.000047,
            0.000042,
            0.000040,
            0.000037,
            0.000035,
            0.000023,
        ]
        periodic2 = sum([i*math.sin(j) for i, j in zip(A1, A)])
        W = (
            0.00306
            - 0.00038*E*math.cos(M)
            + 0.00026*math.cos(M1)
            - 0.00002*math.cos(M1 - M)
            + 0.00002*math.cos(M1 + M)
            + 0.00002*math.cos(2*F)
        )
        if quarter in (1, 3):
            W = W if quarter == 1 else -W
        else:
            W = 0
        jde += periodic1 + periodic2 + W
        if 0:
            print("Debug output from TimeOfMoonPhase:")
            print("  T                                :  %.5f" % T)
            print("  E                                :  %.7f" % E)
            print("  M                                :  %.6f rad" % M)
            print("  M'                               :  %.6f rad" % M1)
            print("  F                                :  %.6f rad" % F)
            print("  OO                               :  %.6f rad" % OO)
            print("  Correction with harmonics (corr1):  %.5f" % periodic1)
            print("  Correction with A's (corr2)      :  %.5f" % periodic2)
            print("  W                                :  %.5f" % W)
            print("  JDE                              :  %.5f" % jde)
        return jde
if 1:  # Solving the Kepler equation
    def KeplerEquationSinnott(e, M, reltol=0):
        '''Returns eccentric anomaly E in radians by solving Kepler's equation 30.5 pg 195 via
        Sinnott's binary search algorithm on page 206.  e is orbital eccentricity (dimensionless)
        and M is the mean anomaly in radians.  Meeus gives the number of iterations required as
        3.32*digits, where digits is the platform's number of floating point digits (3.32 is the
        reciprocal of the base 10 logarithm of 2).
        
        I've typed the BASIC algorithm in mostly verbatim and translated it to python.  The numbers
        in the comments are the line numbers of the BASIC code.
        
        I've modified the program by stopping at a desired relative tolerance between iterations.
        Note if you set e.g. reltol to about 1e-15 or less, the algorithm won't get any better --
        it will just run its normal number of iterations.
        '''
        sgn = dpmath.signum
                            #   Number after '#' is line number in Sinnot's BASIC code
        P1 = math.pi                        # 100
        F = sgn(M)                          # 110
        M = abs(M)/(2*P1)                   # 110
        M = (M - int(M))*2*P1*F             # 120
        if M < 0:                           # 130
            M += 2*P1                       # 130
        F = 1                               # 140
        if M > P1:                          # 150
            F = -1                          # 150
        if M > P1:                          # 160
            M = 2*P1 - M                    # 160
        E0 = P1/2                           # 170
        D = P1/4                            # 170
        Elast = E0/2
        max_iterations = math.ceil(sys.float_info.dig/math.log10(2))  # Typically == 50
        for J in range(max_iterations):     # 180
            M1 = E0 - e*math.sin(E0)        # 190
            E0 = E0 + D*sgn(M - M1)         # 200
            D = D/2                         # 200
            if reltol and J > 5:
                if abs((E0 - Elast)/Elast) <= reltol:
                    break
            Elast = E0
                                            # NEXT J                                                            # 210
        E0 = E0*F                           # 220
        return E0
    class Alg(enum.Enum):
        iteration = enum.auto()
        newton = enum.auto()
        binary_search = enum.auto()
        c_code = enum.auto()
        root_finder = enum.auto()
    def Kepler(m, e, abstol=1e-8, algorithm=Alg.binary_search):
        '''Call one of the Kepler equation solving methods.  m is the mean anomaly and e
        is the orbital eccentricity.  The mean anomaly is the angular distance from
        perihelion which a planet would have if it moved around the sun with a constant
        angular velocity.  By definition, the angle m increases uniformly with time.
        Return the value of E (eccentric anomaly) and the number of iterations required.
        Kepler's equation is E = m + e*sin(E), a transcendental equation in the desired
        value E.  See Meeus pg 193.
        '''
        def SolveKeplerIteration(m, e, abstol=abstol):
            '''Use simple iteration to the indicated precision.'''
            E0, E, count = m/2, m, 0
            while abs(E - E0) > abstol/10 and count <= g.max_iterations:
                E0 = E
                count += 1
                E = m + e*math.sin(E0)
            if count > g.max_iterations:
                msg = "Too many iterations ({0}) in SolveKeplerIteration"
                raise ValueError(msg.format(count))
            return (E, count)
        def SolveKeplerNewton(m, e, abstol=abstol):
            '''Use Newton's method to solve for the root.'''
            E0, E, count = m/2, m, 0
            while abs(E - E0) > abstol and count <= g.max_iterations:
                E0 = E
                count += 1
                E = E0 + (m + e*math.sin(E0) - E0)/(1 - e*math.cos(E0))
            if count > g.max_iterations:
                msg = "Too many iterations ({0}) in SolveKeplerNewton"
                raise ValueError(msg.format(count))
            return (E, count)
        def SolveKeplerBinarySearch(m, e, abstol=abstol):
            '''Uses Sinnott's binary search algorithm.  abstol is
            ignored.
            '''
            m, f = math.fmod(m, math.tau), 1
            m = m + math.tau if m < 0 else m
            if m > math.pi:
                m, f = math.tau - m, -1
            e0, d = math.pi/2, math.pi/4
            for i in range(1, 54, 1):
                m1 = e0 - e*math.sin(e0)
                e0 = e0 + d*dpmath.signum(m - m1)
                d = d/2
            return (e0*f, 54)
        def SolveKeplerCCode(m, e, abstol=abstol):
            '''Translated from C code at
            http://www.projectpluto.com/kepler.htm (note 1).  "Meeus" refers to
            "Astronomical Algorithms" by J. Meeus.  I've modified the routine
            slightly for e < 0.3 because it was not converging to the desired
            precision.  It also required adding checks for too many iterations.
            
            Note 1:  https://github.com/Bill-Gray/lunar/blob/master/astfuncs.cpp is to
            be consulted for later code.
            '''
            neg, count, thresh = False, 0, abstol*math.fabs(1 - e)
            if not m:
                return (0, 0)
            if e < 0.3:  # Low-eccentricity formula from Meeus, p. 195
                curr = math.atan2(math.sin(m), math.cos(m) - e)
                err = curr - e*math.sin(curr) - m
                while math.fabs(err) > thresh:
                    curr -= err/(1 - e*math.cos(curr))
                    err = curr - e*math.sin(curr) - m
                    if count > g.max_iterations:
                        msg = "Too many iterations ({0}) in SolveKeplerCCode for e < 0.3 case"
                        raise ValueError(msg.format(count))
                    count += 1
                return (curr, count)
            if m < 0:
                m = -m
                neg = True
            curr = m
            if e > 0.8 and m < math.pi/3 or e > 1:  # Up to 60 degrees
                trial = m/math.fabs(1 - e)
                if trial**2 > 6*math.fabs(1 - e):  # Cubic term is dominant
                    if m < math.pi:
                        trial = (6*m) ** (1/3)
                    else:  # Hyperbolic w/ 5th & higher-order terms predominant
                        trial = math.asinh(m/e)
                curr = trial
            if e < 1:
                err = curr - e*math.sin(curr) - m
                while math.fabs(err) > thresh:
                    curr -= err/(1 - e*math.cos(curr))
                    err = curr - e*math.sin(curr) - m
                    if count > g.max_iterations:
                        msg = "Too many iterations ({0}) in SolveKeplerCCode for e < 1 case"
                        raise ValueError(msg.format(count))
                    count += 1
            else:
                err = e*math.sinh(curr) - curr - m
                while math.fabs(err) > thresh:
                    curr -= err/(e*math.cosh(curr) - 1)
                    err = e*math.sinh(curr) - curr - m
                    if count > g.max_iterations:
                        msg = "Too many iterations ({0}) in SolveKeplerCCode for e >= 1 case"
                        raise ValueError(msg.format(count))
                    count += 1
            curr = -curr if neg else curr
            return (curr, count)
        def SolveKepler4(m, e, abstol=abstol):
            '''Use RootFinder, which is Jack Crenshaw's enhancements to an older IBM
            FORTRAN routine that uses inverse parabolic interpolation.
            '''
            def f(E):
                return m + e*math.sin(E) - E
            # Need to find a reliable way to bracket the root
            root, count = RootFinder(m/2, m, f, eps=abstol)
            return root
        if algorithm == Alg.iteration:
            return SolveKeplerIteration(m, e, abstol=abstol)
        elif algorithm == Alg.newton:
            return SolveKeplerNewton(m, e, abstol=abstol)
        elif algorithm == Alg.binary_search:
            return SolveKeplerBinarySearch(m, e, abstol=abstol)
        elif algorithm == Alg.c_code:
            return SolveKeplerCCode(m, e, abstol=abstol)
        # elif algorithm == Alg.root_finder:
        #    return SolveKepler4(m, e, abstol=abstol)
        else:
            raise ValueError("Bad algorithm number")
    def ShowKeplerSolutions(m, e, p):
        def P(N, E, n, p, s):
            digits = int(math.log10(1/p)) + 1
            msg = "  Algorithm {N} = {E:.{digits}f} n = {n:2}  ({s})"
            print(msg.format(**locals()))
        E, n = Kepler(math.radians(m), e, p, algorithm=Alg.iteration)
        P(0, E, n, p, "Simple iteration")
        E, n = Kepler(math.radians(m), e, p, algorithm=Alg.newton)
        P(1, E, n, p, "Newton's method")
        E, n = Kepler(math.radians(m), e, algorithm=Alg.binary_search)
        P(2, E, n, p, "Sinnott's binary search")
        E, n = Kepler(math.radians(m), e, p, algorithm=Alg.c_code)
        P(3, E, n, p, "Projectpluto algorithm")
        # E, n = Kepler(math.radians(m), e, p, algorithm=Alg.root_finder)
        # P(4, E, n, p, "Inverse parabolic interpolation")
        print()

if __name__ == "__main__":  
    import sys
    import random
    from dpseq import frange
    from lwtest import run, assert_equal, Assert, raises
    def Test_JulianDay():
        # Test cases come from page 60 and 61 of Meeus.  Remember that the Julian day
        # traditionally starts at noon GMT.
        Assert(JD(1957, 10, 4.81) == 2436116.31)    # pg 61
        Assert(JD( 333,  1, 27.5) == 1842713)       # pg 61
        Assert(JD(2000,  1,  1.5) == 2451545)       # pg 62
        Assert(JD(2000,  1,  1.0) == 2451544.5)     # pg 62
        Assert(JD(1900,  1,  1)   == 2415020.5)     # pg 62
        Assert(JD(1600,  1,  1)   == 2305447.5)     # pg 62
        Assert(JD(1600, 12, 31)   == 2305812.5)     # pg 62
        Assert(JD( 837,  4, 10.3) == 2026871.8)     # pg 62
        Assert(JD(-123, 12,   31) == 1676496.5)     # pg 62
        Assert(JD(-122,  1,    1) == 1676497.5)     # pg 62
        Assert(JD(-1000, 7, 12.5) == 1356001.0)     # pg 62
        Assert(JD(-1000, 2,   29) == 1355866.5)     # pg 62
        Assert(JD(-1001, 8, 17.9) == 1355671.4)     # pg 62
        Assert(JD(-4712, 1,  1.5) ==       0.0)     # pg 62
    def Test_JulianDayDT():
        'Note that DT2JD and JD2DT should be inverses'
        # ∞∞2 Bug:  note the following will fail on 2415020.5 (1Jan1900), so there's still
        # some problem in one of these routines.
        for jd in (2461103.5, 2436116.31, 2451545, 2451545.5):
            dt = JD2DT(jd)
            jd1 = DT2JD(dt)
            Assert(jd == jd1)
    def Test_DayOfWeek():
        assert_equal(DayOfWeek(11, 13, 1949), 0)
        assert_equal(DayOfWeek(5, 30, 1998), 6)
        assert_equal(DayOfWeek(6, 30, 1954), 3)
    def Test_DayOfYear():
        assert_equal(DayOfYear(11, 14, 1978), 318)
        assert_equal(DayOfYear(4, 22, 1980), 113)
    def Test_JD2DT():
        eps = 1e-5
        # 4.81 Oct 1957 (Launch of Sputnik 1) [Meeus pg 61]
        dt = JD2DT(2436116.31)
        Assert(dt == datetime.datetime(1957, 10, 4, 19, 26, 24, 4))
        # 27 Jan 333 at 12 noon [Meeus pg 61]
        dt = JD2DT(1842713.0)
        Assert(dt == datetime.datetime(333, 1, 27, 12, 0))
        # Exception for year JD == 0 because datetime module only supports to year == 1
        raises(ValueError, JD2DT, 0)
    def Test_NumDaysInMonth():
        yr = 1999
        DIM = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for mo, dim in enumerate(DIM):
            Assert(NumDaysInMonth(mo + 1, yr) == dim)
        y = 2000
        months = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for m, days in zip(range(1, 13), months):
            Assert(NumDaysInMonth(m, y) == days)
        y = 2001
        months = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for m, days in zip(range(1, 13), months):
            Assert(NumDaysInMonth(m, y) == days)
    def Test_IsLeapYear():
        for y in (1700, 1800, 1900, 2100, 2001):
            Assert(not IsLeapYear(y))
        for y in (1600, 2000, 2400, 2004):
            Assert(IsLeapYear(y))
    def Test_IsValidDate():
        for m, d, y in (
            (1, 1, 1753),
            (12, 31, 1753),
            (1, 1, 2000),
        ):
            Assert(IsValidDate(m, d, y))
        # Invalid dates for year 2001, a non-leap year
        for m, d in (
            (1, 0),
            (1, 0.999),
            (1, 32),
            (2, 29),
            (3, 32),
            (4, 31),
            (5, 32),
            (6, 31),
            (7, 32),
            (8, 32),
            (9, 31),
            (10, 32),
            (11, 31),
            (12, 32),
        ):
            Assert(not IsValidDate(m, d, 2001))
    def Test_AngularSeparation():
        # Page 110:  Angular separation
        ra1 = math.radians(213.9154)
        dec1 = math.radians(19.1825)
        ra2 = math.radians(201.2983)
        dec2 = math.radians(-11.1614)
        d = AngularSeparation(ra1, dec1, ra2, dec2)
        Assert(math.fabs(math.degrees(d) - 32.7930) < 1e-4)
    def Test_SiderealTime():
        # Page 88 and 89:  Sidereal time
        # 10 April 1987 at 19:21:00 UT
        d = 10 + (19 + 21/60.0)/24  # Example 12.b
        t = MeanSiderealTime(1987, 4, d)
        expected = 8 + 34.0/60 + 57.0896/3600
        Assert(t - expected < 1e-10)
        # 10 April 1987 at 00:00:00 UT
        t = MeanSiderealTime(1987, 4, 10)
        h, m, s = hr2hms(t)
        Assert(h == 13 and m == 10)
        Assert(math.fabs(s - 46.3668) < 0.0001)
        # 10 April 1987 at 00:00:00 UT
        t = ApparentSiderealTime(1987, 4, 10)
        h, m, s = hr2hms(t)
        Assert(h == 13 and m == 10)
        expected = 46.1351  # Example 12.a bottom
        Assert(math.fabs(s - expected) < 0.01)
    def Test_CheckIntegerDate():
        # Bad month
        raises(ValueError, CheckIntegerDate, 13, 1, 1)
        raises(ValueError, CheckIntegerDate, 0, 1, 1)
        # Bad day
        raises(ValueError, CheckIntegerDate, 1, 0, 1)
        raises(ValueError, CheckIntegerDate, 1, 32, 1)
        # Bad year
        raises(ValueError, CheckIntegerDate, 1, 1, g.minimum_year - 1)
        max_year = datetime.MAXYEAR
        raises(ValueError, CheckIntegerDate, 1, 1, max_year + 1)
        # OK date
        CheckIntegerDate(1, 1, 2000)
        CheckIntegerDate(12, 31, 2000)
        CheckIntegerDate(1, 1.1, 2000, decimal_day=True)
        CheckIntegerDate(12, 30.1, 2000, decimal_day=True)
    def Test_EarthSurfaceDistance():
        # Page 85:  Distance between points in France & USNO
        long1 = dms2rad(-2, 20, 14)
        lat1 = dms2rad(48, 50, 11)
        long2 = dms2rad(77, 3, 56)
        lat2 = dms2rad(38, 55, 17)
        d = EarthSurfaceDistance(lat1, long1, lat2, long2)
        Assert(math.fabs(d - 6181.63) <= 0.05)
    def Test_LongitudinalDistance():
        # Page 83:  distance along a line of constant latitude
        latitude = dms2rad(42, 0, 0)
        angle = dms2rad(1, 0, 0)
        d = LongitudinalDistance(latitude, angle)
        Assert(math.fabs(d - 82.8508) < 0.0001)
        # Page 84:  distance along a line of constant longitude
        latitude = dms2rad(42, 0, 0)
        angle = dms2rad(1, 0, 0)
        d = LatitudinalDistance(latitude, angle)
        Assert(math.fabs(d - 111.0733) < 0.0001)
    def Test_UT2DT():
        # Page 78:  Correction to universal time to get dynamical time
        Assert(math.fabs(UT2DT(1977) - 48) < 1)
        Assert(math.fabs(UT2DT(333) - 6146) < 1)
    def Test_LinearRegression():
        # Page 40:  Linear regression
        x = (73, 38, 35, 42, 78, 68, 74, 42, 52, 54, 39, 61, 42, 49, 50, 62, 44, 39, 43, 54,
            44, 37,)
        y = (90.4, 125.3, 161.8, 143.4, 52.5, 50.8, 71.5, 152.8, 131.3, 98.5, 144.8,
            78.1, 89.5, 63.9, 112.1, 82.0, 119.8, 161.2, 208.4, 111.6, 167.1, 162.1,)
        slope, intercept, r = LinearRegression(x, y)
        Assert(math.fabs(slope + 2.49) < 0.01)
        Assert(math.fabs(intercept - 244.18) < 0.01)
        Assert(math.fabs(r + 0.767) < 0.001)
    def Test_TransformationOfCoordinates():
        # Page 95:  Transformation of coordinates
        jd = JD(1987, 4, 10 + (19 + 21/60.0)/24)
        longitude = dms2rad(77, 3, 56)
        latitude = dms2rad(38, 55, 17)
        ra = hms2rad(23, 9, 16.641)
        dec = dms2rad(-6, 43, 11.61)
        azimuth, altitude = LocalCoordinates(latitude, longitude, ra, dec, jd)
        Assert(math.fabs(azimuth - 248.03) < 0.01)
        Assert(math.fabs(altitude - 15.12) < 0.01)
    def Test_Precession():
        # Page 135:  Precession
        ra0 = hms2rad(2, 44, 11.986)
        dec0 = dms2rad(49, 13, 42.48)
        pm_ra = math.radians(0.03425/3600*15)
        pm_dec = math.radians(-0.0895/3600)
        jd0 = 2451545.0
        jd = 2462088.69
        ra, dec = Precession(jd, jd0, ra0, dec0, pm_ra, pm_dec)
        eps = 2e-6
        Assert(math.fabs(math.degrees(ra) - 41.547214) < eps)
        Assert(math.fabs(math.degrees(dec) - 49.348483) < eps)
    def Test_PolarisPrecession():
        # For Polaris
        ra0 = hms2rad(2, 31, 48.704)
        dec0 = dms2rad(89, 15, 50.72)
        pm_ra = math.radians(0.19877/3600*15)
        pm_dec = math.radians(-0.0152/3600)
        jd0 = 2451545.0
        jd = JD(2050, 1, 1)
        ra, dec = Precession(jd, jd0, ra0, dec0, pm_ra, pm_dec)
        h, m, s = rad2hms(ra)
        Assert(h == 3 and m == 48 and math.fabs(s - 16.427) < 0.01)
        d, m, s = rad2dms(dec)
        Assert(d == 89 and m == 27 and math.fabs(s - 15.375) < 0.01)
    def Test_EclipticObliquity():
        # Page 148:  obliquity of the ecliptic
        d, m, s = rad2dms(EclipticObliquity(2446895.5))
        Assert(d == 23 and m == 26 and math.fabs(s - 27.407) < 0.01)
        d_psi, d_eps = Nutation(2446895.5)
        Assert(math.fabs(d_psi + math.radians(3.788/3600)) < math.radians(0.5/3600))
        Assert(math.fabs(d_eps - math.radians(9.443/3600)) < math.radians(0.1/3600))
        # Page 147:  Obliquity of the ecliptic; example 28.b pg 185.
        eps = EclipticObliquity(JD(1992, 10, 13))
        Assert(math.fabs(math.degrees(eps) - 23.44023) < 1e-5)
    def Test_SunPosition():
        # Page 165:  solar coordinates
        ra, dec = SunPosition(2448908.5, apparent=0)
        Assert(math.fabs(math.degrees(ra) - 198.38) < 0.01)
        Assert(math.fabs(math.degrees(dec) + 7.785) < 0.001)
    def Test_EquationOfTime():
        # Page 183:  Equation of Time; example 28.b pg 185
        jd = JD(1992, 10, 13)
        Assert(math.fabs(EquationOfTime(jd) - 0.059825572) < 1e-8)
    def Test_SunMeanLongitude():
        # Page 183:  Sun's mean longitude; example 28.b pg 185
        T = (JD(1992, 10, 13) - 2451545)/36525
        L0 = SunMeanLongitude(T)  # In radians
        Assert(math.fabs(math.degrees(L0) - 201.80720) < 1e-5)
    def Test_EarthOrbitEccentricity():
        # Page 163:  Eccentricity of Earth's orbit; example 28.b pg 185.
        T = (JD(1992, 10, 13) - 2451545)/36525
        e = EarthOrbitEccentricity(T)
        Assert(math.fabs(e - 0.016711668) < 1e-9)
    def Test_SunMeanAnomaly():
        # Page 163:  Sun's mean anomaly; example 28.b pg 185.
        T = (JD(1992, 10, 13) - 2451545)/36525
        M = math.degrees(SunMeanAnomaly(T))
        Assert(math.fabs(M - 278.99397) < 1e-5)
    def Test_KeplerEquation():
        # Page 195:  Kepler's equation
        e, M = 0.1, math.radians(5)  # Example 30.a pg 196
        Assert(math.fabs(math.degrees(KeplerEquationSinnott(e, M)) - 5.554589) < 1e-6)
        e, M = 0.99, 0.2  # Example 30.a pg 196
        Assert(math.fabs(KeplerEquationSinnott(e, M) - 1.066997365282) < 1e-12)
    def Test_Meeus_SunriseSunset():
        # Sunrise & sunset for Alamo, CA on 15 Dec 2012.  Correct values come from
        # http://www.sunrisesunset.com/ (I prefer to use the USNO pages, but that website seems to
        # be down much of the time).  The MST times from the web were 05:07 and 20:30.  MST's
        # offset from UT is -7 hours.
        lat, long = math.radians(37 + 51.4/60), math.radians(121 + 59.9/60)
        rise, set = SunriseSunset(12, 15, 2012, lat, long)
        # Results should be sunrise = 7:16 am, sunset = 4:50 pm.
        offset = -8
        rise += offset
        set += offset
        if rise < 0:
            rise += 24
        if set < 0:
            set += 24
        hr = int(rise)
        min = int((rise - hr)*60 + 0.5)
        Assert(hr == 7 and abs(min - 16) < 1)
        hr = int(set)
        min = int((set - hr)*60 + 0.5)
        Assert(hr == 16 and abs(min - 50) < 1)
    def Test_Meeus_IsDST():
        # Test cases from http://www.webexhibits.org/daylightsaving/b.html
        # accessed Mon 19 May 2014 09:23:55 AM.
        test_cases = ((2010,  3, 14),
                      (2010, 11,  7),
                      (2011,  3, 13),
                      (2011, 11,  6),
                      (2012,  3, 11),
                      (2012, 11,  4),
                      (2013,  3, 10),
                      (2013, 11,  3),
                      (2014,  3,  9),
                      (2014, 11,  2),
                      (2015,  3,  8),
                      (2015, 11,  1),
                      (2016,  3, 13),
                      (2016, 11,  6))
        for y, m, d in test_cases:
            if m == 3:
                Assert(IsDST(y, m, d))
                Assert(not IsDST(y, m, d - 1))
            else:
                Assert(not IsDST(y, m, d))
                Assert(IsDST(y, m, d - 1))
    def Test_Meeus_TimeOfMoonPhase():
        yr = 1977.13  # Example 49.a, p 353
        t = TimeOfMoonPhase(yr, quarter=0)
        Assert(abs(t - 2443192.65118) < 0.00001)
        yr = 2044  # Example 49.b, p 353
        t = TimeOfMoonPhase(yr, quarter=3)
        Assert(abs(t - 2467636.49186) < 0.00001)
    def Test_Meeus__dms2rad():
        d, m, s = 22, 30, 30
        t_rad = math.radians(d + m/60 + s/3600)
        Assert(t_rad == dms2rad(d, m, s))
    def Test_Meeus__hms2rad():
        h, m, s = 22, 30, 30
        hrs = h + m/60.0 + s/3600.0
        t_deg = hrs*15
        t_rad = math.radians(t_deg)
        Assert(t_rad == hms2rad(h, m, s))
    def Test_Meeus__hr2hms():
        hr, hms = 12.5822222222, 12.3456
        h, m, s = hr2hms(hr)
        hms1 = h + m/1e2 + s/1e4
        Assert(abs(hms - hms1) < 0.0001)
    def Test_Meeus_IsLeapYear():
        Assert(IsLeapYear(1600))
        Assert(IsLeapYear(2000))
        Assert(IsLeapYear(2004))
        Assert(IsLeapYear(2400))
        Assert(not IsLeapYear(1700))
        Assert(not IsLeapYear(1800))
        Assert(not IsLeapYear(1900))
        Assert(not IsLeapYear(2100))
        Assert(not IsLeapYear(2200))
    def Test_Meeus_IsValidGregorianDate():
        Assert(IsValidGregorianDate(1, 1, 1583))
        Assert(IsValidGregorianDate(12, 31, 1583))
        Assert(not IsValidGregorianDate(1, 1, 1582))
        Assert(not IsValidGregorianDate(1, 32, 2000))
    def Test_Meeus_NormalizeAngle():
        Assert(NormalizeAngle(0, degrees=True) == 0)
        Assert(NormalizeAngle(1, degrees=True) == 1)
        Assert(NormalizeAngle(361, degrees=True) == 1)
        Assert(NormalizeAngle(-1, degrees=True) == 359)
        Assert(NormalizeAngle(0) == 0)
        Assert(NormalizeAngle(-math.pi/2) == 3*math.pi/2)
        Assert(NormalizeAngle(-math.pi) == math.pi)

    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
    def Test_Meeus__product():
        a = (1, 2, 3, 4, 5, 6)
        Assert(product(a) == 720)
    def Test_Meeus__rad2dms():
        Assert(dms2rad(*rad2dms(math.pi/6)) == math.pi/6)
    def Test_Meeus__rad2hms():
        Assert(hms2rad(*rad2hms(math.pi/6)) == math.pi/6)
    def Test_Meeus__SGN():
        Assert(sgn(-5) == -1)
        Assert(sgn(-1) == -1)
        Assert(sgn(0) == 0)
        Assert(sgn(1) == 1)
        Assert(sgn(5) == 1)
        Assert(sgn(-5.0) == -1)
        Assert(sgn(-1.0) == -1)
        Assert(sgn(0.0) == 0)
        Assert(sgn(1.0) == 1)
        Assert(sgn(5.0) == 1)
    def Test_Meeus__JD():
        D = (  # jd, m, d for 2000 (a leap year)
            (1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 4), (5, 1, 5), (6, 1, 6), (7, 1, 7),
            (8, 1, 8), (9, 1, 9), (10, 1, 10), (11, 1, 11), (12, 1, 12), (13, 1, 13),
            (14, 1, 14), (15, 1, 15), (16, 1, 16), (17, 1, 17), (18, 1, 18), (19, 1,
            19), (20, 1, 20), (21, 1, 21), (22, 1, 22), (23, 1, 23), (24, 1, 24), (25,
            1, 25), (26, 1, 26), (27, 1, 27), (28, 1, 28), (29, 1, 29), (30, 1, 30),
            (31, 1, 31), (32, 2, 1), (33, 2, 2), (34, 2, 3), (35, 2, 4), (36, 2, 5),
            (37, 2, 6), (38, 2, 7), (39, 2, 8), (40, 2, 9), (41, 2, 10), (42, 2, 11),
            (43, 2, 12), (44, 2, 13), (45, 2, 14), (46, 2, 15), (47, 2, 16), (48, 2,
            17), (49, 2, 18), (50, 2, 19), (51, 2, 20), (52, 2, 21), (53, 2, 22), (54,
            2, 23), (55, 2, 24), (56, 2, 25), (57, 2, 26), (58, 2, 27), (59, 2, 28),
            (60, 2, 29), (61, 3, 1), (62, 3, 2), (63, 3, 3), (64, 3, 4), (65, 3, 5),
            (66, 3, 6), (67, 3, 7), (68, 3, 8), (69, 3, 9), (70, 3, 10), (71, 3, 11),
            (72, 3, 12), (73, 3, 13), (74, 3, 14), (75, 3, 15), (76, 3, 16), (77, 3,
            17), (78, 3, 18), (79, 3, 19), (80, 3, 20), (81, 3, 21), (82, 3, 22), (83,
            3, 23), (84, 3, 24), (85, 3, 25), (86, 3, 26), (87, 3, 27), (88, 3, 28),
            (89, 3, 29), (90, 3, 30), (91, 3, 31), (92, 4, 1), (93, 4, 2), (94, 4, 3),
            (95, 4, 4), (96, 4, 5), (97, 4, 6), (98, 4, 7), (99, 4, 8), (100, 4, 9),
            (101, 4, 10), (102, 4, 11), (103, 4, 12), (104, 4, 13), (105, 4, 14), (106,
            4, 15), (107, 4, 16), (108, 4, 17), (109, 4, 18), (110, 4, 19), (111, 4,
            20), (112, 4, 21), (113, 4, 22), (114, 4, 23), (115, 4, 24), (116, 4, 25),
            (117, 4, 26), (118, 4, 27), (119, 4, 28), (120, 4, 29), (121, 4, 30), (122,
            5, 1), (123, 5, 2), (124, 5, 3), (125, 5, 4), (126, 5, 5), (127, 5, 6),
            (128, 5, 7), (129, 5, 8), (130, 5, 9), (131, 5, 10), (132, 5, 11), (133, 5,
            12), (134, 5, 13), (135, 5, 14), (136, 5, 15), (137, 5, 16), (138, 5, 17),
            (139, 5, 18), (140, 5, 19), (141, 5, 20), (142, 5, 21), (143, 5, 22), (144,
            5, 23), (145, 5, 24), (146, 5, 25), (147, 5, 26), (148, 5, 27), (149, 5,
            28), (150, 5, 29), (151, 5, 30), (152, 5, 31), (153, 6, 1), (154, 6, 2),
            (155, 6, 3), (156, 6, 4), (157, 6, 5), (158, 6, 6), (159, 6, 7), (160, 6,
            8), (161, 6, 9), (162, 6, 10), (163, 6, 11), (164, 6, 12), (165, 6, 13),
            (166, 6, 14), (167, 6, 15), (168, 6, 16), (169, 6, 17), (170, 6, 18), (171,
            6, 19), (172, 6, 20), (173, 6, 21), (174, 6, 22), (175, 6, 23), (176, 6,
            24), (177, 6, 25), (178, 6, 26), (179, 6, 27), (180, 6, 28), (181, 6, 29),
            (182, 6, 30), (183, 7, 1), (184, 7, 2), (185, 7, 3), (186, 7, 4), (187, 7,
            5), (188, 7, 6), (189, 7, 7), (190, 7, 8), (191, 7, 9), (192, 7, 10), (193,
            7, 11), (194, 7, 12), (195, 7, 13), (196, 7, 14), (197, 7, 15), (198, 7,
            16), (199, 7, 17), (200, 7, 18), (201, 7, 19), (202, 7, 20), (203, 7, 21),
            (204, 7, 22), (205, 7, 23), (206, 7, 24), (207, 7, 25), (208, 7, 26), (209,
            7, 27), (210, 7, 28), (211, 7, 29), (212, 7, 30), (213, 7, 31), (214, 8, 1),
            (215, 8, 2), (216, 8, 3), (217, 8, 4), (218, 8, 5), (219, 8, 6), (220, 8,
            7), (221, 8, 8), (222, 8, 9), (223, 8, 10), (224, 8, 11), (225, 8, 12),
            (226, 8, 13), (227, 8, 14), (228, 8, 15), (229, 8, 16), (230, 8, 17), (231,
            8, 18), (232, 8, 19), (233, 8, 20), (234, 8, 21), (235, 8, 22), (236, 8,
            23), (237, 8, 24), (238, 8, 25), (239, 8, 26), (240, 8, 27), (241, 8, 28),
            (242, 8, 29), (243, 8, 30), (244, 8, 31), (245, 9, 1), (246, 9, 2), (247, 9,
            3), (248, 9, 4), (249, 9, 5), (250, 9, 6), (251, 9, 7), (252, 9, 8), (253,
            9, 9), (254, 9, 10), (255, 9, 11), (256, 9, 12), (257, 9, 13), (258, 9, 14),
            (259, 9, 15), (260, 9, 16), (261, 9, 17), (262, 9, 18), (263, 9, 19), (264,
            9, 20), (265, 9, 21), (266, 9, 22), (267, 9, 23), (268, 9, 24), (269, 9,
            25), (270, 9, 26), (271, 9, 27), (272, 9, 28), (273, 9, 29), (274, 9, 30),
            (275, 10, 1), (276, 10, 2), (277, 10, 3), (278, 10, 4), (279, 10, 5), (280,
            10, 6), (281, 10, 7), (282, 10, 8), (283, 10, 9), (284, 10, 10), (285, 10,
            11), (286, 10, 12), (287, 10, 13), (288, 10, 14), (289, 10, 15), (290, 10,
            16), (291, 10, 17), (292, 10, 18), (293, 10, 19), (294, 10, 20), (295, 10,
            21), (296, 10, 22), (297, 10, 23), (298, 10, 24), (299, 10, 25), (300, 10,
            26), (301, 10, 27), (302, 10, 28), (303, 10, 29), (304, 10, 30), (305, 10,
            31), (306, 11, 1), (307, 11, 2), (308, 11, 3), (309, 11, 4), (310, 11, 5),
            (311, 11, 6), (312, 11, 7), (313, 11, 8), (314, 11, 9), (315, 11, 10), (316,
            11, 11), (317, 11, 12), (318, 11, 13), (319, 11, 14), (320, 11, 15), (321,
            11, 16), (322, 11, 17), (323, 11, 18), (324, 11, 19), (325, 11, 20), (326,
            11, 21), (327, 11, 22), (328, 11, 23), (329, 11, 24), (330, 11, 25), (331,
            11, 26), (332, 11, 27), (333, 11, 28), (334, 11, 29), (335, 11, 30), (336,
            12, 1), (337, 12, 2), (338, 12, 3), (339, 12, 4), (340, 12, 5), (341, 12,
            6), (342, 12, 7), (343, 12, 8), (344, 12, 9), (345, 12, 10), (346, 12, 11),
            (347, 12, 12), (348, 12, 13), (349, 12, 14), (350, 12, 15), (351, 12, 16),
            (352, 12, 17), (353, 12, 18), (354, 12, 19), (355, 12, 20), (356, 12, 21),
            (357, 12, 22), (358, 12, 23), (359, 12, 24), (360, 12, 25), (361, 12, 26),
            (362, 12, 27), (363, 12, 28), (364, 12, 29), (365, 12, 30),
        )
        yr = 2000
        for jd, m, d in D:
            Assert(jd == JD(*JD2MDY(jd, yr)))
    def Test_Meeus__MDY2ISO():
        Assert(MDY2ISO(1, 1, 2014) == 20140101)
        Assert(MDY2ISO(12, 31, 2014) == 20141231)
        raises(ValueError, MDY2ISO, 12, 32, 2014)
    def Test_Julian1_DayOfWeek():
        assert_equal(DayOfWeek(11, 13, 1949), 0)
        assert_equal(DayOfWeek(5, 30, 1998), 6)
        assert_equal(DayOfWeek(6, 30, 1954), 3)
    def Test_Julian1_DayOfYear():
        assert_equal(DayOfYear(11, 14, 1978), 318)
        assert_equal(DayOfYear(4, 22, 1988), 113)
    def Test_Julian1_NumericalInit():
        data = ( # Test vectors from Meeus pg 61 & 62
            #  y,    m,     d,     jd
            (1957,  10, 4.81, 2436116.31),
            (333,    1, 27.5, 1842713.0),
            (2000,   1,  1.5, 2451545.0),
            (1999,   1,  1.0, 2451179.5),
            (1988,   6, 19.5, 2447332.0),
            (1600,   1,  1.0, 2305447.5),
            (1600,  12, 31.0, 2305812.5),
            (-123,  12, 31.0, 1676496.5),
            (-122,   1,  1.0, 1676497.5),
            (-1000,  2, 29.0, 1355866.5),
            (-4712,  1,  1.5, 0.0),
        )
        for y, m, d, jd in data:
            jul = JD(m, d, y)
            Assert(jd - jul == 0)
    def Test_Julian1_StringInit():
        data = (
            # Test_Julian1_ points from Meeus pg 62
            ("4Oct1957:19:26:24", 2436116.31),
            ("27Jan333:12", 1842713.0),
            ("1.5jan2000", 2451545.0),
            ("1.0jan1999", 2451179.5),
            ("19.5JUN1988", 2447332.0),
            ("1.0jan1600", 2305447.5),
            ("31.0Dec1600", 2305812.5),
            ("31.0Dec-123", 1676496.5),
            ("1.0jan-122", 1676497.5),
            ("29Feb-1000", 1355866.5),
            ("1.5Jan-4712", 0.0),
        )
        data
    def Test_Julian1_DaysToHMS():
        Assert(DaysToHMS(0.5) == (0, 12, 0, 0))
        Assert(DaysToHMS(1.5) == (1, 12, 0, 0))
    def Test_Julian1_NumDaysInMonth():
        yr = 1999
        DIM = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for mo, dim in enumerate(DIM):
            Assert(NumDaysInMonth(mo + 1, yr) == dim)
        y = 2000
        months = (31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for m, days in zip(range(1, 13), months):
            Assert(NumDaysInMonth(m, y) == days)
        y = 2001
        months = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
        for m, days in zip(range(1, 13), months):
            Assert(NumDaysInMonth(m, y) == days)
    def Test_Julian1_IsLeapYear():
        for y in (1700, 1800, 1900, 2100, 2001):
            Assert(not IsLeapYear(y))
        for y in (1600, 2000, 2400, 2004):
            Assert(IsLeapYear(y))
    def Test_Julian1_IsValidDate():
        for m, d, y in (
            (1, 1, 1753),
            (12, 31, 1753),
            (1, 1, 2000),
        ):
            Assert(IsValidDate(m, d, y))
        # Invalid dates for year 2001, a non-leap year
        for m, d in (
            (1, 0),
            (1, 0.999),
            (1, 32),
            (2, 29),
            (3, 32),
            (4, 31),
            (5, 32),
            (6, 31),
            (7, 32),
            (8, 32),
            (9, 31),
            (10, 32),
            (11, 31),
            (12, 32),
        ):
            Assert(not IsValidDate(m, d, 2001))
    def Test_Kepler():
        '''Run a variety of test cases on the different algorithms and show
        they all produce answers essentially equal to each other.
        '''
        tol = 1e-12
        for theta in range(5, 91):
            radians = math.radians(theta)
            for ecc in frange("0.1", "1.0", "0.1"):
                E = []
                for alg in (Alg.iteration, Alg.newton, Alg.binary_search, Alg.c_code):
                    try:
                        e, n = Kepler(radians, ecc, tol, algorithm=alg)
                    except ValueError:
                        print("Too many iterations {0}".format(g.max_iterations))
                        print("theta = {theta}, ecc = {ecc:.1f}".format(**locals()))
                        print("algorithm =", alg)
                        exit(1)
                    E.append(e)
                actual, n = Kepler(radians, ecc, tol/100, algorithm=Alg.c_code)
                for i, e in enumerate(E):
                    if abs(e - actual) > tol:
                        print("theta = {theta}, ecc = {ecc:.1f}".format(**locals()))
                        print("E =")
                        for j, k in enumerate(E):
                            print(" ", j, "    ", k)
                        print("actual =", actual)
                        print("Error for i =", i)
                        print("  E[i] - actual =", E[i] - actual)
                        exit(1)
    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
