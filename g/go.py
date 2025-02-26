"""
Classes used by the g.py module
    Objects that cause a drawing or state change will emit a proper
    PostScript string on the update() method.

    Class hierarchy:

    BaseClass
        State              Objects that control the graphical state
            Orientation
            Units
            Line
                LineType
            FillType
            TextType
            Color
            Clip
        PathObj            Encapsulates paths
            Path           Container object
            Point          <--+
            ArcCCW         <--|   These objects are just containers for the
            ArcCW          <--|   parameters defining each geometrical object.
            Bezier         <--+

    Copyright (c) 2011 Don Peterson
    Contact:  gmail.com@someonesdad1

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

        - Redistributions of source code must retain the above copyright
          notice, this list of conditions and the following disclaimer.
        - Redistributions in binary form must reproduce the above copyright
          notice, this list of conditions and the following disclaimer in
          the documentation and/or other materials provided with the
          distribution.
        - Don Peterson's name may not be used to endorse or promote
          products derived from this software without specific prior
          written permission.

    This software is provided by Don Peterson "as is" and any express or
    implied warranties, including, but not limited to, the implied
    warranties of merchantability and fitness for a particular purpose are
    disclaimed.  In no event shall Don Peterson be liable for any direct,
    indirect, incidental, special, exemplary, or consequential damages
    (including, but not limited to, procurement of substitute goods or
    services; loss of use, data, or profits; or business interruption)
    however caused and on any theory of liability, whether in contract,
    strict liability, or tort (including negligence or otherwise) arising
    in any way out of the use of this software, even if advised of the
    possibility of such damage.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    #
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    import copy
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from gco import *
if 1:  # Utility

    def f(number):
        """Utility function to avoid printing lots of digits in floats.  This
        is because Postscript can use more digits and it avoids annoyingly long
        strings like '0.10000000000000001' for 0.1.
        """
        return "%.7g" % float(number)

    def f3(number):
        "Print 3 significant figures for color changes"
        return "%.3g" % float(number)


if 1:  # Classes

    class Base:
        pass

    class State(Base):
        pass

    class Color(State):
        """Colors are stored internally as RGB; color parameters are between
        0 and 1.  The RGB-HSV transformations are from "Colour Space Conversions"
        by Ford and Roberts, 11 Aug 1998, which can be gotten from
        http://www.poynton.com/PDFs/coloureq.pdf.  Also see
        http://www.efg2.com/Lab/Library/Color/ (defunct as of May 2022).
        """

        def __init__(self, color):
            """color is expected to be a 3-tuple of RGB values.  For
            convenience, we maintain both the color attribute (the (r, g, b)
            tuple) and the individual RGB values.
            """
            self.r, self.g, self.b = color
            self.setRGB(self.r, self.g, self.b)

        def setRGB(self, r, g, b):
            if r < 0 or r > 1:
                raise Exception("Red value must be between 0 and 1")
            if g < 0 or g > 1:
                raise Exception("Green value must be between 0 and 1")
            if b < 0 or b > 1:
                raise Exception("Blue value must be between 0 and 1")
            self.r = r
            self.g = g
            self.b = b
            self.color = (r, g, b)

        def setHSV(self, H, S, V):
            """Set the color via an HSV value; convert from HSV to RGB."""
            from math import floor

            if H < 0 or H > 1:
                raise Exception("Hue must be between 0 and 1")
            if S < 0 or S > 1:
                raise Exception("Saturation must be between 0 and 1")
            if V < 0 or V > 1:
                raise Exception("Value must be between 0 and 1")
            Hex = H * 6.0  # Algorithm wants H in degrees, then divides by 60
            primary_color = floor(Hex)
            secondary_color = Hex - primary_color
            a = (1 - S) * V
            b = (1 - (S * secondary_color)) * V
            c = (1 - (S * (1 - secondary_color))) * V
            if primary_color == 0 or primary_color == 6:
                self.r, self.g, self.b = (V, c, a)
            elif primary_color == 1:
                self.r, self.g, self.b = (b, V, a)
            elif primary_color == 2:
                self.r, self.g, self.b = (a, V, c)
            elif primary_color == 3:
                self.r, self.g, self.b = (a, b, V)
            elif primary_color == 4:
                self.r, self.g, self.b = (c, a, V)
            elif primary_color == 5:
                self.r, self.g, self.b = (V, a, b)
            else:
                raise Exception("Internal error:  unexpected value of primary_color")
            self.color = (self.r, self.g, self.b)

        def getRGB(self):
            return self.color

        def getHSV(self):
            """Return an (h, s, v) tuple by converting from RGB to HSV."""
            r, g, b = self.r, self.g, self.b
            max_, min_ = max(self.color), min(self.color)
            try:
                sat = (max_ - min_) / float(max_)
            except ZeroDivisionError:
                sat = 0
            val = max_
            d = float(max_ - min_)
            if sat == 0 or d == 0:
                return (0.0, 0.0, val)
            r1 = (max_ - r) / d
            g1 = (max_ - g) / d
            b1 = (max_ - b) / d
            if sat == 0:
                hue = 0
            elif r == max_ and g == min_:
                hue = 5 + b1
            elif r == max_ and g != min_:
                hue = 1 - g1
            elif g == max_ and b == min_:
                hue = r1 + 1
            elif g == max_ and b != min_:
                hue = 3 - b1
            elif r == max_:
                hue = 3 + g1
            else:
                hue = 5 - r1
            hue = hue / 6.0
            assert 0 <= hue and hue <= 1
            assert 0 <= sat and sat <= 1
            assert 0 <= val and val <= 1
            return (hue, sat, val)

        def interp(self, other_color, T):
            """Interpolates in RGB space between two colors; the parameter T
            determines where on the line between the two indicated colors.
            For t == 0, we're at the self color and for t == 1, we're at
            other_color.  other_color is another Color object.
            """
            t = float(T)
            assert 0.0 <= t and t <= 1.0
            new_color = Color(other_color.color)
            rd = other_color.r - self.r
            gd = other_color.g - self.g
            bd = other_color.b - self.b
            new_color.setRGB(self.r + t * rd, self.g + t * gd, self.b + t * bd)
            return new_color

        def update(self, out):
            """Note we always update the color if asked."""
            out("%s %s %s setrgbcolor\n" % tuple(map(f3, self.color)))

        def colorName(self):
            """If we can find a color name, use it; otherwise, return the
            three RGB values.
            """
            if self.color in INV:
                return INV[self.color]
            else:
                return "%s, %s, %s" % tuple(map(f3, self.color))

        def __repr__(self):
            return "Color(" + self.colorName() + ")"

    class TextType(State):
        def __init__(self):
            self.setName("Sans")
            self.setSize(1)
            self.setColor(Color(black))

        def setName(self, name):
            self.name = name
            self.changed = 1

        def setSize(self, size):
            assert size > 0
            self.size = size
            self.changed = 1

        def setColor(self, color):
            self.color = color
            self.changed = 1

        def update(self):
            str_ = ""
            if self.changed:
                str_ = "/%s findfont %s scalefont setfont\n" % (self.name, f(self.size))
                self.changed = 0
            return str_

    class Paper:
        def __init__(self, size=paper_letter):
            self.validateSize(size)
            self.size = size

        def validateSize(self, size):
            if size not in paper_sizes:
                raise Exception("Unrecognized paper size")

    class Orientation(State):
        """We initialize with the assumption that we are in PostScript's default
        units, points (otherwise, the translations will be wrong).
        """

        def __init__(self, orientation=portrait, paper=None):
            self.orientation = orientation
            if paper == None:
                self.paper = Paper()  # Default paper size
            else:
                self.paper = paper
            rotation = allowed_orientations[orientation]
            width, height = paper_sizes[self.paper.size]
            self.s = (f(rotation), f(width), f(height))

        def update(self):
            return "%s rotation %s %s translation\n" % self.s

    class Line(State):
        default_width = [yes, 1]  # In points

        def __init__(self):
            self.width = self.default_width[:]
            self.color = Color(black)
            self.dash_type = [yes, solid_line]
            self.cap = [yes, cap_butt]
            self.join = [yes, join_miter]
            self.on = yes
            self.scale_width = yes
            self.scale_dash = yes
            self.width_scale_factor = 1.0
            self.dash_scale_factor = 1.0
            self.resetDashes()

        def scaleWidth(self, scale_factor_, reset=no):
            if self.scale_width == yes:
                if reset == yes:
                    self.width = self.default_width[:]
                self.width[g_changed] = yes
                self.width[g_value] = self.width[g_value] * scale_factor_

        def scaleDash(self, scale_factor_, reset=no):
            """Scale all of the allowed dash types by the set factor."""
            if self.scale_dash == yes:
                if reset == yes:
                    self.resetDashes()
                self.scale_factor = scale_factor_
                for Key in self.dashes.keys():
                    if (
                        not isinstance(self.dashes[Key], type([]))
                        or len(self.dashes[Key]) == 0
                    ):
                        continue
                    self.dashes[Key] = map(self._scaleDashSize, self.dashes[Key])
                self.dashes[scale_factor_] = 1.0

        def _scaleDashSize(self, num):
            """Scale the passed-in number by the dash scale factor."""
            return num * self.scale_factor

        def resetDashes(self):
            """Set the dashes to the default values."""
            self.dashes = copy.deepcopy(dashes)

        def update(self, out):
            if self.on == yes:
                if self.width[g_changed] == yes:
                    out("%s setlinewidth\n" % f(self.width[g_value]))
                    self.width[g_changed] = no
                if self.dash_type[g_changed] == yes:
                    str_ = "[ "
                    for num in self.dashes[self.dash_type[g_value]]:
                        str_ = str_ + ("%s " % f(num))
                    str_ = str_ + "] 0 setdash\n"
                    out(str_)
                    self.dash_type[g_changed] = no
                if self.cap[g_changed] == yes:
                    out("%d setlinecap\n" % line_caps[self.cap[g_value]])
                    self.cap[g_changed] = no
                if self.join[g_changed] == yes:
                    out("%d setlinejoin\n" % line_joins[self.join[g_value]])
                    self.join[g_changed] = no

    class Fill(State):
        def __init__(self):
            self.type = solid_fill
            self.color = Color(black)
            self.gradient_color = Color(white)
            self.gradient_angle = 0.0
            self.gradient_factor = 1.0
            self.line = Line()
            self.angle = 0.0
            self.separation = 0.0
            self.phase = 0.0
            self.on = no

        def setType(self, fill_type):
            self.type = fill_type

        def setDashType(self, dash_type):
            self.line.dash_type[g_value] = dash_type
            self.line.dash_type[g_changed] = yes

        def setColor(self, color):
            self.color = color
            self.line.color = color

        def setGradientColor(self, color):
            self.gradient_color = color

    class Font(State):
        default_size = [yes, 11]  # In points

        def __init__(self):
            self.name = [yes, Helvetica]
            self.size = self.default_size[:]
            self.color = Color(black)
            self.scale_font_size = yes

        def scaleFont(self, scale_factor_, reset=no):
            if scale_factor_ == 0:
                raise Exception("Font scale factor must be != 0")
            if reset == yes:
                self.size = self.default_size[:]
            scale_factor_ = abs(scale_factor_)
            self.size[g_value] = self.size[g_value] * scale_factor_
            self.size[g_changed] = yes

        def update(self, out):
            font_name = allowed_font_names[self.name[g_value]]
            if self.name[g_changed] == yes or self.size[g_changed] == yes:
                out(
                    "/%s findfont %s scalefont setfont\n"
                    % (font_name, self.size[g_value])
                )
                self.name[g_changed] = no
                self.size[g_changed] = no


if 1:  # Path-related classes

    class PathObj(Base):
        def GetBBox(self):
            # self.bb is the object's bounding box
            return self.bb

        def plot(self, out, is_first_point=no):
            """This function is responsible for sending the proper PostScript
            to the output stream.  out is the write method to the output
            stream and if is_first_point is yes, then there is no current
            point defined, so issue the proper moveto command.
            """
            raise Exception("Abstract method")

    class Point(PathObj):
        def __init__(self, x, y):
            self.x = float(x)
            self.y = float(y)
            self.bb = (x, y, x, y)
            self.s = (f(x), f(y))

        def plot(self, out, is_first_point=no):
            if is_first_point == yes:
                out("%s %s moveto\n" % self.s)
            else:
                out("%s %s lineto\n" % self.s)

        def __repr__(self):
            return "Point   (%s, %s)" % self.s

    class ArcCCW(PathObj):
        def __init__(self, xcenter, ycenter, radius, angle_start, angle_end):
            self.xcenter = float(xcenter)
            self.ycenter = float(ycenter)
            self.radius = float(radius)
            self.angle_start = float(angle_start)
            self.angle_end = float(angle_end)
            self.bb = (
                self.xcenter - radius,
                self.ycenter - radius,
                self.xcenter + radius,
                self.ycenter + radius,
            )
            self.s = tuple(
                map(
                    f,
                    (
                        self.xcenter,
                        self.ycenter,
                        self.radius,
                        self.angle_start,
                        self.angle_end,
                    ),
                )
            )

        def plot(self, out, is_first_point=no):
            from math import sin, cos, pi

            if is_first_point == yes:
                x = self.xcenter + self.radius * cos(self.angle_start * pi / 180)
                y = self.ycenter + self.radius * sin(self.angle_start * pi / 180)
                out("%s %s moveto\n" % (f(x), f(y)))
            out("%s %s %s %s %s arc\n" % self.s)

        def __repr__(self):
            return "Arc CCW (%s, %s, %s, %s, %s)" % self.s

    class ArcCW(PathObj):
        def __init__(self, xcenter, ycenter, radius, angle_start, angle_end):
            self.xcenter = float(xcenter)
            self.ycenter = float(ycenter)
            self.radius = float(radius)
            self.angle_start = float(angle_start)
            self.angle_end = float(angle_end)
            self.bb = (
                self.xcenter - radius,
                self.ycenter - radius,
                self.xcenter + radius,
                self.ycenter + radius,
            )
            self.s = tuple(
                map(
                    f,
                    (
                        self.xcenter,
                        self.ycenter,
                        self.radius,
                        self.angle_start,
                        self.angle_end,
                    ),
                )
            )

        def plot(self, out, is_first_point=no):
            from math import sin, cos, pi

            if is_first_point == yes:
                x = self.xcenter + self.radius * cos(self.angle_start * pi / 180)
                y = self.ycenter + self.radius * sin(self.angle_start * pi / 180)
                out("%s %s moveto\n" % (f(x), f(y)))
            out("%s %s %s %s %s arcn\n" % self.s)

        def __repr__(self):
            return "Arc CW  (%s, %s, %s, %s, %s)" % self.s

    class Bezier(PathObj):
        """A Bezier curve is a smooth curve in the X,Y plane given by a
        parametric representation that uses cubic polynomials in the parameter.
        The curve starts at (x0, y0) and ends at (x3, y3).  The initial
        direction at (x0, y0) is in the direction of the line (x0, y0)-(x1, y1)
        and analogously for the end.  The points (x1, y1) and (x2, y2) are
        called the control points.  See the PostScript reference manual, 2nd
        ed., pg 393 for the parametric equations.
        """

        def __init__(self, x0, y0, x1, y1, x2, y2, x3, y3):
            self.x0 = float(x0)
            self.y0 = float(y0)
            self.x1 = float(x1)
            self.y1 = float(y1)
            self.x2 = float(x2)
            self.y2 = float(y2)
            self.x3 = float(x3)
            self.y3 = float(y3)
            bbx0 = min(x0, x1, x2, x3)
            bby0 = min(y0, y1, y2, y3)
            bbx1 = max(x0, x1, x2, x3)
            bby1 = max(y0, y1, y2, y3)
            self.bb = (bbx0, bby0, bbx1, bby1)
            self.s = tuple(
                map(
                    f,
                    (
                        self.x0,
                        self.y0,
                        self.x1,
                        self.y1,
                        self.x2,
                        self.y2,
                        self.x3,
                        self.y3,
                    ),
                )
            )

        def __repr__(self):
            return "Bezier  [(%s, %s), (%s, %s), (%s, %s), (%s, %s)]" % self.s

        def plot(self, out, is_first_point=no):
            out("%s %s moveto %s %s %s %s %s %s curveto\n" % self.s)

    class Path(PathObj):
        """A path is a list of one or more subpaths:

            [ S1, S2, ..., Sn ]

        where S1, ..., Sn are subpaths.  A subpath is of one of the following
        forms:

            (O1, O2, ..., Om)
            [O1, O2, ..., Om]

        where the O's are objects that can be a point, a circular arc, or a
        Bezier curve.  The tuple indicates a closed subpath and a list
        indicates an open subpath.

        The last element in the path is always a list, since the user can
        append points, arcs, or Bezier curves to it at any time.  When
        pathClose() is called, it is converted into a tuple and a new empty
        list is made the container for the next subpath element.  The user
        can also call pathMove() to start a new subpath, which leaves the
        prior subpath open.
        """

        def __init__(self):
            self.pathlist = [[]]
            self.bb = ((inf, inf), (-inf, -inf))

        def add(self, obj):
            self.pathlist[-1].append(obj)
            bb = obj.GetBBox()
            self.UpdateBoundingBox(bb[0], bb[1])
            self.UpdateBoundingBox(bb[2], bb[3])

        def UpdateBoundingBox(self, x, y):
            bb = self.bb
            x0, y0, x1, y1 = bb[0][0], bb[0][1], bb[1][0], bb[1][1]
            if x < x0:
                x0 = x
            if x > x1:
                x1 = x
            if y < y0:
                y0 = y
            if y > y1:
                y1 = y
            self.bb = ((x0, y0), (x1, y1))

        def close(self):
            """Close the current subpath."""
            self.pathlist[-1] = tuple(self.pathlist[-1])
            self.pathlist.append([])

        def move(self):
            """Start a new subpath."""
            self.pathlist.append([])

        def setPath(self, out):
            """Set this path as the PostScript current path.  Out is the
            write method of the stream to send the data.
            """
            out("newpath\n")
            if len(self.pathlist) == 0 or len(self.pathlist[0]) < 1:
                raise Exception("Not enough points in path")
            num_subpaths = len(self.pathlist)
            for i in range(num_subpaths):
                subpath = self.pathlist[i]
                is_closed_path = no
                if isinstance(subpath, tuple):
                    is_closed_path = yes
                if len(subpath) == 0:
                    if i == (num_subpaths - 1):
                        # OK to have empty subpath at end
                        continue
                    else:
                        str_ = "Warning:  subpath %d is empty\n" % i
                        sys.stderr.write(str_)
                        continue
                if len(subpath) == 1:
                    # Only a problem if it's a point
                    if isinstance(subpath, Point):
                        str_ = "Warning:  subpath with one point encountered\n"
                        sys.stderr.write(str_)
                        continue
                first_item_in_subpath = yes
                for item in subpath:
                    if first_item_in_subpath == yes:
                        item.plot(out, is_first_point=yes)
                        first_item_in_subpath = no
                    else:
                        item.plot(out, is_first_point=no)
                if is_closed_path == yes:
                    out("  closepath\n")

        def __repr__(self):
            if len(self.pathlist) == 0:
                return "Path is empty"
            if len(self.pathlist) > 1:
                s = "s"
            else:
                s = ""
            str_ = "Path with %d subpath%s\n" % (len(self.pathlist), s)
            for i in range(len(self.pathlist)):
                subpath = self.pathlist[i]
                str_ = str_ + (" Subpath %d:  (" % i)
                if isinstance(subpath, tuple):
                    str_ = str_ + "closed subpath)\n"
                elif isinstance(subpath, type([])):
                    str_ = str_ + "open subpath)\n"
                else:
                    raise Exception("Internal error:  unknown subpath type")
                for item in subpath:
                    str_ = str_ + "  " + repr(item) + "\n"
            return str_

        def isEmpty(self):
            if len(self.pathlist) == 1 and len(self.pathlist[0]) == 0:
                return 1
            else:
                return 0
