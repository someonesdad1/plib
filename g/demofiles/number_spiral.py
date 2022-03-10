'''
Draw a number spiral.  See http://numberspiral.com/index.html
    The formula for the number n's position is 
        r = sqrt(n)
        theta = sqrt(n)
    where theta is measured in revolutions, not degrees or radians.
'''
from math import fmod, sin, cos, sqrt, pi
from g import *
import primes
N = 1e3
N = int(N)
X0 = 8.5
Y0 = 11
dot_dia = 0.75
scale_factor = 0.12
prime_color = yellow
normal_color = gray(0.8)
def BlackBackground():
    # Make whole plotting area black
    push()
    fillOn()
    fillColor(black)
    move(-X0, -Y0)
    rectangle(2 * X0, 2 * Y0)
    pop()
def PlotNum(n):
    r = sqrt(n) * scale_factor
    theta = fmod(2 * pi * sqrt(n), 2 * pi)
    x = r * cos(theta)
    y = r * sin(theta)
    move(x, y)
    push()
    fillOn()
    lineOff()
    try:
        isprime = primes.IsPrime(n)
    except:
        isprime = 1
    if isprime:
        try:
            x = (-1 - sqrt(1 - 4 * (41 - n))) / 2
        except:
            x = 0.1
        if x == int(x):
            fillColor(magenta)  # Number is of the form x*x + x + 41
        else:
            fillColor(prime_color)
        circle(dot_dia * scale_factor)
    else:
        fillColor(normal_color)
        circle(dot_dia * scale_factor / 2)
    pop()
def NumberSpiral(file):
    s = Setup(file, portrait, inches)
    dx, dy = X0 / 2, Y0 / 2
    translate(dx, dy)
    BlackBackground()
    push()
    if 0:
        # Draw axes
        lineColor(gray(0.8))
        move(0, 0)
        rline(dx, 0)
        move(0, 0)
        rline(-dx, 0)
        move(0, 0)
        rline(0, dy)
        move(0, 0)
        rline(0, -dy)
    pop()
    # Figure out scale factor so plot fits on page
    r = sqrt(N)
    global scale_factor
    scale_factor = dx / (r * 1.1)
    for i in range(N):
        PlotNum(i)
    textColor(red)
    textSize(0.3)
    move(-dx + 0.2, dy - 0.4)
    text("Primes & regular numbers")
    move(-dx + 0.2, dy - 0.7)
    text("Magenta are primes from x^2 + x + 41 (Euler's formula)")
    move(-dx + 0.2, dy - 1.0)
    text("N = %d" % N)
    s.close()
NumberSpiral("out/number_spiral.ps")
