'''
Turning a ball on the lathe:  calculations via the incremental cut method
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2012 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Ball turning in the lathe
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import sys
        import os
        import getopt
    if 1:   # Custom imports
        from f import flt, sqrt
        from wrap import dedent
        import u
        from lwtest import Assert
    if 1:   # Global variables
        ii = isinstance
if 1:  # Utility
    def Manpage():
        print(dedent(f'''
    
    The method to turn a desired profile on the lathe involves positioning the cutting bit at a
    discrete number of points on along the profile.  This can be done for nearly any profile that
    can be written in Cartesian coordinates with a function or in parametric form.  Most often, the
    shape of a sphere is desired, so the method uses the Cartesian formula of a circle, which is x²
    + y² = r² where r is the radius of the circle.  This is solved to give x² = r² - y² and the
    positive square root is taken to get the required x coordinate for the given y coordinate.

    Here, the x coordinate runs in the direction of the axis of rotation with the direction towards
    the tailstock as positive.  The y direction is in the direction of the cross slide movement.

    We'll imagine the turning of a ball that is 1 inch in diameter.  This is a sphere with a radius
    of 1/2 inch.  I'm using this because my lathe's cross slide dial is graduated in inches.

    To get a picture in your head of the method, imagine you are looking down on the lathe from
    overhead.  A finished ball of diameter 1 inch sits in the chuck (ignore that there must be a
    chunk of metal holding it to e.g. some bar stock).  Imagine a the left edge of a square cutting
    tool (I use a parting tool for these cuts) is just touching the ball at the point where the
    diameter is 1 inch.  Call this the origin of the Cartesian coordinate system.  If the cutting
    tool travels a distance of 1/2 inch in the x direction towards the tailstock and the cutting tool
    also moves in the y direction a distance of 1/2 inch in, then the cutting point is at the center
    and end of the 1 inch diameter ball.

    We divide this 1/2 inch x distance into N steps where N is a reasonably-sized integer, say in the
    range of 5 to 20.  Let's choose N to be 10 for easy calculations.

    The "zeroth" cut is where the cutting tool is positioned at the origin and there's no actual
    removal of material.  The first cutting position will be at x = 1/20.  Since we have a 1 inch
    diameter circle, the radius is 1/2, so the Cartesian equation for x = 0.1 is y = sqrt(1/2² - x²) =
    sqrt(1/4 - 1/20²) = 0.49749.  

    Now, the cross slide on most lathes is graduated in diameter, not radius, so we must move the
    cross slide in half this distance, which means the reading from the zero setting will be 
    (1 - 0.994987)/2 or 0.002506.

    The steps you'll follow to turn a hemisphere are:

        - Center a square cutting toolbit (I use a cutoff tool and take light cuts).  I assume all
          material to the right of the tool is at the diameter of the hemisphere.
        - Suppose you're feeding towards the tailstock.  Place the left edge of the cutoff tool at
          the longitudinal position of the hemisphere's center.
        - Move the carriage to the right a distance of x₁.  Then feed the crossfeed in a distance
          of 2*dy.  Cut to the right end of the hemisphere, then return to the starting position.
        - Move right to x₂, feed the crossfeed again in a distance of 2*dy from where it was, then
          cut to the right end.
        - Repeat steps 3 and 4 until you've finished with the last yₖ.

    I use a 2" dial indicator to measure the position of the carriage, so it's easy to move the
    carriage to the next required position.

    The formulas for the calculations are as follows.

        xₖ = the kth ordinate (here, ordinate = longitudinal feed)
        yₖ = the kth abscissa (here, abscissa = cross feed)
        r  = the radius of the ball
        dy = the increment in y
        n  = number of desired steps

        yₖ = r - k*dy   for k = 0, 1, 2, ..., n
        xₖ = sqrt(2*r*k*dy-k*k*dy*dy)

    The table that gets printed is then:
        column 1:  k
        column 2:  xₖ
        column 3:  2*yₖ   (the 2 corrects from radius to diameter)

        '''))
        exit(0)
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} OD N
          Print a table of N incremental cuts to form a spherical shape on a lathe.  The x
          direction is parallel to the rotation axis and the y direction is in the direction the
          cross slide moves.  The table that is printed out cuts half of the sphere, so you'll need
          to use it in both longitudinal directions to cut a complete sphere.
        Options
          -h    Print a manpage describing the method
          -u u  Unit to use for distance measurement [{d["-u"]}]
          -r    The cross feed dial reads in radius, not diameter
          -y    Use equal steps in the y direction
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3         # Number of significant figures
        d["-r"] = False     # The cross feed dial reads in radius, not diameter
        d["-u"] = "inch"    # Unit to use for distance measurement
        d["-y"] = False     # Use equal steps in y direction
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "d:hu:")
        except getopt.GetoptError as str:
            msg, option = str
            print(msg)
            sys.exit(1)
        for o, a in optlist:
            if o in "":
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-u":
                try:
                    d[o] = a
                    # a must be a length unit
                    if u.dim(a) != u.Dim("L"):
                        raise Exception()
                except Exception:
                    Error(f"{a!r} is not a valid length unit")
            elif o == "-h":
                Manpage()
        if len(args) != 2:
            Usage()
        x = flt(0)
        x.N = d["-d"]
        x.rtz = x.rtdp = False
        return args
if 1:   # Core functionality
    def Calculate(OD, nsteps):
        units = d["-u"]
        f = 1/u.u(units)  # Conversion factor to convert m to user's desired units
        # Convert OD to SI
        D = OD*u.u(units)    # D is now in m
        r = D/2
        dy = r/nsteps
        print(f"Ball diameter  = {D*f} {units}")
        print(f"Crossfeed step = {dy*f} {units}\n")
        print("Num      Longitudinal      Crossfeed")
        print("---      ------------      ---------")
        w1, w2, w3, s = 3, 12, 9, " "*6
        for i in range(1, nsteps + 1):
            yi = r - i*dy
            xi = sqrt(2*r*i*dy - i*i*dy*dy)
            print(f"{i!s:^{w1}s}", end=s)
            print(f"{(xi*f)!s:^{w2}s}", end=s)
            y = 2*(r - yi)
            print(f"{(y*f)!s:^{w3}s}")

if __name__ == "__main__": 
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    OD = flt(args[0])
    nsteps = int(args[1])
    if OD <= 0:
        Error("OD must be > 0")
    if nsteps <= 0:
        Error("num_steps must be > 0")
    Calculate(OD, nsteps)
