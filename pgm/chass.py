'''

ToDo
    - Turn this into a design tool given wire insulation temperature rating, number of conductors
      bundled, and ambient temperature.  In the report, note that it's an estimate and that
      construction of a real prototype with temperature measurement at the rated power for each
      wire is needed to check the design.

MIL5088L has tables for maximum currents in copper conductors for aeronautical vehicles.  This
standard was based on a lot of work in the 1960's and still appears to be an important design
document (see URLs below).

I suspect the chassis currents found elsewhere are derived from these milspec numbers.  The key
document is a log-log graph of allowed current versus temperature difference between ambient and
the wire; the lines are parameterized by the AWG wire size.  The graph is Figure 3 on page 46 and
47 of the PDF.  These currents are for a single copper wire in free air.

In Table 1 below, I picked two points off each line, one at 30°C (bottom end of line) and one at
250°C (top end of line).  The PDF of the page was maximized and screen captured; I plotted this to
a piece of letter paper scaled to take up the whole page in landscape mode.  This let me read off
the numbers with fairly good accuracy.  This table was used to get the empirical line slopes and
intercepts.

              Table 1
              -------
    AWG     ΔT = 30°C     ΔT = 250°C 
    ---     ---------     ----------
    10         38             104
    12         29             79
    14         21.6           60
    16         16.15          45
    18         13.9           38
    20         10.6           28.2
    22         8.22           21
    24         6.2            16
    26         4.58           12.1

https://www.lectromec.com/maximum-harness-ampacity/
https://www.lectromec.com/ampacity-improvements/ 

    Summary:  electrical harness design has become much more sophisticated, with both better
    thermal modeling (including lower air pressures at elevated altitudes) and predicting
    degradation of insulation at elevated temperatures.

    Fundamentally, the design of cable bundles is a heat transfer and materials problem, compounded
    by the need to worry about the long-term degradation of insulation at elevated temperatures.  

The HP 6033A power supply manual on page 37 of the Agilent PDF gives a table of stranded copper
wire ampacity in A derived from MIL-W-5088B (is probably for 50 °C ambient):

                  Table 2
                  -------
              Agilent
    AWG     Ampacity, A     My Chass, A
    ---     -----------     -----------
    0          245             240
    2          180             180
    4          135             140
    6          100             100
    8          75              73
    10         55              55
    12         40              41
    14         31.2            32
    16         19.4            22
    18         15.4            16
    20         8.33            11
    22         5.0             7

    Bundled derating for each wire:  2: 0.94, 3: 0.89, 4: 0.83, 5: 0.76
    Maximum ambient 50°C, conductor 105°C

The My Chass values in Table 2 come from the chassis values I use in /plib/pgm/cu_wire.py; these in
turn came from SAMS, Handbook of Electronics Tables and Formulas, various editions.  Years ago I
read comments that this SAMS information probably was based on a military standard and, through the
Agilent 6033 manual, I found the number MIL-W-5088L (the L revision is dated in the 1990's and appears
to be the latest).
'''

from math import log10
from get import GetNumberArray
from f import flt
if 1:
    import debug
    debug.SetDebugger()

# Columns are
#  AWG        
data = '''
    10         38             104
    12         29             79
    14         21.6           60
    16         16.15          45
    18         13.9           38
    20         10.6           28.2
    22         8.22           21
    24         6.2            16
    26         4.58           12.1
'''
# The array Ig contains the values I read from the MIL5088L graph for 60°C
Ig = [51.3, 40.4, 29.7, 22.3, 19, 14.4, 11, 8.6, 6.4]
# AWG  10    12    14    16   18   20   22  24   26

def GetLine(Δt30, Δt250):
    'Return the slope m and intercept 10**b'
    x1, y1 = log10(30), log10(Δt30)
    x2, y2 = log10(250), log10(Δt250)
    m = (y2 - y1)/(x2 - x1)
    b = y1 - m*x1
    return flt(m), flt(10**b)

indent = " "*4
# Calculate linear fit slope and intercept
AWG, ΔT30, ΔT250 = GetNumberArray(data)
AWG = [int(i) for i in AWG]
M, B = [], []
print("Slope and intercept from MIL5088L graph for 60°C:")
print(f"{indent}AWG       Slope      Intercept 10**b")
print(f"{indent}---       -----      ---------------")
for i, awg in enumerate(AWG):
    Δt30, Δt250 = ΔT30[i], ΔT250[i]
    m, b = GetLine(Δt30, Δt250)
    M.append(m)
    B.append(b)
    print(f"{indent}{awg:2d}        {m} {b!s:^22s}")
mean_slope = flt(sum(M)/len(M))
print(f"{indent}Mean slope = {mean_slope}")

# Print the formula's prediction:  i = b*ΔT**m
print(f"Chassis current estimates for ΔT = 60°C")
print(f"{indent}AWG    Formula    Graph     %diff")
print(f"{indent}---    -------    -----     -----")
ΔT = 60
for i, awg in enumerate(AWG):
    I = flt(B[i]*ΔT**M[i])
    pdiff = flt(100*(Ig[i] - I)/Ig[i])
    print(f"{indent}{awg}       {I!s:6s}    {flt(Ig[i])!s:6s}    {pdiff:4.1f}")

# Compare to Chass currents in existing table
print("Compared to existing Chass currents in table")
print(f"{indent}         Exact    Mean slope             Chass to Exact")
print(f"{indent}AWG      Calc        Calc        Chass        %diff")
print(f"{indent}---      -----    ----------     -----   --------------")
Chass = "55 41 32 22 16 11 7 3.5 2.2".split()
x = flt(0)
x.n = 2
x.rtz = x.rtdp = True
for i, awg in enumerate(AWG):
    I = flt(B[i]*ΔT**M[i])
    Im = flt(B[i]*ΔT**mean_slope)
    exact = I
    chass = Chass[i]
    pct = flt(100*(chass - exact)/exact)
    s = "*" if -pct > 5 else ""
    print(f"{indent}{awg}     {I:6.1f}      {Im:6.1f}       "
          f"{Chass[i]:^6s}     {pct!s:^12s} {s}")

'''
Results:

Slope and intercept:
    AWG       Slope      Intercept 10**b
    ---       -----      ---------------
    10        0.475          7.56         
    12        0.473          5.81         
    14        0.482          4.19         
    16        0.483          3.12         
    18        0.474          2.77         
    20        0.461          2.21         
    22        0.442          1.83         
    24        0.447          1.35         
    26        0.458         0.964         
    Mean slope = 0.466
Chassis current estimates for ΔT = 60°C
    AWG    Formula    Graph     %diff
    ---    -------    -----     -----
    10       52.8      51.3      -2.9
    12       40.2      40.4       0.4
    14       30.2      29.7      -1.6
    16       22.6      22.3      -1.2
    18       19.3      19.0      -1.6
    20       14.6      14.4      -1.4
    22       11.2      11.0      -1.5
    24       8.45      8.60       1.7
    26       6.29      6.40       1.7
Compared to existing Chass currents in table
             Exact    Mean slope             Chass to Exact
    AWG      Calc        Calc        Chass        %diff
    ---      -----    ----------     -----   --------------
    10       52.8        51.0         55           4.1      
    12       40.2        39.2         41           1.9      
    14       30.2        28.3         32           6.1      
    16       22.6        21.1         22           -2.6     
    18       19.3        18.7         16           -17      *
    20       14.6        14.9         11           -25      *
    22       11.2        12.3         7            -37      *
    24        8.5         9.1        3.5           -59      *
    26        6.3         6.5        2.2           -65      *

Because of the large %diff values for 18 AWG and below (flagged by *), I
felt it was appropriate to run some actual tests at the 'Exact Calc'
values.  I suspect the 'Exact Calc' values may be too large.  

The wires I have on-hand to test are:  18 ga solid copper bell wire and 24
ga solid copper from some CAT5 cable.

'''
