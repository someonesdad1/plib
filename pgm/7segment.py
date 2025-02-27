"""
This is a drawing library (using the g library) that can draw 7
segment and alphanumeric displays like those seen on instruments.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Draws 7 segment characters
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Custom imports
    from wrap import dedent
    import g
if 1:  # Global variables
    # Encodings (http://en.wikipedia.org/wiki/Seven-segment_display)
    # Digit, gfedcba, abcdefg.
    digits = {
        "0": (0x3F, 0x7E),
        "1": (0x06, 0x30),
        "2": (0x5B, 0x6D),
        "3": (0x4F, 0x79),
        "4": (0x66, 0x33),
        "5": (0x6D, 0x5B),
        "6": (0x7D, 0x5F),
        "7": (0x07, 0x70),
        "8": (0x7F, 0x7F),
        "9": (0x6F, 0x7B),
        "A": (0x77, 0x77),
        "b": (0x7C, 0x1F),
        "C": (0x39, 0x4E),
        "d": (0x5E, 0x3D),
        "E": (0x79, 0x4F),
        "F": (0x71, 0x47),
    }


def SetUp(file, orientation=g.landscape, units=g.mm):
    """Convenience function to set up the drawing environment and return a
    file object to the output stream.
    """
    ofp = open(file, "w")
    g.ginitialize(ofp, wrap_in_PJL=0)
    g.setOrientation(orientation, units)
    return ofp


class Seg7(object):
    def __init__(self, h, **kw):
        """Initialize with a height.  The other dimensions are gotten
        as a fraction of this height and are keywords:
            sf      Separation fraction
            wf      Width fraction
            df      Delta fraction
            vf      Vertical fraction (gives height of vertical segment)
            lc      Line color
            fc      Fill color
            lw      Line width
        The encoding is 'gfedcba' (default) or 'abcdefg'.
        """
        self.h = h  # Height
        self.lw = kw.setdefault("lw", 0.1)
        self.lc = kw.setdefault("lc", g.black)
        self.fc = kw.setdefault("fc", g.black)
        self.vf = kw.setdefault("vf", 1)
        self.wf = kw.setdefault("wf", 1 / 4)
        self.df = kw.setdefault("df", 1 / 8)
        self.sf = kw.setdefault("sf", 1 / 60)
        self.enc = kw.setdefault("enc", "gfedcba")
        if self.enc == "gfedcba":
            self.A = 1 << 1
            self.B = 1 << 2
            self.C = 1 << 3
            self.D = 1 << 4
            self.E = 1 << 5
            self.F = 1 << 6
            self.G = 1 << 7
        else:
            self.A = 1 << 7
            self.B = 1 << 6
            self.C = 1 << 5
            self.D = 1 << 4
            self.E = 1 << 3
            self.F = 1 << 2
            self.G = 1 << 1

    def DrawSegment(self, x, y, vert=False):
        # Get the dimensions
        h = self._h * self.vf if vert else self._h
        w, d = h * self.wf, h * self.df
        # Now draw the segment
        g.push()
        g.translate(x, y)
        if 0:  # Mark origin
            g.line(-10, 0, 10, 0)
            g.line(0, -10, 0, 10)
            g.move(0, 10)
            g.circle(1)
            g.move(0, 0)
            g.circle(2)
        if vert:
            g.rotate(90)
        g.NewPath()
        g.PathAddPoint(0, 0)
        g.PathAddPoint(d, -w / 2)
        g.PathAddPoint(h - d, -w / 2)
        g.PathAddPoint(h, 0)
        g.PathAddPoint(h - d, w / 2)
        g.PathAddPoint(d, w / 2)
        g.PathClose()
        p = g.GetPath()
        g.LineWidth(self.lw)
        g.LineColor(self.lc)
        g.FillColor(self.fc)
        g.FillOn()
        g.DrawPath(p)
        g.FillPath(p)
        g.pop()

    def draw(self, x, y, char=0):
        g.push()
        g.translate(x, y)
        h = self.h
        dx = h * self.sf
        if isinstance(char, str):
            char = digits[char][0]
        if char & 8:
            s.DrawSegment(h, h)  # D segment
        if char & 16:
            s.DrawSegment(h - dx, h + dx, True)  # E segment
        if char & 4:
            s.DrawSegment(2 * h + dx, h + dx, True)  # C segment
        if char & 64:
            s.DrawSegment(h, 2 * (h + dx))  # G segment
        if char & 32:
            s.DrawSegment(h - dx, 2 * h + 3 * dx, True)  # F segment
        if char & 2:
            s.DrawSegment(2 * h + dx, 2 * h + 3 * dx, True)  # B segment
        if char & 1:
            s.DrawSegment(h, 3 * h + 4 * dx)  # A segment
        g.pop()

    @property
    def h(self):
        "Segment height"
        return self._h

    @h.setter
    def h(self, h):
        assert h > 0
        self._h = h


if __name__ == "__main__":
    ofp = SetUp("a.ps")
    g.translate(10, 50)
    h = 10
    s = Seg7(h)
    h *= 1.5
    s.draw(0, 0, "0")
    s.draw(h, 0, "1")
    s.draw(2 * h, 0, "2")
    s.draw(3 * h, 0, "3")
    s.draw(4 * h, 0, "4")
    s.draw(5 * h, 0, "5")
    s.draw(6 * h, 0, "6")
    s.draw(7 * h, 0, "7")
    s.draw(8 * h, 0, "8")
    s.draw(9 * h, 0, "9")
    s.draw(10 * h, 0, "A")
    s.draw(11 * h, 0, "b")
    s.draw(12 * h, 0, "C")
    s.draw(13 * h, 0, "d")
    s.draw(14 * h, 0, "E")
    s.draw(15 * h, 0, "F")
