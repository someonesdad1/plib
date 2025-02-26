"""
Print out the frequency of musical notes

    The data came from the table at
    https://en.wikipedia.org/wiki/Scientific_pitch_notation.

    Data from web page (tab-delimited):

    Octaves range from 0 to 10
    Number in parentheses is semitones above or below middle C
    CD means C sharp or D flat

    C 	16.352 (−48) 	32.703 (−36) 	65.406 (−24) 	130.81 (−12) 	261.63 (0) 	523.25 (+12) 	1046.5 (+24) 	2093.0 (+36) 	4186.0 (+48) 	8372.0 (+60) 	16744.0 (+72)
    CD 	17.324 (−47) 	34.648 (−35) 	69.296 (−23) 	138.59 (−11) 	277.18 (+1) 	554.37 (+13) 	1108.7 (+25) 	2217.5 (+37) 	4434.9 (+49) 	8869.8 (+61) 	17739.7 (+73)
    D 	18.354 (−46) 	36.708 (−34) 	73.416 (−22) 	146.83 (−10) 	293.66 (+2) 	587.33 (+14) 	1174.7 (+26) 	2349.3 (+38) 	4698.6 (+50) 	9397.3 (+62) 	18794.5 (+74)
    ED 	19.445 (−45) 	38.891 (−33) 	77.782 (−21) 	155.56 (−9) 	311.13 (+3) 	622.25 (+15) 	1244.5 (+27) 	2489.0 (+39) 	4978.0 (+51) 	9956.1 (+63) 	19912.1 (+75)
    E 	20.602 (−44) 	41.203 (−32) 	82.407 (−20) 	164.81 (−8) 	329.63 (+4) 	659.26 (+16) 	1318.5 (+28) 	2637.0 (+40) 	5274.0 (+52) 	10548.1 (+64) 	21096.2 (+76)
    F 	21.827 (−43) 	43.654 (−31) 	87.307 (−19) 	174.61 (−7) 	349.23 (+5) 	698.46 (+17) 	1396.9 (+29) 	2793.8 (+41) 	5587.7 (+53) 	11175.3 (+65) 	22350.6 (+77)
    FG 	23.125 (−42) 	46.249 (−30) 	92.499 (−18) 	185.00 (−6) 	369.99 (+6) 	739.99 (+18) 	1480.0 (+30) 	2960.0 (+42) 	5919.9 (+54) 	11839.8 (+66) 	23679.6 (+78)
    G 	24.500 (−41) 	48.999 (−29) 	97.999 (−17) 	196.00 (−5) 	392.00 (+7) 	783.99 (+19) 	1568.0 (+31) 	3136.0 (+43) 	6271.9 (+55) 	12543.9 (+67) 	25087.7 (+79)
    GA 	25.957 (−40) 	51.913 (−28) 	103.83 (−16) 	207.65 (−4) 	415.30 (+8) 	830.61 (+20) 	1661.2 (+32) 	3322.4 (+44) 	6644.9 (+56) 	13289.8 (+68) 	26579.5 (+80)
    A 	27.500 (−39) 	55.000 (−27) 	110.00 (−15) 	220.00 (−3) 	440.00 (+9) 	880.00 (+21) 	1760.0 (+33) 	3520.0 (+45) 	7040.0 (+57) 	14080.0 (+69) 	28160.0 (+81)
    AB 	29.135 (−38) 	58.270 (−26) 	116.54 (−14) 	233.08 (−2) 	466.16 (+10) 	932.33 (+22) 	1864.7 (+34) 	3729.3 (+46) 	7458.6 (+58) 	14917.2 (+70) 	29834.5 (+82)
    B 	30.868 (−37) 	61.735 (−25) 	123.47 (−13) 	246.94 (−1) 	493.88 (+11) 	987.77 (+23) 	1975.5 (+35) 	3951.1 (+47) 	7902.1 (+59) 	15804.3 (+71) 	31608.5 (+83)

"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Print out the frequency of musical notes
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import os
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    nl = "\n"
    tab = "\t"
    raw_data = dedent("""
    C 	16.352 (-48) 	32.703 (-36) 	65.406 (-24) 	130.81 (-12) 	261.63 (0) 	523.25 (+12) 	1046.5 (+24) 	2093.0 (+36) 	4186.0 (+48) 	8372.0 (+60) 	16744.0 (+72)
    CD 	17.324 (-47) 	34.648 (-35) 	69.296 (-23) 	138.59 (-11) 	277.18 (+1) 	554.37 (+13) 	1108.7 (+25) 	2217.5 (+37) 	4434.9 (+49) 	8869.8 (+61) 	17739.7 (+73)
    D 	18.354 (-46) 	36.708 (-34) 	73.416 (-22) 	146.83 (-10) 	293.66 (+2) 	587.33 (+14) 	1174.7 (+26) 	2349.3 (+38) 	4698.6 (+50) 	9397.3 (+62) 	18794.5 (+74)
    DE 	19.445 (-45) 	38.891 (-33) 	77.782 (-21) 	155.56 (-9) 	311.13 (+3) 	622.25 (+15) 	1244.5 (+27) 	2489.0 (+39) 	4978.0 (+51) 	9956.1 (+63) 	19912.1 (+75)
    E 	20.602 (-44) 	41.203 (-32) 	82.407 (-20) 	164.81 (-8) 	329.63 (+4) 	659.26 (+16) 	1318.5 (+28) 	2637.0 (+40) 	5274.0 (+52) 	10548.1 (+64) 	21096.2 (+76)
    F 	21.827 (-43) 	43.654 (-31) 	87.307 (-19) 	174.61 (-7) 	349.23 (+5) 	698.46 (+17) 	1396.9 (+29) 	2793.8 (+41) 	5587.7 (+53) 	11175.3 (+65) 	22350.6 (+77)
    FG 	23.125 (-42) 	46.249 (-30) 	92.499 (-18) 	185.00 (-6) 	369.99 (+6) 	739.99 (+18) 	1480.0 (+30) 	2960.0 (+42) 	5919.9 (+54) 	11839.8 (+66) 	23679.6 (+78)
    G 	24.500 (-41) 	48.999 (-29) 	97.999 (-17) 	196.00 (-5) 	392.00 (+7) 	783.99 (+19) 	1568.0 (+31) 	3136.0 (+43) 	6271.9 (+55) 	12543.9 (+67) 	25087.7 (+79)
    GA 	25.957 (-40) 	51.913 (-28) 	103.83 (-16) 	207.65 (-4) 	415.30 (+8) 	830.61 (+20) 	1661.2 (+32) 	3322.4 (+44) 	6644.9 (+56) 	13289.8 (+68) 	26579.5 (+80)
    A 	27.500 (-39) 	55.000 (-27) 	110.00 (-15) 	220.00 (-3) 	440.00 (+9) 	880.00 (+21) 	1760.0 (+33) 	3520.0 (+45) 	7040.0 (+57) 	14080.0 (+69) 	28160.0 (+81)
    AB 	29.135 (-38) 	58.270 (-26) 	116.54 (-14) 	233.08 (-2) 	466.16 (+10) 	932.33 (+22) 	1864.7 (+34) 	3729.3 (+46) 	7458.6 (+58) 	14917.2 (+70) 	29834.5 (+82)
    B 	30.868 (-37) 	61.735 (-25) 	123.47 (-13) 	246.94 (-1) 	493.88 (+11) 	987.77 (+23) 	1975.5 (+35) 	3951.1 (+47) 	7902.1 (+59) 	15804.3 (+71) 	31608.5 (+83)
    """)
    data = {}
    for i in raw_data.split(nl):
        i = i.replace("(", "").replace(")", "")
        a = i.split(tab)
        name = a[0].strip()
        del a[0]
        data[name] = []
        for j in a:
            freq, semitones = j.split()
            freq = float(freq)
            if int(freq) == freq:
                freq = int(freq)
            semitones = int(semitones)
            data[name].append((freq, semitones))


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] [note1 [note2 ...]]
      Print out the frequency in Hz of a given note.  Note can be either a
      single letter or a letter and a number, the number denoting the
      octave.  The flat and sharp frequencies are given if they exist.
    Options:
      -i    Round frequencies to integer Hz
      -t    Print the whole table
      -u    Use Unicode for sharp and flat symbols
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-i"] = False  # Round to integer Hz
    d["-t"] = False  # Print table
    d["-u"] = False  # Use Unicode for sharp & flat symbols
    try:
        opts, notes = getopt.getopt(sys.argv[1:], "itu")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in "itu":
            d[o] = not d[o]
    if d["-t"]:
        PrintTable(d)
    if not notes:
        Usage(d)
    return notes


def PrintTable(d):
    sharp, flat, sz = "s", "f", 8
    if d["-u"]:
        sharp, flat = chr(0x266F), chr(0x266D)
    print("Frequencies in Hz")
    print(" " * 48, "Octave")
    print("    ", end="")
    for octave in range(11):
        o = " " * 3 + str(octave)
        print("{:^{}s} ".format(o, sz), end="")
    print()
    for note in "C CD D DE E F FG G GA A AB B".split():
        if len(note) == 1:
            print("{:5s} ".format(note), end="")
        else:
            print("{}{}/{}{} ".format(note[0], sharp, note[1], flat), end="")
        for freq, semitone in data[note]:
            if d["-i"]:
                freq = int(round(freq, 0))
            print("{:^{}s}".format(str(freq), sz), end=" ")
        print()
    exit()


def PrintNote(Note, d):
    note, octaves, notes = Note.upper(), range(11), set("ABCDEFG")
    if len(note) == 1:
        if note not in "ABCDEFG":
            Error("'{}' not a recognized note".format(Note))
        freqs = data[note]
        print(note)
        print("    Octave    Hz         Semitones from C4")
        for octave in octaves:
            freq, semitones = freqs[octave]
            if d["-i"]:
                freq = int(round(freq, 0))
            st = str(semitones)
            if st[0] != "-":
                st = " " + st
            print("     {:2d}       {:10s}       {}".format(octave, str(freq), st))
    elif len(note) == 2:
        try:
            octave = int(note[1])
        except ValueError:
            Error("'{}' not a recognized octave number".format(octave))
        note = note[0]
        if note not in notes:
            Error("'{}' not a recognized note".format(Note))
        if octave not in octaves:
            Error("Octave number must be 0 to 10.".format(octave))
        print(note, "octave", octave)
    else:
        Error("The note must be one or two characters.")


if __name__ == "__main__":
    d = {}  # Options dictionary
    notes = ParseCommandLine(d)
    for note in notes:
        PrintNote(note, d)
