'''
Show the alphabets in some different fonts.  We put similar fonts next
to each other for comparison.  Since I only have access to a LaserJet
4050, these fonts work on my printer -- they may not work on yours.
'''
import sys
from g import *
x = 2.3  # offset
font_list = (
    (AntiqueOlive, "AntiqueOlive", x),
    (Arial, "Arial", x),
    (Helvetica, "Helvetica", x),
    (UniversMedium, "UniversMedium", x),
    (HelveticaNarrow, "HelveticaNarrow", x),
    (UniversCondensedMedium, "UniversCondensedMedium", x),
    (AntiqueOliveBold, "AntiqueOliveBold", x),
    (ArialBold, "ArialBold", x),
    (HelveticaBold, "HelveticaBold", x),
    (UniversBold, "UniversBold", x),
    (AntiqueOliveItalic, "AntiqueOliveItalic", x),
    (ArialItalic, "ArialItalic", x),
    (HelveticaOblique, "HelveticaOblique", x),
    (UniversMediumItalic, "UniversMediumItalic", x),
    (ArialBoldItalic, "ArialBoldItalic", x),
    (HelveticaBoldOblique, "HelveticaBoldOblique", x),
    (UniversBoldItalic, "UniversBoldItalic", x),
    (HelveticaNarrowBold, "HelveticaNarrowBold", x),
    (UniversCondensedBold, "UniversCondensedBold", x),
    (HelveticaNarrowOblique, "HelveticaNarrowOblique", x),
    (UniversCondensedMediumItalic, "UniversCondensedMediumItalic", x),
    (HelveticaNarrowBoldOblique, "HelveticaNarrowBoldOblique", x),
    (UniversCondensedBoldItalic, "UniversCondensedBoldItalic", x),
    (AlbertusMedium, "AlbertusMedium", x),
    (GaramondAntiqua, "GaramondAntiqua", x),
    (Times, "Times", x),
    (AlbertusExtraBold, "AlbertusExtraBold", x),
    (TimesBold, "TimesBold", x),
    (GaramondHalbfett, "GaramondHalbfett", x),
    (TimesItalic, "TimesItalic", x),
    (GaramondKursiv, "GaramondKursiv", x),
    (GaramondKursivHalbfett, "GaramondKursivHalbfett", x),
    (TimesBoldItalic, "TimesBoldItalic", x),
    (Coronet, "Coronet", x),
    (Marigold, "Marigold", x),
    (Courier, "Courier", x),
    (CourierBold, "CourierBold", x),
    (CourierBoldItalic, "CourierBoldItalic", x),
    (CourierItalic, "CourierItalic", x),
    (Symbol, "Symbol", x),
    (Dingbats, "Dingbats", x),
)
def FontGallery1(file):
    # This is the original version with fonts all across the page.
    s = Setup(file, landscape, inches)
    lineWidth(0.01)
    # Set margins
    translate(0.3, 0.3)
    line_spacing = 0.195
    textSize(0.19)
    alphabet = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet = alphabet + "0123456789,./?'\";:][}[\\|=+-_)(*&^%$#@!`~"
    for i in range(len(font_list)):
        font_id = font_list[i][0]
        font_name = font_list[i][1]
        spacing = font_list[i][2]
        textName(font_id)
        move(0, i * line_spacing)
        push()
        if font_id == Symbol or font_id == Dingbats:
            # Change the font so we can read the name
            textName(Arial)
        text("%s" % font_name)
        pop()
        move(spacing, i * line_spacing)
        push()
        textName(font_id)
        text("%s" % alphabet)
        pop()
    s.close()
def FontGallery2(file):
    # This version only prints all the letters for dingbats and symbol.
    s = SetUp(file, landscape, inches)
    line_spacing = 0.2
    fh = 0.2
    textSize(fh)
    #
    push()
    translate(0.3, 0.3)
    for i, item in enumerate(font_list):
        font_id, font_name, spacing = item
        if font_id in (Symbol, Dingbats):
            continue
        textName(font_id)
        move(0, i * line_spacing)
        push()
        text("%s" % font_name)
        pop()
    # Title the fonts
    move(0, 7.8)
    textName(HelveticaBold)
    text("Text size = %.1f inches" % fh)
    pop()
    #
    alphabet = "abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphabet = alphabet + "0123456789,./?'\";:][}[\\|=+-_)(*&^%$#@!`~"
    # Now plot a symbol table of Symbol and Dingbat fonts
    translate(3.0, 7.75)
    push()
    move(3.7, 1.2 * fh)
    textSize(1.5 * fh)
    ctext("Symbol and Dingbat characters")
    pop()
    x, y = 0, 0
    dx, dy = 5.5 * fh, -1.2 * fh
    offset = 33
    numrows = 32
    for i in range(128 if pyver == 3 else 256):
        if i and i % numrows == 0:
            x, y = dx * (i // numrows), 0
        j = i + offset
        if j > 255:
            break
        move(x, y + (i % numrows) * dy)
        textName(Courier)
        text("%03d " % j)
        textName(Symbol)
        c = chr(j) + "   "
        text(c)
        textName(Dingbats)
        text(c)
    s.close()
FontGallery1("out/font_gallery1.ps")
FontGallery2("out/font_gallery2.ps")
