'''
Draws a 1951 USAF-type of resolution target.
'''
from g import *
def Element(X, Y, size, label):
    '''Draws an element whose lower left corner is at (X, Y) with the
    given size.  It is labelled using the given string in label.
    '''
    push()
    fillOn()
    y = 2.5 * size
    x = size / 2
    push()
    translate(X, Y)
    move(0, 0)
    for i in (0, 2, 4):
        move(i * x, 0)
        rectangle(x, y)
    pop()
    push()
    translate(X + 7 * x, Y)
    for i in (0, 2, 4):
        move(0, i * x)
        rectangle(y, x)
    pop()
    move(X, Y + size)
    textSize(size)
    rtext(label + " ")
    pop()
def MakeArray():
    X = 30
    Y = 250
    factor = 2 ** (1 / 6)
    size = 10
    for i in range(15):
        Element(X, Y, size, "%.2f" % (1 / size))
        size /= factor
        Y -= 3.5 * size
    X = 80
    Y = 70
    for i in range(15):
        Element(X, Y, size, "%.2f" % (1 / size))
        size /= factor
        Y -= 3.5 * size
def Chart1():
    s = SetUp("out/resolution_target.ps", portrait, mm)
    MakeArray()
    X = 130
    move(X, 100)
    sz = 10
    textSize(sz)
    ctext("Resolution Chart")
    textSize(sz * 2 / 3)
    move(X, 90)
    ctext("Numbers are approximate lines/mm")
    move(X, 80)
    ctext("DP 5 Aug 2007")
    s.close()
def Chart2():
    s = SetUp("out/resolution_target_gray.ps", portrait, mm)
    c = gray(0.8)
    fillColor(c)
    lineColor(c)
    MakeArray()
    X = 130
    move(X, 100)
    sz = 10
    textSize(sz)
    ctext("Resolution Chart")
    textSize(sz * 2 / 3)
    move(X, 90)
    ctext("Numbers are approximate lines/mm")
    move(X, 80)
    ctext("DP 5 Aug 2007")
    s.close()
if __name__ == "__main__": 
    Chart1()
    Chart2()
