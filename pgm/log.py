# Print out logarithms
from math import log10
from columnize import Columnize
from color import t
t.l = t("purl")
t.o = t("ornl")
t.g = t("grnl")
t.print(f"{t.g}Base 10 logarithms")
o = []
r = list(range(11, 100))
for i in r:
    s = f"{int(10000*log10(i) - 10000):3d}"
    while len(s) < 4:
        s = "0" + s
    o.append(f"  {t.o}{i:2d}{t.n}  {t.l}{s}{t.n}")
for i in Columnize(o):
    print(i)
# Short form
t.print(f"\n{t.g}Short form:")
o = '''2   3
3   5
4   6
5   7
6   78
7   84
8   9
9   95'''
for i in o.split("\n"):
    a, b = i.split()
    print(f"  {t.o}{a:1s}{t.n}  {t.l}{b}{t.n}")
