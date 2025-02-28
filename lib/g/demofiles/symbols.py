"""
Create two pages that demonstrate the symbols available in the g.py
framework.

This worked well under python 2.7, but because of the change to Unicode in
python 3, the characters with the 8th bit set no longer render correctly;
thus, I limited the output to the 7-bit characters.

"""

import string
import sys
import re
from math import pow
from g import *

text_size = 0.25
origin_x, origin_y = 0.5, 0.5
scale_factor = 0.9
rng = 128


def Symbols(hex=0):
    push()
    translate(origin_x, origin_y)
    scale(scale_factor, scale_factor)
    move(0.5, 8.2)
    textSize(0.25)
    s = f"{'(hex)' if hex else '(decimal)'}"
    text(f"Characters available in the Symbol font {s}")
    dx = 1.0
    dy = 0.3
    top = 7.9
    left = 0.5
    for i in range(rng):
        if i == 92:
            continue
        x = i % 10
        y = i // 10
        move(left + dx * x, top - dy * y)
        textName(Symbol)
        textSize(text_size)
        text(chr(i))
        s = f"{i:02x}:{chr(i)}"
        move(left + dx * x + dx / 6, top - dy * y)
        textName(Sans)
        textSize(text_size * 0.8)
        if hex:
            text("   %02x" % i)
        else:
            text("  %3d" % i)
    pop()


def Regular():
    push()
    translate(origin_x, origin_y)
    scale(scale_factor, scale_factor)
    move(0.5, 8.2)
    textSize(0.25)
    text("Characters available in the regular Sans font")
    dx = 1.0
    dy = 0.3
    top = 7.9
    left = 0.5
    textName(Sans)
    for i in range(rng):
        if i == 92:
            continue
        x = i % 10
        y = i // 10
        move(left + dx * x, top - dy * y)
        textSize(text_size)
        text(chr(i))
        move(left + dx * x + dx / 6, top - dy * y)
        textSize(text_size * 0.8)
        text("  %3d" % i)
    pop()


if __name__ == "__main__":
    s = SetUp("out/symbols.ps", landscape, inches)
    Symbols(hex=1)
    newPage()
    Symbols()
    newPage()
    Regular()
    s.close()
