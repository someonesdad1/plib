# Resistor color code

from color import C, fg, black, white
class g:
    pass
g.red = C.lred
g.yel = C.lyel
g.grn = C.lgrn
g.blu = C.lblu
g.vio = C.lmag
g.gry = C.gry
g.wht = C.lwht
g.n = C.norm

print("     ", end="")
print(f'''
{fg(black, white)}Resistor color code{g.n}

Color     Number   Multiplier
------    ------   ----------
Black       0         10⁰
Brown       1         10¹
{g.red}Red         2         10²{g.n}
Orange      3         10³
{g.yel}Yellow      4         10⁴{g.n}
{g.grn}Green       5         10⁵{g.n}
{g.blu}Blue        6         10⁶{g.n}
{g.vio}Violet      7         10⁷{g.n}
{g.gry}Gray        8         10⁸{g.n}
{g.wht}White       9         10⁹{g.n}
Gold        -         10⁻¹
Silver      -         10⁻²
'''[1:-1])
