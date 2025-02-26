"""
Print out solder melting points.  Data taken from
https://www.kester.com/Portals/0/Documents/Knowledge%20Base/Alloy%20Temperature%20Chart.pdf
"""

from color import *

data = """
                         °C           °F
HIGH-TEMP
    Sn5Pb93.5Ag1.5    296-301
    Sn10Pb88Ag2       268-299
    Sn35Pb65          247
    Sn5Pb92.5Ag2.5    287-347
MID-RANGE
    Sn40Pb60          183-238
    Sn50Pb50          183-216
    Sn60Pb40          183-190
    Sn63Pb37          183
    Sn62Pb36Ag2       179
LOW-TEMP
    Sn43Pb43Bi14      144-163
LEAD-FREE
    Sn100             232
    Sn99.3Cu0.7       227
    Sn96.5Ag3.5       221
    Sn95.5Ag3.8Cu0.7  217
    Sn96.5Ag3Cu0.5    217-220
    Sn96.3Ag3.7       221-223
    Sn95Sb5           232-240
"""[1:-1]

if __name__ == "__main__":

    def c2f(x):
        return 1.8 * x + 32

    print("Solder melting point ranges\n")
    for i, line in enumerate(data.split("\n")):
        if not i:
            print(line)
            continue
        if line.startswith(" "):
            name, mp = line.strip().split()
            if name == "Sn60Pb40":
                fg(lgreen)
            elif name == "Sn63Pb37":
                fg(lcyan)
            if "-" in mp:
                low, high = [int(j) for j in mp.split("-")]
                mp = (low + high) / 2
                pm = (high - low) / 2
                dc = "{} ± {}".format(int(mp), int(pm))
                df = "{} ± {}".format(int(c2f(mp)), int(1.8 * pm))
            else:
                mp = int(mp)
                dc = "{}".format(mp)
                mp = c2f(mp)
                df = "{}".format(int(c2f(mp)))
            print("   {:20s} {:12s} {}".format(name, dc, df))
            normal()
        else:
            print(line)
