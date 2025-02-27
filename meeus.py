"""

ToDo
    -

Various formulas from Meeus, "Astronomical Algorithms", 2nd ed.
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 1999 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # <science> Various astronomical formulas from Meeus, "Astronomical Algorithms", 2nd ed.
        ##∞what∞#
        ##∞test∞# run #∞test∞#
        pass
    if 1:  # Standard imports
        import datetime
        import functools
        from math import pi, floor, sqrt, sin, cos, tan, asin, acos, atan, atan2
        from math import fabs, fmod, radians, degrees, ceil, log10
        import operator
        import sys
    if 1:  # Custom imports
        from lwtest import Assert
    if 1:  # Global variables
        reduce = functools.reduce
        ii = isinstance

        class Global:  # Constants
            pass

        g = Global()
        g.earth_equatorial_radius_km = 6378.14
        g.earth_flattening = f = 1 / 298.257
        g.earth_meridian_eccentricity = sqrt(2 * f - f * f)
        del f
        g.minimum_year = -4712
        # Days in months (February handled specially because of leap years)
        months = {
            1: 31,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def IsInt(x, msg):
        "Check that x is an integer"
        if not ii(x, int):
            raise TypeError(msg)

    def sgn(x):
        "Signum function"
        return 1 if x > 0 else -1 if x < 0 else 0

    def hms2rad(h, m, s):
        "Converts angular measure in hours, minutes, seconds to radians"
        # One hour = 360/24 = 15 degrees
        IsInt(h, "h must be an integer")
        IsInt(m, "m must be an integer")
        Assert(m >= 0, "m must be >= 0")
        Assert(s >= 0, "s must be >= 0")
        decimal_hours = abs(h) + abs(m) / 60 + abs(s) / 3600
        return radians(sgn(h) * decimal_hours * 15)

    def dms2rad(d, m, s):
        """Converts angular measure in degrees, minutes, seconds to radians.
        The result will have the sign of d.
        """
        IsInt(d, "d must be an integer")
        IsInt(m, "m must be an integer")
        Assert(m >= 0, "m must be >= 0")
        Assert(s >= 0, "s must be >= 0")
        deg = abs(d) + abs(m) / 60 + abs(s) / 3600
        return radians(sgn(d) * deg)

    def hr2hms(hr):
        """Return a tuple (hours, minutes, seconds) of a decimal hour value hr.  hours will have
        the sign of hr.
        """
        h = int(abs(hr))
        m = 60 * (abs(hr) - h)
        s = 60 * (m - int(m))
        return sgn(hr) * h, int(m), s

    def rad2dms(x):
        """Return a tuple (degrees, minutes, seconds) of a radian value.  The degrees value will
        have the sign of x.
        """
        sig = sgn(x)
        x = fabs(x)
        d = degrees(x)
        deg = int(d)
        min = 60 * (d - deg)
        sec = 60 * (min - int(min))
        return sig * deg, int(min), sec

    def rad2hms(x):
        "Return a tuple (hour, minutes, seconds) of a radian value"
        return rad2dms(x / 15)

    def product(x):
        "Returns the product of the components of the iterable x"
        return reduce(operator.mul, x)

    def LinearRegression(X, Y):
        """Page 36.  Returns a tuple (slope, intercept, correlation) from the linear regression of
        Y against X.  X and Y are sequences of the abscissas and ordinates, respectively; they must
        be of the same size.
        """
        Assert(len(X) == len(Y))
        N, sx, sy = len(X), sum(X), sum(Y)
        sq, prod = lambda x: x * x, lambda x, y: x * y
        sxx, syy, sxy = sum(map(sq, X)), sum(map(sq, Y)), sum(map(prod, X, Y))
        denomx, denomy = N * sxx - sx * sx, N * syy - sy * sy
        if not denomx or not denomy:
            raise ValueError("Regression equation denominator is zero")
        slope = (N * sxy - sx * sy) / denomx
        intercept = (sy * sxx - sx * sxy) / denomx
        r = (N * sxy - sx * sy) / sqrt(denomx * denomy)
        Assert(-1 <= r <= 1, "Correlation coefficient out of range")
        return (slope, intercept, r)

    def AngularSeparation(ra1, dec1, ra2, dec2):
        """Page 109.  Returns the angular separation in radians between two bodies at (ra1, dec1)
        and (ra2, dec2).  ra is right ascension and dec is declination, both in radians.
        """
        d = acos(sin(dec1) * sin(dec2) + cos(dec1) * cos(dec2) * cos(ra1 - ra2))
        if d < 1 / 60:
            # Use an approximation for small angles
            a = (ra1 - ra2) * cos((dec1 + dec2) / 2)
            b = dec1 - dec2
            d = sqrt(a * a + b * b)
        return d

    def Normalize(angle, degrees=0):
        "Normalize an angle to between 0 and 2*pi radians (0 and 360 degrees if degrees is true)"
        rotation = 360 if degrees else 2 * pi
        new_angle = fmod(angle, rotation)
        if new_angle < 0:
            new_angle += rotation
        return new_angle


if 1:  # Time routines

    def MDY2ISO(month, day, year):
        """Returns an integer in the ISO form YYYYMMDD.  month and year must be integers.  day can
        be a float; it is truncated to an integer.
        """
        IsInt(month, "month must be an integer")
        IsInt(year, "year must be an integer")
        day = int(day)
        if not IsValidGregorianDate(month, day, year):
            raise ValueError("Not a valid Gregorian calendar date")
        return int("%d%02d%02d" % (year, month, day))

    def IsLeapYear(year):
        "Page 62, returns True if year is a leap year"
        IsInt(year, "year must be an integer")
        Assert(year > 0, "year must be >= 0")
        return (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0)

    def NumDaysInMonth(month, year):
        IsInt(year, "year must be an integer")
        IsInt(month, "month must be an integer")
        Assert(year > 0, "year must be >= 0")
        Assert(1 <= month <= 12, "month must be between 1 and 12")
        if month == 2:
            return 29 if IsLeapYear(year) else 28
        return months[month]

    def DayOfYear(month, day, year):
        """Page 65.  Returns an integer between 1 and 366 corresponding to the day of the year.  1
        January is day 1 and 31 December is day 365 (366 in a leap year).
        """
        IsInt(month, "month must be an integer")
        IsInt(day, "day must be an integer")
        IsInt(year, "year must be an integer")
        K = 1 if IsLeapYear(year) else 2
        N = int(275 * month / 9) - K * int((month + 9) / 12) + day - 30
        if not 1 <= N <= 366:
            raise ValueError("Illegal day number")
        return N

    def DayOfYear2MDY(day_of_year, year):
        """Page 66.  Returns a tuple of integers (month, day, year) given the day number and a
        year.
        """
        IsInt(year, "year must be an integer")
        IsInt(day_of_year, "day_of_year must be an integer")
        Assert(1 <= day_of_year <= 366, "Bad day of year number")
        N = day_of_year
        K = 1 if IsLeapYear(year) else 2
        M = int((9 * (K + N) / 275) + 0.98)
        if N < 32:
            M = 1
        D = N - int(275 * M / 9) + K * int((M + 9) / 12) + 30
        return (M, D, year)

    def CheckIntegerDate(month, day, year, decimal_day=False):
        """Raises a ValueError if month, day, and year aren't integers and properly bounded.  If
        decimal_day is True, then day can be a floating point number.
        """
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

    def DayOfWeek(month, day, year):
        "Page 65, returns a number between 0 (Sunday) and 6 (Saturday) for a given date"
        CheckIntegerDate(month, day, year, decimal_day=True)
        julian = int(JulianAstro(month, int(day), year) + 1.5)
        return julian % 7

    def IsDST(month, day, year):
        """Return True if daylight savings time (DST) is in effect.  Assumes a location in the US
        that utilizes DST.  Note the rules can change at any time.
        """
        IsInt(month, "month must be an integer")
        IsInt(day, "day must be an integer")
        IsInt(year, "year must be an integer")
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
        """Returns True if the year is a valid Gregorian calendar date (i.e., year is 1583 or
        greater) and the month and day numbers are valid.  The maximum year allowed is
        datetime.MAXYEAR.
        """
        IsInt(month, "month must be an integer")
        IsInt(day, "day must be an integer")
        IsInt(year, "year must be an integer")
        if year < 1583:
            return False
        try:
            CheckIntegerDate(month, day, year)
            return True
        except ValueError:
            return False

    def UT2DT(year):
        """Page 78, returns the correction in seconds to add to Universal Time to get dynamical
        time.
        """
        t = (year - 2000) / 100.0
        if year < 948:
            return 2177 + 497 * t + 44.1 * t * t
        if 948 <= year <= 1600 or year >= 2000:
            correction = 0
            if 2000 <= year <= 2100:
                correction = 0.37 * (year - 2100)
            return 102 + 102 * t + 25.3 * t * t + correction
        if 1800 <= year <= 1997:
            # Maximum error <= 2.3 seconds
            t = (year - 1900) / 100.0
            dt = -1.02 + t * (
                91.02
                + t
                * (
                    265.90
                    + t
                    * (
                        -839.16
                        + t
                        * (
                            -1545.20
                            + t
                            * (
                                3603.62
                                + t
                                * (
                                    4385.98
                                    + t
                                    * (
                                        -6993.23
                                        + t
                                        * (
                                            -6090.04
                                            + t
                                            * (
                                                6298.12
                                                + t
                                                * (
                                                    4102.86
                                                    + t * (-2137.64 + t * (-1081.51))
                                                )
                                            )
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
            return dt
        if int(year + 0.5) == 1998:
            return 63.0
        if int(year + 0.5) == 1999:
            return 64.0
        raise ValueError("Year is out of bounds")

    def MeanSiderealTime(month, day, year):
        "Page 87, returns the mean sidereal time in decimal hours for 0 UT on the given day"
        jd = JulianAstro(month, day, year)
        T = (jd - 2451545.0) / 36525  # Julian centuries
        # Calculate mst = mean sidereal time in degrees using eq. 12.4
        mst = (
            280.46061837
            + 360.98564736629 * (jd - 2451545)
            + 0.000387933 * T * T
            - T * T * T / 38710000
        )
        mst = fmod(mst, 360)
        if mst < 0:
            mst += 360
        return mst / 15

    def ApparentSiderealTime(month, day, year):
        "Page 88, returns the apparent sidereal time in decimal hours for 0 UT on the given day"
        jd = JulianAstro(month, day, year)
        T = (jd - 2451545.0) / 36525  # Julian centuries
        # Calculate mst = mean sidereal time in degrees using eq. 12.4
        mst = (
            280.46061837
            + 360.98564736629 * (jd - 2451545)
            + 0.000387933 * T * T
            - T * T * T / 38710000
        )
        mst = fmod(mst, 360)
        if mst < 0:
            mst += 360
        # mst is in decimal degrees.  Get the correction for nutation.
        d_psi, d_eps = Nutation(jd)
        d_psi = degrees(d_psi)
        eps = EclipticObliquity(jd)  # Leave in radians
        mst += d_psi * cos(eps)  # Correction to apparent sid. time
        return mst / 15  # Convert to decimal hours


if 1:  # Julian date routines

    def JulianAstro(month, day, year):
        """Page 60.  Returns the astronomical Julian day number which is a floating point number whose
        decimal fraction part is zero at Greenwich mean noon.
        """
        CheckIntegerDate(month, day, year, decimal_day=True)
        Assert(year >= g.minimum_year)
        M, D, Y = month, day, year  # Meeus' notation
        if M in (1, 2):
            Y -= 1
            M += 12
        A = int(Y / 100)
        tmp = year + month / 100 + day / 10000
        B = 0 if tmp < 1582.1015 else 2 - A + int(A / 4)  # B==0 ==> Julian cal.
        julian = int(365.25 * (Y + 4716)) + int(30.6001 * (M + 1)) + D + B - 1524.5
        return julian

    def JD(month, day, year):
        "Return Julian day of the year, int <= 366"
        jd = int(JulianAstro(month, day, year) + 0.55)
        jd0 = int(JulianAstro(1, 1, year) + 0.55)
        return jd - jd0 + 1

    def JD2MDY(julian_day, year):
        "Return (month, day, year) for the given julian_day and year"
        IsInt(julian_day, "julian_day must be an integer")
        IsInt(year, "year must be an integer")
        Assert(1 <= julian_day <= 366)
        # Days in month indexed by (month - 1).
        days_in_month = (
            31,
            28 + IsLeapYear(year),
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        )
        # Get month and day
        cum_num_days = [sum(days_in_month[:m]) for m in range(1, 13)]
        for i in range(len(cum_num_days)):
            if cum_num_days[i] >= julian_day:  # It's this month
                month = i + 1
                cum_days = cum_num_days[i]
                day = days_in_month[i] - (cum_days - julian_day)
                return (month, day, year)

    def JulianToMonthDayYear(jd):
        """Page 63.  Returns (month, day, year) given the Julian day jd.  month and year are
        integers; day may be an integer or float.
        """
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


if 1:  # Earth-related calculations

    def EarthSurfaceDistance(lat1, long1, lat2, long2):
        """Page 85.  Returns the distance in km between two points on the Earth's surface.  The
        latitudes and longitudes must be in radians.  The returned value is in km.  The relative
        error of the result is on the order of 1e-5.
        """
        Assert(abs(lat1) <= pi / 2, "abs(lat1) must be <= pi/2")
        Assert(abs(lat2) <= pi / 2, "abs(lat2) must be <= pi/2")
        Assert(abs(long1) <= pi / 2, "abs(long1) must be <= pi/2")
        Assert(abs(long2) <= pi / 2, "abs(long2) must be <= pi/2")
        a = g.earth_equatorial_radius_km
        f = g.earth_flattening
        F = (lat1 + lat2) / 2
        G1 = (lat1 - lat2) / 2
        L = (long1 - long2) / 2
        S = sin(G1) * sin(G1) * cos(L) * cos(L) + cos(F) * cos(F) * sin(L) * sin(L)
        C = cos(G1) * cos(G1) * cos(L) * cos(L) + sin(F) * sin(F) * sin(L) * sin(L)
        omega = atan(sqrt(S / C))
        R = sqrt(S * C) / omega
        D = 2 * omega * a
        H1 = (3 * R - 1) / (2 * C)
        H2 = (3 * R + 1) / (2 * S)
        return D * (
            1
            + f * H1 * sin(F) * sin(F) * cos(G1) * cos(G1)
            - f * H2 * cos(F) * cos(F) * sin(G1) * sin(G1)
        )

    def LongitudinalDistance(latitude, angle):
        """Page 83.  Returns the distance in km along a circle of constant latitude for Earth for
        an angular longitude distance of angle.  Both angles must be in radians.
        """
        Assert(abs(latitude) <= pi / 2, "abs(latitude) must be <= pi/2")
        angle = fmod(angle, 2 * pi)
        if angle < 0:
            angle += 2 * pi
        a = g.earth_equatorial_radius_km
        e = g.earth_meridian_eccentricity
        return (
            angle * a * cos(latitude) / sqrt(1 - e * e * sin(latitude) * sin(latitude))
        )

    def LatitudinalDistance(latitude, angle):
        """Page 84.  Returns the distance in km along a circle of constant longitude for Earth for
        an angular distance of angle along the latitude.  Both angles must be in radians.
        """
        Assert(abs(latitude) <= pi / 2, "abs(latitude) must be <= pi/2")
        angle = fmod(angle, 2 * pi)
        if angle < 0:
            angle += 2 * pi
        a = g.earth_equatorial_radius_km
        e = g.earth_meridian_eccentricity
        d = 1 - e * e * sin(latitude) * sin(latitude)
        return angle * a * (1 - e * e) / pow(d, 3 / 2.0)

    def EclipticObliquity(jd):
        """Page 147.  Returns the obliquity of the ecliptic in radians given the Julian day jd.
        This is the angle between the Earth's axis of rotation and the ecliptic.  This is the mean
        obliquity, meaning nutation isn't taken into account.
        """
        # Convert Julian day to units of 1e4 years
        u = (jd - 2451545.0) / (36525 * 100)
        Assert(abs(u) <= 1)  # Only to be used for +/- 1e4 years from 2000
        c = dms2rad(23, 26, 21.448)  # Major component constant
        e = u * (
            -4680.93
            + u
            * (
                -1.55
                + u
                * (
                    1999.25
                    + u
                    * (
                        -51.38
                        + u
                        * (
                            -249.67
                            + u
                            * (
                                -39.05
                                + u * (7.12 + u * (27.87 + u * (5.79 + u * (2.45))))
                            )
                        )
                    )
                )
            )
        )
        # e is in arcseconds; convert to radians and add the constant
        e = c + radians(e / 3600)
        return e

    def Nutation(jd):
        """Page 143.  Returns the tuple (d_psi, d_eps) in radians where d_psi is the nutation in
        longitude and d_eps is the nutation in obliquity.  jd is the Julian astronomical day.
        Accuracy is 2.4 μrad for psi and 0.48 μrad for eps.
        """
        T = (jd - 2451545.0) / 36525  # Julian centuries
        # Mean elongation of the moon from the sun
        D = 297.85036 + 445267.111480 * T - 0.0019142 * T * T + T * T * T / 189474
        # Mean anomaly of the sun (earth)
        M = 357.52772 + 35999.050340 * T - 0.0001603 * T * T - T * T * T / 300000
        # Mean anomaly of the moon
        m = 134.96298 + 477198.867398 * T + 0.0086972 * T * T + T * T * T / 56250
        # Moon's argument of latitude
        F = 93.27191 + 483202.017538 * T - 0.0036825 * T * T + T * T * T / 327270
        # Longitude of ascending node of moon's mean orbit on ecliptic
        Omega = 125.04452 - 1934.136261 * T + 0.0020708 * T * T + T * T * T / 450000
        # Mean longitude of sun
        L = 280.4665 + 36000.7698 * T
        # Mean longitude of moon
        Lm = 218.3165 + 481267.8813 * T
        # Note:  I use the formulas on page 144 which give 0.5" accuracy
        # in d_psi and 0.1" accuracy in d_eps.
        d_psi = (
            -17.20 * sin(radians(Omega))
            - 1.32 * sin(radians(2 * L))
            - 0.23 * sin(radians(2 * Lm))
            + 0.21 * sin(radians(2 * Omega))
        )
        d_eps = (
            9.20 * cos(radians(Omega))
            + 0.57 * cos(radians(2 * L))
            + 0.10 * cos(radians(2 * L))
            - 0.09 * cos(radians(2 * Omega))
        )
        return (radians(d_psi) / 3600, radians(d_eps) / 3600)

    def EarthOrbitEccentricity(T):
        """Returns Earth's orbit eccentricity (dimensionless) for the time T in Julian centuries
        from 1 Jan 2000.  Equation 25.4 on page 163.
        """
        return 0.016708634 - 0.000042037 * T - 0.0000001267 * T * T

    def LocalCoordinates(latitude, longitude, ra, dec, jd):
        """Page 93.  Calculate the local horizontal coordinates for an object with right ascension
        ra and declination dec.  The current time is specified in the Julian day jd.  The latitude
        and longitude are of the observer on the surface of the Earth.  The tuple (azimuth,
        altitude) in degrees are returned.  Meeus' convention is that longitude is positive when it
        is west of Greenwich.  Units are:
            latitude, longitude, dec:  radians
            ra:  decimal hours
        """
        # Get the sidereal time at Greenwich
        month, day, year = JulianToMonthDayYear(jd)
        sidereal_time_in_hours = MeanSiderealTime(month, day, year)
        theta0 = radians(sidereal_time_in_hours * 15)
        H = theta0 - longitude - ra  # Hour angle in radians
        H = fmod(H, 2 * pi)
        if H < 0:
            H += 2 * pi
        Assert(0 <= H <= 2 * pi)
        A = degrees(atan(sin(H) / (cos(H) * sin(latitude) - tan(dec) * cos(latitude))))
        h = degrees(asin(sin(latitude) * sin(dec) + cos(latitude) * cos(dec) * cos(H)))
        # Convert A to an attitude reckoned from north
        A = fmod(A + 180, 360)
        Assert(0 <= A <= 360)
        Assert(-90 <= h <= 90)
        return (A, h)

    def Precession(jd, jd0, ra0, dec0, pm_ra=0, pm_dec=0):
        """Page 134.  Returns (ra, dec) representing a position in equatorial coordinates at time
        Julian day jd for a position (ra0, dec0) given at time jd0.  ra and dec mean right
        ascension and declination angles.  This function corrects for the precession of the Earth's
        axis of rotation over time.  (ra and dec) are in radians.  pm_ra and pm_dec, if given, are
        the proper motions of the object in radians/year.
        """
        T = (jd0 - 2451545.0) / 36525
        t = (jd - jd0) / 36525
        # The following are in seconds of arc
        zeta = (
            (2306.2181 + 1.39656 * T - 0.000139 * T * T) * t
            + (0.30188 - 0.000344 * T) * t * t
            + 0.017998 * t * t * t
        )
        z = (
            (2306.2181 + 1.39656 * T - 0.000139 * T * T) * t
            + (1.09468 + 0.000066 * T) * t * t
            + 0.018203 * t * t * t
        )
        theta = (
            (2004.3109 - 0.85330 * T - 0.000217 * T * T) * t
            - (0.42665 + 0.000217 * T) * t * t
            - 0.041833 * t * t * t
        )
        zeta = radians(zeta / 3600)
        z = radians(z / 3600)
        theta = radians(theta / 3600)
        # Adjust for the proper motion
        years = (jd - jd0) / 365.25
        ra = ra0 + pm_ra * years
        dec = dec0 + pm_dec * years
        # Now calculate the new position
        A = cos(dec) * sin(ra + zeta)
        B = cos(theta) * cos(dec) * cos(ra + zeta) - sin(theta) * sin(dec)
        C = sin(theta) * cos(dec) * cos(ra + zeta) + cos(theta) * sin(dec)
        ra = atan2(A, B) + z
        if fabs(C - 1) < 0.001:
            # It's within a degree or so to the celestial pole, so use a
            # different formula
            dec = acos(sqrt(A * A + B * B))
        else:
            dec = asin(C)
        return (ra, dec)


if 1:  # Sun

    def SunMeanAnomaly(T):
        "Return the Sun's mean anomaly in radians, equation 25.3 pg 163"
        return Normalize(radians(357.52911 + 35999.05029 * T + 0.0001537 * T * T))

    def SunPosition(jd, apparent=0):
        """Page 163.  Returns equatorial coordinates (ra, dec) in radians for the true position of
        the sun at the specified Julian day.  If apparent is true, then the position returned is
        the apparent position.
        """
        T = (jd - 2451545.0) / 36525  # Centuries from 2000 Jan 1.5 TD
        # Geometric mean longitude in radians
        L0 = Normalize(radians(280.46646 + 36000.76983 * T + 0.0003032 * T * T))
        # Mean anomaly of sun in radians
        M = Normalize(radians(357.52911 + 35999.05029 * T + 0.0001537 * T * T))
        # Eccentricity of earth's orbit
        e = 0.016708634 - 0.000042037 * T - 0.0000001267 * T * T
        # Sun's equation of center in radians
        C = radians(
            (1.914602 - 0.004817 * T - 0.000014 * T * T) * sin(M)
            + (0.019993 - 0.000101 * T) * sin(2 * M)
            + 0.000289 * sin(3 * M)
        )
        C = Normalize(C)
        # Sun's true geometric longitude in radians referred to the mean
        # equinox of the date
        L = Normalize(L0 + C)
        # Sun's true anomaly in radians
        nu = Normalize(M + C)
        # Sun's radius vector in AU
        R = 1.000001018 * (1 - e * e) / (1 + e * cos(radians(nu)))
        # Calculate the sun's apparent longitude in radians, referred to
        # the true equinox of the date, correcting for nutation and
        # aberration.
        Omega = Normalize(radians(125.04 - 1934.136 * T))
        Lambda = Normalize(L - radians(0.00569 - 0.00478 * sin(Omega)))
        # Mean obliquity of the ecliptic
        eps = EclipticObliquity(jd)  # In radians
        if apparent:
            eps += radians(0.00256 * cos(Omega))
            ra = Normalize(atan2(cos(eps) * sin(Lambda), cos(Lambda)))
            dec = asin(sin(eps) * sin(Lambda))
        else:
            ra = Normalize(atan2(cos(eps) * sin(L), cos(L)))
            dec = asin(sin(eps) * sin(L))
        return (ra, dec)

    def SunriseSunset(month, day, year, latitude, longitude):
        """Returns a tuple (t_UT_sunrise, t_UT_sunset) of the UT times in decimal hours for sunrise
        and sunset on the indicated day.  latitude and longitude must be in radians.  If you
        convert the returned times to your local time zone and get a negative time, add 24 hours.
        """
        jd = JulianAstro(month, day, year)
        # Convert apparent sidereal time from decimal hours to radians
        ast = radians(ApparentSiderealTime(month, day, year) * 15)
        h0 = radians(-0.8333)  # Geometric altitude of center at rising
        ra, dec = SunPosition(jd)
        s = sin(latitude) * sin(dec)
        if s < -1 or s > 1:
            raise "Object doesn't go below horizon"
        H0 = acos((sin(h0) - s) / (cos(latitude) * cos(dec)))
        m0 = (ra + longitude - ast) / (2 * pi)
        m1 = m0 - H0 / (2 * pi)
        m2 = m0 + H0 / (2 * pi)
        while m1 > 1:
            m1 -= 1
        while m1 < 0:
            m1 += 1
        return 24 * m1, 24 * m2

    def SunMeanLongitude(T):
        """Returns sun's mean longitude in radians for time T in Julian centuries.  Equation 28.2
        pg 183.
        """
        tau = T / 10  # Julian millenia
        L0 = (
            280.4664567
            + 360007.6982779 * tau
            + 0.03032028 * tau * tau
            + tau * tau * tau / 49931
            - tau**4 / 15300
            - tau**5 / 2000000
        )
        L0 = fmod(L0, 360)  # In degrees
        if L0 < 0:
            L0 += 360
        return radians(L0)

    def EquationOfTime(jd):
        """Returns the Equation of Time in radians given the Julian day; see equation 28.1 pg 183.
        The equation of time is the time difference between a sundial and the "mean" sun.

        To use month, day, year, calculate Julian day by JulianAstro(month, day, year).  To convert
        radians to e.g. minutes use 15*degrees(EOT)/60.

        This is Smart's formula 28.3 pg 185.
        """
        T = (jd - 2451545) / 36525  # Time in Julian centuries
        epsilon = EclipticObliquity(jd)  # In radians
        L0 = SunMeanLongitude(T)  # In radians
        y = tan(epsilon / 2) ** 2
        e = EarthOrbitEccentricity(T)
        M = SunMeanAnomaly(T)
        E = (
            y * sin(2 * L0)
            - 2 * e * sin(M)
            + 4 * e * y * sin(M) * cos(2 * L0)
            - y * y / 2 * sin(4 * L0)
            - 5 / 4 * e * e * sin(2 * M)
        )
        return E


if 1:  # Moon

    def TimeOfMoonPhase(year, quarter=0):
        """Returns the time in JDE (Julian Day Ephemeris, which is equivalent to Dynamical Time
        TD).  Note if you want the time in UT, you'll have to correct it using the equation of
        time.  See Chapter 49 starting on page 349.

        year should be a floating point number; quarter should be 0 for new moon, 1 for first
        quarter, 2 for full moon, and 3 for last quarter.  k = 0 corresponds to the new moon of 6
        Jan 2000.  Use negative values of k for phases before 2000.

        Maximum error for years between 1980-2020 is less than 18 seconds with mean error of 3.7 s.
        """

        def norm(x):
            """Normalize x to a number in [0, 360)."""
            while x < 0:
                x += 360
            while x >= 360:
                x -= 360
            return x

        if quarter not in range(4):
            raise ValueError("quarter must be 0, 1, 2, or 3")
        # Calculate the needed value of k
        k = floor((year - 2000) * 12.3685) + quarter / 4.0
        # T is time in Julian centuries since year 2000
        T = k / 1236.85  # Eq 49.3, p 350
        # Time of mean phase of moon in Julian days
        jde = (
            2451550.09766
            + k * 29.530588861
            + T * T * (0.00015437 + T * (-0.000000150 + T * 0.00000000073))
        )  # Eq 49.1, p 349
        E = 1 - 0.002516 * T - 0.0000074 * T * T  # Eq 47.6, pg 338
        # The following four items are in degrees
        M = (
            2.5534 + 29.10535670 * k - 1.4e-6 * T * T - 1.1e-7 * T * T * T
        )  # Sun mean anomaly
        M1 = (
            201.5643
            + 385.81693528 * k
            + 0.0107582 * T * T
            + 1.238e-5 * T * T * T
            - 5.8e-8 * T * T * T * T
        )  # Moon's mean anomaly
        F = (
            160.7108
            + 390.67050284 * k
            - 0.0016118 * T * T
            - 2.27e-6 * T * T * T
            + 1.1e-8 * T * T * T * T
        )  # Moon's argument of latitude
        # Longitude of the ascending node of the lunar orbit
        OO = 124.7746 - 1.56375588 * k + 0.0020672 * T * T + 2.15e-6 * T * T * T
        # Normalize
        M, M1, F, OO = [norm(i) for i in (M, M1, F, OO)]
        # Convert to radians
        M, M1, F, OO = [radians(i) for i in (M, M1, F, OO)]
        A = (
            # Planetary arguments in radians p 351
            radians(299.77 + 0.107408 * k - 0.009173 * T * T),
            radians(251.88 + 0.016321 * k),
            radians(251.83 + 26.651886 * k),
            radians(349.42 + 36.412478 * k),
            radians(84.66 + 18.206239 * k),
            radians(141.74 + 53.303771 * k),
            radians(207.14 + 2.453732 * k),
            radians(154.84 + 7.306860 * k),
            radians(34.52 + 27.261239 * k),
            radians(207.19 + 0.121824 * k),
            radians(291.34 + 1.844379 * k),
            radians(161.72 + 24.198154 * k),
            radians(239.56 + 25.513099 * k),
            radians(331.55 + 3.592518 * k),
        )
        # Get correction to true (apparent phase) p 351
        if not quarter:
            # New moon
            corr = (
                -0.40720 * sin(M1),
                +0.17241 * E * sin(M),
                +0.01608 * sin(2 * M1),
                +0.01039 * sin(2 * F),
                +0.00739 * E * sin(M1 - M),
                -0.00514 * E * sin(M1 + M),
                +0.00208 * E * E * sin(2 * M),
                -0.00111 * sin(M1 - 2 * F),
                -0.00057 * sin(M1 + 2 * F),
                +0.00056 * E * sin(2 * M1 + M),
                -0.00042 * sin(3 * M1),
                +0.00042 * E * sin(M + 2 * F),
                +0.00038 * E * sin(M - 2 * F),
                -0.00024 * E * sin(2 * M1 - M),
                -0.00017 * sin(OO),
                -0.00007 * sin(M1 + 2 * M),
                +0.00004 * sin(2 * M1 - 2 * F),
                +0.00004 * sin(3 * M),
                +0.00003 * sin(M1 + M - 2 * F),
                +0.00003 * sin(2 * M1 + 2 * F),
                -0.00003 * sin(M1 + M + 2 * F),
                +0.00003 * sin(M1 - M + 2 * F),
                -0.00002 * sin(M1 - M - 2 * F),
                -0.00002 * sin(3 * M1 + M),
                +0.00002 * sin(4 * M1),
            )
        elif quarter == 2:
            # Full moon
            corr = (
                -0.40614 * sin(M1),
                +0.17302 * E * sin(M),
                +0.01614 * sin(2 * M1),
                +0.01043 * sin(2 * F),
                +0.00734 * E * sin(M1 - M),
                -0.00515 * E * sin(M1 + M),
                +0.00209 * E * E * sin(2 * M),
                -0.00111 * sin(M1 - 2 * F),
                -0.00057 * sin(M1 + 2 * F),
                +0.00056 * E * sin(2 * M1 + M),
                -0.00042 * sin(3 * M1),
                +0.00042 * E * sin(M + 2 * F),
                +0.00038 * E * sin(M - 2 * F),
                -0.00024 * E * sin(2 * M1 - M),
                -0.00017 * sin(OO),
                -0.00007 * sin(M1 + 2 * M),
                +0.00004 * sin(2 * M1 - 2 * F),
                +0.00004 * sin(3 * M),
                +0.00003 * sin(M1 + M - 2 * F),
                +0.00003 * sin(2 * M1 + 2 * F),
                -0.00003 * sin(M1 + M + 2 * F),
                +0.00003 * sin(M1 - M + 2 * F),
                -0.00002 * sin(M1 - M - 2 * F),
                -0.00002 * sin(3 * M1 + M),
                +0.00002 * sin(4 * M1),
            )
        else:
            # First or last quarter
            pass
            corr = (  # p 352
                -0.62801 * sin(M1),
                +0.17172 * E * sin(M),
                -0.01183 * E * sin(M1 + M),
                +0.00862 * sin(2 * M1),
                +0.00804 * sin(2 * F),
                +0.00454 * E * sin(M1 - M),
                +0.00204 * E * E * sin(2 * M),
                -0.00180 * sin(M1 - 2 * F),
                -0.00070 * sin(M1 + 2 * F),
                -0.00040 * sin(3 * M1),
                -0.00034 * E * sin(2 * M1 - M),
                +0.00032 * E * sin(M + 2 * F),
                +0.00032 * E * sin(M - 2 * F),
                -0.00028 * E * E * sin(M1 + 2 * M),
                +0.00027 * E * sin(2 * M1 + M),
                -0.00017 * sin(OO),
                -0.00005 * sin(M1 - M - 2 * F),
                +0.00004 * sin(2 * M1 + 2 * F),
                -0.00004 * sin(M1 + M + 2 * F),
                +0.00004 * sin(M1 - 2 * M),
                +0.00003 * sin(M1 + M - 2 * F),
                +0.00003 * sin(3 * M),
                +0.00002 * sin(2 * M1 - 2 * F),
                +0.00002 * sin(M1 - M + 2 * F),
                -0.00002 * sin(3 * M1 + M),
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
        periodic2 = sum([i * sin(j) for i, j in zip(A1, A)])
        W = (
            0.00306
            - 0.00038 * E * cos(M)
            + 0.00026 * cos(M1)
            - 0.00002 * cos(M1 - M)
            + 0.00002 * cos(M1 + M)
            + 0.00002 * cos(2 * F)
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


if 1:  # Astronomical

    def KeplerEquation(e, M, reltol=0):
        """Returns eccentric anomaly E in radians by solving Kepler's equation 30.5 pg 195 via
        Sinnott's binary search algorithm on page 206.  e is orbital eccentricity (dimensionless)
        and M is the mean anomaly in radians.  Meeus gives the number of iterations required as
        3.32*digits, where digits is the platform's number of floating point digits (3.32 is the
        reciprocal of the base 10 logarithm of 2).

        I've typed the BASIC algorithm in mostly verbatim and translated it to python.  The numbers
        in the comments are the line numbers of the BASIC code.

        I've modified the program by stopping at a desired relative tolerance between iterations.
        Note if you set e.g. reltol to about 1e-15 or less, the algorithm won't get any better --
        it will just run its normal number of iterations.
        """
        P1 = pi  # 100
        F = sgn(M)  # 110
        M = abs(M) / (2 * P1)  # 110
        M = (M - int(M)) * 2 * P1 * F  # 120
        if M < 0:  # 130
            M += 2 * P1  # 130
        F = 1  # 140
        if M > P1:  # 150
            F = -1  # 150
        if M > P1:  # 160
            M = 2 * P1 - M  # 160
        E0 = P1 / 2  # 170
        D = P1 / 4  # 170
        Elast = E0 / 2
        max_iterations = ceil(sys.float_info.dig / log10(2))  # Typically == 50
        for J in range(max_iterations):  # 180
            M1 = E0 - e * sin(E0)  # 190
            E0 = E0 + D * sgn(M - M1)  # 200
            D = D / 2  # 200
            if reltol and J > 5:
                if abs((E0 - Elast) / Elast) <= reltol:
                    break
            Elast = E0
        # NEXT J                                 # 210
        E0 = E0 * F  # 220
        return E0


if __name__ == "__main__":
    from lwtest import run, raises

    def TestAngularSeparation():
        # Page 110:  Angular separation
        ra1 = radians(213.9154)
        dec1 = radians(19.1825)
        ra2 = radians(201.2983)
        dec2 = radians(-11.1614)
        d = AngularSeparation(ra1, dec1, ra2, dec2)
        Assert(fabs(degrees(d) - 32.7930) < 1e-4)

    def TestSiderealTime():
        # Page 88 and 89:  Sidereal time
        d = 10 + (19 + 21 / 60.0) / 24  # Example 12.b
        t = MeanSiderealTime(4, d, 1987)
        expected = 8 + 34.0 / 60 + 57.0896 / 3600
        Assert(t - expected < 1e-10)
        t = MeanSiderealTime(4, 10, 1987)
        h, m, s = hr2hms(t)
        Assert(h == 13 and m == 10)
        Assert(fabs(s - 46.3668) < 0.0001)
        t = ApparentSiderealTime(4, 10, 1987)
        h, m, s = hr2hms(t)
        Assert(h == 13 and m == 10)
        expected = 46.1351  # Example 12.a bottom
        Assert(fabs(s - expected) < 0.01)

    def TestCheckIntegerDate():
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

    def TestDayOfYear2MDY():
        # Page 65:  Day of the year
        Assert(DayOfYear2MDY(113, 1988) == (4, 22, 1988))
        Assert(DayOfYear2MDY(318, 1978) == (11, 14, 1978))

    def TestEarthSurfaceDistance():
        # Page 85:  Distance between points in France & USNO
        long1 = dms2rad(-2, 20, 14)
        lat1 = dms2rad(48, 50, 11)
        long2 = dms2rad(77, 3, 56)
        lat2 = dms2rad(38, 55, 17)
        d = EarthSurfaceDistance(lat1, long1, lat2, long2)
        Assert(fabs(d - 6181.63) <= 0.05)

    def TestLongitudinalDistance():
        # Page 83:  distance along a line of constant latitude
        latitude = dms2rad(42, 0, 0)
        angle = dms2rad(1, 0, 0)
        d = LongitudinalDistance(latitude, angle)
        Assert(fabs(d - 82.8508) < 0.0001)
        # Page 84:  distance along a line of constant longitude
        latitude = dms2rad(42, 0, 0)
        angle = dms2rad(1, 0, 0)
        d = LatitudinalDistance(latitude, angle)
        Assert(fabs(d - 111.0733) < 0.0001)

    def TestUT2DT():
        # Page 78:  Correction to universal time to get dynamical time
        Assert(fabs(UT2DT(1977) - 48) < 1)
        Assert(fabs(UT2DT(333) - 6146) < 1)

    def TestLinearRegression():
        # Page 40:  Linear regression
        x = (
            73,
            38,
            35,
            42,
            78,
            68,
            74,
            42,
            52,
            54,
            39,
            61,
            42,
            49,
            50,
            62,
            44,
            39,
            43,
            54,
            44,
            37,
        )
        y = (
            90.4,
            125.3,
            161.8,
            143.4,
            52.5,
            50.8,
            71.5,
            152.8,
            131.3,
            98.5,
            144.8,
            78.1,
            89.5,
            63.9,
            112.1,
            82.0,
            119.8,
            161.2,
            208.4,
            111.6,
            167.1,
            162.1,
        )
        slope, intercept, r = LinearRegression(x, y)
        Assert(fabs(slope + 2.49) < 0.01)
        Assert(fabs(intercept - 244.18) < 0.01)
        Assert(fabs(r + 0.767) < 0.001)

    def TestJulian():
        # Page 59:  Julian day and associated routines
        Assert(JulianAstro(10, 4.81, 1957) == 2436116.31)
        Assert(JulianAstro(1, 27.5, 333) == 1842713.0)
        Assert(JulianAstro(1, 1.5, -4712) == 0.0)
        Assert(DayOfWeek(11, 13, 1949) == 0)
        Assert(DayOfWeek(5, 30, 1998) == 6)
        Assert(DayOfYear(11, 14, 1978) == 318)
        Assert(DayOfYear(4, 22, 1980) == 113)
        month, day, year = JulianToMonthDayYear(2436116.31)
        Assert(month == 10)
        Assert(year == 1957)
        Assert(abs(day - 4.81) < 0.00001)
        month, day, year = JulianToMonthDayYear(1842713.0)
        Assert(month == 1)
        Assert(year == 333)
        Assert(abs(day - 27.5) < 0.00001)
        month, day, year = JulianToMonthDayYear(1507900.13)
        Assert(month == 5)
        Assert(year == -584)
        Assert(abs(day - 28.63) < 0.00001)
        Assert(NumDaysInMonth(1, 1999) == 31)
        Assert(NumDaysInMonth(2, 1999) == 28)
        Assert(NumDaysInMonth(3, 1999) == 31)
        Assert(NumDaysInMonth(4, 1999) == 30)
        Assert(NumDaysInMonth(5, 1999) == 31)
        Assert(NumDaysInMonth(6, 1999) == 30)
        Assert(NumDaysInMonth(7, 1999) == 31)
        Assert(NumDaysInMonth(8, 1999) == 31)
        Assert(NumDaysInMonth(9, 1999) == 30)
        Assert(NumDaysInMonth(10, 1999) == 31)
        Assert(NumDaysInMonth(11, 1999) == 30)
        Assert(NumDaysInMonth(12, 1999) == 31)
        Assert(NumDaysInMonth(1, 2000) == 31)
        Assert(NumDaysInMonth(2, 2000) == 29)
        Assert(NumDaysInMonth(3, 2000) == 31)
        Assert(NumDaysInMonth(4, 2000) == 30)
        Assert(NumDaysInMonth(5, 2000) == 31)
        Assert(NumDaysInMonth(6, 2000) == 30)
        Assert(NumDaysInMonth(7, 2000) == 31)
        Assert(NumDaysInMonth(8, 2000) == 31)
        Assert(NumDaysInMonth(9, 2000) == 30)
        Assert(NumDaysInMonth(10, 2000) == 31)
        Assert(NumDaysInMonth(11, 2000) == 30)
        Assert(NumDaysInMonth(12, 2000) == 31)

    def TestTransformationOfCoordinates():
        # Page 95:  Transformation of coordinates
        jd = JulianAstro(4, 10 + (19 + 21 / 60.0) / 24, 1987)
        longitude = dms2rad(77, 3, 56)
        latitude = dms2rad(38, 55, 17)
        ra = hms2rad(23, 9, 16.641)
        dec = dms2rad(-6, 43, 11.61)
        azimuth, altitude = LocalCoordinates(latitude, longitude, ra, dec, jd)
        Assert(fabs(azimuth - 248.03) < 0.01)
        Assert(fabs(altitude - 15.12) < 0.01)

    def TestPrecession():
        # Page 135:  Precession
        ra0 = hms2rad(2, 44, 11.986)
        dec0 = dms2rad(49, 13, 42.48)
        pm_ra = radians(0.03425 / 3600 * 15)
        pm_dec = radians(-0.0895 / 3600)
        jd0 = 2451545.0
        jd = 2462088.69
        ra, dec = Precession(jd, jd0, ra0, dec0, pm_ra, pm_dec)
        eps = 2e-6
        Assert(fabs(degrees(ra) - 41.547214) < eps)
        Assert(fabs(degrees(dec) - 49.348483) < eps)

    def TestPolarisPrecession():
        # For Polaris
        ra0 = hms2rad(2, 31, 48.704)
        dec0 = dms2rad(89, 15, 50.72)
        pm_ra = radians(0.19877 / 3600 * 15)
        pm_dec = radians(-0.0152 / 3600)
        jd0 = 2451545.0
        jd = JulianAstro(1, 1, 2050)
        ra, dec = Precession(jd, jd0, ra0, dec0, pm_ra, pm_dec)
        h, m, s = rad2hms(ra)
        Assert(h == 3 and m == 48 and fabs(s - 16.427) < 0.01)
        d, m, s = rad2dms(dec)
        Assert(d == 89 and m == 27 and fabs(s - 15.375) < 0.01)

    def TestEclipticObliquity():
        # Page 148:  obliquity of the ecliptic
        d, m, s = rad2dms(EclipticObliquity(2446895.5))
        Assert(d == 23 and m == 26 and fabs(s - 27.407) < 0.01)
        d_psi, d_eps = Nutation(2446895.5)
        Assert(fabs(d_psi + radians(3.788 / 3600)) < radians(0.5 / 3600))
        Assert(fabs(d_eps - radians(9.443 / 3600)) < radians(0.1 / 3600))
        # Page 147:  Obliquity of the ecliptic; example 28.b pg 185.
        eps = EclipticObliquity(JulianAstro(10, 13, 1992))
        Assert(fabs(degrees(eps) - 23.44023) < 1e-5)
        jd = JulianAstro(1, 1, 2050)

    def TestSunPosition():
        # Page 165:  solar coordinates
        ra, dec = SunPosition(2448908.5, apparent=0)
        Assert(fabs(degrees(ra) - 198.38) < 0.01)
        Assert(fabs(degrees(dec) + 7.785) < 0.001)

    def TestEquationOfTime():
        # Page 183:  Equation of Time; example 28.b pg 185
        jd = JulianAstro(10, 13, 1992)
        Assert(fabs(EquationOfTime(jd) - 0.059825572) < 1e-8)

    def TestSunMeanLongitude():
        # Page 183:  Sun's mean longitude; example 28.b pg 185
        T = (JulianAstro(10, 13, 1992) - 2451545) / 36525
        L0 = SunMeanLongitude(T)  # In radians
        Assert(fabs(degrees(L0) - 201.80720) < 1e-5)

    def TestEarthOrbitEccentricity():
        # Page 163:  Eccentricity of Earth's orbit; example 28.b pg 185.
        T = (JulianAstro(10, 13, 1992) - 2451545) / 36525
        e = EarthOrbitEccentricity(T)
        Assert(fabs(e - 0.016711668) < 1e-9)

    def TestSunMeanAnomaly():
        # Page 163:  Sun's mean anomaly; example 28.b pg 185.
        T = (JulianAstro(10, 13, 1992) - 2451545) / 36525
        M = degrees(SunMeanAnomaly(T))
        Assert(fabs(M - 278.99397) < 1e-5)

    def TestKeplerEquation():
        # Page 195:  Kepler's equation
        e, M = 0.1, radians(5)  # Example 30.a pg 196
        Assert(fabs(degrees(KeplerEquation(e, M)) - 5.554589) < 1e-6)
        e, M = 0.99, 0.2  # Example 30.a pg 196
        Assert(fabs(KeplerEquation(e, M) - 1.066997365282) < 1e-12)

    def TestSignum():
        # Signum function
        Assert(sgn(5) == 1)
        Assert(sgn(0) == 0)
        Assert(sgn(-5) == -1)
        Assert(sgn(5.0) == 1)
        Assert(sgn(0.0) == 0)
        Assert(sgn(-5.0) == -1)

    def TestSunriseSunset():
        # Sunrise & sunset for Alamo, CA on 15 Dec 2012.  Correct values come from
        # http://www.sunrisesunset.com/ (I prefer to use the USNO pages, but that website seems to
        # be down much of the time).  The MST times from the web were 05:07 and 20:30.  MST's
        # offset from UT is -7 hours.
        lat, long = radians(37 + 51.4 / 60), radians(121 + 59.9 / 60)
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
        min = int((rise - hr) * 60 + 0.5)
        Assert(hr == 7 and abs(min - 16) < 1)
        hr = int(set)
        min = int((set - hr) * 60 + 0.5)
        Assert(hr == 16 and abs(min - 50) < 1)

    def TestIsDST():
        # IsDST:  Test cases from http://www.webexhibits.org/daylightsaving/b.html accessed Mon 19
        # May 2014 09:23:55 AM.
        M, D, Y = 3, 14, 2010
        Assert(IsDST(M, D, Y))
        Assert(not IsDST(M, D - 1, Y))
        M, D, Y = 11, 7, 2010
        Assert(not IsDST(M, D, Y))
        Assert(IsDST(M, D - 1, Y))
        M, D, Y = 3, 13, 2011
        Assert(IsDST(M, D, Y))
        Assert(not IsDST(M, D - 1, Y))
        M, D, Y = 11, 6, 2011
        Assert(not IsDST(M, D, Y))
        Assert(IsDST(M, D - 1, Y))
        M, D, Y = 3, 11, 2012
        Assert(IsDST(M, D, Y))
        Assert(not IsDST(M, D - 1, Y))
        M, D, Y = 11, 4, 2012
        Assert(not IsDST(M, D, Y))
        Assert(IsDST(M, D - 1, Y))
        M, D, Y = 3, 10, 2013
        Assert(IsDST(M, D, Y))
        Assert(not IsDST(M, D - 1, Y))
        M, D, Y = 11, 3, 2013
        Assert(not IsDST(M, D, Y))
        Assert(IsDST(M, D - 1, Y))
        M, D, Y = 3, 9, 2014
        Assert(IsDST(M, D, Y))
        Assert(not IsDST(M, D - 1, Y))
        M, D, Y = 11, 2, 2014
        Assert(not IsDST(M, D, Y))
        Assert(IsDST(M, D - 1, Y))
        M, D, Y = 3, 8, 2015
        Assert(IsDST(M, D, Y))
        Assert(not IsDST(M, D - 1, Y))
        M, D, Y = 11, 1, 2015
        Assert(not IsDST(M, D, Y))
        Assert(IsDST(10, 31, Y))
        M, D, Y = 3, 13, 2016
        Assert(IsDST(M, D, Y))
        Assert(not IsDST(M, D - 1, Y))
        M, D, Y = 11, 6, 2016
        Assert(not IsDST(M, D, Y))
        Assert(IsDST(M, D - 1, Y))

    def TestTimeOfMoonPhase():
        yr = 1977.13  # Example 49.a, p 353
        t = TimeOfMoonPhase(yr, quarter=0)
        Assert(abs(t - 2443192.65118) < 0.00001)
        yr = 2044  # Example 49.b, p 353
        t = TimeOfMoonPhase(yr, quarter=3)
        Assert(abs(t - 2467636.49186) < 0.00001)

    def Test_dms2rad():
        d, m, s = 22, 30, 30
        t_rad = radians(d + m / 60 + s / 3600)
        Assert(t_rad == dms2rad(d, m, s))

    def Test_hms2rad():
        h, m, s = 22, 30, 30
        hrs = h + m / 60.0 + s / 3600.0
        t_deg = hrs * 15
        t_rad = radians(t_deg)
        Assert(t_rad == hms2rad(h, m, s))

    def Test_hr2hms():
        hr, hms = 12.5822222222, 12.3456
        h, m, s = hr2hms(hr)
        hms1 = h + m / 1e2 + s / 1e4
        Assert(abs(hms - hms1) < 0.0001)

    def TestIsLeapYear():
        Assert(IsLeapYear(1600))
        Assert(IsLeapYear(2000))
        Assert(IsLeapYear(2004))
        Assert(IsLeapYear(2400))
        Assert(not IsLeapYear(1700))
        Assert(not IsLeapYear(1800))
        Assert(not IsLeapYear(1900))
        Assert(not IsLeapYear(2100))
        Assert(not IsLeapYear(2200))

    def TestIsValidGregorianDate():
        Assert(IsValidGregorianDate(1, 1, 1583))
        Assert(IsValidGregorianDate(12, 31, 1583))
        Assert(not IsValidGregorianDate(1, 1, 1582))
        Assert(not IsValidGregorianDate(1, 32, 2000))

    def TestNormalize():
        Assert(Normalize(0, degrees=True) == 0)
        Assert(Normalize(1, degrees=True) == 1)
        Assert(Normalize(361, degrees=True) == 1)
        Assert(Normalize(-1, degrees=True) == 359)
        Assert(Normalize(0) == 0)
        Assert(Normalize(-pi / 2) == 3 * pi / 2)
        Assert(Normalize(-pi) == pi)

    def Test_product():
        a = (1, 2, 3, 4, 5, 6)
        Assert(product(a) == 720)

    def Test_rad2dms():
        Assert(dms2rad(*rad2dms(pi / 6)) == pi / 6)

    def Test_rad2hms():
        Assert(hms2rad(*rad2hms(pi / 6)) == pi / 6)

    def Test_SGN():
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

    def Test_JD():
        D = (  # jd, m, d for 2000 (a leap year)
            (1, 1, 1),
            (2, 1, 2),
            (3, 1, 3),
            (4, 1, 4),
            (5, 1, 5),
            (6, 1, 6),
            (7, 1, 7),
            (8, 1, 8),
            (9, 1, 9),
            (10, 1, 10),
            (11, 1, 11),
            (12, 1, 12),
            (13, 1, 13),
            (14, 1, 14),
            (15, 1, 15),
            (16, 1, 16),
            (17, 1, 17),
            (18, 1, 18),
            (19, 1, 19),
            (20, 1, 20),
            (21, 1, 21),
            (22, 1, 22),
            (23, 1, 23),
            (24, 1, 24),
            (25, 1, 25),
            (26, 1, 26),
            (27, 1, 27),
            (28, 1, 28),
            (29, 1, 29),
            (30, 1, 30),
            (31, 1, 31),
            (32, 2, 1),
            (33, 2, 2),
            (34, 2, 3),
            (35, 2, 4),
            (36, 2, 5),
            (37, 2, 6),
            (38, 2, 7),
            (39, 2, 8),
            (40, 2, 9),
            (41, 2, 10),
            (42, 2, 11),
            (43, 2, 12),
            (44, 2, 13),
            (45, 2, 14),
            (46, 2, 15),
            (47, 2, 16),
            (48, 2, 17),
            (49, 2, 18),
            (50, 2, 19),
            (51, 2, 20),
            (52, 2, 21),
            (53, 2, 22),
            (54, 2, 23),
            (55, 2, 24),
            (56, 2, 25),
            (57, 2, 26),
            (58, 2, 27),
            (59, 2, 28),
            (60, 2, 29),
            (61, 3, 1),
            (62, 3, 2),
            (63, 3, 3),
            (64, 3, 4),
            (65, 3, 5),
            (66, 3, 6),
            (67, 3, 7),
            (68, 3, 8),
            (69, 3, 9),
            (70, 3, 10),
            (71, 3, 11),
            (72, 3, 12),
            (73, 3, 13),
            (74, 3, 14),
            (75, 3, 15),
            (76, 3, 16),
            (77, 3, 17),
            (78, 3, 18),
            (79, 3, 19),
            (80, 3, 20),
            (81, 3, 21),
            (82, 3, 22),
            (83, 3, 23),
            (84, 3, 24),
            (85, 3, 25),
            (86, 3, 26),
            (87, 3, 27),
            (88, 3, 28),
            (89, 3, 29),
            (90, 3, 30),
            (91, 3, 31),
            (92, 4, 1),
            (93, 4, 2),
            (94, 4, 3),
            (95, 4, 4),
            (96, 4, 5),
            (97, 4, 6),
            (98, 4, 7),
            (99, 4, 8),
            (100, 4, 9),
            (101, 4, 10),
            (102, 4, 11),
            (103, 4, 12),
            (104, 4, 13),
            (105, 4, 14),
            (106, 4, 15),
            (107, 4, 16),
            (108, 4, 17),
            (109, 4, 18),
            (110, 4, 19),
            (111, 4, 20),
            (112, 4, 21),
            (113, 4, 22),
            (114, 4, 23),
            (115, 4, 24),
            (116, 4, 25),
            (117, 4, 26),
            (118, 4, 27),
            (119, 4, 28),
            (120, 4, 29),
            (121, 4, 30),
            (122, 5, 1),
            (123, 5, 2),
            (124, 5, 3),
            (125, 5, 4),
            (126, 5, 5),
            (127, 5, 6),
            (128, 5, 7),
            (129, 5, 8),
            (130, 5, 9),
            (131, 5, 10),
            (132, 5, 11),
            (133, 5, 12),
            (134, 5, 13),
            (135, 5, 14),
            (136, 5, 15),
            (137, 5, 16),
            (138, 5, 17),
            (139, 5, 18),
            (140, 5, 19),
            (141, 5, 20),
            (142, 5, 21),
            (143, 5, 22),
            (144, 5, 23),
            (145, 5, 24),
            (146, 5, 25),
            (147, 5, 26),
            (148, 5, 27),
            (149, 5, 28),
            (150, 5, 29),
            (151, 5, 30),
            (152, 5, 31),
            (153, 6, 1),
            (154, 6, 2),
            (155, 6, 3),
            (156, 6, 4),
            (157, 6, 5),
            (158, 6, 6),
            (159, 6, 7),
            (160, 6, 8),
            (161, 6, 9),
            (162, 6, 10),
            (163, 6, 11),
            (164, 6, 12),
            (165, 6, 13),
            (166, 6, 14),
            (167, 6, 15),
            (168, 6, 16),
            (169, 6, 17),
            (170, 6, 18),
            (171, 6, 19),
            (172, 6, 20),
            (173, 6, 21),
            (174, 6, 22),
            (175, 6, 23),
            (176, 6, 24),
            (177, 6, 25),
            (178, 6, 26),
            (179, 6, 27),
            (180, 6, 28),
            (181, 6, 29),
            (182, 6, 30),
            (183, 7, 1),
            (184, 7, 2),
            (185, 7, 3),
            (186, 7, 4),
            (187, 7, 5),
            (188, 7, 6),
            (189, 7, 7),
            (190, 7, 8),
            (191, 7, 9),
            (192, 7, 10),
            (193, 7, 11),
            (194, 7, 12),
            (195, 7, 13),
            (196, 7, 14),
            (197, 7, 15),
            (198, 7, 16),
            (199, 7, 17),
            (200, 7, 18),
            (201, 7, 19),
            (202, 7, 20),
            (203, 7, 21),
            (204, 7, 22),
            (205, 7, 23),
            (206, 7, 24),
            (207, 7, 25),
            (208, 7, 26),
            (209, 7, 27),
            (210, 7, 28),
            (211, 7, 29),
            (212, 7, 30),
            (213, 7, 31),
            (214, 8, 1),
            (215, 8, 2),
            (216, 8, 3),
            (217, 8, 4),
            (218, 8, 5),
            (219, 8, 6),
            (220, 8, 7),
            (221, 8, 8),
            (222, 8, 9),
            (223, 8, 10),
            (224, 8, 11),
            (225, 8, 12),
            (226, 8, 13),
            (227, 8, 14),
            (228, 8, 15),
            (229, 8, 16),
            (230, 8, 17),
            (231, 8, 18),
            (232, 8, 19),
            (233, 8, 20),
            (234, 8, 21),
            (235, 8, 22),
            (236, 8, 23),
            (237, 8, 24),
            (238, 8, 25),
            (239, 8, 26),
            (240, 8, 27),
            (241, 8, 28),
            (242, 8, 29),
            (243, 8, 30),
            (244, 8, 31),
            (245, 9, 1),
            (246, 9, 2),
            (247, 9, 3),
            (248, 9, 4),
            (249, 9, 5),
            (250, 9, 6),
            (251, 9, 7),
            (252, 9, 8),
            (253, 9, 9),
            (254, 9, 10),
            (255, 9, 11),
            (256, 9, 12),
            (257, 9, 13),
            (258, 9, 14),
            (259, 9, 15),
            (260, 9, 16),
            (261, 9, 17),
            (262, 9, 18),
            (263, 9, 19),
            (264, 9, 20),
            (265, 9, 21),
            (266, 9, 22),
            (267, 9, 23),
            (268, 9, 24),
            (269, 9, 25),
            (270, 9, 26),
            (271, 9, 27),
            (272, 9, 28),
            (273, 9, 29),
            (274, 9, 30),
            (275, 10, 1),
            (276, 10, 2),
            (277, 10, 3),
            (278, 10, 4),
            (279, 10, 5),
            (280, 10, 6),
            (281, 10, 7),
            (282, 10, 8),
            (283, 10, 9),
            (284, 10, 10),
            (285, 10, 11),
            (286, 10, 12),
            (287, 10, 13),
            (288, 10, 14),
            (289, 10, 15),
            (290, 10, 16),
            (291, 10, 17),
            (292, 10, 18),
            (293, 10, 19),
            (294, 10, 20),
            (295, 10, 21),
            (296, 10, 22),
            (297, 10, 23),
            (298, 10, 24),
            (299, 10, 25),
            (300, 10, 26),
            (301, 10, 27),
            (302, 10, 28),
            (303, 10, 29),
            (304, 10, 30),
            (305, 10, 31),
            (306, 11, 1),
            (307, 11, 2),
            (308, 11, 3),
            (309, 11, 4),
            (310, 11, 5),
            (311, 11, 6),
            (312, 11, 7),
            (313, 11, 8),
            (314, 11, 9),
            (315, 11, 10),
            (316, 11, 11),
            (317, 11, 12),
            (318, 11, 13),
            (319, 11, 14),
            (320, 11, 15),
            (321, 11, 16),
            (322, 11, 17),
            (323, 11, 18),
            (324, 11, 19),
            (325, 11, 20),
            (326, 11, 21),
            (327, 11, 22),
            (328, 11, 23),
            (329, 11, 24),
            (330, 11, 25),
            (331, 11, 26),
            (332, 11, 27),
            (333, 11, 28),
            (334, 11, 29),
            (335, 11, 30),
            (336, 12, 1),
            (337, 12, 2),
            (338, 12, 3),
            (339, 12, 4),
            (340, 12, 5),
            (341, 12, 6),
            (342, 12, 7),
            (343, 12, 8),
            (344, 12, 9),
            (345, 12, 10),
            (346, 12, 11),
            (347, 12, 12),
            (348, 12, 13),
            (349, 12, 14),
            (350, 12, 15),
            (351, 12, 16),
            (352, 12, 17),
            (353, 12, 18),
            (354, 12, 19),
            (355, 12, 20),
            (356, 12, 21),
            (357, 12, 22),
            (358, 12, 23),
            (359, 12, 24),
            (360, 12, 25),
            (361, 12, 26),
            (362, 12, 27),
            (363, 12, 28),
            (364, 12, 29),
            (365, 12, 30),
        )
        yr = 2000
        for jd, m, d in D:
            Assert(jd == JD(*JD2MDY(jd, yr)))

    def Test_MDY2ISO():
        Assert(MDY2ISO(1, 1, 2014) == 20140101)
        Assert(MDY2ISO(12, 31, 2014) == 20141231)
        raises(ValueError, MDY2ISO, 12, 32, 2014)

    exit(run(globals(), halt=1)[0])
