"""

If no arguments are given, print a table of the circumference of an ellipse
with a major diameter of 1 as a function of the eccentricity.  This table
lets you calculate the circumference of an ellipse by multiplying the table
value by the ellipse's major diameter.

If an argument is given, plot the circumference of an ellipse with
semimajor diameter of a = pi/2 and eccentricity of eps.  This requires a
python installation with scipy and matplotlib.

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

There are two simple checks for the plotted function.  First, the
circumference of a unit circle (eps == 0) must be 2*pi.  Second, when the
eccentricity is 1, the ellipse is a flat line and the circumference is 4.

"""

if 1:  # Header
    if 1:  # Standard imports
        import sys
    if 1:  # Custom imports
        from lwtest import Assert
        from f import pi, flt
        from frange import frange
        from color import t
        from elliptic import EllipseCircumference
        from wrap import dedent
    if 1:  # Global variables
        t.title = t("grnl")
        t.hdr = t("royl")
        t.ecc = t("magl")
if 1:  # Utility

    def E(eps):
        """Return the complete elliptical integral of the second kind for
        an ellipse with unity major diameter and eccentricity eps.
        """
        Assert(0 <= eps <= 1)
        a = 1 / 2
        b = a * (1 - eps**2)
        return EllipseCircumference(2 * a, 2 * b)


if 1:  # Core functionality

    def rational(x):
        """Rational approximation for complete elliptic integral of the second
        kind, https://www.exstrom.com/math/elliptic/ellipint.html.
        """
        Assert(0 <= x <= 1)
        x2 = x  # The web page uses x**2, but scipy's ellipe uses x
        if 1:
            G = 1 / 4 + 4 / (8 - x2) + 1 / (2 * (2 - x2))
        else:
            x4 = x2 * x2
            G = (x4 - 28 * x2 + 64) / (4 * x4 - 40 * x2 + 64)
        return (1 - x2 * G / 4) * pi / 2

    def Plot():
        ecc, c = [], []
        a = 1 / 2
        for eps in frange("0", "1", "0.01", include_end=True):
            ecc.append(eps)
            c.append(4 * a * E(eps))
        # Plot straight line approximation
        m = -0.83
        plot(
            ecc,
            [m * eps + pi for eps in ecc],
            "r--",
            label=f"Linear approximation = ${m}ϵ + \pi$",
        )
        # Plot a rational approximation
        r = [2 * rational(eps) for eps in ecc]
        plot(ecc, r, "g--", label=f"Rational approximation")
        # Plot actual curve
        plot(ecc, c, "b", label="Exact")
        # Set up the plot's details
        grid()
        xlabel("Eccentricity, ϵ")
        ylabel("Circumference, $C$")
        title("Ellipse Circumference C\n (semimajor axis $a = 1/2$)")
        legend()
        # Message
        msg = (
            r"$C = 4 a E(ϵ) = 4 a\int_0^{\pi/2}\sqrt{1 - ϵ^2 \sin^2 \theta} d\theta$"
            "\n"
            r"$C = 2\pi = 6.2832$ for $ϵ = 0$ (a circle)"
            "\n"
            r"$b^2 = a^2(1 - ϵ^2), ϵ^2 = 1 - (b/a)^2$"
            "\n"
            r"$b$ = semiminor axis of ellipse"
            "\n"
            r"Rational approx:  $E(ϵ) = (1 - ϵg/4)\pi/2$ where"
            "\n"
            r"$g = 1/4 + 4/(8 - ϵ^2) + 1/(2(2 - ϵ^2))$"
            "\n"
            r"Rule:  Given major diameter $D$ of an ellipse and"
            "\n"
            r"eccentricity ϵ, calculate circumference with $D C$."
        )
        text(0.02, 2.0, msg)
        # Put an errorbar to show rational deviation at eps == 1
        bar_length = (r[-1] - 2) / 2
        x = 1.01
        errorbar(x, 2 + bar_length, yerr=0.05)
        text(1.003 * x, 2 + bar_length / 2, f"{100 * bar_length:.0f}%")
        savefig("ellcircum.png")

    def Table():
        print(
            dedent(f"""
        {t.title}Circumference C(eps) of an ellipse with unit major diameter
            eps = eccentricity = sqrt(1 - b**2), b = minor diameter{t.n}

        """)
        )
        w = 6
        # Header
        t.print(" " * 30, f"{t.ecc}Eccentricity")
        print(" " * 5, f"{t.hdr}", end="")
        for j in frange("0.0", "0.1", "0.01"):
            print(f"{j:^{w}.2f}", end=" ")
        t.print()
        # Table body
        for i in frange("0", "1", "0.1"):
            for j in frange("0", "0.1", "0.01"):
                if not j:
                    print(f"{t.hdr}{i:3.1f}{t.n}", end=" " * 3)
                eps = flt(i + j)
                c = E(eps)
                print(f"{c:^{w}.4f}", end=" ")
            print()


if __name__ == "__main__":
    if len(sys.argv) == 1:
        Table()
    else:
        from pylab import *
        from scipy.special import ellipe as E

        Plot()
