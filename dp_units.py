'''
Produce a units definition file to stdout that uses GNU units syntax
'''
# Number:  0: base SI, 1: minimal, 2: common usage
data = '''
# This is a set of units using the GNU units configuration file syntax.
# The primary units are the 7 base SI units and the dollar $.  Note the
# assumption is that mpmath will be used for numerical calculation, so
# mpmathpi is defined as a base unit with the expectation that it will 
# be replaced by its numerical value at runtime.
# Constructed by /plib/dp_units.py.
# Base units
    0   m                    !
    0   kg                   !
    0   s                    !
    0   A                    !
    0   cd                   !
    0   mol                  !
    0   K                    !
    0   $                    !
# Constants (pi to 30 digits, far more than is practical)
    0   mpmathpi             3.14159265358979323846264338328
# Angle
    0   radian               !dimensionless
    0   degree               mpmathpi*radian/180
    1   rad                  radian
    2   radians              radian
    1   rev                  2*mpmathpi*radian
    2   revs                 1*rev
    2   circle               1*rev
    2   circles              circle
    1   deg                  degree
    2   degrees              degree
    2   turn                 1*circle
    2   turns                1*circle
    2   grad                 circle/400
    1   arcmin               degree/60
    1   arcsec               arcmin/60
# Solid angle
    1   sr                   !dimensionless
    2   steradian            sr
    2   steradians           sr
    2   sphere               4*mpmathpi*sr
# Length
    2   meter                m
    2   metre                m
    2   meters               m
    2   metres               m
    1   inch                 0.0254*m
    1   in                   inch
    2   inches               inch
    1   ft                   12*inch
    2   foot                 ft
    2   feet                 ft
    1   mi                   5280*ft
    2   mile                 mi
    2   miles                mi
    1   nmi                  1852*m
    2   nmile                nmi
    2   nauticalmile         nmi
    2   nauticalmiles        nmi
    1   yd                   3*ft
    2   yds                  3*ft
    2   yard                 yd
    2   yards                3*ft
    1   ly                   365.25*24*3600*c*m
    2   lightyear            1*ly
    1   au                   149597870700*m
    2   astronomicalunit     au
    2   earthradius          6.37101e6*m
    2   moonradius           1.73710e6*m
    2   sunradius            6.96342e8*m
    1   micron               1e-6*m
    1   mil                  inch/1000
    2   thou                 mil
    2   Angstrom             1e-10*m
    2   ang                  Angstrom
    2   angstrom             Angstrom
    2   cable                nmi/10
    2   caliber              inch/100
    2   chain                20.11684*m
    2   link                 chain/100
    2   click                1000*m
    2   clicks               click
    2   klick                click
    2   klicks               click
    1   fathom               6*ft
    2   rod                  5.5*yard
    2   furlong              40*rod
    2   furlongs             furlong
    2   hand                 4*inches
    2   hands                hand
    1   league               3*miles
    2   ls                   c*m
    2   lightsecond          ls
    2   pace                 2.5*feet
    2   pc                   3.08567758149e+16*m
    1   parsec               3.08567758149e+16*m
    2   point                inch/72.27
    2   dpenny               0.75*inches
    2   dnickel              0.835*inches
    2   ddime                0.705*inches
    2   dquarter             0.955*inches
    2   dhalf                1.205*inches
# Area
    1   acre                 4046.87260987425*m**2
    1   hectare              1e4*m**2
    2   barn                 1e-28*m**2
    2   are                  100*m**2
    1   letter               8.5*11*inch**2
    2   legal                8.5*14*inch**2
    2   ledger               11*17*inch**2
    2   A4paper              0.21*0.297*m**2
    2   dollarbill           2.61*6.14*inch**2
    2   circmil              mpmathpi*(1e-3*inch)**2/4
    2   mcm                  1000*circmil
# Volume
    0   L                    1e-3*m**3
    1   l                    L
    2   liter                L
    2   liters               L
    2   litre                L
    2   litres               L
    1   gal                  231*inch**3
    2   gallon               gal
    2   gallons              gal
    1   cc                   1e-6*m**3
    2   acrefoot             acre*foot
    1   qt                   gal/4
    2   qts                  qt
    2   quart                qt
    2   quarts               qt
    1   pint                 qt/2
    2   pints                pint
    1   floz                 pint/16
    2   fluidounce           floz
    1   cup                  8*floz
    2   cups                 cup
    2   dixiecup             cup
    2   cuft                 ft**3
    2   cubicfoot            cuft
    2   cubicfeet            cuft
    2   cuin                 inch**3
    2   cubicinch            cuin
    2   cubicinches          cuin
    2   bbl                  42*gal
    2   barrel               bbl
    2   barrels              bbl
    1   bdft                 12*12*1*inch**3
    2   boardfoot            bdft
    2   boardfeet            bdft
    1   bushel               35.2391*L
    2   bushels              bushel
    1   cord                 4*4*8*ft**3
    2   fldram               floz/8
    2   fifth                gal/5
    2   gill                 pint/4
    2   hogshead             63*gal
    2   jigger               1.5*floz
    2   shot                 jigger
    2   magnum               1.5*L
    2   minim                fldram/60
    1   drop                 (L/1000)/20
    2   bloodunit            0.45*L
    2   peck                 bushel/4
    2   popcan               12*floz
    2   beercan              popcan
    2   bigbeercan           16*floz
    2   shippington          40*ft**3
    2   tbl                  cup/16
    2   tablespoon           tbl
    2   tsp                  cup/48
    2   teaspoon             tsp
    2   saltspoon            tbl/12
    2   winebottle           3/4*L
    2   wineglass            4*floz
# Time
    1   sec                  s
    1   min                  60*s
    1   hr                   3600*s
    1   yr                   365.242198781*24*hr
    1   day                  24*hr
    1   mo                   yr/12
    1   wk                   7*day
    2   week                 7*day
    2   second               s
    2   seconds              s
    2   minute               min
    2   minutes              min
    2   hour                 hr
    2   hours                hr
    2   days                 day
    2   weeks                week
    2   year                 yr
    2   years                yr
    1   julianyear           365.25*days
    2   month                mo
    2   months               mo
    1   decade               10*yr
    2   decades              10*yr
    1   century              100*yr
    2   centuries            100*yr
    1   millenium            1000*yr
    2   millenia             1000*yr
    2   fortnight            2*weeks
    2   lustrum              5*yr
    2   jiffy                0.01*s
    2   leapyear             366*day
    1   siderealday          23.934469444*hr
    1   siderealyear         365.256360417*day
    2   lunarmonth           2551442.8*s
    2   mercuryday           58.6462*day
    2   venusday             243.01*day
    2   earthday             1*siderealday
    2   marsday              1.02595675*day
    2   jupiterday           0.41354*day
    2   saturnday            0.4375*day
    2   uranusday            0.65*day
    2   neptuneday           0.768*day
    2   plutoday             6.3867*day
    2   mercuryyear          0.2408467*julianyear
    2   venusyear            0.61519726*julianyear
    2   earthyear            1*siderealyear
    2   marsyear             1.8808476*julianyear
    2   jupiteryear          11.862615*julianyear
    2   saturnyear           29.447498*julianyear
    2   uranusyear           84.016846*julianyear
    2   neptuneyear          164.79132*julianyear
    2   plutoyear            247.92065*julianyear
# Velocity
    0   c                    299792458*m/s
    1   mph                  mi/hr
    1   kph                  1000*m/hr
    1   fps                  ft/s
    1   fpm                  ft/min
    1   sfpm                 ft/min
    1   knot                 1852*m/hr
    2   light                c*m/s
# Frequency
    0   Hz                   1/s
    1   rpm                  1/min
    2   hertz                Hz
    2   rps                  Hz
# Mass
    0   g                    kg/1000
    1   lb                   0.45359237*kg
    2   electron_m           9.109384e-31*kg
    2   gram                 g
    2   grams                g
    2   pound                lb
    2   lbs                  lb
    2   lbm                  lb
    1   amu                  1.660538921e-27*kg
    1   oz                   lb/16
    1   ton                  2000*lb
    1   tonne                1000*kg
    2   gm                   g
    2   gramme               g
    2   grammes              g
    2   pounds               lb
    1   slug                 14.593903*kg
    1   Da                   amu
    2   ounce                oz
    2   ounces               oz
    1   grain                lb/7000
    2   grains               lb/7000
    2   gr                   lb/7000
    2   troypound            5760.*grain
    2   troyounce            troypound/12
    2   egg                  50*g
    2   cuftwater            28.2661*kg
    2   ft3h2o               cuftwater
    1   galwater             3.7855178*kg
    2   galH2O               galwater
    2   galh2o               galwater
    2   gallonwater          galwater
    2   carat                g/5
    2   ct                   carat
    2   dram                 ounce/16
    2   stone                14*lb
    2   mpenny               2.5*g
    2   mnickel              5*g
    2   mdime                2.268*g
    2   mquarter             5.670*g
    2   mhalf                11.340*g
    2   sunmass              1.9891e30*kg
    2   moonmass             7.3483e22*kg
    2   mercurymass          0.33022e24*kg
    2   venusmass            4.8690e24*kg
    2   earthmass            5.9742e24*kg
    2   marsmass             0.64191e24*kg
    2   jupitermass          1898.8e24*kg
    2   saturnmass           568.5e24*kg
    2   uranusmass           86.625e24*kg
    2   neptunemass          102.78e24*kg
    2   plutomass            0.015e24*kg
# Energy
    0   J                    kg*m**2/s**2
    1   btu                  1055.056*J
    1   eV                   1.602176565e-19*J
    1   cal                  4.1868*J
    2   kcal                 1000*cal
    2   Whr                  3600*J
    2   Wh                   Whr
    1   erg                  1e-7*J
    2   CAL                  kcal
    2   Calorie              kcal
    2   calorie              cal
    2   therm                1.054804e8*J
    2   BTU                  btu
    2   ttnt                 4.184e12*J
# Quantity
    2   mole                 mol
    1   molar                mol/L
# Avogadro's number
    0   NA                   6.02214129e23/mol
# Force
    0   N                    kg*m/s**2
    1   lbf                  4.4482216152605*N
    1   gravity              9.80665*m/s**2
    2   kgf                  kg*gravity
    2   gf                   g*gravity
    2   dyne                 1e-5*N
    2   poundf               lbf
    2   kip                  1000*lbf
    2   slugf                slug*gravity
    2   tonf                 ton*gravity
# Pressure
    0   Pa                   N/m**2
    1   psi                  lbf/inch**2
    1   atm                  101325*Pa
    1   bar                  1e5*Pa
    2   psf                  lbf/ft**2
    2   torr                 atm/760
    2   ksi                  kip/inch**2
    2   water                g*gravity/(m/100)**3
    2   fth2o                ft*water
    2   inh2o                inch*water
    2   mh2o                 m*water
    2   mmh2o                m*water/1000
    2   Hg                   13.5951*g*gravity/(m/100)**3
    2   ftHg                 ft*Hg
    2   fthg                 ft*Hg
    2   inHg                 inch*Hg
    2   inhg                 inch*Hg
    2   mHg                  m*Hg
    2   mhg                  m*Hg
    2   mmHg                 m*Hg/1000
    2   mmhg                 m*Hg/1000
# Dynamic viscosity
    2   P                    0.1*Pa*s
    1   poise                0.1*Pa*s
# Kinematic viscosity
    1   stoke                1e-4*m**2/s
    2   stokes               1e-4*m**2/s
# Flow
    2   gph                  gallon/hr
    2   gpm                  gallon/min
    2   gps                  gallon/s
    2   cfh                  ft**3/hr
    2   cfm                  ft**3/min
    2   cfs                  ft**3/s
    2   lpm                  liter/min
    2   lph                  liter/hr
    2   lps                  liter/s
    2   minersinch           0.566*lps
# Power
    0   W                    J/s
    1   hp                   550.*ft*lb*gravity/s
    2   HP                   550.*ft*lb*gravity/s
    2   metrichp             735.49875*W
    2   tonref               ton*144.*btu/(lbm*day)
    2   sccs                 atm*cc/s
    2   sccm                 atm*cc/minute
    2   scfh                 atm*cfh
    2   scfm                 atm*cfm
    2   slpm                 atm*lpm
    2   slph                 atm*lph
# Temperature
    1   degC                 K
    1   degF                 5/9*K
# Current
    2   amp                  A
    2   ampere               A
    2   abamp                10*A
    2   abampere             abamp
    2   biot                 abamp
# Charge
    0   coul                 A/s
    2   electron_q           1.602176634e-19*coul
    2   Ahr                  3600*coul
    2   amphour              3600*coul
    2   coulomb              coul
    2   C                    coul
    2   abcoul               abamp/s
# Voltage
    0   V                    J/coul
    1   volt                 V
    2   abvolt               dyne*(m/100)/(abamp*s)
# Resistance
    0   ohm                  V/A
    2   abohm                1*abvolt/abamp
# Conductivity
    1   S                    A/V
    2   siemens              S
    2   mho                  A/V
    2   abmho                abamp/abvolt
# Magnetic flux
    1   Wb                   J/A
    2   Oe                   1000/(4*mpmathpi)*A/m
    2   oersted              1000/(4*mpmathpi)*A/m
    2   Maxwell              abvolt*s
    2   unitpole             4*mpmathpi*Maxwell
# Magnetic flux density
    1   T                    Wb/m**2
    2   Tesla                T
    2   tesla                T
    2   gauss                T/10000
# Capacitance
    0   F                    coul/V
    2   abfarad              abamp*s/abvolt
# Inductance
    0   H                    m**2*kg/coul**2
    2   abhenry              abvolt*s/abamp
# Luminous intensity/flux
    2   candela              cd
    2   candle               1.02*cd
    1   lm                   cd*sr
    2   lumen                lm
# Illuminance (luminous flux per unit area)
    1   lux                  lm/m**2
    2   footcandle           lm/ft**2
    2   phot                 1e4*lux
# Reciprocal focal length
    1   diopter              1/m
# Cost
    1   dollar               $
    1   cent                 $/100
    2   buck                 $
    2   bucks                $
'''
if __name__ == "__main__":  
    import sys
    from wrap import dedent
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] arg
          Send a GNU units compatible configuration file to stdout.  arg gives type:
            min     Minimal for basic tasks like testing a library
            norm    Basic set of SI units 
            com     Common use including oddball US units
          Describe behavior
        Options:
            -a      Describe
            -d n    Number of significant digits
            -h      Print help
        '''))
        exit(status)
    def ProduceDefinitions(level):
        '''level is a string:
            min    Minimal for basic tasks
            norm   Basic SI
            com    Common with some US customary
        '''
        number = {"min": 0, "norm": 1, "com": 2}[level]
        for i, line in enumerate(data.split("\n")):
            s = line.strip()
            if not s:
                continue
            if line.startswith("#"):
                print(s)
            else:
                try:
                    num, name, definition = s.split()
                    num = int(num)
                    if num > number:
                        continue
                    W = 25
                    w = W - 4 - len(name)
                    out = f"    {name}{' ':{w}s}{definition}"
                    assert " " in out.strip()
                    print(out)
                except Exception as e:
                    print(f"Line {i+1} bad:")
                    print(f"    {line!r}")
                    print(f"    Exception:  {e}")
                    exit(1)
    if len(sys.argv) == 1:
        Usage()
    else:
        level = sys.argv[1].lower().strip()
        if level not in "min norm com".split(): 
            Usage()
        else:
            ProduceDefinitions(level)
