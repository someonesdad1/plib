'''
Print out colored LED properties.  


I need to measure the 3 and 5 mm banggood LED properties and develop an 
empirical model for the for about 0.1 to 20 mA currents, as these are the
practical current levels used in almost all applications.  

    https://en.wikipedia.org/wiki/Diode_modelling#Iterative_solution
    discusses the solution of a circuit problem with a diode using the
    Shockley diode equation.  In a python script, it would just be simpler
    to have the empirical equation and step through all the discrete
    current points looking for a solution (since this would be < 30 points,
    this would be very fast).

Once this diode i(V) relationship is known, it can be used iteratively to
solve practical problems.  A typical problem is to select a series resistor 
to allow an LED to indicate a particular voltage.  Example:  what resistor
should I use in series with an LED to put across the 120 V line?  The
complicating factor is that you want the dissipated power in the resistor
to be less than or equal to the on-hand resistors' power rating.
Therefore, the problem is stated with:

    * LED size
    * LED color
    * Allowed maximum resistor power, W
    * Set of on-hand resistance values
    * Operating voltage V

Then the calculation's results are:

    * Selected resistor
    * Resulting current through the LED

Once this result is known, you can then interactively enter a smaller
current and a suitable resistor will be chosen.  This lets you pick a
desired operating current, as you can easily check the LED on the bench at
the desired current level.

Note the importance of getting the HP 6181C current source fixed, as it is
a excellent tool for quickly testing LEDs.  It has 2.5 and 25 mA ranges
with a 10-turn pot and analog readout.  You quickly and safely set the
desired current level of the LED to check brightness.

'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2019 Don Peterson #∞copyright∞#
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
if 1:   # Imports
    import getopt
    import os
    import sys
    from pdb import set_trace as xx 
if 1:   # For plotting
    # For plots
    from pylab import *
    if 1:   # banggood 5 mm LEDs
        P = plot
        P = semilogx
        P = loglog
        i = (1, 5, 10, 20, 30, 40, 50)
        # Green
        V = (2.31, 2.52, 2.67, 2.85, 2.96, 3.04, 3.08)
        P(i, V, "go-", label="Green")
        # Red
        V = (1.79, 2.02, 2.18, 2.36, 2.52, 2.65, 2.74)
        P(i, V, "ro-", label="Red")
        # Blue
        V = (2.66, 2.88, 3.05, 3.27, 3.36, 3.45, 3.53)
        P(i, V, "bo-", label="Blue")
        # White
        V = (2.61, 2.84, 3.03, 3.30, 3.27, 3.70, 3.85)
        P(i, V, "ko-", label="White")
        title("banggood 5 mm LEDs")
        xlabel("Current, mA")
        ylabel("Voltage, V")
        grid()
        legend()
        show()
        exit(0)
    if 0:   # banggood 88 cent 10 W bright white LEDs, 12 Feb 2017:  plot i/V
        i_mA = (10, 20, 50, 100, 150, 200, 250, 300, 400, 500, 600, 700, 750,
                800, 900, 1000, 1100)
        V_V = (8.14, 8.34, 8.71, 9.25, 9.71, 10.1, 10.47, 10.77, 11.34, 11.84,
            12.32, 12.76, 12.92, 13.13, 13.57, 13.98, 14.38)
        plot(i_mA, V_V, ".-")
        if 0:  # Fit-by-eye simple model and rated power for first LED
            axhline(12.96, color="k")
            axvline(761.5, color="k")
            i = array(i_mA)
            plot(i, i**0.34 + 3.5)
            text(75, 7, "V = i**0.34 + 3.5")
            text(1.01*761.5, 0.98*12.96, "10 W rated power")
        # 2nd and 3rd LEDs
        i_mA = arange(100, 1101, 100)
        plot(i_mA, (9.18, 9.91, 10.52, 11.01, 11.41, 11.77, 12.16, 12.53, 
                    12.85, 13.18, 13.51), ".-")
        plot(i_mA, (9.20, 9.98, 10.57, 11.12, 11.57, 12.01, 12.41, 12.76,
                    13.11, 13.49, 13.85), ".-")
        grid()
        xlabel("Current, mA")
        ylabel("Forward voltage, V")
        title("Banggood 88 cent LED, 10 W")
        text(100, 14.5, "Rated 10 W power attained around 800 mA")
        show()
    if 0:   # Gossen light meter
        ev = range(-2, 17)
        lux = (1.4, 2.8, 5.5, 11, 22, 44, 88, 175, 350, 700, 1400, 2800,
            5500, 11e3, 22e3, 44e3, 88e3, 175e3, 350e3)
        grid()
        xlabel("EV")
        ylabel("Base 2 logarithm of lux")
        title("Gossen Light Meter")
        plot(ev, log(lux)/log(2))
        show()
    if 0:   # banggood $3 white LED striplight
        V = (7.41, 7.64, 7.86, 7.95, 8.06, 8.19, 8.29, 8.37, 8.45, 9.56, 10.65,
            12.00, 12.45, 14.18, 15.79, 17.34)
        i_mA = (0.0019, 0.0090, 0.0512, 0.1013, 0.198, 0.408, 0.601, 0.806,
                1.005, 5.02, 10.10, 17.1, 19.9, 30.1, 40.2, 50.2)
        plot(i_mA, V, ".-")
        grid()
        xlabel("Current, mA")
        ylabel("Forward voltage, V")
        title("Banggood $3 strip LED lights, 5 m, one 50 mm section")
        show()
    if 0:   # Single LED from banggood $3 white LED striplight
        i_mA = array((1, 5, 10, 15, 20, 30, 40, 50, 75))
        # Relative to 2.6 EV
        EV = array((-2.5, -0.5, 0.33, 0.8, 1.15, 1.6, 1.8, 2, 2))
        lux = 5.5*2**(EV + 2.6)
        plot(i_mA, lux, ".-")
        grid()
        xlabel("Current, mA")
        ylabel("lux at 100 mm on-axis")
        title("Banggood $3 strip LED lights, one LED's light output")
        i = i_mA[:-1]
        a, b = 6.9, 0.775
        plot(i, a*i**b, "r")
        text(20, 40, "Model:  lux = 6.9*i^0.775")
        text(20, 32, "Valid for 1 to 50 mA")
        show()
    if 0: # Measure voltage across banggood $3 white LED strip's 151 ohm
          # resistor to get section current.
        i_mA = array((0, 50))
        R = 151
        v = i_mA*R/1000
        plot(v, i_mA)
        grid()
        xlabel("Voltage drop across 151 ohm resistor, V")
        ylabel("Current through element, mA")
        title("Banggood $3 strip LED lights, measuring current flow")
        show()
    if 0:   # banggood $3 white LED strip
        # Drop in current as function of section number:  banggood $3 white
        # LED strip.  (Section #40 had shorted 151 ohm resistor, so couldn't
        # estimate current.)
        section = array((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 50,
                        60, 70, 80, 90, 100))
        i_drop = array((16.6, 16.8, 16.4, 16.2, 16.5, 16.0, 15.6, 15.3, 15.4,
                        14.8, 15.2, 12.9, 11.6, 9.3, 8.6, 7.7, 7.8, 7.5,
                        7.2))/16.6
        plot(section, i_drop, ".-")
        grid()
        xlabel("Section")
        ylabel("Fraction of current of section 1")
        title("Banggood $3 strip LED lights:  current drop due to lead resistance")
        # Model with an exponential fall-off
        plot(section, exp(-section/100), "r")
        text(40, 0.83, "Red:  exp(-section/100)")
        show()
    if 0:   # banggood $3 white LED strip
        # Drop in voltage as function of section number:  banggood $3 white
        # LED strip.  
        section = array((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50,
                        60, 70, 80, 90, 100))
        delta_V = array((0.00, 0.04, 0.10, 0.14, 0.18, 0.23, 0.27, 0.31, 0.35,
                        0.40, 0.45, 0.78, 1.08, 1.36, 1.54, 1.69, 1.80, 1.89,
                        1.92, 1.98))
        plot(section, delta_V, ".-")
        grid()
        xlabel("Section")
        ylabel("Voltage drop, V")
        title("Banggood $3 strip LED lights:  voltage drop due to lead resistance")
        # Model with an exponential fall-off
        plot(section, 2.1*(1 - exp(-section**1.25/100)), "r")
        text(40, 0.83, "Red:  2.1*(1 - exp(-section^1.25/100))")
        show()
    if 0:   # 42 section $3 banggood white strip.  Drop in lux as normal
        # distance from strip increases.
        z_m = array((0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1,
                    1.2, 1.3, 2.1))
        # Centerline
        EV = array((7, 5.9, 5.2, 4.7, 4.3, 4, 3.75, 3.5, 3.2, 3, 2.8,
                    2.65, 2.55, 1.3))
        lux = 5.5*2**EV
        plot(z_m, lux, "b.-", label="center")
        # Sink end
        EV = array((5.6, 4.8, 4.1, 3.7, 3.3, 3.0, 2.9, 2.6, 2.5, 2.3,
                    2.05, 2, 1.95, 1.1))
        lux = 5.5*2**EV
        plot(z_m, lux, "g.-", label="end, sink")
        # Stove end
        EV = array((5.7, 4.7, 4.1, 3.75, 3.35, 3.1, 2.8, 2.6, 2.5, 2.3, 2.1,
                    2, 1.9, 1.1))
        lux = 5.5*2**EV
        plot(z_m, lux, "r.-", label="end, stove")
        grid()
        xlabel("z = distance from strip center, m")
        ylabel("lux")
        title("Banggood $3 strip LED lights:  lux vs distance")
        legend(loc="upper right")
        # Plot an inverse function
        plot(z_m, 60/z_m, "m")
        text(0.5, 250, "Magenta:  60/z, so inverse fall-off model is reasonable")
        show()
    if 0:   # 42 section $3 banggood white strip.  Drop in lux as transverse
        # distance increases.  Distance from strip is 1.345 m.
        h_m = array((0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1,
                    1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 2.1, 2.2))
        h_m -= 0.383    # Set origin where 0 is under strip
        lux = ((23.6, 25.3, 31.1, 32.2, 33.3, 33.3, 33.3, 30.1, 31.1, 31.1, 30.1,
                27.1, 25.3, 25.3, 22.0, 17.9, 16.7, 13.5, 13.5, 11.8, 10.6, 8.9,
                5.5))
        plot(h_m, lux, "b.-")
        grid()
        xlabel("h = distance from strip center, m")
        ylabel("lux")
        title("Banggood $3 strip LED lights:\n"
            "lux vs horiz distance with z = 1.345 m")
        plot((0.2, 2.2 - 0.383), (33.3, 5.5), "r")
        show()
    if 0:   # Single section $3 banggood white strip.  EV measured as function
        # of normal distance (note integrating sphere axis was about 5 mm
        # below the LED's normal for all but the first measurement at z = 0).
        if 1:  # Plot all
            h_mm = array((0, 20, 50, 100, 200, 300, 400, 500, 600))
            EV = array((12.3, 8.2, 5.3, 3.3, 1.2, 0, -0.95, -1.55, -2))
            lux = 5.5*2**EV
            semilogy(h_mm, lux, "b.-", label="LED 1")
            EV = array((11.2, 7.9, 5.4, 3.3, 1.55, 0, -0.95, -1.4, -2.1))
            lux = 5.5*2**EV
            semilogy(h_mm, lux, "g.-", label="LED 2")
        else:   # Plot >= 100 mm
            h_mm = array((0, 20, 50, 100, 200, 300, 400, 500, 600))
            EV = array((12.3, 8.2, 5.3, 3.3, 1.2, 0, -0.95, -1.55, -2))
            lux = 5.5*2**EV
            semilogy(h_mm[3:], lux[3:], "b.-", label="LED 1")
            EV = array((11.2, 7.9, 5.4, 3.3, 1.55, 0, -0.95, -1.4, -2.1))
            lux = 5.5*2**EV
            semilogy(h_mm[3:], lux[3:], "g.-", label="LED 2")
            # Plot a slope 2 line
            lux = 5.5*2**3.3
            semilogy((100, 300), (lux, lux/16), "r")
            # Plot a slope 1 line
            lux = 5.5*2**-2.05
            semilogy((400, 600), (2*lux, lux), "r")
        grid()
        xlabel("h = distance from LED, mm")
        ylabel("lux")
        title("Banggood $3 strip LED lights:\n"
            "lux vs distance along normal")
        show()
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
def LED_data():
    LEDs = dedent('''
                        LED Characteristics
    
    12 Feb 2017:  10 W white LED from banggood for 88 cents.  Mounted on
    1/8" thick 3/4 aluminum channel 4' long.  10 degF temperature rise when
    run at 750 mA.  V/i/P characteristics:
    
     Current, mA    Voltage, V  Power, W
     -----------    ----------  --------
         10            8.14       0.081
         20            8.34       0.17
         50            8.71       0.44
        100            9.25       0.93
        150            9.71       1.5
        200           10.10       2.0
        250           10.47       2.6
        300           10.77       3.2
        400           11.34       4.5
        500           11.84       5.9
        600           12.32       7.4
        700           12.76       8.9
        750           12.92       9.7
        800           13.13      11
        900           13.57      12
       1000           13.98      14
       1100           14.38      16
    
    Variation in forward voltage at 800 mA:
        1:13.4, 2:12.8, 3:13.0, 4:12.6, 5:12.8, 6:13.2, 7:13.0, 8:13.4
        mean = 13.02 V, s = 0.29 V.
    
    Lumens per watt
        Incandescent    10-11
        Halogen A-line  12-22
        Hg vapor        25-60
        Fluorescent     30-110
        CFL             40-70
        White LED       40-100
        Hi press. Na    50-140
        Metal halide    70-115
    
    Ref: 
        https://www.mge.com/saving-energy/home/lighting/lumens-comparison.htm
        https://en.wikipedia.org/wiki/Luminous_efficacy#Lighting_efficiency
    
    Illuminance:  lux = lumen/m^2 (EV is Gossen light meter reading at 50 ASA)
        Lux          EV      
        -----     ----------
        0.1 m        -5.8           Starlight
        0.3-1        -3             Full moon
        3.5          -0.7           Civil twilight
        20-50      1.9-3.2          Public areas with dark surroundings
        50           3.2            Living room lights
        80           3.9            Office building hallway, bathroom lighting
        100          4.2            Dark overcast day
        300-500     5.8-6.5         Office lighting
        400          6.2            Sunrise/sunset
        1 k          7.5            Overcast day; TV studio lighting
        10-25 k    10.8-12.2        Daylight (not direct sun)
        32-100 k   12.5-14.2        Direct sunlight
    ''')
    print(LEDs)
    # Gossen light meter conversions from EV to lux (set to ASA 50)
    print("Gossen light meter set to 50 ASA:  EV to lux")
    EV = range(-2, 17)
    LUX = (1.4, 2.8, 5.5, 11, 22, 44, 88, 175, 350, 700, 1400, 2800,
           5500, 11e3, 22e3, 44e3, 88e3, 175e3, 350e3)
    o = []
    for ev, lux in zip(EV, LUX):
        o.append("{:3d} {:>6d}".format(ev, int(lux)))
    for i in Columnize(o, col_width=20):
        print(i)
    print(dedent('''
    Representative forward voltages at 10 mA:
        Red     1.6-2
        Amber   1.9
        Green   2-2.5
        Blue    2.7, 3.8
        White   2.8-3.6
    
    Banggood 3 mm LEDs V vs i (measured)
        mA     Yellow   Green     Red      Blue    White
        0.5     1.85     1.87     1.81     2.62     2.60
         1      1.90     1.91     1.84     2.67     2.64
         2      1.94     1.94     1.87     2.74     2.70
         5      1.99     1.98     1.93     2.86     2.80
        10      2.03     2.02     1.97     3.00     2.90
        15      2.06     2.04     2.01     3.10     2.98
        20      2.07     2.06     2.03     3.16     3.05
        25      2.09     2.07     2.05     3.21     3.11
        30      2.10     2.08     2.07     3.25     3.17
    Banggood 5 mm LEDs V vs i (measured)
        mA     Yellow   Green     Red      Blue    White
        0.5     1.85     2.28     1.76     2.61     2.61
         1      1.88     2.33     1.79     2.65     2.65
         2      1.92     2.40     1.83     2.71     2.70
         5      1.98     2.54     1.90     2.82     2.82
        10      2.05     2.68     1.98     2.95     2.96
        15      2.09     2.78     2.03     3.05     3.07
        20      2.12     2.86     2.07     3.13     3.14
        25      2.15     2.92     2.10     3.19     3.21
        30      2.16     2.98     2.13     3.25     3.26
    '''))
def LED(color="green"):
    '''Returns a sequence of (i, V, R) values for the 5 mm LEDs that I use.
    '''
    leds = {"red": [], "green": [], "blue": []}
    Int = lambda x:  int(x) if int(x) == x else x
    data = '''
        # i_mA  V_red   V_green V_blue
        0.5     1.71    2.18    2.42
        1       1.77    2.30    2.52
        2       1.82    2.43    2.59
        5       1.89    2.65    2.71
        10      1.97    2.89    2.89
        15      2.02    3.06    3.02
        20      2.06    3.19    3.13
        25      2.09    3.30    3.23
        30      2.12    3.40    3.32
        40      2.17    3.57    3.46
        50      2.21    3.72    3.58'''.strip()
    for line in data.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            continue
        i_mA, V_red, V_green, V_blue = [float(i) for i in line.split()]
        leds["red"].append((Int(i_mA), V_red, int(1000*V_red/i_mA)))
        leds["green"].append((Int(i_mA), V_green, int(1000*V_green/i_mA)))
        leds["blue"].append((Int(i_mA), V_blue, int(1000*V_blue/i_mA)))
    return leds[color]
def Iterate(R, V, color):
    '''Given R in ohms and V in volts, estimate the current through the
    given color of banggood LED.  color must be 'red', 'yel', grn', 'blu',
    'wht'.
    '''
    i_mA = 1000*V/R     # Current must be less than this value
    if i_mA > 50:
        print("Current > 50 mA")
        exit(1)
if __name__ == "__main__": 
    #if len(sys.argv) > 1:
    #    Iterate(sys.argv[1:])
    LED_data()
    if 0:
        print()
        print(dedent('''
        5 mm colored LED properties
        V in volts, R in ohms'''))
        red = LED("red")
        green = LED("green")
        blue = LED("blue")
        fmt = " {:3s}     " + "{:4.2f}    {:4d}   "*3
        print(dedent('''
                    Red           Green           Blue
        i, mA      V       R      V       R      V       R 
        -----    ------------   ------------   ------------'''))
        for j in range(len(red)):
            i, Vr, Rr = red[j]
            Vg, Rg = green[j][1:]
            Vb, Rb = blue[j][1:]
            print(fmt.format(str(i), Vr, Rr, Vg, Rg, Vb, Rb))
    exit(0)
