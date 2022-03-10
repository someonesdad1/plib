'''This prints a scale that can be used to calibrate your printer.
By printing the scales, you can measure the physical printing limits
of your printer.  This assumes letter size paper and inches.
'''
from g import *
def DrawScaleTickMarks(y0, y1, spacing=0.02, major=5):
    assert y1 > y0
    assert spacing > 0
    assert major > 1
    width = 0.025
    num_marks = abs(int((y0 - y1) / spacing))
    d = float(y1 - y0) / num_marks
    for ix in range(num_marks):
        y = y0 + ix * d
        if ix % major == 0:
            line(-2 * width, y, 2 * width, y)
        else:
            line(-width, y, width, y)
def PaperScale(file):
    s = Setup(file, portrait, inches)
    lineWidth(0.001)
    width = 8.5
    height = 11.0
    text_size = 0.15
    x_text = -3.5
    y_text = 4.5
    line(width / 2, 0, width / 2, height)
    line(0, height / 2, width, height / 2)
    textSize(text_size)
    # Put origin at center of page
    translate(width / 2, height / 2)
    y0 = height / 2.0 - 0.5
    y1 = y0 + 1.0
    x0 = width / 2.0 - 0.5
    x1 = x0 + 1.0
    # Label the drawing
    move(x_text, y_text)
    text("Top left of page")
    move(x_text, y_text - text_size)
    text("x start position from origin = %g inches" % x0)
    move(x_text, y_text - 2 * text_size)
    text("y start position from origin = %g inches" % y0)
    # Draw the axis marks
    DrawScaleTickMarks(y0, y1)
    rotate(90)
    DrawScaleTickMarks(x0, x1)
    rotate(90)
    DrawScaleTickMarks(y0, y1)
    rotate(90)
    DrawScaleTickMarks(x0, x1)
    s.close()
PaperScale("out/paper_scale.ps")
