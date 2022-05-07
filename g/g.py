''' 
Python module to produce drawings rendered in Postscript
    Functions beginning with _ aren't intended to be called by the user.
 
    Bug 25 Oct 2012:  The global init_ellipse is initialized only once.
        This caused a problem in /math/probability_plots/probplot.py where
        two different plots were being generated to different files.  In
        the second file, the ellipse_ps definition was missing.  These
        global variables should be reset, probably when ginitialize is
        called.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Library to generate drawings using PostScript.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import sys
    import re
    from pdb import set_trace as xx
if 1:   # Custom imports
    import go
    from gco import *  # Module that contains our constants
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    pyver = sys.version_info[0]
    if pyver == 3:
        Int = (int,)
        long = int
        String = (str,)
    else:
        Int = (int, long)
        String = (str, unicode)
    escaped_char = re.compile(r"(\\[0-9a-zA-Z][0-9a-zA-Z])")
    _f = go.f
    # The following dictionary is the default graphics state.  This is used to
    # initialize the global variable gs defined below.
    gs_default = {
        g_paper_size          : go.Paper(),
        g_orientation         : go.Orientation(),
        g_units               : inches,
        g_line                : go.Line(),
        g_fill                : go.Fill(),
        g_font                : go.Font(),
        g_ctm                 : (1, 0, 0, 1, 0, 0),
        g_current_path        : None,
        g_current_clip_path   : None,
        g_current_point       : None,
        g_current_color       : go.Color(black),
        g_scale_line_width    : yes,
        g_scale_font_size     : yes,
    }
    gs             = None           # The graphics state
    gs_stack       = []             # The graphics state stack
    debug_stream   = sys.stderr
    trace_stream   = sys.stderr
    output_stream  = None           # Keep a copy from ginitialize()
    debugging      = no             # Set to yes for debugging output
    tracing        = no             # Set to yes for tracing output
    trace_indent   = 0              # Indent level of tracing messages
    trace_indent_incr = 2           # How many spaces to increase tracing indent
    out            = None           # Use for output to the Postscript stream
    err          = sys.stderr.write # Use for error output
    push_count     = 0              # Identifies unmatched pop()'s
    sent_PJL       = no             # True if PJL wrapper sent
    error_xfm_path = yes            # Exception if xfm with path set
    # The following variables keep track of whether we have emitted the
    # needed Postscript for various chunks of functionality.
    init_ellipse     = no
    init_text_circle = no
    init_path_circle = no
    init_fractions   = no
if 1:   # Functions that change the graphics state
    def ginitialize(stream, wrap_in_PJL=0):
        Entering("ginitialize")
        global output_stream
        global out
        global init_ellipse, init_text_circle, init_path_circle, init_fractions
        init_ellipse, init_text_circle, init_path_circle, init_fractions = 4*[no]
        if not stream:
            raise gException("stream must be open")
        output_stream = stream
        out = stream.write
        if wrap_in_PJL:
            out("%s@PJL JOB\n@PJL ENTER LANGUAGE=POSTSCRIPT\n" % UEL)
            global sent_PJL
            sent_PJL = yes  # Remember to send the ending UEL in Close()
        out("20 setmiterlimit\n\n")
        reset()
        Leaving()
    def reset():
        Entering("reset")
        _SetDefaultGraphicsState()
        _SetStateFromGS(new_page=yes)
        Leaving()
    def gclose():
        Entering("gclose")
        if sent_PJL == yes:
            out(UEL)
        else:
            out("showpage") # Needed to be able to export bitmaps in GSview.
            # 13 Oct 2009:  note that this command, when used, makes it
            # necessary for some reason to run the program twice before GSView
            # version 4.9 will update the screen; this didn't happen with
            # previous versions.  If you leave it out, there's no problem.
            # Hence the warning.
            err("Warning:  using gclose causes an annoyance with GSView 4.9\n")
        if push_count != 0:
            err("Warning:  push count is %d\n" % push_count)
        global output_stream
        output_stream = None  # Now it can be garbage collected
        Leaving()
    def SetOrientation(orientation=portrait, units=inches):
        Entering("SetOrientation(%s, %s)" % (INV[orientation], INV[units]))
        if orientation not in allowed_orientations:
            raise gException("orientation not recognized")
        if units not in allowed_units:
            raise gException("units not recognized")
        comment("Resetting orientation")
        gs[g_orientation].orientation = orientation
        gs[g_units]       = units
        _SetStateFromGS(new_page=yes)
        comment("End orientation reset")
        Leaving()
    def ScaleDash(Factor=1):
        Entering("ScaleDash(%s)" % _f(Factor))
        factor = float(Factor)
        if factor <= 0.0:
            raise gException("Dash scale factor must be > 0.0")
        dashes[scale_factor] = factor
        gs[g_line].scaleDash(factor)
        gs[g_fill].line.scaleDash(factor)
        Leaving()
    def ScaleDashAutomatically(yes_or_no):
        Entering("ScaleDashAutomatically(%s)" % INV[yes_or_no])
        global gs
        if yes_or_no:
            gs[g_scale_line_type] = yes
        else:
            gs[g_scale_line_type] = no
        Leaving()
    def NewPage():
        Entering("NewPage")
        out("showpage\n")
        _SetStateFromGS(new_page=yes)
        Leaving()
    def grey(Value=0.0):
        Entering("grey(%s)" % _f(Value))
        value = float(Value)
        if value < 0.0 or value > 1.0:
            raise gException("Grey value must be between 0.0 and 1.0")
        Leaving()
        return (value, value, value)
    def gray(Value=0.0):
        Entering("gray(%s)" % _f(Value))
        Leaving()
        return grey(Value)
    def LineWidth(Width):
        Entering("LineWidth(%s)" % _f(Width))
        width = float(Width)
        if width <= 0.0:
            raise gException("Line width must be > 0.0")
        global gs
        gs[g_line].width[g_value]   = width
        gs[g_line].width[g_changed] = yes
        Leaving()
    def LineFillWidth(Width):
        Entering("LineFillWidth(%s)" % _f(Width))
        width = float(Width)
        if width <= 0.0:
            raise gException("Line width must be > 0.0")
        global gs
        gs[g_fill].line.width[g_value]   = width
        gs[g_fill].line.width[g_changed] = yes
        Leaving()
    def LineType(dash_type):
        Entering("LineType(%s)" % INV[dash_type])
        if not isinstance(dash_type, Int):
            raise gException("LineType's argument must be an integer")
        if dash_type not in dashes:
            raise gException("LineType's argument '%d' not a valid number" % dash_type)
        global gs
        gs[g_line].dash_type[g_value]   = dash_type
        gs[g_line].dash_type[g_changed] = yes
        # Make sure we update the lines for the next line fill drawn
        gs[g_fill].line.dash_type[g_changed] = yes
        Leaving()
    def LineFillType(dash_type):
        Entering("LineFillType(%s)" % INV[dash_type])
        if not isinstance(dash_type, Int):
            raise gException("LineFillType's argument must be an integer")
        if dash_type not in dashes:
            raise gException("LineFillType's argument '%d' not a valid number" % dash_type)
        global gs
        gs[g_fill].setDashType(dash_type)
        # The following makes sure we update the lines for the next border drawn
        gs[g_line].dash_type[g_changed] = yes
        Leaving()
    def LineColor(color):
        Entering("LineColor(%s)" % go.Color(color).colorName())
        global gs
        gs[g_line].color = go.Color(color)
        Leaving()
    def FillColor(color):
        Entering("FillColor(%s)" % go.Color(color).colorName())
        global gs
        gs[g_fill].setColor(go.Color(color))
        Leaving()
    def GradientFill(color, Angle=0.0, factor=1.0):
        Entering("GradientFill(%s, angle=%s, factor=%s)" % \
                 (go.Color(color).colorName(), _f(Angle), _f(float(factor))))
        global gs
        from math import fmod
        angle = fmod(float(Angle), 360.)
        if angle < 0:
            angle = angle + 360.
        gs[g_fill].gradient_color  = go.Color(color)
        gs[g_fill].gradient_angle  = angle
        gs[g_fill].gradient_factor = float(factor)
        if gs[g_fill].gradient_factor <= 0:
            raise gException("factor must be > 0")
        Leaving()
    def SetColor(color):
        Entering("SetColor(%s)" % go.Color(color).colorName())
        global gs
        LineColor(color)
        FillColor(color)
        TextColor(color)
        Leaving()
    def LineCap(cap):
        Entering("LineCap(%s)" % INV[cap])
        assert(isinstance(cap, Int))
        if cap not in line_caps:
            raise gException("Unrecognized line cap type")
        global gs
        gs[g_line].cap[g_value]   = cap
        gs[g_line].cap[g_changed] = yes
        out("%d setlinecap\n" % line_caps[cap])
        Leaving()
    def LineJoin(join):
        Entering("LineJoin(%s)" % INV[join])
        assert(isinstance(join, Int))
        if join not in line_joins:
            raise gException("Unrecognized line join type")
        global gs
        gs[g_line].join[g_value]   = join
        gs[g_line].join[g_changed] = yes
        out("%d setlinejoin\n" % line_joins[join])
        Leaving()
    def LineOn():
        Entering("LineOn")
        global gs
        gs[g_line].on = yes
        Leaving()
    def LineOff():
        Entering("LineOff")
        global gs
        gs[g_line].on = no
        Leaving()
    def FillOn():
        Entering("FillOn")
        global gs
        gs[g_fill].on = yes
        Leaving()
    def FillOff():
        Entering("FillOff")
        global gs
        gs[g_fill].on = no
        Leaving()
    def FillType(fill_type):
        Entering("FillType(%s)" % INV[fill_type])
        if fill_type not in allowed_fill_types:
            raise gException("Unrecognized fill type")
        global gs
        gs[g_fill].setType(fill_type)
        Leaving()
    def TextName(text_name):
        Entering("TextName(%s)" % text_name)
        if text_name not in allowed_font_names:
            raise gException("Text name '%s' not recognized" % text_name)
        global gs
        gs[g_font].name[g_value]   = text_name
        gs[g_font].name[g_changed] = yes
        Leaving()
    def TextSize(text_size):
        Entering("TextSize(%s)" % _f(text_size))
        size = float(text_size)
        if size <= 0.0:
            raise gException("Text size must be > 0.0")
        global gs
        gs[g_font].size[g_value]   = size
        gs[g_font].size[g_changed] = yes
        Leaving()
    def TextColor(text_color):
        Entering("TextColor %s" % repr(text_color))
        global gs
        gs[g_font].color = go.Color(text_color)
        Leaving()
    def rotate(angle_in_degrees):
        '''For a rotation of t, the xfm equations are:
            x' =  x*cos(t) + y*sin(t)
            y' = -x*sin(t) + y*cos(t)
        '''
        global gs
        from math import sin, cos, pi
        Entering("rotate(%s)" % _f(angle_in_degrees))
        angle = float(angle_in_degrees)
        out("%s rotate\n" % _f(angle))
        a, b, c, d, e, f = gs[g_ctm]    # Update the CTM
        Cos = cos(angle_in_degrees*pi/180)
        Sin = sin(angle_in_degrees*pi/180)
        A =  a*Cos + c*Sin
        B =  b*Cos + d*Sin
        C = -a*Sin + c*Cos
        D = -b*Sin + d*Cos
        gs[g_ctm] = (A, B, C, D, e, f)
        p = gs[g_current_path]
        if p != None and not p.isEmpty() and error_xfm_path == yes:
            # The reason for raising an exception if a current path exists
            # under a transformation is that the drawing of the path is
            # deferred, but the effect of the transformation is immediate.
            # (This isn't a problem in Postscript, since the path's points are
            # converted to device space immediately.)
            raise gException("Transformation issued while path exists")
        Leaving()
    def translate(X, Y):
        Entering("translate(%s, %s)" % (_f(X), _f(Y)))
        x = float(X)
        y = float(Y)
        out("%s %s translate\n" % (_f(x), _f(y)))
        global gs
        a, b, c, d, e, f = gs[g_ctm]
        gs[g_ctm] = (a, b, c, d, e+X, f+Y)
        p = gs[g_current_path]
        if p != None and not p.isEmpty() and error_xfm_path == yes:
            raise gException("Transformation issued while path exists")
        Leaving()
    def scale(X, Y=None, reset=no):
        '''If reset == yes, it means the line & font objects should reset
        themselves to their default values before the scaling.  This lets us
        handle e.g. an orientation change, which typically includes a units
        change (normal behavior would e.g. be to scale a size that's already
        been scaled).
    
        If Y is None, then it is an isotropic scaling.
        '''
        global gs
        x = float(X)
        if Y is None:
            y = x
        else:
            y = float(Y)
        Entering("scale(%s, %s, reset=%s)" % (_f(x), _f(y), INV[reset]))
        if x == 0.0:
            raise gException("X scaling factor must be non-zero")
        if y == 0.0:
            raise gException("Y scaling factor must be non-zero")
        out("%s %s scale\n" % (_f(x), _f(y)))
        # If it's an isotropic scaling, update font, fill, & line stuff if needed
        if x == y:
            gs[g_line].scaleWidth(1/x, reset)
            gs[g_line].scaleDash(1/x, reset)
            gs[g_fill].line.scaleWidth(1/x, reset)
            gs[g_fill].line.scaleDash(1/x, reset)
            gs[g_font].scaleFont(1/x, reset)
        a, b, c, d, e, f = gs[g_ctm]
        gs[g_ctm] = (x*a, b, c, y*d, e, f)
        p = gs[g_current_path]
        if p != None and not p.isEmpty() and error_xfm_path == yes:
            raise gException("Transformation issued while path exists")
        Leaving()
    def getGS():
        '''Returns a copy of the graphics state.
        '''
        Entering("getGS")
        import copy
        Leaving()
        return copy.deepcopy(gs)
    def SetGS(new_GS):
        Entering("SetGS")
        global gs
        gs = new_GS
        _SetStateFromGS(new_page=yes)
        Leaving()
    def push():
        Entering("push")
        global push_count
        push_count = push_count + 1
        out("gsave\n")
        gs_stack.append(getGS())
        Leaving()
    def pop():
        Entering("pop")
        global push_count
        global gs
        if push_count < 1:
            raise gException("Pop without a corresponding Push()")
        out("grestore\n")
        push_count = push_count - 1
        assert(len(gs_stack) > 0)
        gs = gs_stack[-1]
        del gs_stack[-1]
        Leaving()
    def ScaleLineWidth(scale_width):
        Entering("ScaleLineWidth(%s)" % INV[scale_width])
        global gs
        if not isinstance(scale_width, Int):
            raise gException("Argument must be an integer")
        if scale_width:
            gs[g_scale_line_width] = yes
        else:
            gs[g_scale_line_width] = no
        Leaving()
    def ScaleTextSize(scale_size):
        Entering("ScaleTextSize(%s)" % INV[scale_size])
        global gs
        if not isinstance(scale_size, Int):
            raise gException("Argument must be an integer")
        if scale_size:
            gs[g_scale_font_size] = yes
        else:
            gs[g_scale_font_size] = no
        Leaving()
    def LineFill(angle, separation=0, phase=0.0):
        Entering("LineFill(angle=%s, sep=%s, phase=%s)" % \
              (_f(angle), _f(separation), _f(phase)))
        global gs
        gs[g_fill].angle      = float(angle)
        gs[g_fill].separation = float(separation)
        gs[g_fill].phase      = float(phase)
        Leaving()
    def clip(path=None):
        Entering("clip")
        _clip(path, eoclip=no)
        Leaving()
    def eoclip(path=None):
        Entering("eoclip")
        _clip(path, eoclip=yes)
        Leaving()
    def _clip(path=None, eoclip=no):
        '''Note we issue a newpath after the clip, since Postscript doesn't
        execute an implicit newpath after a clip command unlike it does after
        fill or stroke.
        '''
        if path == None:
            path = gs[g_current_path]
            if path == None:
                raise gException("No current path exists")
            Entering("_clip(current path, eoclip=%s"% INV[eoclip])
        else:
            Entering("_clip(user-defined path, eoclip=%s"% INV[eoclip])
        prefix = ""
        if eoclip == yes:
            prefix = "eo"
        path.setPath(out)
        out("%sclip newpath\n" % prefix)
        NewPath()
        Leaving()
    def SetPageSize(page_size):
        '''Allows the user to set the page size.  page_size can either be an
        integer constant like paper_letter, paper_A4, etc. or it can be a
        sequence of size 2 (width, height) where width and height are in
        the current units.  
     
        Note:  ISO_paper in gco.py provides a utility function to provide this
        tuple for any valid ISO paper size.
        xx:  But this function returns the size in points, so a conversion tool
        or optional parameter must be used.
        '''
        Entering("SetPageSize()")
        raise NotImplemented()
        Leaving()
    def ClipRectangle(x0, y0, x1, y1):
        Entering("ClipRectangle(%s, %s, %s, %s)" % \
                 tuple(map(_f, (x0, y0, x1, y1))))
        p = go.Path()
        p.add(go.Point(x0, y0))
        p.add(go.Point(x1, y0))
        p.add(go.Point(x1, y1))
        p.add(go.Point(x0, y1))
        p.close()
        _clip(p)
        Leaving()
    def unclip():
        Entering("unclip")
        out("initclip\n")
        Leaving()
    def comment(comment, linefeed=no):
        Entering("comment('%s', linefeed=%s)" % (comment, INV[linefeed]))
        if not isinstance(comment, String):
            raise gException("Comment must be a string")
        if linefeed == yes:
            out("\n")
        out("%% %s\n" % comment)
        Leaving()
    def move(X, Y):
        Entering("move(x=%s, y=%s)" % (_f(X), _f(Y)))
        global gs
        x = float(X)
        y = float(Y)
        out("%s %s moveto\n" % (_f(x), _f(y)))
        gs[g_current_point] = (x, y)
        Leaving()
    def rmove(X, Y):
        Entering("rmove(x=%s, y=%s)" % (_f(X), _f(Y)))
        global gs
        _CheckCurrentPoint()
        x0, y0 = gs[g_current_point]
        x = float(X)
        y = float(Y)
        out("%s %s moveto %s %s rmoveto\n" % (_f(x0), _f(y0), _f(x), _f(y)))
        gs[g_current_point] = (x+x0, y+y0)
        Leaving()
    def inline(str):
        Entering("inline '%s'" % str)
        out("%inline\n" + str + "\n")
        Leaving()
if 1:   # Functions that put marks on the page
    def line(X0, Y0, X, Y):
        Entering("line(%s, %s, %s, %s)" % tuple(map(_f, (X0, Y0, X, Y))))
        global gs
        x0 = float(X0)
        y0 = float(Y0)
        x  = float(X)
        y  = float(Y)
        gs[g_line].update(out)
        _Color(gs[g_line].color)
        out("%s %s moveto %s %s lineto stroke\n" % (_f(x0), _f(y0), _f(x), _f(y)))
        gs[g_current_point] = (x, y)
        Leaving()
    def rline(X, Y):
        Entering("rline(%s, %s)" % (_f(X), _f(Y)))
        global gs
        _CheckCurrentPoint()
        x = float(X)
        y = float(Y)
        gs[g_line].update(out)
        _Color(gs[g_line].color)
        out("%s %s rlineto stroke\n" % (_f(x), _f(y)))
        gs[g_current_point] = (x, y)
        Leaving()
    def rectangle(Width, Height):
        Entering("rectangle(width=%s, height=%s)" % (_f(Width), _f(Height)))
        _CheckCurrentPoint()
        width  = float(Width)
        height = float(Height)
        if (width == 0.0 and height == 0.0):
            Leaving()
            return
        x, y = gs[g_current_point]
        NewPath()
        PathAddPoint(x, y)
        PathAddPoint(x+width, y)
        PathAddPoint(x+width, y+height)
        PathAddPoint(x, y+height)
        PathClose()
        p = GetPath()
        gs[g_current_path] = None
        _DrawAndFill(p)
        Leaving()
    def _DrawAndFill(p):
        '''Given a path, fill it if filling is on, then stroke the outline.
        '''
        Entering("_DrawAndFill")
        _FillPath(p)
        DrawPath(p)
        Leaving()
    def RoundedRectangle(Width, Height, Corner_diam):
        Entering("RoundedRectangle(width=%s, height=%s, diam=%s)"% \
               tuple(map(_f, (Width, Height, Corner_diam))))
        _CheckCurrentPoint()
        w = float(Width)
        h = float(Height)
        r = float(Corner_diam/2.0)
        if w < 0.0:
            raise gException("Width must be >= 0.0")
        if h < 0.0:
            raise gException("Height must be >= 0.0")
        if r < 0.0:
            raise gException("Corner diameter must be >= 0.0")
        if (w == 0.0 and h == 0.0):
            Leaving()
            return
        if h - 2*r < 0.0:
            raise gException("Corner diameter is too large for the height")
        if w - 2*r < 0.0:
            raise gException("Corner diameter is too large for the width")
        # Create a rounded rectangle path
        p = go.Path()
        x, y = gs[g_current_point]
        p.add(go.Point(x+r, y))
        p.add(go.Point(x+w-r, y))
        p.add(go.ArcCCW(x+w-r, y+r, r, 270, 360))
        p.add(go.Point(x+w, y+h-r))
        p.add(go.ArcCCW(x+w-r, y+h-r, r, 0, 90))
        p.add(go.Point(x+r, y+h))
        p.add(go.ArcCCW(x+r, y+h-r, r, 90, 180))
        p.add(go.Point(x, y+r))
        p.add(go.ArcCCW(x+r, y+r, r, 180, 270))
        p.close()
        gs[g_current_path] = None
        _DrawAndFill(p)
        Leaving()
    def circle(diameter):
        Entering("circle(%s)" % _f(diameter))
        EllipticalArc(diameter, diameter, 0.0, 360.0)
        Leaving()
    def ellipse(major_diameter, minor_diameter):
        Entering("ellipse(maj_dia=%s, min_dia=%s)" % \
              (_f(major_diameter), _f(minor_diameter)))
        EllipticalArc(major_diameter, minor_diameter, 0.0, 360.0)
        Leaving()
    def arc(diameter, start, stop):
        Entering("arc(diam=%s, start=%s, stop=%s)" % \
              tuple(map(_f, (diameter, start, stop))))
        EllipticalArc(diameter, diameter, start, stop)
        Leaving()
    def EllipticalArc(major_diam, minor_diam, start, stop):
        Entering("EllipticalArc(maj_dia=%s, min_dia=%s, start=%s, stop=%s)" % \
               tuple(map(_f, (major_diam, minor_diam, start, stop))))
        _CheckCurrentPoint()
        global init_ellipse
        if init_ellipse == no:
            out(ellipse_ps)
            init_ellipse = yes
        x, y = gs[g_current_point]
        major = float(major_diam)
        minor = float(minor_diam)
        assert(major >= 0.0)
        assert(minor >= 0.0)
        if major == 0.0 and minor == 0.0:
            Leaving()
            return
        if gs[g_line].on == no and gs[g_fill].on == no:
            Leaving()
            return
        # We'll send the _DrawAndFill() routine a tuple of the ellipse
        # parameters and the bounding box.  The data structure is:
        # (str, ((xll, yll), (xur, yur))) where str contains the ellipse
        # Postscript command and ll and ur are the lower left and upper
        # right points of the bounding box.
        xll, yll = x - major/2, y - minor/2
        xur, yur = x + major/2, y + minor/2
        bb = ((xll, yll), (xur, yur))
        args = (_f(x), _f(y), _f(major), _f(minor), \
                _f(float(start)), _f(float(stop)))
        str = "%s %s %s %s %s %s ellipse " % args
        _DrawAndFill((str, bb))
        Leaving()
    def stext(text_string):
        '''This function is the same as text(), except it finds escaped
        hex values in the string and causes them to be interpreted in the
        symbol font.  Thus, for example, the command
            stext("67 \\b0C") 
        will cause one to see 67 deg C, where deg is the degree symbol.
        '''
        # Find any escaped hex values in the text.
        mo = escaped_char.search(text_string)
        if not mo:
            # Found none; just pass the string to text()
            text(text_string)
            Leaving()
            return
        while mo:
            text(text_string[:mo.start(1)])  # Print leading plain string
            hex_string = mo.group(1)[1:]
            # Print the hex string in Symbol font
            num = int(hex_string, 16)
            assert(0 <= num < 256)
            current_text_name = gs[g_font].name[g_value]
            TextName(Symbol)
            text(chr(num))
            TextName(current_text_name)
            # Do regexp search on remaining text
            text_string = text_string[mo.end(1):]
            mo = escaped_char.search(text_string)
        if text_string != "":
            text(text_string)
    # TODO: Condense these three text functions into one function and use an
    # optional parameter to provide the justification.
    def text(text):
        Entering("text('%s')" % text)
        if not isinstance(text, String):
            raise gException("text() function requires a string parameter")
        if len(text) == 0:
            Leaving()
            return
        _CheckCurrentPoint()
        def EscapeParentheses(text):
            text = text.replace("(", r"\(")
            Leaving()
            return text.replace(")", r"\)")
        _Color(gs[g_font].color)
        gs[g_font].update(out)
        out("(%s) show\n" % EscapeParentheses(text))
        Leaving()
    def ctext(text):
        Entering("ctext('%s')" % text)
        if not isinstance(text, String):
            raise gException("ctext() function requires a string parameter")
        if len(text) == 0:
            Leaving()
            return
        _CheckCurrentPoint()
        # Escape any parentheses
        text = text.replace("(", "\\(")
        text = text.replace(")", "\\)")
        _Color(gs[g_font].color)
        gs[g_font].update(out)
        x, y = gs[g_current_point]
        s = (_f(x), text, _f(y), text)
        out("%s (%s) stringwidth pop 2 div sub %s moveto (%s) show\n" % s)
        Leaving()
    def rtext(text):
        Entering("rtext('%s')" % text)
        if not isinstance(text, String):
            raise gException("rtext() function requires a string parameter")
        if len(text) == 0:
            Leaving()
            return
        _CheckCurrentPoint()
        # Escape any parentheses
        text = text.replace("(", "\\(")
        text = text.replace(")", "\\)")
        _Color(gs[g_font].color)
        gs[g_font].update(out)
        x, y = gs[g_current_point]
        s = (_f(x), text, _f(y), text)
        out("%s (%s) stringwidth pop sub %s moveto (%s) show\n" % s)
        Leaving()
    def TextLines(lines, spacing=0):
        Entering("TextLines(%d lines, spacing=%s)" % (len(lines), _f(spacing)))
        if not isinstance(lines, (list, tuple)):
            raise gException("TextLines() requires a tuple or list parameter")
        spc = float(spacing)
        if spc == 0:
            spc = gs[g_font].size[g_value]
        _CheckCurrentPoint()
        x, y = gs[g_current_point]
        _Color(gs[g_font].color)
        gs[g_font].update(out)
        for line in lines:
            # Escape any parentheses
            line = line.replace("(", "\\(")
            line = line.replace(")", "\\)")
            out("%s %s moveto (%s) show\n" % (_f(x), _f(y), line))
            y = y - spc
        Leaving()
    def TextCircle(text, diameter, center_angle=90, inside=no):
        '''Draw text around the current point in a circle of specified
        diameter.  The text will be centered around center_angle.  If inside
        is yes, then it will be drawn inside the circle; otherwise, it will
        be drawn on the outside of the circle.
        '''
        global init_text_circle
        Entering("TextCircle('%s', diam=%s, center_angle=%s, inside=%s)" % \
                 (text, _f(diameter), _f(center_angle), INV[inside]))
        if not isinstance(text, String):
            raise gException("TextCircle() function requires a string parameter")
        if len(text) == 0:
            Leaving()
            return
        if init_text_circle == no:
            out(circ_text_ps)
            init_text_circle = yes
        _CheckCurrentPoint()
        diam = float(diameter)
        angle = float(center_angle)
        if inside == no:
            cmd = "outsidecircletext"
        else:
            cmd = "insidecircletext"
        # Escape any parentheses
        text = text.replace("(", "\\(")
        text = text.replace(")", "\\)")
        _Color(gs[g_font].color)
        gs[g_font].update(out)
        x, y = gs[g_current_point]
        push()
        translate(x, y)  # Postscript algorithm requires circle center at origin
        # Params for PS routine are:  textsize center_angle radius string cmd
        str = "(%s) %s %s %s %s\n" % (text, _f(gs[g_font].size[g_value]), 
                                       _f(angle), _f(diam/2.), cmd)
        out(str)
        pop()
        Leaving()
    def TextPath(text, path, Offset=0.0):
        global init_path_circle
        Entering("TextPath('%s', path with %d elements, offset=%s)" % \
                 (text, len(path.pathlist), _f(Offset)))
        if not isinstance(text, String):
            raise gException("TextPath() function requires a string parameter")
        if not isinstance(path, go.Path):
            raise gException("TextPath() function requires the path parameter to be a path")
        if len(text) == 0:
            Leaving()
            return
        offset = float(Offset)
        if init_path_circle == no:
            out(path_text_ps)
            init_path_circle = yes
        _CheckCurrentPoint()
        # Escape any parentheses
        text = text.replace("(", "\\(")
        text = text.replace(")", "\\)")
        _Color(gs[g_font].color)
        gs[g_font].update(out)
        path.setPath(out)
        out("(%s) %s pathtext\n" % (text, _f(offset)))
        Leaving()
    def TextFraction(Numerator, Denominator):
        global init_fractions
        if isinstance(Numerator, Int):
            numerator = "%d" % Numerator
        elif not isinstance(Numerator, String):
            raise gException("TextFraction() numerator must be an integer or string")
        else:
            numerator = Numerator
        if isinstance(Denominator, Int):
            denominator = "%d" % Denominator
        elif not isinstance(Denominator, String):
            raise gException("TextFraction() denominator must be an integer or string")
        else:
            denominator = Denominator
        Entering("TextFraction(%s, %s)" % (numerator, denominator))
        if init_fractions == no:
            out(fraction_text_ps)
            init_fractions = yes
        _CheckCurrentPoint()
        _Color(gs[g_font].color)
        gs[g_font].update(out)
        out("(%s) (%s) fractionshow\n" % (numerator, denominator))
        Leaving()
    def RegularPolygon(diameter, num_sides, start_angle=0, draw=yes):
        Entering("RegularPolygon(diam=%s, num_sides=%s, start_angle=%s)" % \
              tuple(map(_f, (diameter, num_sides, start_angle))))
        _CheckCurrentPoint()
        radius = float(diameter/2.0)  # Radius of circumscribed circle
        if radius <= 0.0:
            raise gException("Diameter of inscribed circle must be greater than zero")
        assert(isinstance(num_sides, Int))
        if num_sides < 3:
            raise gException("Number of sides must be at least 3")
        if gs[g_current_point] == None:
            raise gException("Current point (which would be the polygon's center) is undefined")
        if gs[g_line].on == no and gs[g_fill].on == no:
            Leaving()
            return
        xcenter, ycenter = gs[g_current_point]
        from math import sin, cos, pi
        p = go.Path()
        offset_radians = start_angle * pi/180
        for n in range(num_sides):
            theta = 2*pi*n/num_sides + offset_radians
            x = xcenter + radius * cos(theta)
            y = ycenter + radius * sin(theta)
            p.add(go.Point(x, y))
        p.close()
        if draw == no:  # Just return the path if we're not to draw it
            Leaving()
            return p
        if gs[g_fill].on == yes:
            _Color(gs[g_fill].color)
            if gs[g_fill].type == solid_fill:
                FillPath(p)
            elif gs[g_fill].type == line_fill:
                _LineFillRegion(p)
            elif gs[g_fill].type == gradient_fill:
                _GradientFillRegion(p)
            else:
                raise gException("Unknown fill type")
        if gs[g_line].on == yes:
            _Color(gs[g_line].color)
            DrawPath(p)
        # Leave the current point at the center of the polygon
        Leaving()
        return p
if 1:   # Dealing with bitmaps via the Python Imaging Library
    def picture(image_object, width, height, stretch=no):
        '''Places a bitmap image at the current point (which will be the
        lower left corner of the picture) and makes the picture span a
        rectangle of size (width, height).  The width and height are in the
        current units.  If stretch is yes, then the picture is stretched to
        fit in the box defined by the current point and the width and height.
     
        The image variable can be either be a filename or a PIL image object.
     
        If you don't have the Python Imaging library (PIL), you can get an
        open-source version from http://www.pythonware.com/products/pil/.

            Update May 2022:  the PIL went defunct around 2011; you can 
            check out https://python-pillow.org for a replacement.  Sadly,
            Fredrik Lundh, a long-time python contributor, passed away in
            Nov 2021.
        '''
        try:
            from PIL import Image, PSDraw
        except:
            raise gException("Functionality not available.  You must have PIL installed.")
        if isinstance(image_object, String):
            # It's a filename
            image = Image.open(image_object)
        else:
            image = image_object
        Entering("picture(im=%s, width=%s,height=%s, stretch=%s)" % \
              (repr(image_object), _f(width), _f(height), INV[stretch]))
        _CheckCurrentPoint()
        x0, y0 = gs[g_current_point]
        x1, y1 = (x0 + width, y0 + height)
        bounding_box = (x0, y0, x1, y1)
        xpic, ypic = image.size
        if stretch == yes:
            # Get the scale factor by considering two boxes.  Get the ratio of
            # their height to width and set them equal.  Then ask for the
            # two factors to convert the height and width of the first box
            # into a box with the same ratio as the second; you can generally
            # pick one of the factors to be 1.  The factor works out to be
            # (w1*h2)/(w2*h1) where w1 is the width of the first box, h1 is
            # its height, etc.
            scale_factor = float(xpic)*height/(ypic*width)
            image = image.resize((xpic, scale_factor*ypic))
        p = PSDraw.PSDraw(output_stream)
        #
        # 24 Jan 2003:  This chunk of code doesn't work anymore; I get an
        # error when using GSview/Ghostscript.  The offending command is
        # the gsize command; I found that when I removed it from the
        # Postscript data, the image appeared on the page.  Thus, as a
        # workaround, I changed line 94 in the PSDraw.py file in the
        # PIL library.
        p.image(bounding_box, image)
        Leaving()
if 1:   # Functionality dealing with paths
    def PathAddPoint(X, Y):
        Entering("PathAddPoint(%s, %s)" % (_f(X), _f(Y)))
        PathAdd((X, Y), path_point)
        Leaving()
    def PathAddPoints(points):
        if not isinstance(points, (list, tuple)):
            raise gException("Must input a list or tuple of points")
        Entering("PathAddPoints(%d points)" % len(points))
        for point in points:
            if not isinstance(point, tuple) and len(point) != 2:
                raise gException("Point must be a tuple of two numbers")
            x = float(point[0])
            y = float(point[1])
            PathAddPoint(x, y)
        Leaving()
    def PathAdd(o, object_type=path_point, move=no):
        '''Add a point, arc, or Bezier curve to the path.  If move is yes, we
        start a new subpath.
        '''
        Entering("PathAdd(%s)" % repr(o))
        global gs
        if not isinstance(o, tuple):
            raise gException("First parameter must be a tuple")
        if gs[g_current_path] == None:
            raise gException("No current path -- use NewPath() first")
        if object_type == path_point:
            if len(o) != 2:
                raise gException("A point must be a tuple of length 2")
            obj = go.Point(o[0], o[1])
        elif object_type == path_arc_ccw:
            if len(o) != 5:
                raise gException("An arc must be a tuple of length 5")
            obj = go.ArcCCW(o[0], o[1], o[2], o[3], o[4])
        elif object_type == path_arc_cw:
            if len(o) != 5:
                raise gException("An arc must be a tuple of length 5")
            obj = go.ArcCW(o[0], o[1], o[2], o[3], o[4])
        elif object_type == path_bezier:
            if len(o) != 6:
                raise gException("A Bezier curve must be a tuple of length 6")
            _CheckCurrentPoint()
            x0, y0 = gs[g_current_point]
            obj = go.Bezier(x0, y0, o[0], o[1], o[2], o[3], o[4], o[5])
        else:
            raise gException("Unrecognized type")
        g = gs[g_current_path]
        if move == yes and len(g.pathlist[0]) > 0:
            g.move()
        g.add(obj)
        Leaving()
    def PathMove(o, object_type):
        '''Add a new object, but start a new subpath (leaving the old one open).
        '''
        Entering("PathMove(%s)" % repr(o))
        raise NotImplemented()
        Leaving()
    def PathClose():
        Entering("PathClose")
        p = gs[g_current_path]
        if p == None:
            raise gException("No current path")
        p.close()
        Leaving()
    def NewPath():
        Entering("NewPath")
        global gs
        gs[g_current_path] = go.Path()
        Leaving()
    def GetPath():
        # Returns a copy of the current path
        import copy
        Entering("GetPath")
        Leaving()
        return copy.deepcopy(gs[g_current_path])
    def SetPath(p):
        Entering("SetPath")
        global gs
        if not isinstance(p, go.Path):
            raise gException("Not a path")
        gs[g_current_path] = p
        Leaving()
    def DrawPath(path=None):
        '''path can be two types:  a path object or a tuple containing
        information about an elliptical arc to fill.  The data in the tuple
        are: (str, ((xll, yll), (xur, yur))) where str contains the ellipse
        parameters.  The remaining tuple contains a pair of points
        representing the lower left and upper right points of the bounding
        box.
        '''
        global gs
        if path == None:
            path = gs[g_current_path]
            Entering("DrawPath:  using current path")
            if path == None:
                raise gException("No current path")
        else:
            Entering("DrawPath:  using passed-in path")
        if isinstance(path, tuple):
            is_ellipse = yes
            str = path[0]
            bb  = path[1]
        else:
            is_ellipse = no
            if not isinstance(path, go.Path):
                raise gException("Not a path")
        if gs[g_line].on == no:
            Leaving()
            return
        _Color(gs[g_line].color)
        if is_ellipse == yes:
            out("newpath " + str)
        else:
            path.setPath(out)
        gs[g_line].update(out)
        out("stroke\n")
        gs[g_current_path] = None
        Leaving()
    def FillPath(p=None):
        Entering("FillPath")
        _FillPath(p, "fill")
        Leaving()
    def EoFillPath(p=None):
        Entering("EoFillPath")
        _FillPath(p, "eofill")
        Leaving()
if 1:   # Utility & debugging functions
    def DebugOn():
        global debugging
        debugging = yes
        Entering("DebugOn")
        Leaving()
    def DebugOff():
        Entering("DebugOff")
        global debugging
        debugging = no
        Leaving()
    def TraceOn():
        global tracing
        tracing = yes
        Entering("TraceOn")
        Leaving()
    def TraceOff():
        Entering("TraceOff")
        global tracing
        tracing = no
        Leaving()
    def Entering(str):
        if tracing == yes:
            global trace_indent
            assert(trace_indent >= 0)
            s = " " * trace_indent
            trace_stream.write(s + str + "\n")
            trace_indent += trace_indent_incr
    def Leaving():
        if tracing == yes:
            global trace_indent
            trace_indent = max(trace_indent - trace_indent_incr, 0)
    def DumpGS():
        '''Print the graphics state to stdout; useful for debugging.
        '''
        Entering("DumpGS")
        # Invert the global symbol dictionary
        g = globals()
        gk = g.keys()
        sym = {}
        for key in gk:
            if not isinstance(g[key], Int):
                continue
            sym[g[key]] = key
        # Now sym contains the variable names as the keys and the integer
        # identifiers as the values.
        keys = gs.keys()
        debug_stream.write("Graphics state:\n")
        for key in sorted(keys):
            number = key
            symbol = sym[number]
            value  = gs[number]
            if not isinstance(symbol, String):
                continue
            debug_stream.write("  %-20s %d:   %s\n" % (symbol, number,
                                repr(value)))
        Leaving()
    def hsv2rgb(H, S, V):
        Entering("hsv2rgb(%s, %s, %s)" % (_f(H), _f(S), _f(V)))
        c = go.Color(black)
        c.setHSV(H, S, V)
        Leaving()
        return c.getRGB()
    def rgb2hsv(color):
        '''color is expected to be a tuple of 3 floats.
        '''
        if not isinstance(color, tuple) and len(color) != 3:
            raise gException("You must pass in a color tuple")
        Entering("rgb2hsv(%s)" % go.Color(color).colorName())
        c = go.Color(color)
        Leaving()
        return c.getHSV()
if 1:   # Utility functions that don't need to be called by the user
    def _maxmin(a, b, c):
        '''Return a tuple of the maximum and minimum of the three values.
        '''
        return (max(a, b, c), min(a, b, c))
    def _SetDefaultGraphicsState():
        import copy
        global gs
        gs = copy.deepcopy(gs_default)
    def _SetStateFromGS(new_page=no):
        '''Output the necessary Postscript to set the current Postscript
        environment from this module's graphics state.  If a new page is
        indicated, set the orientation and units from the gs dictionary's
        values; default to portrait and inches.
        '''
        Entering("_SetStateFromGS(new_page=%s)" % INV[new_page])
        global gs
        out("initmatrix ")
        str = ""
        if new_page == yes:
            gs[g_ctm] = (1, 0, 0, 1, 0, 0)
            orientation_obj = gs[g_orientation]
            orientation = orientation_obj.orientation
            rotation_angle = allowed_orientations[orientation]
            width, height = paper_sizes[gs[g_paper_size].size]  # In points
            rotate(rotation_angle)
            if orientation == portrait:
                pass   # Don't need to do anything
            elif orientation == landscape:
                translate(-height, 0)
            elif orientation == inversePortrait:
                translate(-width, -height)
            elif orientation == seascape:
                translate(0, -width)
            else:
                raise gException("Unrecognized orientation")
            if gs[g_units] != None:
                units = allowed_units[gs[g_units]]
                # reset=yes means to set the sizes to the defaults before scaling
                scale(units, units, reset=yes)  
        else:
            # Set via the CTM
            a, b, c, d, e, g = gs[g_ctm]
            str = "[ %s %s %s %s %s %s ] " % \
                (_f(a), _f(b), _f(c), _f(d), _f(e), _f(g))
            str = str + "concat "
        gs[g_line].update(out)
        if gs[g_current_clip_path] != None:
            gs[g_current_clip_path].setpath()
        Leaving()
    def _Color(color):
        '''We'll send out a Postscript color command only if the passed-in
        color object doesn't match the current color object.
        '''
        global gs
        if color.color == gs[g_current_color].color:
            Entering("_Color:  no color change needed")
            Leaving()
            return
        color.update(out)
        Entering("_Color:  color changed to %s" % color.colorName())
        gs[g_current_color] = color
        Leaving()
    def _Line_cap():
        Entering("_Line_cap")
        out("%d setlinecap\n" % line_caps[gs[g_line_cap]])
        Leaving()
    def _Line_join():
        Entering("_Line_join")
        out("%d setlinejoin\n" % line_joins[gs[g_line_join]])
        Leaving()
    def _Clipping():
        Entering("_Clipping")
        if gs[g_current_path] == None:
            Leaving()
            return
        _Update[g_current_path]()
        out("clip\n")
        Leaving()
    def _Current_point():
        Entering("_Current_point")
        x, y = gs[g_current_point]
        out("%s %s moveto\n" % (_f(x), _f(y)))
        Leaving()
    def _RoundRect(w, h, r):
        Entering("_RoundRect")
        _CheckCurrentPoint()
        x, y = gs[g_current_point]
        out("newpath %s %s moveto %s %s lineto" % (x+r, y, x+w-r, y))
        out(" %s %s %s 270 360 arc" % (x+w-r, y+r,   r))
        out(" %s %s lineto "        % (x+w,   y+h-r))
        out(" %s %s %s 0 90 arc"    % (x+w-r, y+h-r, r))
        out(" %s %s lineto"         % (x+r,   y+h))
        out(" %s %s %s 90 180 arc"  % (x+r,   y+h-r, r))
        out(" %s %s lineto"         % (x,     y+r))
        out(" %s %s %s 180 270 arc" % (x+r,   y+r,   r))
        Leaving()
    def _CheckCurrentPoint():
        if gs[g_current_point] == None:
            raise gException("Current point undefined")
        x = _f(gs[g_current_point][0])
        y = _f(gs[g_current_point][1])
        Entering("_CheckCurrentPoint (is (%s, %s))" % (x, y))
        Leaving()
    def _ConstantTable(stream):
        '''Print out a table of the constants
        '''
        g = globals()
        table     = {}
        # Invert the global dictionary
        for key in g.keys():
            if isinstance(g[key], Int) and g[key] >= 1000:
                table[g[key]] = key
        constants = table.keys()
        constants.sort()
        for c in constants:
            stream.write("%-35s %d\n" % (table[c], c))
    def _Rotation(x, y, theta):
        '''Convenience function to return a tuple of (x', y') of (x, y)
        rotated by an angle of theta degrees.
        '''
        from math import sin, cos, pi
        t = theta*pi/180
        s = sin(t)
        c = cos(t)
        return (x*c + y*s, -x*s + y*c)
    def _FillPath(path, type_of_PS_fill="fill"):
        '''path can be two types:  a path object or a tuple containing
        information about an elliptical arc to fill.  The data in the tuple
        are: (str, ((xll, yll), (xur, yur))) where str contains the ellipse
        parameters.  The remaining tuple contains a pair of points
        representing the lower left and upper right points of the bounding
        box.
        '''
        if path == None:
            path = gs[g_current_path]
            Entering("_FillPath:  using current path")
            if path == None:
                raise gException("No current path")
        else:
            Entering("_FillPath:  using passed-in path")
        if isinstance(path, tuple):
            str = path[0]
            bb  = path[1]
            is_ellipse = yes
        else:
            is_ellipse = no
            if not isinstance(path, go.Path):
                raise gException("Not a path")
        if gs[g_fill].on == no:
            Leaving()
            return
        if gs[g_fill].type == solid_fill:
            _Color(gs[g_fill].color)
            if is_ellipse == no:
                path.setPath(out)
                out(type_of_PS_fill + "\n")
            else:
                out("newpath " + str + " flattenpath fill\n")
        elif gs[g_fill].type == line_fill:
            _LineFillRegion(path)
        elif gs[g_fill].type == gradient_fill:
            _GradientFillRegion(path)
        else:
            raise gException("Unrecognized fill type")
        gs[g_current_path] = None
        Leaving()
    def _LineFillRegion(path):
        '''This routine fills the interior of a region with the current fill
        line.  We set the path and clip to it.  Then we position a
        coordinate system at the lower left corner of the bounding box and
        rotate the required line angle.  We then draw lines from (-r, y) to
        (r, y) for each required y value; r is the diagonal length of the
        bounding box; this guarantees we'll cover the original clipping
        region.
    
        See _FillPath() for a description of the incoming path parameter
        (it can be a tuple (ellipse) or Path object).
        '''
        Entering("_LineFillRegion")
        from math import sqrt
        g = gs[g_fill]
        phase      = g.phase
        separation = g.separation
        theta      = g.angle
        if separation == 0:
            # Default is to use a multiple of the line width
            separation = 10 * g.line.width[g_value]
        push()
        if isinstance(path, tuple):
            # Elliptical arc case
            str = path[0]
            bb  = path[1]
            out("newpath " + str + " flattenpath clip newpath ")
        else:
            # path is a path
            clip(path)
            bb = path.GetBBox()
        x_origin, y_origin = bb[0][0], bb[0][1]
        # The upper right corner of bb after the translation to the new origin
        xb, yb = bb[1][0] - x_origin, bb[1][1] - y_origin
        translate(x_origin, y_origin)
        rotate(theta)
        r = sqrt(xb*xb + yb*yb)  # Length of the bounding box's diagonal
        # Ready to draw lines; set up with proper line characteristics
        _Color(g.color)
        g.line.update(out)
        # Draw the lines above the origin
        y = 0 + phase
        while y <= r:
            s = (_f(-r), _f(y), _f(r), _f(y))
            out("%s %s moveto %s %s lineto stroke\n" % s)
            y = y + separation
        # Draw the lines below the origin
        y = 0 + phase - separation
        while y >= -r:
            s = (_f(-r), _f(y), _f(r), _f(y))
            out("%s %s moveto %s %s lineto stroke\n" % s)
            y = y - separation
        pop()
        Leaving()
    def DumpNamespace(stream, remove_colors=no, remove_fonts=no):
        '''Prints a sorted list of symbols in the global namespace.  Remove
        names that begin with "_".  Also print the object's value.
        '''
        g = globals()
        List = []
        for key in g.keys():
            if key[0] != "_":
                List.append(key)
        List.sort()
        for item in List:
            obj = eval(compile("%s" % item, "", "eval"))
            if remove_colors == yes:
                if isinstance(obj, tuple) and len(obj) == 3:
                    continue # It's a color
            if remove_fonts == yes and isinstance(obj, Int):
                if obj in allowed_font_names:
                    continue # It's a font name
            if isinstance(obj, types.DictType):
                obj_type = "Dictionary"
            elif isinstance(obj, list):
                obj_type = "List"
            elif isinstance(obj, String):
                obj_type = "String"
            elif isinstance(obj, tuple) and len(obj) == 3:
                obj_type = "Color (%s, %s, %s)" % tuple(map(_f, obj))
            elif isinstance(obj, Int):
                if obj in allowed_font_names:
                    obj_type = repr(obj) + " (font name)"
                else:
                    obj_type = repr(obj)
            else:
                obj_type = repr(obj)
            stream.write("%-30s %s\n" % (item, obj_type))
    def _GradientFillRegion(path):
        '''We'll fill the passed-in path with a gradient.  To do this, we
        do a gsave and set the clipping region with the path, then set the
        path.  We then draw thin rectangles rotated at the proper angle
        that interpolate between the two gradient colors.  The methods we
        use are device dependent in the sense that the number of boxes and
        their separation is determined by the current units.  If the
        current units are unrecognized (e.g., the user has anisotropically
        scaled the coordinate system), we make a best guess from the CTM.
        The tension is between providing too many boxes (and bloating the
        output stream) and not providing enough boxes, making the printed
        transition too discrete.
    
        See _FillPath() for a description of the incoming path parameter.
        '''
        global gs
        Entering("_GradientFillRegion")
        from math import sqrt
        push()
        if isinstance(path, tuple):
            # Elliptical arc case
            str = path[0]
            bb  = path[1]
            out("newpath " + str + " flattenpath clip newpath ")
        else:
            # path is a path
            clip(path)
            bb = path.GetBBox()
        x_origin, y_origin = float(bb[0][0]), float(bb[0][1])
        # The upper right corner of bb after the translation to the new origin
        xb, yb = bb[1][0] - x_origin, bb[1][1] - y_origin
        translate(x_origin, y_origin)
        theta = gs[g_fill].gradient_angle
        rotate(gs[g_fill].gradient_angle)
        r = sqrt(xb*xb + yb*yb)  # Length of the bounding box's diagonal
    
        # Get the y limits of where we should draw boxes in the rotated
        # coordinate system.  The box at y0 will be drawn with the gradient
        # (bottom) color and the box at y1 will be drawn with the current
        # fill color.
        if     0 <= theta and theta <  90:
            x, y0 = _Rotation(xb, 0, theta)
            x, y1 = _Rotation(0, yb, theta)
        elif  90 <= theta and theta < 180:
            x, y0 = _Rotation(xb, yb, theta)
            y1    = 0
        elif 180 <= theta and theta < 270:
            x, y0 = _Rotation(0, yb, theta)
            x, y1 = _Rotation(xb, 0, theta)
        elif 270 <= theta and theta < 360:
            y0    = 0
            x, y1 = _Rotation(xb, yb, theta)
        else:
            raise gException("Internal error:  theta not in range 0 to 360")
        height = y1 - y0  # Height of the rotated box we'll draw short boxes in
    
        top_color    = gs[g_fill].color
        bottom_color = gs[g_fill].gradient_color
    
        # Calculate how many boxes to draw.  This is empirically found by
        # what looks good on my printer.  You may want to modify the
        # points_per_box value to get acceptable appearance on your printer.
    
        points_per_box = 3.6  # Gives a box every 0.05 inches on paper
        a, b, c, d, e, f = gs[g_ctm]
        # Transform (r, height) back to the original dimensions in points
        x = a*r + b*height + e
        y = c*r + d*height + f
        if x > y:
            distance = x
        else:
            distance = y
        # Now distance contains the largest dimension in points
        factor = gs[g_fill].gradient_factor
        num_boxes = int(factor*float(distance)/points_per_box)
        if tracing == yes:
            s = " " * trace_indent
            trace_stream.write(s + "num_boxes = %d\n" % num_boxes)
        top_color    = gs[g_fill].color
        bottom_color = gs[g_fill].gradient_color
        LineOff()
        FillOn()
    
        # We need solid fills temporarily so we can call _FillPath() and not
        # get infinite recursion.
        gs[g_fill].type = solid_fill
    
        # Also keep track of current solid fill color so we can reset it.  We
        # need to set it to the current box's color because _Color() needs it.
        fill_color = gs[g_fill].color
    
        # Now draw boxes of height dy from y=y0 to y=y1.  To make sure we cover
        # the region, the boxes will have x coordinates from -r to r.
        dy = height/num_boxes
        for i in range(num_boxes):
            t = float(i)/num_boxes  # Color interpolating parameter 0 <= t <= 1
            y = y0 + t * height
            gs[g_fill].color = bottom_color.interp(top_color, t)
            # Construct a new rectangle path
            NewPath()
            PathAddPoint(-r, y)
            PathAddPoint(r, y)
            PathAddPoint(r, y+dy)
            PathAddPoint(-r, y+dy)
            PathClose()
            p = GetPath()
            _FillPath(p)
        pop()
        # Restore our incoming state
        gs[g_fill].type = gradient_fill
        gs[g_fill].color = fill_color
        Leaving()
if 1:   # Symbol naming
    # The original symbols were mixed camel case, but I prefer regular
    # camel case today.
    mixed = '''
        clipRectangle debugOff debugOn drawPath ellipticalArc
        eoFillPath fillColor fillOff fillOn fillPath fillType getPath
        gradientFill lineCap lineColor lineFill lineFillType
        lineFillWidth lineJoin lineOff lineOn lineType lineWidth
        newPage newPath pathAdd pathAddPoint pathAddPoints pathClose
        pathMove regularPolygon roundedRectangle scaleDash
        scaleDashAutomatically scaleLineWidth scaleTextSize setColor
        setGS setOrientation setPageSize setPath textCircle textColor
        textFraction textLines textName textPath textSize traceOff
        traceOn'''.split()
    for old in mixed:
        new = old[0].upper() + old [1:]
        exec(f"{old} = {new}")
if 1:   # Miscellaneous
    def tst():
        '''Utility function for a quick test file.  This should produce a
        filled annulus; the fill is a gradient from blue to pink and the
        label inside the annulus is in yellow text along a circle.
        '''
        stream = open("a.ps", "w")
        ginitialize(stream, wrap_in_PJL=no)
        SetOrientation(portrait, mm)
        LineOff()
        # Draw a gradient-filled rectangle
        FillOn()
        FillType(gradient_fill)
        FillColor(navy)
        GradientFill(pink, 45)
        move(72, 200)
        circle(130)
        FillType(solid_fill)
        FillColor(white)
        circle(40)
        TextName(SansBold)
        TextColor(yellow)
        TextSize(10)
        TextCircle("Example of gradient fill", 85, inside=no)
        gclose()
    def SetUp(file, orientation=portrait, units=mm):
        '''Convenience function to set up the drawing environment and return
        the output stream.
        '''
        stream = open(file, "w")
        ginitialize(stream)
        SetOrientation(orientation, units)
        return stream
    Setup = SetUp
    class Monitor(object):
        '''This class is used solely to check the push_count variable at
        exit.
        '''
        def __del__(self):
            if push_count:
                print("Warning:  push count is %d" % push_count)
    monitor = Monitor()
