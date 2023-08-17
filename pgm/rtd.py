'''
Print RTD tables
'''
from math import sqrt
from columnize import Columnize
from color import t

a, b, R0 = 3.9083e-3, -5.775e-7, 100
t.r = ""
t.t = t("denl")
print("DIN EN 60751 RTD α = 0.00385")
if 1:   # Resistance to temperature
    print(f"\n{t.r}Resistance{t.n} in Ω to {t.t}temperature{t.n} in °C")
    o = []
    for R in range(100, 176):
        if R == 100:
            T = 0.0
        else:
            T = (sqrt(a*a - 4*b*(1 - R/R0)) - a)/(2*b)
        o.append(f"{t.r}{R:3d}{t.n} {t.t}{T:5.1f}{t.n}")
    for i in Columnize(o):
        print(i)
    print()
if 1:   # Temperature to resistance
    print(f"{t.t}Temperature{t.n} in °C to {t.r}resistance{t.n} in Ω")
    o = []
    for T in range(0, 200):
        R = R0*(1 + a*T + b*T**2)
        o.append(f"{t.t}{T:3d}{t.n} {t.r}{R:5.1f}{t.n}")
    for i in Columnize(o):
        print(i)
    print("\nClass B:  dT = ±(0.3 + 0.005 |T|) °C")
    print("Class A:  dT = ±(0.15 + 0.002 |T|) °C")
