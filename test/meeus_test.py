import sys
from meeus import *
from lwtest import run, assert_equal, raises
from pdb import set_trace as xx

def TestAngularSeparation():
    # Page 110:  Angular separation
    ra1  = radians(213.9154)
    dec1 = radians(19.1825)
    ra2  = radians(201.2983)
    dec2 = radians(-11.1614)
    d = AngularSeparation(ra1, dec1, ra2, dec2)
    assert(fabs(degrees(d) - 32.7930) < 1e-4)
def TestSiderealTime():
    # Page 88 and 89:  Sidereal time
    d = 10 + (19 + 21/60.)/24   # Example 12.b
    t = MeanSiderealTime(4, d, 1987)
    expected = 8 + 34./60 + 57.0896/3600
    assert(t - expected < 1e-10)
    t = MeanSiderealTime(4, 10, 1987)
    h, m, s = hr2hms(t)
    assert(h == 13 and m == 10)
    assert(fabs(s - 46.3668) < 0.0001)
    t = ApparentSiderealTime(4, 10, 1987)
    h, m, s = hr2hms(t)
    assert(h == 13 and m == 10)
    expected = 46.1351  # Example 12.a bottom
    assert(fabs(s - expected) < 0.01)
def TestCheckIntegerDate():
    # Bad month
    raises(ValueError, CheckIntegerDate, 13, 1, 1)
    raises(ValueError, CheckIntegerDate, 0, 1, 1)
    # Bad day
    raises(ValueError, CheckIntegerDate, 1, 0, 1)
    raises(ValueError, CheckIntegerDate, 1, 32, 1)
    # Bad year
    raises(ValueError, CheckIntegerDate, 1, 1, G.minimum_year - 1)
    max_year = datetime.MAXYEAR
    raises(ValueError, CheckIntegerDate, 1, 1, max_year + 1)
    # OK date
    CheckIntegerDate( 1,  1, 2000)
    CheckIntegerDate(12, 31, 2000)
    CheckIntegerDate( 1,  1.1, 2000, decimal_day=True)
    CheckIntegerDate(12, 30.1, 2000, decimal_day=True)

def TestDayOfYear2MDY():
    # Page 65:  Day of the year
    assert(DayOfYear2MDY(113, 1988) == (4, 22, 1988))
    assert(DayOfYear2MDY(318, 1978) == (11, 14, 1978))
def TestEarthSurfaceDistance():
    # Page 85:  Distance between points in France & USNO
    long1 = dms2rad(-2, 20, 14)
    lat1  = dms2rad(48, 50, 11)
    long2 = dms2rad(77,  3, 56)
    lat2  = dms2rad(38, 55, 17)
    d = EarthSurfaceDistance(lat1, long1, lat2, long2)
    assert(fabs(d - 6181.63) <= .05)
def TestLongitudinalDistance():
    # Page 83:  distance along a line of constant latitude
    latitude = dms2rad(42, 0, 0)
    angle = dms2rad(1, 0, 0)
    d = LongitudinalDistance(latitude, angle)
    assert(fabs(d - 82.8508) < 0.0001)
    # Page 84:  distance along a line of constant longitude
    latitude = dms2rad(42, 0, 0)
    angle = dms2rad(1, 0, 0)
    d = LatitudinalDistance(latitude, angle)
    assert(fabs(d - 111.0733) < 0.0001)
def TestUT2DT():
    # Page 78:  Correction to universal time to get dynamical time
    assert(fabs(UT2DT(1977) - 48) < 1)
    assert(fabs(UT2DT(333) - 6146) < 1)
def TestLagrangeInterpolation():
    # Page 34:  Lagrangian interpolation
    X = [29.43, 30.97, 27.69, 28.11, 31.58, 33.05]
    Y = [0.4913598528, 0.5145891926, 0.4646875083, 0.4711658342,
         0.5236885653, 0.5453707057]
    d = LagrangeInterpolation(30, X, Y)
    assert(fabs(d - 1/2.) < 1e-9)
    d = LagrangeInterpolation(0, X, Y)
    assert(fabs(d - 0.0000482) < 1e-5)
    d = LagrangeInterpolation(90, X, Y)
    assert(fabs(d - 1.00007) < 2e-4)
def TestLinearRegression():
    # Page 40:  Linear regression
    x = (73, 38, 35, 42, 78, 68, 74, 42, 52, 54, 39,
         61, 42, 49, 50, 62, 44, 39, 43, 54, 44, 37)
    y = (90.4, 125.3, 161.8, 143.4,  52.5,  50.8,  71.5, 152.8,
         131.3,  98.5, 144.8, 78.1,  89.5,  63.9, 112.1,  82.0, 119.8,
         161.2, 208.4, 111.6, 167.1, 162.1)
    slope, intercept, r = LinearRegression(x, y)
    assert(fabs(slope + 2.49) < .01)
    assert(fabs(intercept - 244.18) < .01)
    assert(fabs(r + 0.767) < .001)
def TestJulian():
    # Page 59:  Julian day and associated routines
    assert(JulianAstro(10, 4.81, 1957) == 2436116.31)
    assert(JulianAstro(1, 27.5, 333) == 1842713.0)
    assert(JulianAstro(1, 1.5, -4712) == 0.0)
    assert(DayOfWeek(11, 13, 1949) == 0)
    assert(DayOfWeek( 5, 30, 1998) == 6)
    assert(DayOfYear(11, 14, 1978) == 318)
    assert(DayOfYear( 4, 22, 1980) == 113)
    month, day, year = JulianToMonthDayYear(2436116.31)
    assert(month == 10)
    assert(year == 1957)
    assert(abs(day - 4.81) < 0.00001)
    month, day, year = JulianToMonthDayYear(1842713.0)
    assert(month == 1)
    assert(year == 333)
    assert(abs(day - 27.5) < 0.00001)
    month, day, year = JulianToMonthDayYear(1507900.13)
    assert(month == 5)
    assert(year == -584)
    assert(abs(day - 28.63) < 0.00001)
    assert(NumDaysInMonth( 1, 1999) == 31)
    assert(NumDaysInMonth( 2, 1999) == 28)
    assert(NumDaysInMonth( 3, 1999) == 31)
    assert(NumDaysInMonth( 4, 1999) == 30)
    assert(NumDaysInMonth( 5, 1999) == 31)
    assert(NumDaysInMonth( 6, 1999) == 30)
    assert(NumDaysInMonth( 7, 1999) == 31)
    assert(NumDaysInMonth( 8, 1999) == 31)
    assert(NumDaysInMonth( 9, 1999) == 30)
    assert(NumDaysInMonth(10, 1999) == 31)
    assert(NumDaysInMonth(11, 1999) == 30)
    assert(NumDaysInMonth(12, 1999) == 31)
    assert(NumDaysInMonth( 1, 2000) == 31)
    assert(NumDaysInMonth( 2, 2000) == 29)
    assert(NumDaysInMonth( 3, 2000) == 31)
    assert(NumDaysInMonth( 4, 2000) == 30)
    assert(NumDaysInMonth( 5, 2000) == 31)
    assert(NumDaysInMonth( 6, 2000) == 30)
    assert(NumDaysInMonth( 7, 2000) == 31)
    assert(NumDaysInMonth( 8, 2000) == 31)
    assert(NumDaysInMonth( 9, 2000) == 30)
    assert(NumDaysInMonth(10, 2000) == 31)
    assert(NumDaysInMonth(11, 2000) == 30)
    assert(NumDaysInMonth(12, 2000) == 31)
def TestTransformationOfCoordinates():
    # Page 95:  Transformation of coordinates
    jd = JulianAstro(4, 10 + (19 + 21/60.)/24, 1987)
    longitude = dms2rad(77, 3, 56)
    latitude = dms2rad(38, 55, 17)
    ra = hms2rad(23, 9, 16.641)
    dec = dms2rad(-6, 43, 11.61)
    azimuth, altitude = LocalCoordinates(latitude, longitude, ra, dec, jd)
    assert(fabs(azimuth - 248.03) < 0.01)
    assert(fabs(altitude - 15.12) < 0.01)
def TestPrecession():
    # Page 135:  Precession
    ra0 = hms2rad(2, 44, 11.986)
    dec0 = dms2rad(49, 13, 42.48)
    pm_ra = radians(0.03425/3600*15)
    pm_dec = radians(-0.0895/3600)
    jd0 = 2451545.0
    jd = 2462088.69
    ra, dec = Precession(jd, jd0, ra0, dec0, pm_ra, pm_dec)
    eps = 2e-6
    assert(fabs(degrees(ra) - 41.547214) < eps)
    assert(fabs(degrees(dec) - 49.348483) < eps)
def TestPolarisPrecession():
    # For Polaris
    ra0 = hms2rad(2, 31, 48.704)
    dec0 = dms2rad(89, 15, 50.72)
    pm_ra = radians(0.19877/3600*15)
    pm_dec = radians(-0.0152/3600)
    jd0 = 2451545.0
    jd = JulianAstro(1, 1, 2050)
    ra, dec = Precession(jd, jd0, ra0, dec0, pm_ra, pm_dec)
    h, m, s = rad2hms(ra)
    assert(h == 3 and m == 48 and fabs(s - 16.427) < 0.01)
    d, m, s = rad2dms(dec)
    assert(d == 89 and m == 27 and fabs(s - 15.375) < 0.01)
def TestEclipticObliquity():
    # Page 148:  obliquity of the ecliptic
    d, m, s = rad2dms(EclipticObliquity(2446895.5))
    assert(d == 23 and m == 26 and fabs(s - 27.407) < 0.01)
    d_psi, d_eps = Nutation(2446895.5)
    assert(fabs(d_psi + radians(3.788/3600)) < radians(0.5/3600))
    assert(fabs(d_eps - radians(9.443/3600)) < radians(0.1/3600))
    # Page 147:  Obliquity of the ecliptic; example 28.b pg 185.
    eps = EclipticObliquity(JulianAstro(10, 13, 1992))
    assert(fabs(degrees(eps) - 23.44023) < 1e-5)
    jd = JulianAstro(1, 1, 2050)
def TestSunPosition():
    # Page 165:  solar coordinates
    ra, dec = SunPosition(2448908.5, apparent=0)
    assert(fabs(degrees(ra) - 198.38) < 0.01)
    assert(fabs(degrees(dec) + 7.785) < 0.001)
def TestEquationOfTime():
    # Page 183:  Equation of Time; example 28.b pg 185
    jd = JulianAstro(10, 13, 1992)
    assert(fabs(EquationOfTime(jd) - 0.059825572) < 1e-8)
def TestSunMeanLongitude():
    # Page 183:  Sun's mean longitude; example 28.b pg 185
    T = (JulianAstro(10, 13, 1992) - 2451545)/36525
    L0 = SunMeanLongitude(T)            # In radians
    assert(fabs(degrees(L0) - 201.80720) < 1e-5)
def TestEarthOrbitEccentricity():
    # Page 163:  Eccentricity of Earth's orbit; example 28.b pg 185.
    T = (JulianAstro(10, 13, 1992) - 2451545)/36525
    e = EarthOrbitEccentricity(T)
    assert(fabs(e - 0.016711668) < 1e-9)
def TestSunMeanAnomaly():
    # Page 163:  Sun's mean anomaly; example 28.b pg 185.
    T = (JulianAstro(10, 13, 1992) - 2451545)/36525
    M = degrees(SunMeanAnomaly(T))
    assert(fabs(M - 278.99397) < 1e-5)
def TestKeplerEquation():
    # Page 195:  Kepler's equation
    e, M = 0.1, radians(5)  # Example 30.a pg 196
    assert(fabs(degrees(KeplerEquation(e, M)) - 5.554589) < 1e-6)
    e, M = 0.99, 0.2  # Example 30.a pg 196
    assert(fabs(KeplerEquation(e, M) - 1.066997365282) < 1e-12)
def TestSignum():
    # Signum function
    assert(SGN(5) == 1)
    assert(SGN(0) == 0)
    assert(SGN(-5) == -1)
    assert(SGN(5.0) == 1)
    assert(SGN(0.0) == 0)
    assert(SGN(-5.0) == -1)
def TestSunriseSunset():
    # Sunrise & sunset for Alamo, CA on 15 Dec 2012.  Correct values
    # come from http://www.sunrisesunset.com/ (I prefer to use the
    # USNO pages, but that website seems to be down much of the time).
    # The MST times from the web were 05:07 and 20:30.  MST's offset
    # from UT is -7 hours.
    lat, long = radians(37 + 51.4/60), radians(121 + 59.9/60)
    rise, set = SunriseSunset(12, 15, 2012, lat, long)
    # Results should be sunrise = 7:16 am, sunset = 4:50 pm.
    offset = -8
    rise += offset
    set  += offset
    if rise < 0:
        rise += 24
    if set < 0:
        set += 24
    hr = int(rise)
    min = int((rise - hr)*60 + 0.5)
    assert(hr == 7 and abs(min - 16) < 1)
    hr = int(set)
    min = int((set - hr)*60 + 0.5)
    assert(hr == 16 and abs(min - 50) < 1)
def TestIsDST():
    # IsDST:  Test cases from
    # http://www.webexhibits.org/daylightsaving/b.html accessed Mon 19
    # May 2014 09:23:55 AM.
    M, D, Y = 3, 14, 2010
    assert(IsDST(M, D, Y))
    assert(not IsDST(M, D-1, Y))
    M, D, Y = 11, 7, 2010
    assert(not IsDST(M, D, Y))
    assert(IsDST(M, D-1, Y))
    M, D, Y = 3, 13, 2011
    assert(IsDST(M, D, Y))
    assert(not IsDST(M, D-1, Y))
    M, D, Y = 11, 6, 2011
    assert(not IsDST(M, D, Y))
    assert(IsDST(M, D-1, Y))
    M, D, Y = 3, 11, 2012
    assert(IsDST(M, D, Y))
    assert(not IsDST(M, D-1, Y))
    M, D, Y = 11, 4, 2012
    assert(not IsDST(M, D, Y))
    assert(IsDST(M, D-1, Y))
    M, D, Y = 3, 10, 2013
    assert(IsDST(M, D, Y))
    assert(not IsDST(M, D-1, Y))
    M, D, Y = 11, 3, 2013
    assert(not IsDST(M, D, Y))
    assert(IsDST(M, D-1, Y))
    M, D, Y = 3,  9, 2014
    assert(IsDST(M, D, Y))
    assert(not IsDST(M, D-1, Y))
    M, D, Y = 11, 2, 2014
    assert(not IsDST(M, D, Y))
    assert(IsDST(M, D-1, Y))
    M, D, Y = 3,  8, 2015
    assert(IsDST(M, D, Y))
    assert(not IsDST(M, D-1, Y))
    M, D, Y = 11, 1, 2015
    assert(not IsDST(M, D, Y))
    assert(IsDST(10, 31, Y))
    M, D, Y = 3, 13, 2016
    assert(IsDST(M, D, Y))
    assert(not IsDST(M, D-1, Y))
    M, D, Y = 11, 6, 2016
    assert(not IsDST(M, D, Y))
    assert(IsDST(M, D-1, Y))
def TestTimeOfMoonPhase():
    yr = 1977.13    # Example 49.a, p 353
    t = TimeOfMoonPhase(yr, quarter=0)
    assert(abs(t - 2443192.65118) < 0.00001)
    yr = 2044       # Example 49.b, p 353
    t = TimeOfMoonPhase(yr, quarter=3)
    assert(abs(t - 2467636.49186) < 0.00001)
def Test_dms2rad():
    d, m, s = 22, 30, 30
    t_rad = radians(d + m/60 + s/3600)
    assert(t_rad == dms2rad(d, m, s))
def Test_hms2rad():
    h, m, s = 22, 30, 30
    hrs = h + m/60.0 + s/3600.0
    t_deg = hrs*15
    t_rad = radians(t_deg)
    assert(t_rad == hms2rad(h, m, s))
def Test_hr2hms():
    hr, hms = 12.5822222222, 12.3456
    h, m, s = hr2hms(hr)
    hms1 = h + m/1e2 + s/1e4
    assert(abs(hms - hms1) < 0.0001)
def TestIsLeapYear():
    assert(IsLeapYear(1600))
    assert(IsLeapYear(2000))
    assert(IsLeapYear(2004))
    assert(IsLeapYear(2400))
    assert(not IsLeapYear(1700))
    assert(not IsLeapYear(1800))
    assert(not IsLeapYear(1900))
    assert(not IsLeapYear(2100))
    assert(not IsLeapYear(2200))
def TestIsValidGregorianDate():
    assert(IsValidGregorianDate(1, 1, 1583))
    assert(IsValidGregorianDate(12, 31, 1583))
    assert(not IsValidGregorianDate(1, 1, 1582))
    assert(not IsValidGregorianDate(1, 32, 2000))
def TestNormalize():
    assert(Normalize(0, degrees=True) == 0)
    assert(Normalize(1, degrees=True) == 1)
    assert(Normalize(361, degrees=True) == 1)
    assert(Normalize(-1, degrees=True) == 359)
    assert(Normalize(0) == 0)
    assert(Normalize(-pi/2) == 3*pi/2)
    assert(Normalize(-pi) == pi)
def Test_product():
    a = (1, 2, 3, 4, 5, 6)
    assert(product(a) == 720)
def Test_rad2dms():
    assert(dms2rad(*rad2dms(pi/6)) == pi/6)
def Test_rad2hms():
    assert(hms2rad(*rad2hms(pi/6)) == pi/6)
def Test_SGN():
    assert(SGN(-5) == -1)
    assert(SGN(-1) == -1)
    assert(SGN( 0) ==  0)
    assert(SGN( 1) ==  1)
    assert(SGN( 5) ==  1)
    assert(SGN(-5.) == -1)
    assert(SGN(-1.) == -1)
    assert(SGN( 0.) ==  0)
    assert(SGN( 1.) ==  1)
    assert(SGN( 5.) ==  1)
def Test_JD():
    D = ( # jd, m, d for 2000 (a leap year)
        (1, 1, 1), (2, 1, 2), (3, 1, 3), (4, 1, 4), (5, 1, 5), (6, 1, 6),
        (7, 1, 7), (8, 1, 8), (9, 1, 9), (10, 1, 10), (11, 1, 11),
        (12, 1, 12), (13, 1, 13), (14, 1, 14), (15, 1, 15), (16, 1, 16),
        (17, 1, 17), (18, 1, 18), (19, 1, 19), (20, 1, 20), (21, 1, 21),
        (22, 1, 22), (23, 1, 23), (24, 1, 24), (25, 1, 25), (26, 1, 26),
        (27, 1, 27), (28, 1, 28), (29, 1, 29), (30, 1, 30), (31, 1, 31),
        (32, 2, 1), (33, 2, 2), (34, 2, 3), (35, 2, 4), (36, 2, 5),
        (37, 2, 6), (38, 2, 7), (39, 2, 8), (40, 2, 9), (41, 2, 10),
        (42, 2, 11), (43, 2, 12), (44, 2, 13), (45, 2, 14), (46, 2, 15),
        (47, 2, 16), (48, 2, 17), (49, 2, 18), (50, 2, 19), (51, 2, 20),
        (52, 2, 21), (53, 2, 22), (54, 2, 23), (55, 2, 24), (56, 2, 25),
        (57, 2, 26), (58, 2, 27), (59, 2, 28), (60, 2, 29), (61, 3, 1),
        (62, 3, 2), (63, 3, 3), (64, 3, 4), (65, 3, 5), (66, 3, 6),
        (67, 3, 7), (68, 3, 8), (69, 3, 9), (70, 3, 10), (71, 3, 11),
        (72, 3, 12), (73, 3, 13), (74, 3, 14), (75, 3, 15), (76, 3, 16),
        (77, 3, 17), (78, 3, 18), (79, 3, 19), (80, 3, 20), (81, 3, 21),
        (82, 3, 22), (83, 3, 23), (84, 3, 24), (85, 3, 25), (86, 3, 26),
        (87, 3, 27), (88, 3, 28), (89, 3, 29), (90, 3, 30), (91, 3, 31),
        (92, 4, 1), (93, 4, 2), (94, 4, 3), (95, 4, 4), (96, 4, 5),
        (97, 4, 6), (98, 4, 7), (99, 4, 8), (100, 4, 9), (101, 4, 10),
        (102, 4, 11), (103, 4, 12), (104, 4, 13), (105, 4, 14),
        (106, 4, 15), (107, 4, 16), (108, 4, 17), (109, 4, 18),
        (110, 4, 19), (111, 4, 20), (112, 4, 21), (113, 4, 22),
        (114, 4, 23), (115, 4, 24), (116, 4, 25), (117, 4, 26),
        (118, 4, 27), (119, 4, 28), (120, 4, 29), (121, 4, 30),
        (122, 5, 1), (123, 5, 2), (124, 5, 3), (125, 5, 4),
        (126, 5, 5), (127, 5, 6), (128, 5, 7), (129, 5, 8),
        (130, 5, 9), (131, 5, 10), (132, 5, 11), (133, 5, 12),
        (134, 5, 13), (135, 5, 14), (136, 5, 15), (137, 5, 16),
        (138, 5, 17), (139, 5, 18), (140, 5, 19), (141, 5, 20),
        (142, 5, 21), (143, 5, 22), (144, 5, 23), (145, 5, 24),
        (146, 5, 25), (147, 5, 26), (148, 5, 27), (149, 5, 28),
        (150, 5, 29), (151, 5, 30), (152, 5, 31), (153, 6, 1),
        (154, 6, 2), (155, 6, 3), (156, 6, 4), (157, 6, 5),
        (158, 6, 6), (159, 6, 7), (160, 6, 8), (161, 6, 9),
        (162, 6, 10), (163, 6, 11), (164, 6, 12), (165, 6, 13),
        (166, 6, 14), (167, 6, 15), (168, 6, 16), (169, 6, 17),
        (170, 6, 18), (171, 6, 19), (172, 6, 20), (173, 6, 21),
        (174, 6, 22), (175, 6, 23), (176, 6, 24), (177, 6, 25),
        (178, 6, 26), (179, 6, 27), (180, 6, 28), (181, 6, 29),
        (182, 6, 30), (183, 7, 1), (184, 7, 2), (185, 7, 3),
        (186, 7, 4), (187, 7, 5), (188, 7, 6), (189, 7, 7),
        (190, 7, 8), (191, 7, 9), (192, 7, 10), (193, 7, 11),
        (194, 7, 12), (195, 7, 13), (196, 7, 14), (197, 7, 15),
        (198, 7, 16), (199, 7, 17), (200, 7, 18), (201, 7, 19),
        (202, 7, 20), (203, 7, 21), (204, 7, 22), (205, 7, 23),
        (206, 7, 24), (207, 7, 25), (208, 7, 26), (209, 7, 27),
        (210, 7, 28), (211, 7, 29), (212, 7, 30), (213, 7, 31),
        (214, 8, 1), (215, 8, 2), (216, 8, 3), (217, 8, 4),
        (218, 8, 5), (219, 8, 6), (220, 8, 7), (221, 8, 8),
        (222, 8, 9), (223, 8, 10), (224, 8, 11), (225, 8, 12),
        (226, 8, 13), (227, 8, 14), (228, 8, 15), (229, 8, 16),
        (230, 8, 17), (231, 8, 18), (232, 8, 19), (233, 8, 20),
        (234, 8, 21), (235, 8, 22), (236, 8, 23), (237, 8, 24),
        (238, 8, 25), (239, 8, 26), (240, 8, 27), (241, 8, 28),
        (242, 8, 29), (243, 8, 30), (244, 8, 31), (245, 9, 1),
        (246, 9, 2), (247, 9, 3), (248, 9, 4), (249, 9, 5),
        (250, 9, 6), (251, 9, 7), (252, 9, 8), (253, 9, 9),
        (254, 9, 10), (255, 9, 11), (256, 9, 12), (257, 9, 13),
        (258, 9, 14), (259, 9, 15), (260, 9, 16), (261, 9, 17),
        (262, 9, 18), (263, 9, 19), (264, 9, 20), (265, 9, 21),
        (266, 9, 22), (267, 9, 23), (268, 9, 24), (269, 9, 25),
        (270, 9, 26), (271, 9, 27), (272, 9, 28), (273, 9, 29),
        (274, 9, 30), (275, 10, 1), (276, 10, 2), (277, 10, 3),
        (278, 10, 4), (279, 10, 5), (280, 10, 6), (281, 10, 7),
        (282, 10, 8), (283, 10, 9), (284, 10, 10), (285, 10, 11),
        (286, 10, 12), (287, 10, 13), (288, 10, 14), (289, 10, 15),
        (290, 10, 16), (291, 10, 17), (292, 10, 18), (293, 10, 19),
        (294, 10, 20), (295, 10, 21), (296, 10, 22), (297, 10, 23),
        (298, 10, 24), (299, 10, 25), (300, 10, 26), (301, 10, 27),
        (302, 10, 28), (303, 10, 29), (304, 10, 30), (305, 10, 31),
        (306, 11, 1), (307, 11, 2), (308, 11, 3), (309, 11, 4),
        (310, 11, 5), (311, 11, 6), (312, 11, 7), (313, 11, 8),
        (314, 11, 9), (315, 11, 10), (316, 11, 11), (317, 11, 12),
        (318, 11, 13), (319, 11, 14), (320, 11, 15), (321, 11, 16),
        (322, 11, 17), (323, 11, 18), (324, 11, 19), (325, 11, 20),
        (326, 11, 21), (327, 11, 22), (328, 11, 23), (329, 11, 24),
        (330, 11, 25), (331, 11, 26), (332, 11, 27), (333, 11, 28),
        (334, 11, 29), (335, 11, 30), (336, 12, 1), (337, 12, 2),
        (338, 12, 3), (339, 12, 4), (340, 12, 5), (341, 12, 6),
        (342, 12, 7), (343, 12, 8), (344, 12, 9), (345, 12, 10),
        (346, 12, 11), (347, 12, 12), (348, 12, 13), (349, 12, 14),
        (350, 12, 15), (351, 12, 16), (352, 12, 17), (353, 12, 18),
        (354, 12, 19), (355, 12, 20), (356, 12, 21), (357, 12, 22),
        (358, 12, 23), (359, 12, 24), (360, 12, 25), (361, 12, 26),
        (362, 12, 27), (363, 12, 28), (364, 12, 29), (365, 12, 30),
    )
    yr = 2000
    for jd, m, d in D:
        assert(jd == JD(*JD2MDY(jd, yr)))
def Test_MDY2ISO():
    assert(MDY2ISO(1, 1, 2014) == 20140101)
    assert(MDY2ISO(12, 31, 2014) == 20141231)
    raises(ValueError, MDY2ISO, 12, 32, 2014)

if __name__ == "__main__":
    exit(run(globals())[0])
