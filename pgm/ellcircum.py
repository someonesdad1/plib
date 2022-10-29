'''

Plot the circumference of an ellipse with semimajor diameter of a = pi/2 and
eccentricity of eps.  

Ref: https://en.wikipedia.org/wiki/Ellipse#Circumference.  For a picture of
a circle with ellipses of the same circumference, see See
https://en.wikipedia.org/wiki/File:Ellipses_same_circumference.png

The formula for the ellipse circumference C is 

    C = 4 a\int_0^{\pi/2}\sqrt{1 - \epsilon^2 \sin^2 \theta} d\theta
      = 4 a E(\epsilon)

where E is the complete elliptic integral of the second kind.  The
eccentricity is related to a and the semiminor diameter b:

    \epsilon = \sqrt{1 - b^2/a^2}

Warning:  there is annoyingly no standardization in the definition of
elliptic integrals for the modulus, so if you get incorrect results,
suspect you should have used either the square or square root.

'''

from pylab import *
from lwtest import Assert
from math import pi
from scipy.special import ellipe as E
from frange import frange

def f(x):
    '''Rational approximation for complete elliptic integral of the second
    kind, https://www.exstrom.com/math/elliptic/ellipint.html.
    '''
    Assert(0 <= x <= 1)
    x2 = x  # The web page uses x**2, but scipy's ellipe uses x
    if 1:
        G = 1/4 + 4/(8 - x2) + 1/(2*(2 - x2))
    else:
        x4 = x2*x2
        G = (x4 - 28*x2 + 64)/(4*x4 - 40*x2 + 64)
    return (1 - x2*G/4)*pi/2

eps, c = [], []
a = 1
for i in frange("0", "1", "0.01", include_end=True):
    eps.append(i)
    c.append(4*a*E(i))
# Plot straight line approximation
m = -1.65
plot(eps, [m*i + 2*pi for i in eps], "r--", label=f"Linear approximation = ${m}ϵ + 2\pi$")
# Plot actual curve
plot(eps, c, "b", label="Exact")
# Plot a rational approximation
plot(eps, [4*f(i) for i in eps], "g--", label=f"Rational approximation")
# Set up the plot's details
grid()
xlabel("Eccentricity, ϵ")
ylabel("Circumference, $C$")
title("Ellipse Circumference C\n (semimajor axis $a = 1/2$)")
legend()
# Message
msg = (r"$C = 4 a E(ϵ) = 4 a\int_0^{\pi/2}\sqrt{1 - ϵ^2 \sin^2 \theta} d\theta$"
        "\n"
       r"$C = 2\pi = 6.2832$ for $ϵ = 0$ (a circle)"
        "\n"
       r"$b^2 = a^2(1 - ϵ^2)$"
        "\n"
       r"$b$ = semiminor axis of ellipse"
        "\n"
       r"Rational approx:  $E(ϵ) = (1 - ϵg/4)$ where"
        "\n"
       r"$g = 1/4 + 4/(8 - ϵ^2) + 1/(2(2 - ϵ^2))$"
        "\n"
       r"Rule:  Given major diameter $D$ of an ellipse and"
        "\n"
       r"eccentricity ϵ, calculate circumference with $D C$."
       )
text(0.02, 4.05, msg)
savefig("ellcircum.png")
