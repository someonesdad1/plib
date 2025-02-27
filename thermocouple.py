"""
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
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2009 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Print thermocouple tables
    ##∞what∞#
    ##∞test∞# #∞test∞#
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
    class G:  # Storage for global variables as attributes
        pass

    g = G()
    g.dbg = False
    ii = isinstance
    # Thermocouple table ranges
    g.table_ranges = {
        # [(temp_low_C, temp_high_C), (V_low_mV, V_high_mV)]
        "B": ((0, 1820), (-0.003, 13.820)),
        "E": ((-270, 1000), (-9.835, 76.373)),
        "J": ((-210, 1200), (-8.095, 69.553)),
        "K": ((-270, 1372), (-6.095, 54.886)),
        "N": ((-270, 1300), (-4.345, 47.513)),
        "R": ((-50, 1768), (-0.226, 21.101)),
        "S": ((-50, 1768), (-0.236, 18.693)),
        "T": ((-270, 400), (-6.258, 20.872)),
    }
    # Colors
    U.title = U("ornl")
    U.ref = U("magl")
    U.row = U("denl")
if 1:  # NIST coefficients for thermocouple polynomials
    # The following are the exponential coefficients for the type K
    # thermocouple.
    type_K_exponential = (
        0.1185976e00,
        -0.1183432e-03,
        0.1269686e03,
    )
    # In the following, E is EMF in mV and t is temperature in °C.  These coefficients came
    # from https://srdata.nist.gov/its90/main/.  Click on the "Download tables" link, then
    # click on the "Coefficients of All Thermocouple Types", which is
    # https://srdata.nist.gov/its90/download/allcoeff.tab for the text file of all the
    # coefficients.
    nist_tc_forward = {
        # Polynomials for E(t)
        "B": (
            (
                (0.000, 630.615),  # degC range over which polynomial valid
                6,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    -0.246508183460e-03,
                    0.590404211710e-05,
                    -0.132579316360e-08,
                    0.156682919010e-11,
                    -0.169445292400e-14,
                    0.629903470940e-18,
                ),
            ),
            (
                (630.615, 1820.000),  # degC range over which polynomial valid
                8,  # Polynomial degree
                (  # Polynomial coefficients
                    -0.389381686210e01,
                    0.285717474700e-01,
                    -0.848851047850e-04,
                    0.157852801640e-06,
                    -0.168353448640e-09,
                    0.111097940130e-12,
                    -0.445154310330e-16,
                    0.989756408210e-20,
                    -0.937913302890e-24,
                ),
            ),
        ),
        "E": (
            (
                (-270.000, 0.000),  # degC range over which polynomial valid
                13,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    0.586655087080e-01,
                    0.454109771240e-04,
                    -0.779980486860e-06,
                    -0.258001608430e-07,
                    -0.594525830570e-09,
                    -0.932140586670e-11,
                    -0.102876055340e-12,
                    -0.803701236210e-15,
                    -0.439794973910e-17,
                    -0.164147763550e-19,
                    -0.396736195160e-22,
                    -0.558273287210e-25,
                    -0.346578420130e-28,
                ),
            ),
            (
                (0.000, 1000.000),  # degC range over which polynomial valid
                10,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    0.586655087100e-01,
                    0.450322755820e-04,
                    0.289084072120e-07,
                    -0.330568966520e-09,
                    0.650244032700e-12,
                    -0.191974955040e-15,
                    -0.125366004970e-17,
                    0.214892175690e-20,
                    -0.143880417820e-23,
                    0.359608994810e-27,
                ),
            ),
        ),
        "J": (
            (
                (-210.000, 760.000),  # degC range over which polynomial valid
                8,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    0.503811878150e-01,
                    0.304758369300e-04,
                    -0.856810657200e-07,
                    0.132281952950e-09,
                    -0.170529583370e-12,
                    0.209480906970e-15,
                    -0.125383953360e-18,
                    0.156317256970e-22,
                ),
            ),
            (
                (760.000, 1200.000),  # degC range over which polynomial valid
                5,  # Polynomial degree
                (  # Polynomial coefficients
                    0.296456256810e03,
                    -0.149761277860e01,
                    0.317871039240e-02,
                    -0.318476867010e-05,
                    0.157208190040e-08,
                    -0.306913690560e-12,
                ),
            ),
        ),
        "K": (
            (
                (-270.000, 0.000),  # degC range over which polynomial valid
                10,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    0.394501280250e-01,
                    0.236223735980e-04,
                    -0.328589067840e-06,
                    -0.499048287770e-08,
                    -0.675090591730e-10,
                    -0.574103274280e-12,
                    -0.310888728940e-14,
                    -0.104516093650e-16,
                    -0.198892668780e-19,
                    -0.163226974860e-22,
                ),
            ),
            (
                (0.000, 1372.000),  # degC range over which polynomial valid
                9,  # Polynomial degree
                (  # Polynomial coefficients
                    -0.176004136860e-01,
                    0.389212049750e-01,
                    0.185587700320e-04,
                    -0.994575928740e-07,
                    0.318409457190e-09,
                    -0.560728448890e-12,
                    0.560750590590e-15,
                    -0.320207200030e-18,
                    0.971511471520e-22,
                    -0.121047212750e-25,
                ),
            ),
        ),
        "N": (
            (
                (-270.000, 0.000),  # degC range over which polynomial valid
                8,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    0.261591059620e-01,
                    0.109574842280e-04,
                    -0.938411115540e-07,
                    -0.464120397590e-10,
                    -0.263033577160e-11,
                    -0.226534380030e-13,
                    -0.760893007910e-16,
                    -0.934196678350e-19,
                ),
            ),
            (
                (0.000, 1300.000),  # degC range over which polynomial valid
                10,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    0.259293946010e-01,
                    0.157101418800e-04,
                    0.438256272370e-07,
                    -0.252611697940e-09,
                    0.643118193390e-12,
                    -0.100634715190e-14,
                    0.997453389920e-18,
                    -0.608632456070e-21,
                    0.208492293390e-24,
                    -0.306821961510e-28,
                ),
            ),
        ),
        "R": (
            (
                (-50.000, 1064.180),  # degC range over which polynomial valid
                9,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    0.528961729765e-02,
                    0.139166589782e-04,
                    -0.238855693017e-07,
                    0.356916001063e-10,
                    -0.462347666298e-13,
                    0.500777441034e-16,
                    -0.373105886191e-19,
                    0.157716482367e-22,
                    -0.281038625251e-26,
                ),
            ),
            (
                (1064.180, 1664.500),  # degC range over which polynomial valid
                5,  # Polynomial degree
                (  # Polynomial coefficients
                    0.295157925316e01,
                    -0.252061251332e-02,
                    0.159564501865e-04,
                    -0.764085947576e-08,
                    0.205305291024e-11,
                    -0.293359668173e-15,
                ),
            ),
            (
                (1664.500, 1768.100),  # degC range over which polynomial valid
                4,  # Polynomial degree
                (  # Polynomial coefficients
                    0.152232118209e03,
                    -0.268819888545e00,
                    0.171280280471e-03,
                    -0.345895706453e-07,
                    -0.934633971046e-14,
                ),
            ),
        ),
        "S": (
            (
                (-50.000, 1064.180),  # degC range over which polynomial valid
                8,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    0.540313308631e-02,
                    0.125934289740e-04,
                    -0.232477968689e-07,
                    0.322028823036e-10,
                    -0.331465196389e-13,
                    0.255744251786e-16,
                    -0.125068871393e-19,
                    0.271443176145e-23,
                ),
            ),
            (
                (1064.180, 1664.500),  # degC range over which polynomial valid
                4,  # Polynomial degree
                (  # Polynomial coefficients
                    0.132900444085e01,
                    0.334509311344e-02,
                    0.654805192818e-05,
                    -0.164856259209e-08,
                    0.129989605174e-13,
                ),
            ),
            (
                (1664.500, 1768.100),  # degC range over which polynomial valid
                4,  # Polynomial degree
                (  # Polynomial coefficients
                    0.146628232636e03,
                    -0.258430516752e00,
                    0.163693574641e-03,
                    -0.330439046987e-07,
                    -0.943223690612e-14,
                ),
            ),
        ),
        "T": (
            (
                (-270.000, 0.000),  # degC range over which polynomial valid
                14,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    0.387481063640e-01,
                    0.441944343470e-04,
                    0.118443231050e-06,
                    0.200329735540e-07,
                    0.901380195590e-09,
                    0.226511565930e-10,
                    0.360711542050e-12,
                    0.384939398830e-14,
                    0.282135219250e-16,
                    0.142515947790e-18,
                    0.487686622860e-21,
                    0.107955392700e-23,
                    0.139450270620e-26,
                    0.797951539270e-30,
                ),
            ),
            (
                (0.000, 400.000),  # degC range over which polynomial valid
                8,  # Polynomial degree
                (  # Polynomial coefficients
                    0.000000000000e00,
                    0.387481063640e-01,
                    0.332922278800e-04,
                    0.206182434040e-06,
                    -0.218822568460e-08,
                    0.109968809280e-10,
                    -0.308157587720e-13,
                    0.454791352900e-16,
                    -0.275129016730e-19,
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
        "B": (
            (
                (0.291, 2.431),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    9.8423321e01,
                    6.9971500e02,
                    -8.4765304e02,
                    1.0052644e03,
                    -8.3345952e02,
                    4.5508542e02,
                    -1.5523037e02,
                    2.9886750e01,
                    -2.4742860e00,
                ),
            ),
            (
                (2.431, 13.820),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    2.1315071e02,
                    2.8510504e02,
                    -5.2742887e01,
                    9.9160804e00,
                    -1.2965303e00,
                    1.1195870e-01,
                    -6.0625199e-03,
                    1.8661696e-04,
                    -2.4878585e-06,
                ),
            ),
        ),
        "E": (
            (
                (-8.825, 0),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.0000000e00,
                    1.6977288e01,
                    -4.3514970e-01,
                    -1.5859697e-01,
                    -9.2502871e-02,
                    -2.6084314e-02,
                    -4.1360199e-03,
                    -3.4034030e-04,
                    -1.1564890e-05,
                ),
            ),
            (
                (0, 76.373),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.0000000e00,
                    1.7057035e01,
                    -2.3301759e-01,
                    6.5435585e-03,
                    -7.3562749e-05,
                    -1.7896001e-06,
                    8.4036165e-08,
                    -1.3735879e-09,
                    1.0629823e-11,
                    -3.2447087e-14,
                ),
            ),
        ),
        "J": (
            (
                (-8.095, 0),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.0000000e00,
                    1.9528268e01,
                    -1.2286185e00,
                    -1.0752178e00,
                    -5.9086933e-01,
                    -1.7256713e-01,
                    -2.8131513e-02,
                    -2.3963370e-03,
                    -8.3823321e-05,
                ),
            ),
            (
                (0, 42.919),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.000000e00,
                    1.978425e01,
                    -2.001204e-01,
                    1.036969e-02,
                    -2.549687e-04,
                    3.585153e-06,
                    -5.344285e-08,
                    5.099890e-10,
                ),
            ),
            (
                (42.919, 69.553),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    -3.11358187e03,
                    3.00543684e02,
                    -9.94773230e00,
                    1.70276630e-01,
                    -1.43033468e-03,
                    4.73886084e-06,
                ),
            ),
        ),
        "K": (
            (
                (-5.891, 0),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.0000000e00,
                    2.5173462e01,
                    -1.1662878e00,
                    -1.0833638e00,
                    -8.9773540e-01,
                    -3.7342377e-01,
                    -8.6632643e-02,
                    -1.0450598e-02,
                    -5.1920577e-04,
                ),
            ),
            (
                (0, 20.644),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.000000e00,
                    2.508355e01,
                    7.860106e-02,
                    -2.503131e-01,
                    8.315270e-02,
                    -1.228034e-02,
                    9.804036e-04,
                    -4.413030e-05,
                    1.057734e-06,
                    -1.052755e-08,
                ),
            ),
            (
                (20.644, 54.886),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    -1.318058e02,
                    4.830222e01,
                    -1.646031e00,
                    5.464731e-02,
                    -9.650715e-04,
                    8.802193e-06,
                    -3.110810e-08,
                ),
            ),
        ),
        "N": (
            (
                (-3.990, 0),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.0000000e00,
                    3.8436847e01,
                    1.1010485e00,
                    5.2229312e00,
                    7.2060525e00,
                    5.8488586e00,
                    2.7754916e00,
                    7.7075166e-01,
                    1.1582665e-01,
                    7.3138868e-03,
                ),
            ),
            (
                (0, 20.613),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.00000e00,
                    3.86896e01,
                    -1.08267e00,
                    4.70205e-02,
                    -2.12169e-06,
                    -1.17272e-04,
                    5.39280e-06,
                    -7.98156e-08,
                ),
            ),
            (
                (20.613, 47.513),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    1.972485e01,
                    3.300943e01,
                    -3.915159e-01,
                    9.855391e-03,
                    -1.274371e-04,
                    7.767022e-07,
                ),
            ),
        ),
        "R": (
            (
                (-0.226, 1.923),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.0000000e00,
                    1.8891380e02,
                    -9.3835290e01,
                    1.3068619e02,
                    -2.2703580e02,
                    3.5145659e02,
                    -3.8953900e02,
                    2.8239471e02,
                    -1.2607281e02,
                    3.1353611e01,
                    -3.3187769e00,
                ),
            ),
            (
                (1.923, 13.228),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    1.334584505e01,
                    1.472644573e02,
                    -1.844024844e01,
                    4.031129726e00,
                    -6.249428360e-01,
                    6.468412046e-02,
                    -4.458750426e-03,
                    1.994710149e-04,
                    -5.313401790e-06,
                    6.481976217e-08,
                ),
            ),
            (
                (11.361, 19.739),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    -8.199599416e01,
                    1.553962042e02,
                    -8.342197663e00,
                    4.279433549e-01,
                    -1.191577910e-02,
                    1.492290091e-04,
                ),
            ),
            (
                (19.739, 21.103),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    3.406177836e04,
                    -7.023729171e03,
                    5.582903813e02,
                    -1.952394635e01,
                    2.560740231e-01,
                ),
            ),
        ),
        "S": (
            (
                (-0.235, 1.874),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.00000000e00,
                    1.84949460e02,
                    -8.00504062e01,
                    1.02237430e02,
                    -1.52248592e02,
                    1.88821343e02,
                    -1.59085941e02,
                    8.23027880e01,
                    -2.34181944e01,
                    2.79786260e00,
                ),
            ),
            (
                (1.874, 11.950),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    1.291507177e01,
                    1.466298863e02,
                    -1.534713402e01,
                    3.145945973e00,
                    -4.163257839e-01,
                    3.187963771e-02,
                    -1.291637500e-03,
                    2.183475087e-05,
                    -1.447379511e-07,
                    8.211272125e-09,
                ),
            ),
            (
                (10.332, 17.536),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    -8.087801117e01,
                    1.621573104e02,
                    -8.536869453e00,
                    4.719686976e-01,
                    -1.441693666e-02,
                    2.081618890e-04,
                ),
            ),
            (
                (17.536, 18.693),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    5.333875126e04,
                    -1.235892298e04,
                    1.092657613e03,
                    -4.265693686e01,
                    6.247205420e-01,
                ),
            ),
        ),
        "T": (
            (
                (-5.603, 0),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.0000000e00,
                    2.5949192e01,
                    -2.1316967e-01,
                    7.9018692e-01,
                    4.2527777e-01,
                    1.3304473e-01,
                    2.0241446e-02,
                    1.2668171e-03,
                ),
            ),
            (
                (0, 20.872),  # mV range over which polynomial valid
                (  # Polynomial coefficients
                    0.000000e00,
                    2.592800e01,
                    -7.602961e-01,
                    4.637791e-02,
                    -2.165394e-03,
                    6.048144e-05,
                    -7.293422e-07,
                ),
            ),
        ),
    }
if 1:  # Classes

    class TC:
        """Implements the polynomials to relate EMF to temperature for various thermocouples per the
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
        """

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
            "Given a temperature in degrees C, return the corresponding voltage in mV"
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
                e = coefficients[i] * t_degC**i
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
                e = a0 * exp(a1 * (t_degC - a2) ** 2)
                if g.dbg:
                    print(" " * 17, "Correction = %+.4f" % e)
                E += a0 * exp(a1 * (t_degC - a2) ** 2)
            return flt(E)

        def T_degC(self, emf_mV):
            "Given a voltage in mV, return the corresponding temperature in degrees C"
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
                t = coefficients[i] * emf_mV**i
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
        print(
            dedent(f"""
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
        """)
        )
        exit(0)

    def ParseCommandLine():
        d["tc_type"] = "K"  # Default thermocouple type letter
        d["deg_scale"] = "C"  # Default temperature scale
        d["-d"] = False  # Abbreviated type K table
        d["-k"] = False  # Abbreviated type K table
        d["-t"] = False  # Perform self-tests
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
            """The TC object in tc should be set up for the proper type of thermocouple.  The
            filename variable contains a file name that contains the test values, one per line and
            of the form:
                t_degC  voltage_mV
            Find E as a function of t and compare it to the value from the file.
            """
            tolerance_mV = 0.5 / 1000
            for line in open(filename).readlines():
                t, Vref = [float(i) for i in line.split()]
                V = tc.E_mV(t)
                if abs(V - Vref) > tolerance_mV:
                    msg = ["Test failure for type %s at %d degC" % (tc.tc_type, t)]
                    msg.append("  V calc = %+8.3f" % V)
                    msg.append("  V ref  = %+8.3f" % Vref)
                    msg.append("  Diff   = %.1f uV" % (abs(V - Vref) * 1000))
                    raise RuntimeError("\n".join(msg))

        def run_t_tests(tc, filename):
            """The TC object in tc should be set up for the proper type of thermocouple.  The
            filename variable contains a file name that contains the test values, one per line and
            of the form:
                t_degC  voltage_mV
            Find t as a function of E and compare it to the value from the file.

            Note we ignore bad voltage exceptions, as the inverse functions are not defined over
            the whole range of voltages given in the tables.
            """
            tolerance_degC = 0.2
            for line in open(filename).readlines():
                tref, V = [float(i) for i in line.split()]
                try:
                    t = tc.T_degC(V)
                    if abs(t - tref) > tolerance_degC:
                        msg = ["Test failure for type %s at %d degC" % (tc.tc_type, t)]
                        msg.append("  t calc = %+8.3f" % t)
                        msg.append("  t ref  = %+8.3f" % tref)
                        msg.append("  Diff   = %.3f degC" % abs(t - tref))
                        raise RuntimeError("\n".join(msg))
                except ValueError:
                    pass  # Out of range, but that's OK

        for tc_type in TC()._allowed_types:
            filename = "/d/pylib/thermocouples/type_%s.tst" % (tc_type.lower())
            run_E_tests(TC(tc_type), filename)
            run_t_tests(TC(tc_type), filename)

    def ToDegC(t, d):
        'Convert the temperature t in the temperature scale d["deg_scale"] to degrees C'
        if d["deg_scale"] == "C":
            return t
        elif d["deg_scale"] == "F":
            return 5 / 9 * (t - 32)
        elif d["deg_scale"] == "K":
            return t - 273.15
        elif d["deg_scale"] == "R":
            t -= 459.67
            return 5 / 9 * (t - 32)
        else:
            raise ValueError("Unknown temperature scale")

    def FromDegC(t_degC):
        'Convert the temperature t_degC in degrees C to the temperature scale d["deg_scale"]'
        if d["deg_scale"] == "C":
            return t_degC
        elif d["deg_scale"] == "F":
            return 9 / 5 * t_degC + 32
        elif d["deg_scale"] == "K":
            return t_degC + 273.15
        elif d["deg_scale"] == "R":
            return (9 / 5 * t_degC + 32) + 459.67
        else:
            raise ValueError("Unknown temperature scale")

    def Voltage():
        "Print a table of voltage in mV versus temperature"
        # We'll start the table at 0 °C and go to the following max temperature
        tmax = {
            "B": 1820,
            "E": 1000,
            "J": 1200,
            "K": 1370,
            "N": 1300,
            "R": 1760,
            "S": 1760,
            "T": 400,
        }[d["tc_type"]]
        assert tmax % 10 == 0
        if 1:  # Print the header
            ty, ds = d["tc_type"], d["deg_scale"]
            U.print(
                f"{U.title}Type {ty} thermocouple:  Temperature in °{ds} vs. voltage in mV"
            )
            U.print(f"    {U.ref}Reference temperature = {FromDegC(0)} °{ds}")
            print(f"{U.row}{'°' + d['deg_scale']:^4s}", end=" ")
            for i in range(10):
                print(f"{U.row}{i:{7 if i else 5}d}", end="")
            U.print()
            # Dashed lines
            print("-" * 4, end=" " * 2)
            for i in range(10):
                s = "-" * 5
                print(f"{s:>6s}", end=" ")
            print()
        if 1:  # Print the table in rows of 10 degree steps
            tc = TC(d["tc_type"])
            # Convert tmax to current temperature units
            tmax, w = int(FromDegC(tmax)), 6
            for t in range(0, tmax, 10):
                print("{:4d}".format(t), end=" " * 2)
                for i in range(10):
                    T = t + i
                    degC = ToDegC(T, d)
                    try:
                        if degC > tmax:
                            raise ValueError()
                        mV = tc.E_mV(degC)
                        print(f"{mV:{w}.2f}", end=" ")
                    except ValueError:
                        print(" " * w, end="")
                print()

    def Temperature():
        "Print the temperature for a given EMF in mV"
        # Start the table at 0 mV and go to the following maximum voltage
        vmax = {
            "B": 13.820,
            "E": 76.373,
            "J": 69.553,
            "K": 54.886,
            "N": 47.513,
            "R": 21.101,
            "S": 18.693,
            "T": 20.872,
        }[d["tc_type"]]
        tc = TC(d["tc_type"])
        if 1:  # Print the header
            ty, ds = d["tc_type"], d["deg_scale"]
            U.print(
                f"{U.title}Type {ty} thermocouple:  Voltage in mV vs. temperature in °{ds}"
            )
            U.print(f"    {U.ref}Reference temperature = {FromDegC(0)} °{ds}")
            print(f"{U.row}mV", end=" " * 2)
            for i in range(10):
                s = f".{i}"
                print(f"{U.row}{s:>6s}", end=" ")
            U.print()
            # Dashed lines
            print("--", end=" " * 2)
            for i in range(10):
                s = "-" * 5
                print(f"{s:>6s}", end=" ")
            print()
        if 1:  # Print the table in rows of 1 mV steps
            width = 7
            for v in range(0, int(vmax) + 1):
                print("{:2d}".format(v), end=" ")
                for i in range(10):
                    mV = v + i / 10
                    if mV > vmax:
                        print(" " * width, end="")
                    else:
                        try:
                            t = FromDegC(tc.T_degC(mV))
                            # print("{:{}.1f}".format(t, width), end="")
                            print(f"{t:{width}.0f}".format(t, width), end="")
                        except ValueError:
                            print(" " * width, end="")
                print()

    def Abbreviated():
        """Print an abbreviated T to mV table for type K, suitable for use
        with a voltmeter that resolves to around 10 to 100 uV.  Also print
        the EMFs for the melting points of various metals.
        """
        print("Abbreviated type K thermocouple tables:")
        # Print a degC table
        tc = TC("K")
        print("degC\tmV\tSlope mV/10 degC")
        for T in range(0, 1301, 50):
            slope = tc.E_mV(T) - tc.E_mV(T - 1)
            print("{:4d}\t{:5.2f}\t{:5.2f}".format(T, tc.E_mV(T), 10 * slope))
        # Print a degF table
        print("\ndegF\tmV\tSlope mV/10 degF")
        for T in range(0, 2501, 100):
            if not T:
                continue
            T_C = (T - 32) * 5 / 9
            slope = 5 / 9 * (tc.E_mV(T_C) - tc.E_mV(T_C - 1))
            print("{:4d}\t{:5.2f}\t{:5.2f}".format(T, tc.E_mV(T_C), 10 * slope))
        # Metal melting points
        print("\nMetal melting points (type K EMFs)")
        print("                         degC        mV     Slope mV/10 degC")
        for metal, mp_C in (
            ("Lead", 360),
            ("Zinc", 420),
            ("Magnesium", 651),
            ("Aluminum", 660),
            ("Brass", 927),
            ("Silver", 951),
            ("Silicon bronze", 980),
            ("Gold", 1063),
            ("Copper", 1083),
            ("Cast iron", 1150),
            ("Nickel", 1452),
            ("Wrought iron", 1482),
            ("Steel, low carbon", 1500),
        ):
            try:
                mV = tc.E_mV(mp_C)
                slope = tc.E_mV(mp_C + 10) - mV
                print(
                    "    {:20s} {:4d} {:10.2f} {:10.2f}".format(metal, mp_C, mV, slope)
                )
            except ValueError:
                print("    {:20s} {:4d}".format(metal, mp_C))
        # Aluminum melting point
        print("\nType K table in degC near the melting point of aluminum:")
        print("    mV", end="")
        for i in range(10):
            print("{:6.1f}".format(i / 10), end="")
        print()
        for V in range(27, 33):
            print("    {:2d} ".format(V), end=" ")
            for i in range(10):
                mV = V + i / 10
                T_C = tc.T_degC(mV)
                print("{:4.0f} ".format(T_C), end=" ")
            print()
        exit(0)

    def K_Linearity():
        "Print out a table of type K linearity from 0 to 200 °C"
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
            mV_pred = m * t + b
            if mV:
                diffpct = flt(100 * (mV_pred - mV) / mV)
                print(f"  {t:3d}    {mV:6.2f}    {mV_pred:6.2f}    {diffpct:4.1f}")
            else:
                print(f"  {t:3d}    {mV:6.2f}    {mV_pred:6.2f}    {'--':>4s}")
        print(
            dedent(
                f"""
 
        Conclusion:  for the approximate use of a type K thermocouple and DMM using
        the DMM's jacks as the reference junction temperature, the correction for the
        reference junction temperature can be made by subtracting the Exact column
        from the measured voltage, as there's not enough nonlineary to matter within
        percent or two.  This is particularly true for a DMM that resolves to 0.1 mV.
 
        """.rstrip()
            )
        )


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine()
    # Process the command line arguments
    tc_type = args[0].upper()
    if len(tc_type) != 1 or tc_type not in "BEJKNRST":
        Error(f"{tc_type!r} is an unrecognized thermocouple type")
    deg_scale = "C"  # Default temperature units
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
