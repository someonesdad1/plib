'''
Module to provide thermocouple class TC instances for calculation of voltage and temperature
    
    The class TC uses NIST-published polynomial approximations to calculate temperature from
    voltage and voltage from temperature.
 
    Example usage for a type K thermocouple:
        tc = TC("K")
        mV = 6.7 # Voltage in mV
        T = tc.T_degC(mV)
            T --> 164.0136451711743     # Temperature in °C referenced to 0 °C
        E = tc.E_mV(164.0136451711743)
            E --> 6.701060829501329     # Voltage in mV
 
    Run as a script to produce thermocouple tables to stdout.
'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2009 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print thermocouple tables
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard Imports
        import sys
        import getopt
        from math import exp
    # Custom imports
        from f import flt
        from wrap import dedent, indent
        from lwtest import run, assert_equal, raises
        from color import t as U
    # Global variables
        class G:    # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        # Thermocouple table ranges
        g.table_ranges = {
            # [(temp_low_C, temp_high_C), (V_low_mV, V_high_mV)]
            "B": ((   0, 1820), (-0.003, 13.820)),
            "E": ((-270, 1000), (-9.835, 76.373)),
            "J": ((-210, 1200), (-8.095, 69.553)),
            "K": ((-270, 1372), (-6.095, 54.886)),
            "N": ((-270, 1300), (-4.345, 47.513)),
            "R": (( -50, 1768), (-0.226, 21.101)),
            "S": (( -50, 1768), (-0.236, 18.693)),
            "T": ((-270,  400), (-6.258, 20.872)),
        }
        # Colors
        U.title = U("ornl")
        U.ref = U("magl")
        U.row = U("denl")
if 1:  # NIST coefficients for thermocouple polynomials
        # The following are the exponential coefficients for the type K
        # thermocouple.
        type_K_exponential = (
            0.1185976E+00,
            -0.1183432E-03,
            0.1269686E+03,
        )
        # In the following, E is EMF in mV and t is temperature in °C.  These coefficients came
        # from https://srdata.nist.gov/its90/main/.  Click on the "Download tables" link, then
        # click on the "Coefficients of All Thermocouple Types", which is
        # https://srdata.nist.gov/its90/download/allcoeff.tab for the text file of all the
        # coefficients.
        nist_tc_forward = {
            # Polynomials for E(t)
            "B" : (
                (
                    (0.000, 630.615),          # degC range over which polynomial valid
                    6,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        -0.246508183460E-03,
                        0.590404211710E-05,
                        -0.132579316360E-08,
                        0.156682919010E-11,
                        -0.169445292400E-14,
                        0.629903470940E-18,
                    )
                ),
                (
                    (630.615, 1820.000),       # degC range over which polynomial valid
                    8,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        -0.389381686210E+01,
                        0.285717474700E-01,
                        -0.848851047850E-04,
                        0.157852801640E-06,
                        -0.168353448640E-09,
                        0.111097940130E-12,
                        -0.445154310330E-16,
                        0.989756408210E-20,
                        -0.937913302890E-24,
                    ),
                )
            ),

            "E" : (
                (
                    (-270.000, 0.000),         # degC range over which polynomial valid
                    13,                        # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        0.586655087080E-01,
                        0.454109771240E-04,
                        -0.779980486860E-06,
                        -0.258001608430E-07,
                        -0.594525830570E-09,
                        -0.932140586670E-11,
                        -0.102876055340E-12,
                        -0.803701236210E-15,
                        -0.439794973910E-17,
                        -0.164147763550E-19,
                        -0.396736195160E-22,
                        -0.558273287210E-25,
                        -0.346578420130E-28,
                    ),
                ),
                (
                    (0.000,   1000.000),       # degC range over which polynomial valid
                    10,                        # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        0.586655087100E-01,
                        0.450322755820E-04,
                        0.289084072120E-07,
                        -0.330568966520E-09,
                        0.650244032700E-12,
                        -0.191974955040E-15,
                        -0.125366004970E-17,
                        0.214892175690E-20,
                        -0.143880417820E-23,
                        0.359608994810E-27,
                    ),
                ),
            ),

            "J" : (
                (
                    (-210.000, 760.000),       # degC range over which polynomial valid
                    8,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        0.503811878150E-01,
                        0.304758369300E-04,
                        -0.856810657200E-07,
                        0.132281952950E-09,
                        -0.170529583370E-12,
                        0.209480906970E-15,
                        -0.125383953360E-18,
                        0.156317256970E-22,
                    ),
                ),
                (
                    (760.000,   1200.000),     # degC range over which polynomial valid
                    5,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.296456256810E+03,
                        -0.149761277860E+01,
                        0.317871039240E-02,
                        -0.318476867010E-05,
                        0.157208190040E-08,
                        -0.306913690560E-12,
                    ),
                ),
            ),

            "K" : (
                (
                    (-270.000, 0.000),         # degC range over which polynomial valid
                    10,                        # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        0.394501280250E-01,
                        0.236223735980E-04,
                        -0.328589067840E-06,
                        -0.499048287770E-08,
                        -0.675090591730E-10,
                        -0.574103274280E-12,
                        -0.310888728940E-14,
                        -0.104516093650E-16,
                        -0.198892668780E-19,
                        -0.163226974860E-22,
                    ),
                ),
                (
                    (0.000, 1372.000),         # degC range over which polynomial valid
                    9,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        -0.176004136860E-01,
                        0.389212049750E-01,
                        0.185587700320E-04,
                        -0.994575928740E-07,
                        0.318409457190E-09,
                        -0.560728448890E-12,
                        0.560750590590E-15,
                        -0.320207200030E-18,
                        0.971511471520E-22,
                        -0.121047212750E-25,
                    ),
                ),
            ),

            "N" : (
                (
                    (-270.000, 0.000),         # degC range over which polynomial valid
                    8,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        0.261591059620E-01,
                        0.109574842280E-04,
                        -0.938411115540E-07,
                        -0.464120397590E-10,
                        -0.263033577160E-11,
                        -0.226534380030E-13,
                        -0.760893007910E-16,
                        -0.934196678350E-19,
                    ),
                ),
                (
                    (0.000, 1300.000),         # degC range over which polynomial valid
                    10,                        # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        0.259293946010E-01,
                        0.157101418800E-04,
                        0.438256272370E-07,
                        -0.252611697940E-09,
                        0.643118193390E-12,
                        -0.100634715190E-14,
                        0.997453389920E-18,
                        -0.608632456070E-21,
                        0.208492293390E-24,
                        -0.306821961510E-28,
                    ),
                ),
            ),

            "R" : (
                (
                    (-50.000, 1064.180),       # degC range over which polynomial valid
                    9,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        0.528961729765E-02,
                        0.139166589782E-04,
                        -0.238855693017E-07,
                        0.356916001063E-10,
                        -0.462347666298E-13,
                        0.500777441034E-16,
                        -0.373105886191E-19,
                        0.157716482367E-22,
                        -0.281038625251E-26,
                    ),
                ),
                (
                    (1064.180, 1664.500),      # degC range over which polynomial valid
                    5,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.295157925316E+01,
                        -0.252061251332E-02,
                        0.159564501865E-04,
                        -0.764085947576E-08,
                        0.205305291024E-11,
                        -0.293359668173E-15,
                    ),
                ),
                (
                    (1664.500, 1768.100),      # degC range over which polynomial valid
                    4,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.152232118209E+03,
                        -0.268819888545E+00,
                        0.171280280471E-03,
                        -0.345895706453E-07,
                        -0.934633971046E-14,
                    ),
                ),
            ),

            "S" : (
                (
                    (-50.000, 1064.180),       # degC range over which polynomial valid
                    8,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        0.540313308631E-02,
                        0.125934289740E-04,
                        -0.232477968689E-07,
                        0.322028823036E-10,
                        -0.331465196389E-13,
                        0.255744251786E-16,
                        -0.125068871393E-19,
                        0.271443176145E-23,
                    ),
                ),
                (
                    (1064.180, 1664.500),      # degC range over which polynomial valid
                    4,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.132900444085E+01,
                        0.334509311344E-02,
                        0.654805192818E-05,
                        -0.164856259209E-08,
                        0.129989605174E-13,
                    ),
                ),
                (
                    (1664.500, 1768.100),      # degC range over which polynomial valid
                    4,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.146628232636E+03,
                        -0.258430516752E+00,
                        0.163693574641E-03,
                        -0.330439046987E-07,
                        -0.943223690612E-14,
                    )  ,
                ),
            ),

            "T" : (
                (
                    (-270.000, 0.000),         # degC range over which polynomial valid
                    14,                        # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        0.387481063640E-01,
                        0.441944343470E-04,
                        0.118443231050E-06,
                        0.200329735540E-07,
                        0.901380195590E-09,
                        0.226511565930E-10,
                        0.360711542050E-12,
                        0.384939398830E-14,
                        0.282135219250E-16,
                        0.142515947790E-18,
                        0.487686622860E-21,
                        0.107955392700E-23,
                        0.139450270620E-26,
                        0.797951539270E-30,
                    ),
                ),
                (
                    (0.000, 400.000),          # degC range over which polynomial valid
                    8,                         # Polynomial degree
                    (                          # Polynomial coefficients
                        0.000000000000E+00,
                        0.387481063640E-01,
                        0.332922278800E-04,
                        0.206182434040E-06,
                        -0.218822568460E-08,
                        0.109968809280E-10,
                        -0.308157587720E-13,
                        0.454791352900E-16,
                        -0.275129016730E-19,
                    ),
                ),
            ),
        }
        # In the following, E is EMF in mV and t is temperature in degC.  These
        # coefficients came from the NIST website at
        # http://srdata.nist.gov/its90/main/its90_main_page.html (click on the
        # "Download tables" link).
        nist_tc_inverse = {
            # Polynomials for the inverse function t(E)

            "B" : (
                (
                    (0.291, 2.431),            # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        9.8423321E+01,
                        6.9971500E+02,
                        -8.4765304E+02,
                        1.0052644E+03,
                        -8.3345952E+02,
                        4.5508542E+02,
                        -1.5523037E+02,
                        2.9886750E+01,
                        -2.4742860E+00,
                    ),
                ),
                (
                    (2.431, 13.820),           # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        2.1315071E+02,
                        2.8510504E+02,
                        -5.2742887E+01,
                        9.9160804E+00,
                        -1.2965303E+00,
                        1.1195870E-01,
                        -6.0625199E-03,
                        1.8661696E-04,
                        -2.4878585E-06,
                    ),
                ),
            ),

            "E" : (
                (
                    (-8.825, 0),               # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.0000000E+00,
                        1.6977288E+01,
                        -4.3514970E-01,
                        -1.5859697E-01,
                        -9.2502871E-02,
                        -2.6084314E-02,
                        -4.1360199E-03,
                        -3.4034030E-04,
                        -1.1564890E-05,
                    ),
                ),
                (
                    (0, 76.373),               # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.0000000E+00,
                        1.7057035E+01,
                        -2.3301759E-01,
                        6.5435585E-03,
                        -7.3562749E-05,
                        -1.7896001E-06,
                        8.4036165E-08,
                        -1.3735879E-09,
                        1.0629823E-11,
                        -3.2447087E-14,
                    ),
                ),
            ),

            "J" : (
                (
                    (-8.095, 0),               # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.0000000E+00,
                        1.9528268E+01,
                        -1.2286185E+00,
                        -1.0752178E+00,
                        -5.9086933E-01,
                        -1.7256713E-01,
                        -2.8131513E-02,
                        -2.3963370E-03,
                        -8.3823321E-05,
                    ),
                ),
                (
                    (0, 42.919),               # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.000000E+00,
                        1.978425E+01,
                        -2.001204E-01,
                        1.036969E-02,
                        -2.549687E-04,
                        3.585153E-06,
                        -5.344285E-08,
                        5.099890E-10,
                    ),
                ),
                (
                    (42.919, 69.553),          # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        -3.11358187E+03,
                        3.00543684E+02,
                        -9.94773230E+00,
                        1.70276630E-01,
                        -1.43033468E-03,
                        4.73886084E-06,
                    ),
                ),
            ),

            "K" : (
                (
                    (-5.891, 0),               # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.0000000E+00,
                        2.5173462E+01,
                        -1.1662878E+00,
                        -1.0833638E+00,
                        -8.9773540E-01,
                        -3.7342377E-01,
                        -8.6632643E-02,
                        -1.0450598E-02,
                        -5.1920577E-04,
                    ),
                ),
                (
                    (0, 20.644),               # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.000000E+00,
                        2.508355E+01,
                        7.860106E-02,
                        -2.503131E-01,
                        8.315270E-02,
                        -1.228034E-02,
                        9.804036E-04,
                        -4.413030E-05,
                        1.057734E-06,
                        -1.052755E-08,
                    ),
                ),
                (
                    (20.644, 54.886),          # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        -1.318058E+02,
                        4.830222E+01,
                        -1.646031E+00,
                        5.464731E-02,
                        -9.650715E-04,
                        8.802193E-06,
                        -3.110810E-08,
                    ),
                ),
            ),

            "N" : (
                (
                    (-3.990, 0),               # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.0000000E+00,
                        3.8436847E+01,
                        1.1010485E+00,
                        5.2229312E+00,
                        7.2060525E+00,
                        5.8488586E+00,
                        2.7754916E+00,
                        7.7075166E-01,
                        1.1582665E-01,
                        7.3138868E-03,
                    ),
                ),
                (
                    (0, 20.613),               # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.00000E+00,
                        3.86896E+01,
                        -1.08267E+00,
                        4.70205E-02,
                        -2.12169E-06,
                        -1.17272E-04,
                        5.39280E-06,
                        -7.98156E-08,
                    ),
                ),
                (
                    (20.613, 47.513),          # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        1.972485E+01,
                        3.300943E+01,
                        -3.915159E-01,
                        9.855391E-03,
                        -1.274371E-04,
                        7.767022E-07,
                    ),
                ),
            ),

            "R" : (
                (
                    (-0.226, 1.923),           # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.0000000E+00,
                        1.8891380E+02,
                        -9.3835290E+01,
                        1.3068619E+02,
                        -2.2703580E+02,
                        3.5145659E+02,
                        -3.8953900E+02,
                        2.8239471E+02,
                        -1.2607281E+02,
                        3.1353611E+01,
                        -3.3187769E+00,
                    ),
                ),
                (
                    (1.923, 13.228),           # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        1.334584505E+01,
                        1.472644573E+02,
                        -1.844024844E+01,
                        4.031129726E+00,
                        -6.249428360E-01,
                        6.468412046E-02,
                        -4.458750426E-03,
                        1.994710149E-04,
                        -5.313401790E-06,
                        6.481976217E-08,
                    ),
                ),
                (
                    (11.361, 19.739),          # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        -8.199599416E+01,
                        1.553962042E+02,
                        -8.342197663E+00,
                        4.279433549E-01,
                        -1.191577910E-02,
                        1.492290091E-04,
                    ),
                ),
                (
                    (19.739, 21.103),          # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        3.406177836E+04,
                        -7.023729171E+03,
                        5.582903813E+02,
                        -1.952394635E+01,
                        2.560740231E-01,
                    ),
                ),
            ),

            "S" : (
                (
                    (-0.235, 1.874),           # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.00000000E+00,
                        1.84949460E+02,
                        -8.00504062E+01,
                        1.02237430E+02,
                        -1.52248592E+02,
                        1.88821343E+02,
                        -1.59085941E+02,
                        8.23027880E+01,
                        -2.34181944E+01,
                        2.79786260E+00,
                    ),
                ),
                (
                    (1.874, 11.950),           # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        1.291507177E+01,
                        1.466298863E+02,
                        -1.534713402E+01,
                        3.145945973E+00,
                        -4.163257839E-01,
                        3.187963771E-02,
                        -1.291637500E-03,
                        2.183475087E-05,
                        -1.447379511E-07,
                        8.211272125E-09,
                    ),
                ),
                (
                    (10.332, 17.536),          # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        -8.087801117E+01,
                        1.621573104E+02,
                        -8.536869453E+00,
                        4.719686976E-01,
                        -1.441693666E-02,
                        2.081618890E-04,
                    ),
                ),
                (
                    (17.536, 18.693),          # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        5.333875126E+04,
                        -1.235892298E+04,
                        1.092657613E+03,
                        -4.265693686E+01,
                        6.247205420E-01,
                    ),
                ),
            ),

            "T" : (
                (
                    (-5.603, 0),               # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.0000000E+00,
                        2.5949192E+01,
                        -2.1316967E-01,
                        7.9018692E-01,
                        4.2527777E-01,
                        1.3304473E-01,
                        2.0241446E-02,
                        1.2668171E-03,
                    ),
                ),
                (
                    (0, 20.872),               # mV range over which polynomial valid
                    (                          # Polynomial coefficients
                        0.000000E+00,
                        2.592800E+01,
                        -7.602961E-01,
                        4.637791E-02,
                        -2.165394E-03,
                        6.048144E-05,
                        -7.293422E-07,
                    ),
                ),
            ),
        }
if 1:  # Classes
    class TC:
        '''Implements the polynomials to relate EMF to temperature for various thermocouples per the
        NIST ITS-90 thermocouple tables.  See http://srdata.nist.gov/its90/main.
     
        Usage:  instantiate a TC object.  The constructor takes an optional argument to specify the
        thermocouple type; use one of the letters B, E, J, K, N, R, S, or T.
                                                          Range, °C
            B   Pt-30% Rh versus Pt-6% Rh                0 to 1820
            E   Ni-Cr alloy versus a Cu-Ni alloy        -270 to 1000
                (Chromel)            (Constantan)
            J   Fe versus a Cu-Ni alloy                 -210 to 1200
                            (Constantan)
            K   Ni-Cr alloy versus Ni-Al alloy          -270 to 1372
                (Chromel)          (Alumel)
            N   Ni-Cr-Si alloy versus Ni-Si-Mg alloy    -270 to 1300
                (Nicrosil)            (Nisil)
            R   Pt-13% Rh versus Pt                     -50 to 1768
            S   Pt-10% Rh versus Pt                     -50 to 1768
            T   Cu versus a Cu-Ni alloy                 -270 to 400
                            (Constantan)
        If you do not set the type, use the set_type() method later; this will be required to avoid an
        exception.  You can change the thermocouple type at any time.
     
        To convert a temperature in deg C to an EMF in mV, call E_mV().
     
        To convert an EMF in mV to a temperature in deg C, call T_degC().
        '''
        def __init__(self, tc_type="K"):
            self._allowed_types = set("BEJKNRST")
            self.tc_type = tc_type.upper()
            self._check_type()
        def _check_type(self):
            if self.tc_type not in self._allowed_types:
                msg = "'{}' is not an allowed thermocouple type"
                raise ValueError(msg.format(self.tc_type))
        def _set_type(self, tc_type):
            self._tc_type = tc_type.upper()
            self._check_type()
        def _get_type(self):
            return self._tc_type
        type = property(_get_type, _set_type, None, "Set TC type")
        def E_mV(self, t_degC):
            'Given a temperature in degrees C, return the corresponding voltage in mV'
            self._check_type()
            # Get polynomial data
            try:
                data = nist_tc_forward[self.tc_type]
            except KeyError:
                raise RuntimeError("Program bug:  bad TC type for dictionary")
            # Figure out which polynomial to use
            range_ok = False
            for Range, degree, coefficients in data:
                low, high = Range
                if low <= t_degC <= high:
                    range_ok = True
                    break
            if not range_ok:
                msg = "Temperature out of allowed range of %s to %s deg C" % Range
                raise ValueError(msg)
            # Consistency check: degree should be one less than the size of the coefficient array
            if len(coefficients) != degree + 1:
                raise RuntimeError("Program bug:  degree & coeff size wrong")
            E = 0
            if g.dbg:
                print("t =", t_degC, "degC")
                print("  low =", low, "high =", high)
            for i in range(degree + 1):
                e = coefficients[i]*t_degC**i
                E += e
                if g.dbg:
                    print("t^%02d = %+4.2e" % (i, t_degC**i), end="")
                    print("coeff = %+4.2e" % coefficients[i], end="")
                    print("term = %+15.10f" % e)
            if g.dbg:
                print("Sum = %.3f" % E)
            if self.tc_type == "K" and t_degC > 0:
                # Include exponential correction
                a0, a1, a2 = type_K_exponential
                e = a0*exp(a1*(t_degC - a2)**2)
                if g.dbg:
                    print(" "*17, "Correction = %+.4f" % e)
                E += a0*exp(a1*(t_degC - a2)**2)
            return flt(E)
        def T_degC(self, emf_mV):
            'Given a voltage in mV, return the corresponding temperature in degrees C'
            self._check_type()
            try:
                data = nist_tc_inverse[self.tc_type]
            except KeyError:
                raise RuntimeError("Program bug:  bad TC type for dictionary")
            # Figure out which polynomial to use
            range_ok = False
            for Range, coefficients in data:
                low, high = Range
                if low <= emf_mV <= high:
                    range_ok = True
                    break
            if not range_ok:
                msg = "{:.3f} mV voltage out of allowed range".format(emf_mV)
                raise ValueError(msg)
            T = 0
            if g.dbg:
                print("E =", emf_mV, "mV")
                print("  low =", low, "high =", high)
            for i in range(len(coefficients)):
                t = coefficients[i]*emf_mV**i
                T += t
                if g.dbg:
                    print("V^%02d = %+4.2e" % (i, emf_mV**i), end="")
                    print("coeff = %+4.2e" % coefficients[i], end="")
                    print("term = %+15.10f" % t)
            if g.dbg:
                print("Sum = %.3f" % T)
            return flt(T)
if 1:  # Utility functionality
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage():
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] tc_type [deg_scale]
          Print thermocouple tables relating temperature and EMF in mV.
            tc_type:    must be one of the letters B E J K N R S T
            deg_scale:  must be one of the letters C F K R [defaults = C]
        Source
          Tables generated from NIST NIST ITS-90 polynomials.
        Options:
          -k    Print an abbreviated type K table suitable for use with a 0.1 mV voltmeter 0.1 mV
          -t    Run self-tests for the TC object.  You must have the *.tst files constructed from the
                *.tab files (i.e., the tables from the above NIST URL) and constructed by the
                gen_table.py script.
        '''))
        exit(0)
    def ParseCommandLine():
        d["tc_type"] = "K"  # Default thermocouple type letter
        d["deg_scale"] = "C"  # Default temperature scale
        d["-d"] = False     # Abbreviated type K table
        d["-k"] = False     # Abbreviated type K table
        d["-t"] = False     # Perform self-tests
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hkt")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "k":
                d[o] = not d[o]
            elif o == "-h":
                Usage()
            elif o == "-t":
                failed, messages = run(globals())
                exit(1 if failed else 0)
        if d["-k"]:
            Abbreviated()
            exit(0)
        return args
if 1:  # Core functionality
    def TestLibrary():
        def run_E_tests(tc, filename):
            '''The TC object in tc should be set up for the proper type of thermocouple.  The
            filename variable contains a file name that contains the test values, one per line and
            of the form:
                t_degC  voltage_mV
            Find E as a function of t and compare it to the value from the file.
            '''
            tolerance_mV = 0.5/1000
            for line in open(filename).readlines():
                t, Vref = [float(i) for i in line.split()]
                V = tc.E_mV(t)
                if abs(V - Vref) > tolerance_mV:
                    msg = ["Test failure for type %s at %d degC" % (tc.tc_type, t)]
                    msg.append("  V calc = %+8.3f" % V)
                    msg.append("  V ref  = %+8.3f" % Vref)
                    msg.append("  Diff   = %.1f uV" % (abs(V - Vref)*1000))
                    raise RuntimeError('\n'.join(msg))
        def run_t_tests(tc, filename):
            '''The TC object in tc should be set up for the proper type of thermocouple.  The
            filename variable contains a file name that contains the test values, one per line and
            of the form:
                t_degC  voltage_mV
            Find t as a function of E and compare it to the value from the file.
     
            Note we ignore bad voltage exceptions, as the inverse functions are not defined over
            the whole range of voltages given in the tables.
            '''
            tolerance_degC = 0.2
            for line in open(filename).readlines():
                tref, V = [float(i) for i in line.split()]
                try:
                    t = tc.T_degC(V)
                    if abs(t - tref) > tolerance_degC:
                        msg = ["Test failure for type %s at %d degC" %
                            (tc.tc_type, t)]
                        msg.append("  t calc = %+8.3f" % t)
                        msg.append("  t ref  = %+8.3f" % tref)
                        msg.append("  Diff   = %.3f degC" % abs(t - tref))
                        raise RuntimeError('\n'.join(msg))
                except ValueError:
                    pass    # Out of range, but that's OK
        for tc_type in TC()._allowed_types:
            filename = "/d/pylib/thermocouples/type_%s.tst" % (tc_type.lower())
            run_E_tests(TC(tc_type), filename)
            run_t_tests(TC(tc_type), filename)
    def ToDegC(t, d):
        'Convert the temperature t in the temperature scale d["deg_scale"] to degrees C'
        if d["deg_scale"] == "C":
            return t
        elif d["deg_scale"] == "F":
            return 5/9*(t - 32)
        elif d["deg_scale"] == "K":
            return t - 273.15
        elif d["deg_scale"] == "R":
            t -= 459.67
            return 5/9*(t - 32)
        else:
            raise ValueError("Unknown temperature scale")
    def FromDegC(t_degC):
        'Convert the temperature t_degC in degrees C to the temperature scale d["deg_scale"]'
        if d["deg_scale"] == "C":
            return t_degC
        elif d["deg_scale"] == "F":
            return 9/5*t_degC + 32
        elif d["deg_scale"] == "K":
            return t_degC + 273.15
        elif d["deg_scale"] == "R":
            return (9/5*t_degC + 32) + 459.67
        else:
            raise ValueError("Unknown temperature scale")
    def Voltage():
        'Print a table of voltage in mV versus temperature'
        # We'll start the table at 0 °C and go to the following max temperature
        tmax = {"B": 1820, "E": 1000, "J": 1200, "K": 1370, "N": 1300,
                "R": 1760, "S": 1760, "T": 400, }[d["tc_type"]]
        assert(tmax % 10 == 0)
        if 1:   # Print the header
            ty, ds = d['tc_type'], d['deg_scale']
            U.print(f"{U.title}Type {ty} thermocouple:  Temperature in °{ds} vs. voltage in mV")
            U.print(f"    {U.ref}Reference temperature = {FromDegC(0)} °{ds}")
            print(f"{U.row}{'°' + d['deg_scale']:^4s}", end=" ")
            for i in range(10):
                print(f"{U.row}{i:{7 if i else 5}d}", end="")
            U.print()
            # Dashed lines
            print("-"*4, end=" "*2)
            for i in range(10):
                s = "-"*5
                print(f"{s:>6s}", end=" ")
            print()
        if 1:   # Print the table in rows of 10 degree steps
            tc = TC(d["tc_type"])
            # Convert tmax to current temperature units
            tmax, w = int(FromDegC(tmax)), 6
            for t in range(0, tmax, 10):
                print("{:4d}".format(t), end=" "*2)
                for i in range(10):
                    T = t + i
                    degC = ToDegC(T, d)
                    try:
                        if degC > tmax:
                            raise ValueError()
                        mV = tc.E_mV(degC)
                        print(f"{mV:{w}.2f}", end=" ")
                    except ValueError:
                        print(" "*w, end="")
                print()
    def Temperature():
        'Print the temperature for a given EMF in mV'
        # Start the table at 0 mV and go to the following maximum voltage
        vmax = {"B": 13.820, "E": 76.373, "J": 69.553, "K": 54.886, "N": 47.513, "R": 21.101,
                "S": 18.693, "T": 20.872, }[d["tc_type"]]
        tc = TC(d["tc_type"])
        if 1:   # Print the header
            ty, ds = d["tc_type"], d["deg_scale"]
            U.print(f"{U.title}Type {ty} thermocouple:  Voltage in mV vs. temperature in °{ds}")
            U.print(f"    {U.ref}Reference temperature = {FromDegC(0)} °{ds}")
            print(f"{U.row}mV", end=" "*2)
            for i in range(10):
                s = f".{i}"
                print(f"{U.row}{s:>6s}", end=" ")
            U.print()
            # Dashed lines
            print("--", end=" "*2)
            for i in range(10):
                s = "-"*5
                print(f"{s:>6s}", end=" ")
            print()
        if 1:   # Print the table in rows of 1 mV steps
            width = 7
            for v in range(0, int(vmax) + 1):
                print("{:2d}".format(v), end=" ")
                for i in range(10):
                    mV = v + i/10
                    if mV > vmax:
                        print(" "*width, end="")
                    else:
                        try:
                            t = FromDegC(tc.T_degC(mV))
                            #print("{:{}.1f}".format(t, width), end="")
                            print(f"{t:{width}.0f}".format(t, width), end="")
                        except ValueError:
                            print(" "*width, end="")
                print()
    def Abbreviated():
        '''Print an abbreviated T to mV table for type K, suitable for use
        with a voltmeter that resolves to around 10 to 100 uV.  Also print
        the EMFs for the melting points of various metals.
        '''
        print("Abbreviated type K thermocouple tables:")
        # Print a degC table
        tc = TC("K")
        print("degC\tmV\tSlope mV/10 degC")
        for T in range(0, 1301, 50):
            slope = tc.E_mV(T) - tc.E_mV(T - 1)
            print("{:4d}\t{:5.2f}\t{:5.2f}".format(T, tc.E_mV(T), 10*slope))
        # Print a degF table
        print("\ndegF\tmV\tSlope mV/10 degF")
        for T in range(0, 2501, 100):
            if not T:
                continue
            T_C = (T - 32)*5/9
            slope = 5/9*(tc.E_mV(T_C) - tc.E_mV(T_C - 1))
            print("{:4d}\t{:5.2f}\t{:5.2f}".format(T, tc.E_mV(T_C), 10*slope))
        # Metal melting points        
        print("\nMetal melting points (type K EMFs)")
        print("                         degC        mV     Slope mV/10 degC")
        for metal, mp_C in (("Lead",  360),
                            ("Zinc",  420),
                            ("Magnesium", 651),
                            ("Aluminum",  660),
                            ("Brass", 927),
                            ("Silver",951),
                            ("Silicon bronze",980),
                            ("Gold",  1063),
                            ("Copper",1083),
                            ("Cast iron", 1150),
                            ("Nickel",1452),
                            ("Wrought iron",  1482),
                            ("Steel, low carbon", 1500)):
            try:
                mV = tc.E_mV(mp_C)
                slope = (tc.E_mV(mp_C + 10) - mV)
                print("    {:20s} {:4d} {:10.2f} {:10.2f}".format(metal,
                      mp_C, mV, slope))
            except ValueError:
                print("    {:20s} {:4d}".format(metal, mp_C))
        # Aluminum melting point
        print("\nType K table in degC near the melting point of aluminum:")
        print("    mV", end="")
        for i in range(10):
            print("{:6.1f}".format(i/10), end="")
        print()
        for V in range(27, 33):
            print("    {:2d} ".format(V), end=" ")
            for i in range(10):
                mV = V + i/10
                T_C = tc.T_degC(mV)
                print("{:4.0f} ".format(T_C), end=" ")
            print()
        exit(0)
    def K_Linearity():
        'Print out a table of type K linearity from 0 to 200 °C'
        tc = TC("K")
        R = range(0, 201, 10)
        # Perform a linear regression to predict mV from T
        from linreg import LinearRegression
        x, y = [], []
        for t in R:
            x.append(t)
            y.append(tc.E_mV(t))
        m, b, Rsq = LinearRegression(x, y)
        # Regression gives m = 0.0408916, b = -0.0084873, Rsq = 0.999963.
        # Print out results.
        U.print(f"{U.title}Type K linearity from 0 to 200 °C")
        print("  T      = temperature in °C")
        print("  Exact  = NIST polynomial EMF in mV")
        print("  Linear = prediction in mV from simple linear regression")
        print("  %diff  = difference of Linear value from Exact")
        m.N = 6
        print(f"  Regression model:  m = {m}, b = {b}, Rsq = {Rsq}\n")
        print("   T      Exact    Linear   %diff")
        print("  ---     -----    ------   -----")
        for t in R:
            mV = tc.E_mV(t)
            mV_pred = m*t + b
            if mV:
                diffpct = flt(100*(mV_pred - mV)/mV)
                print(f"  {t:3d}    {mV:6.2f}    {mV_pred:6.2f}    {diffpct:4.1f}")
            else:
                print(f"  {t:3d}    {mV:6.2f}    {mV_pred:6.2f}    {'--':>4s}")
        print(dedent(f'''
 
        Conclusion:  for the approximate use of a type K thermocouple and DMM using
        the DMM's jacks as the reference junction temperature, the correction for the
        reference junction temperature can be made by subtracting the Exact column
        from the measured voltage, as there's not enough nonlineary to matter within
        percent or two.  This is particularly true for a DMM that resolves to 0.1 mV.
 
        '''.rstrip()))

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine()
    # Process the command line arguments
    tc_type = args[0].upper() 
    if len(tc_type) != 1 or tc_type not in "BEJKNRST":
        Error(f"{tc_type!r} is an unrecognized thermocouple type")
    deg_scale = "C"     # Default temperature units
    if len(args) == 2:
        deg_scale = args[1].upper() 
        if len(tc_type) != 1 or tc_type not in "CFKR":
            Error(f"{deg_scale!r} is an unrecognized temperature unit")
    if len(args) == 2:
        if not len(args[1]) == 1 and args[1].upper() not in "CFKR":
            _Error("'{}' is an unrecognized temperature scale".format(args[1]))
        deg_scale = args[1].upper()
    d["tc_type"], d["deg_scale"] = tc_type, deg_scale
    Temperature()
    print()
    Voltage()
