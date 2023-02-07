'''
Calculate readability statistics for a set of files
 
    I use this script to show me the Flesch-Kincaid grade level (FKGL) and
    the Flesch Reading Ease Score (FRES) for the text files on the command
    line.  My goal for FKGL for general writing is about 8 and for
    technical writing about 12 or less.
 
    Be cautious in applying the results of a program like this.  These
    readability scores are only rough guides.  They cannot measure many
    things that are relevant to reading comprehension.  If you don't
    believe this, randomly shuffle the words in each sentence of a
    document.  The documents will now be unintelligible, yet these
    readability scores will be unchanged.  These scores know nothing about
    semantics or syntax, the formatting/font of the text, how nice it's
    visually organized, or the background and motivation of the reader.
    These and other things are relevent to reading comprehension, yet are
    beyond the ken of a text-based computer program.
 
    One of Hemingway's secrets:  "I write one page of masterpiece to
    ninety-one pages of shit.  I try to put the shit in the wastebasket."
 
    Some good references:
        - Malcom Forbes, "How to Write a Business Letter"
        - Edward Thompson, "How to Write Clearly"
        - Kenneth Roman and Joel Raphaelson, "Writing that Works"
        - Strunk & White
        - Chicago Manual of Style
 
    Consult these excellent tools because you care both about the craft of
    writing and your readers.
'''
if 1:   # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2005, 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Calculate various readability statistics for a set of files.
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import getopt
        import math
        import os
        from pathlib import Path as P
        import re
        import sys
    if 1:   # Custom imports
        if 0:
            import debug
            debug.SetDebugger()
        from wrap import dedent
        from color import Color, TRM as t
        import get
        # Load a dictionary of number of syllables if available (otherwise,
        # the number of syllables in each word will be found by the function
        # GuessSyllables.  The words_syllables module contains two
        # dictionaries that greatly speed up getting the number of syllables
        # per word.  See the docstring.
        try:
            from words_syllables import syllables as S, multiple_syllables as MS
        except ImportError:
            pass
    if 1:   # Global variables
        ii = isinstance
        common_abbreviations = (
            "mr", "mrs", "ms", "dr", "no", "mssr", "st", "ave"
        )
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} file1 [file2...]
          Prints readability statistics for text files.  The number of '+'
          after the file name is ceil(log10(file_size)).  For example, if
          you see four + symbols, the file has between 1000 and 10000
          characters.
        '''))
        print(dedent(f'''
            FKGL = Flesch-Kincaid Grade Level     *
            FRES = Flesch-Kincaid Reading Ease (0-100, 100 easy)
          The following are also printed with -a:
            Fog  = Gunning Fog Index              *
            ARI  = Automated Readability Index    *
            CL   = Coleman-Liau Index             *
            SMOG = SMOG Index                     *
          * means a number that is a US grade level
        ''', n=6))
        print(dedent(f'''
        Options
          -a    Print all statistics
          -C    Print color key (also sets -c)
          -c    Colorize the statistics
          -d    Turn on debug printing (shows more data)
          -p    Print to one decimal place (integer is default)
          -t    Run self-tests
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Print all statistics
        d["-C"] = False     # Print color key
        d["-c"] = False     # Print in color
        d["-d"] = False     # Debug output
        d["-p"] = False     # Print to 1 decimal place
        d["-t"] = False     # Run self-tests
        try:
            opts, files = getopt.getopt(sys.argv[1:], "aCcdhpt", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("aCcdpt"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if d["-t"]:
            exit(SelfTests())
        if not files:
            Usage(1)
        if d["-C"]:
            d["-c"] = True
        GetColor()
        return files
    def Clamp(x, low, high):
        'Return a number on [low, high]'
        return min(max(low, x), high)
    def GetColor():
        t.easy = t("purl") if d["-c"] else ""
        t.std = t("grnl") if d["-c"] else ""
        t.med = t("yell") if d["-c"] else ""
        t.medhard = t("ornl") if d["-c"] else ""
        t.hard = t("redl") if d["-c"] else ""
        t.N = t.n if d["-c"] else ""
if 1:   # Testing
    def SelfTests():
        'Return 0 for pass, number of failures for fail'
        # Note:  the formulas written below were independently written from
        # the wikipedia web pages without looking at the script's
        # implementation.
        fail = 0
        p = P(sys.argv[0]).parent
        # This file's data came from "The Martian"
        file = p/"readability.txt"
        s = open(file).read()
        (characters, words, complex_words, one_syllable_words,
                syllables, sentences) = CountStats(s)
        #print(characters, words, complex_words, one_syllable_words, syllables, sentences)
        assert(characters == 2414)
        assert(words == 578)
        assert(complex_words == 38)
        assert(one_syllable_words == 414)
        assert(syllables == 791)
        assert(sentences == 55)
        # FKGL https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
        fkgl = FleschKincaidGradeLevel(words, syllables, sentences)
        expected = 0.39*words/sentences + 11.8*syllables/words - 15.59
        if fkgl != expected:
            fail += 1
        # Fog https://en.wikipedia.org/wiki/Gunning_fog_index
        fog = GunningFogIndex(words, sentences, complex_words)
        expected = 0.4*(words/sentences + 100*complex_words/words)
        if fog != expected:
            fail += 1
        # FRES https://en.wikipedia.org/wiki/Flesch%E2%80%93Kincaid_readability_tests
        fres = FleschReadingEaseScore(words, syllables, sentences)
        expected = 206.835 - 1.015*words/sentences - 84.6*syllables/words
        if fres != expected:
            fail += 1
        # ARI http://en.wikipedia.org/wiki/Automated_Readability_Index
        ari = AutomatedReadabilityIndex(characters, words, sentences)
        expected = 4.71*characters/words + 0.5*words/sentences - 21.43
        if ari != expected:
            fail += 1
        # CL http://en.wikipedia.org/wiki/Coleman-Liau_Index
        cl = ColemanLiauIndex(characters, words, sentences)
        expected = 0.0588*100*characters/words - 0.296*100*sentences/words - 15.8
        if cl != expected:
            fail += 1
        # SMOG http://en.wikipedia.org/wiki/SMOG_Index
        smog = SMOGIndex(complex_words, sentences)
        expected = 1.043*math.sqrt(complex_words*30/sentences) + 3.1291
        if smog != expected:
            fail += 1
        return fail
if 1:   # Core functionality
    def GuessSyllables(word):
        "Guess the number of syllables in a word"
        # Our basic way of guessing is to count the number of vowels
        # in a word.  We then subtract 1 for each dipthong we find,
        # and add 1 for anti-dipthongs (OK, that's probably not the
        # technical term).
        #
        # This function is from the pyflesch.py script written by Seb Bacon,
        # March 29, 2005,  You can find it at
        # http://freshmeat.net/projects/pyflesch/.  Update 10 Nov 2019:  This
        # URL is defunct.
        syl = 0
        subtract_syl = ['cial', 'tia', 'cius', 'cious', 'giu', 'ion', 'iou',
                        'sia$', '.ely$', 'ea.', 'oa.', 'enced$']
        add_syl = ['ia', 'riet', 'dien', 'iu', 'io', 'ii', '[aeiouym]bl$',
                '[aeiou]{3}', '^mc', 'ism$', '([^aeiouy])\1l$',
                '[^l]lien', '^coa[dglx].', '[^gq]ua[^auieo]', 'dnt$']
        word = word.lower()
        word = word.replace("'", "")    # fold contractions
        word = word.replace('"', "")    # remove quotes from around word
        word = re.sub("e$", "", word)
        spl = re.split("[^aeiouy]+", word)
        try:
            spl.remove("")
            spl.remove('')      # why do this twice?
        except ValueError:
            pass
        for rx in subtract_syl:
            if re.match(rx, word):
                syl -= 1
        for rx in add_syl:
            if re.match(rx, word):
                syl += 1
        if len(word) == 1:      # 'x'
            syl += 1
        syl += len(spl)
        return syl if syl else 1
    def Test_Syllable_function():
        '''22 Sep 2010 DP:  this function provides a check of the
        GuessSyllables function's output.  The word_syllables dictionary from
        words.py contains the number of syllables for each word in the
        dictionary; I believe I found this list of syllables from a CS-heavy
        school like CMU.  This function prints out the histogram of the (actual
        - predicted) number of syllables.  This gives the following results
        for the words.py file included with this script:
 
            -2 0.11%
            -1 6.54%
            0 83.56%
            1 9.36%
            2 0.39%
            3 0.04%
            4 0.01%
            5 0.00%
 
        The bottom line is that the GuessSyllables function is correct 84% of
        the time and only off by one syllable 16% of the time.  In my mind,
        this is excellent performance for a relatively simple algorithm.
        '''
        from words import word_syllables
        d, n = {}, len(word_syllables)
        for i in word_syllables:
            actual, calculated = word_syllables[i], GuessSyllables(i)
            diff = actual - calculated
            if diff in d:
                d[diff] += 1
            else:
                d[diff] = 1
        keys = d.keys()
        keys.sort()
        for i in keys:
            print(i, "%.2f%%" % (100.*d[i]/n))
    def GunningFogIndex(words, sentences, complex_words):
        ASL = words/sentences
        PCW = 100*complex_words/words
        fog = 0.4*(ASL + PCW)
        return Clamp(fog, 0, 9999)
    def AutomatedReadabilityIndex(characters, words, sentences):
        ari = 4.71*characters/words + 0.5*words/sentences - 21.43
        return Clamp(ari, 0, 9999)
    def ColemanLiauIndex(characters, words, sentences):
        CL = 0.0588*100*characters/words - 0.296*100*sentences/words - 15.8
        return Clamp(CL, 0, 9999)
    def FleschReadingEaseScore(words, syllables, sentences):
        fres = 206.835 - 1.015*words/sentences - 84.6*syllables/words
        # We clamp to -1 to use -1 for pathological cases where there's
        # only one sentence.
        return Clamp(fres, -1, 9999)
    def FleschKincaidGradeLevel(words, syllables, sentences):
        ASL = words/sentences
        ASW = syllables/words
        fkgl = 0.39*ASL + 11.8*ASW - 15.59
        return Clamp(fkgl, 0, 9999)
    def SMOGIndex(complex_words, sentences):
        # Updated from wikipedia page 5 Feb 2023 (constant in front of
        # radical no longer 1 and constant of 3 updated)
        smog = 1.0430*math.sqrt(30*complex_words/sentences) + 3.1291
        return Clamp(smog, 0, 9999)
    def EndOfSentence(word):
        '''Return 1 if the word is the end of a sentence.
        '''
        if not word:
            raise Exception("Empty word")
        last_char = word[-1]
        end_of_sentence_chars = ".!?"
        non_word_chars = ",;:-" + end_of_sentence_chars
        if last_char in end_of_sentence_chars:
            word = word[:-1]
            while len(word) and word[-1] in non_word_chars:
                word = word[:-1]
            word = word.lower()
            return False if word in common_abbreviations else True
        else:
            return False
    def StripNonletters(word):
        while len(word) and word[-1] not in "abcdefghijklmnopqrstuvwxyz":
            word = word[:-1]
        return word
    def CountSyllables(word):
        num = 0
        try:
            if word in S:
                num = S[word]
            elif word in MS:
                num = MS[word][0]
            else:
                num = GuessSyllables(word)
        except Exception:
            num = GuessSyllables(word)
        return num
    def CountStats(text):
        '''For a set string of text, return a tuple of the following items:
            number of characters
            number of words
            number of sentences
            number of syllables
            number of complex words (i.e., with >= 3 syllables)
        '''
        characters = 0
        words = 0
        complex_words = 0
        one_syllable_words = 0
        syllables = 0
        sentences = 0
        for word in text.split():
            word = word.lower()  # Ignore proper nouns
            if EndOfSentence(word):
                sentences += 1
            words += 1
            word = StripNonletters(word)
            characters += len(word)
            number_of_syllables = CountSyllables(word)
            syllables += number_of_syllables
            if number_of_syllables >= 3:
                complex_words += 1
            if number_of_syllables == 1:
                one_syllable_words += 1
        return [characters, words, complex_words, one_syllable_words,
                syllables, sentences]
    def Print(gradelevel, n, fmt, metric):
        if metric == "fres":
            if gradelevel >= 70:
                c = t.easy
            elif gradelevel >= 60:
                c = t.std
            elif gradelevel >= 50:
                c = t.med
            elif gradelevel >= 30:
                c = t.medhard
            else:
                c = t.hard
        else:
            if gradelevel <= 7:
                c = t.easy
            elif gradelevel <= 10:
                c = t.std
            elif gradelevel <= 12:
                c = t.med
            elif gradelevel <= 16:
                c = t.medhard
            else:
                c = t.hard
        s = fmt % gradelevel
        print(f"{c}{s:{n}s}{t.N}", end="")
    def PrintColorKey():
        print("\nColor key")
        w = len("medium hard") + 3
        print(f"{t.easy}{'Easy':<{w}s} Grade 7 or less")
        print(f"{t.std}{'Standard':<{w}s} Grade 8-10")
        print(f"{t.med}{'Medium':<{w}s} Grade 11-12")
        print(f"{t.medhard}{'Medium hard':<{w}s} Undergraduate college")
        print(f"{t.hard}{'Hard':<{w}s} Graduate-level college")
    def PrintHeader():
        if PrintHeader.hdr:
            return
        if d["-d"]:
            print(f"{'Chars':>7s}", end=" ")
            print(f"{'Words':>6s}", end=" ")
            print(f"{'CpxWrd':>6s}", end=" ")
            print(f"{'OneSyl':>6s}", end=" ")
            print(f"{'Syl':>6s}", end=" ")
            print(f"{'Sent':>6s}", end=" ")
        print(f"{'FKGL':>6s}", end=" ")
        print(f"{'FRES':>6s}", end=" ")
        if d["-a"]:
            print(f"{'Fog':>6s}", end=" ")
            print(f"{'ARI':>6s}", end=" ")
            print(f"{'CL':>6s}", end=" ")
            print(f"{'SMOG':>6s}", end=" ")
        print()
        PrintHeader.hdr = True
    PrintHeader.hdr = False
    def PrintResults(stats, file):
        (characters, words, complex_words, one_syllable_words, 
            syllables, sentences) = stats
        fog = GunningFogIndex(words, sentences, complex_words)
        ari = AutomatedReadabilityIndex(characters, words, sentences)
        cl = ColemanLiauIndex(characters, words, sentences)
        fres = FleschReadingEaseScore(words, syllables, sentences)
        fkgl = FleschKincaidGradeLevel(words, syllables, sentences)
        smog = SMOGIndex(complex_words, sentences)
        PrintHeader()
        if d["-d"]:
            print("%7d %6d %6d %6d %6d %6d" % stats, end=" ")
        n = 6
        fmt = f"%{n}.1f " if d["-p"] else f"%{n}.0f "
        fmt1 = f"%{n}.1f " if d["-p"] else f"%{n-1}.0f. "
        if d["-a"]:
            Print(fkgl, n, fmt, "fkgl")
            Print(fres, n, fmt1, "fres")
            Print(fog, n, fmt, "fog")
            Print(ari, n, fmt, "ari")
            Print(cl, n, fmt, "cl")
            Print(smog, n, fmt, "smog")
        else:
            Print(fkgl, n, fmt, "fkgl")
            Print(fres, n, fmt1, "fres")
        print(file, end=" ")
        # Print "+"*n where n is ceil(log(file_size))
        sz = get.GetFileSize(file)
        n = math.ceil(math.log10(sz))
        print("+"*n)
        if d["-C"]:
            d["-c"] = True
            GetColor()
            PrintColorKey()

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    for file in files:
        stats = CountStats(open(file).read())
        stats[-1] = stats[-1] if stats[-1] else 1
        PrintResults(stats, file)
