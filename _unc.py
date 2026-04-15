'''
Generate some simple uncertainty examples to use as test cases


'''
from uncertainties import *
from uncertainties.umath import *
from wrap import Dedent

unc_ft = 0.1   
x1 = ufloat("100", unc_ft)
x2 = ufloat("150", unc_ft)
spc = " "*2

def Introduction():
    print("Introduction")
    print(Dedent(f'''
    This simulates a measurement made in the yard with a Starrett fiberglass 200 foot
    tape measure.  The tape measure is graduated in units of 0.01 ft.  I have no
    standard or calibration to know the uncertainty, so I'm forced to estimate a type B
    uncertainty.  Much of the measurement uncertainty won't come from the uncertainty in
    the tape measure itself, it will come from going over the bumpy lawn and having to
    be pulled on to get things straighter (tape stretch and small cumulative cosine
    errors).  I'll estimate the uncertainty at 0.1 ft, which means the standard
    deviation is about 1.2 inches.  If you regard a measurement as "nearly certain" if
    it's within 3 standard deviations, then that means we regard each measurement as
    "known" within about ±3.5 inches as a near certainty.  For a 50 to 100 ft typical
    measurement in the yard, that doesn't sound too optimistic or pessimistic.

    ''', n=2))
def BasicArithmetic():
    print("Basic arithmetic:")
    print(f"{spc}x1 = {x1:.2uS}")
    print(f"{spc}x2 = {x2:.2uS}")
    print(f"{spc}x1 + x2 = {x1 + x2:.2uS}")
    print(f"{spc}x1 - x2 = {x1 - x2:.2uS}")
    print(f"{spc}x1*x2 = {x1*x2:.2uS}")
    print(f"{spc}x1/x2 = {x1/x2:.2uS}")
def Problematic():
    print("Problematic:")
    print(f"{spc}sqrt(ufloat(0, 1)) = {sqrt(ufloat(0, 1))}")
    print(f"{spc}ufloat(0, 1)/ufloat(0.0001, 1) = {ufloat(0, 1)/ufloat(0.0001, 1)}")
def Trig():
    angle = ufloat(60, 2)
    y = sqrt(x1*x1 + x2*x2 - 2*x1*x2*cos(radians(angle)))
    print("Trig:")
    print(Dedent(f'''
    Using the cosine law and lengths x1 = {x1} and x2 = {x2},
    calculate the third edge of a triangle if the angle between the two lengths is 
    60(2) degrees, measured with a small compass.  The formula is
        y² = x1² + x2² - 2*x1*x2*cos(angle)
    where angle = {angle}°.  The task is to convert the angle to radians, thend
    peform the calculation.  The terms are
        x1² = {x1*x1}
        x2² = {x2*x2}
        2*x1*x2 = {2*x1*x2}
        cos(radians(angle)) = {cos(radians(angle))}
    Putting the pieces together, the result is
        y = {y}
    Note:  a calculator gives 132.388.
    ''', n=2))

Introduction()
BasicArithmetic()
Problematic()
Trig()
