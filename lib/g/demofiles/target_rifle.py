"""
Rifle target.
"""

from g import *

line_width = 0.0075


def DrawTarget(X, Y, number):
    def rect(side):
        move(0, 0)
        rmove(-side / 2, -side / 2)
        rectangle(side, side)

    push()
    translate(X, Y)
    fillOn()
    rect(1.5)
    fillColor(white)
    rect(1.0)
    if number:
        t = 1.0
        move(-t / 3.5, -t / 2.8)
        textName(SansBold)
        textSize(t)
        text(str(number))
    pop()


def DrawTable(x, y):
    push()
    move(x, y)
    textName(CourierBold)
    data = (
        "Minutes of angle for",
        '1" inside square',
        "  Dist  yd    m",
        "   10  19.1  17.3",
        "   20   9.3   8.4",
        "   25   7.4   6.6",
        "   50   3.5   3.3",
        "   75   2.3   2.2",
        "  100   1.5   1.4",
        "  200   0.6   0.5",
    )
    textLines(data)
    pop()


def Target(file):
    s = SetUp(file, portrait, inches)
    width = 8.5
    height = 11
    nx = 2
    ny = 3
    dx = width / (2 * nx)
    dy = height / ny
    translate(width / 2, height / 2)
    lineWidth(0.05)
    DrawTarget(-dx, dy, 1)
    if 1:
        DrawTarget(dx, dy, 2)
        DrawTarget(-dx, 0, 3)
        DrawTarget(dx, 0, 4)
        DrawTarget(-dx, -dy, 5)
        DrawTarget(dx, -dy, 6)
    DrawTable(-1, -1.2)
    s.close()


Target("out/target_rifle.ps")
