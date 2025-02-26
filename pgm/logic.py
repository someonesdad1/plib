from wrap import dedent
from color import t

t.one = t("redl")
t.zero = t("grnl")
t.e = t("lill")
t.y = t("yell")
t.o = t("ornl")

s = dedent(f"""
                {t.y}Logic truth tables{t.n}
 
        {t.e}A   B   A {t.o}NOR{t.e} B   A {t.o}NAND{t.e} B   A {t.o}XOR{t.e} B
       --- ---  -------   --------   -------{t.n}
        y   y      x         x          y
        y   x      y         x          x
        x   y      y         x          x
        x   x      y         y          y
 
        {t.e}A   B   A {t.o}OR{t.e} B    A {t.o}AND{t.e} B    A {t.o}XNOR{t.e} B
       --- ---  ------    -------    -------{t.n}
        y   y      y         y          x
        y   x      x         y          y
        x   y      x         y          y
        x   x      x         x          x
""")
s = s.replace("x", f"{t.one}1{t.n}")
s = s.replace("y", f"{t.zero}0{t.n}")
print(s)
