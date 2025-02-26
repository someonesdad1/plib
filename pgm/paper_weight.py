"""
Plot US paper weights vs. grammage
"""
# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
from pylab import *

in2mm = 25.4
mm2in = 1 / in2mm
g2oz = 0.035274

# Conversion factors
g2lbm = 0.00220462
in2_to_m2 = 0.00064516

us = (
    ("Cover (500 count)", 20, 26, 500, "r"),
    ("Bond, writing, ledger", 17, 22, 500, "r--"),
    ("Book, text, offset", 25, 38, 500, "b"),
    ("Box cover", 20, 24, 500, "g"),
    ("Paperboard (all types)", 12, 12, 1000, "k"),
    ("Bristol and tag", 22.5, 28.5, 500, "m"),
    ("Index bristol", 25.5, 30.5, 500, "c"),
    # ("Blotting", 19, 24, 500),
    # ("Hanging, waxing, bag, etc.", 24, 36, 500),
    # ("Manuscript cover", 18, 31, 500),
    # ("Newsprint", 24, 36, 500),
    # ("Tissue", 24, 36, 480),
)
gsm = arange(0, 300, 1)

if __name__ == "__main__":
    for name, w, h, count, style in us:
        area_m2 = w * h * count * in2_to_m2
        weight_lb = gsm * area_m2 * 0.00220462
        # plot(gsm, weight_lb, style, label=name)
        plot(weight_lb, gsm, style, label=name)
    # legend(loc="upper left")
    legend(loc="lower right")
    title("US paper weights")
    ylabel("grams per square meter")
    xlabel("Pounds")
    xlim(0, 200)
    grid()
    if 0:
        show()
    else:
        savefig("pictures/paper_weights.png", dpi=100)
