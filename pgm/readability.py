'''
TODO:
    * Add the usual ParseCommandLine
    * Update to more modern syntax

Calculate various readability indices for a set of files
    Changes:

    10 Nov 2019:  I spent time producing the words_syllables.py script,
    which is basically what used to be in the old words.py file from
    about 15 years ago; it's made from a CMU corpus in the NLTK (see the
    script /pylib/pgm/words_syllables_make.py).  The dictionary lookup
    of the number of syllables decreased the run time on
    /ebooks/kindle/Twain/*.txt from 52.4 s to 6.6 s, so having the
    dictionaries is worth the half second or so they take to load.

    22 Sep 2010:  Added test of GuessSyllables().  Changed output to
    just print nearest integer; this better reflects the approximate
    nature of the numbers.
 
    -------------------------------------------------------------------
  
    Note added 22 Sep 2010:  you should be cautious in applying the results
    of a program like this.  Reading scores are only rough guides; they
    cannot measure many things that are relevant to reading comprehension.
    If you don't believe this, the clearest argument I can give you is to
    have you randomly shuffle the words in each sentence of a document.
    Virtually all documents will now be unintelligible, yet the typical
    readability scores will be unchanged.  These scores know nothing about
    semantics or syntax, the formatting/font of the text, how nice it's
    visually organized, or the background and interest of the reader.
    These (and many other) things are relevent to reading comprehension,
    yet are obviously beyond the ken of a computer program.
  
    I personally use this program as a rough guide to how well I am
    writing.  If I'm writing for a general reader, I shoot for a reading
    level around 8th grade; if I'm writing a technical document to educated
    readers, I shoot for around 12th grade level.  It took me many years to
    get out of the habit of writing stilted, hard-to-read text which seems
    to be favored by academia and the published technical literature.
    Certainly some of the motivation for this type of writing is that using
    big words and complex sentences indirectly communicates the author's
    erudition.  This was fine in graduate school, but in the real,
    practical world, it simply turns readers off and lowers comprehension
    (or, worse, a busy executive will simply stop reading your material and
    you haven't communicated anything at all except your lack of writing
    ability).  Track down how-to-write documents like the one from Malcom
    Forbes of Forbes Magazine -- he'll give you valuable advice on how to
    communicate clearly.  It's entitled "How to Write a Business Letter",
    but it's sound advice for any type of writing.  Also find "How to Write
    Clearly" by Edward Thompson, Editor-in-Chief, Reader's Digest, and
    "Writing that Works" by Kenneth Roman and Joel Raphaelson.  Also use
    references like Strunk & White or the Chicago Manual of Style --
    getting the details right means you care about both the craft of
    writing and your reader.
  
    Or, if you're averse to books, do a web search on "how to write well".
    You'll get many useful web pages, and, as is common for the web, much
    junk.
    
    One of Hemingway's secrets:  "I write one page of masterpiece to
    ninety-one pages of shit.  I try to put the shit in the wastebasket."
    
    Update 22 Jul 2021:  As mentioned, I still find this script as a useful
    gauge for my writing.  The measure I use the most is the Flesch-Kincaid
    grade level, rounded to an integer.  Interestingly, a novel like "Pride
    and Prejudice" has a FKGL of around 12th grade, senior in high school.
    "Tom Sawyer" is about 8th grade level.  A real surprise was Andy Weir's 
    "The Martian" is about 5th grade level.  It's an eminently readable book
    and I wouldn't have guessed it would have such a low readability score.
    It's probably a combination of lots of short sentences and avoiding the
    use of long words.
    
    -----------------------------------------------------------------------
    
    Gunning Fog Index
    
        From http://en.wikipedia.org/wiki/Gunning_Fog_Index
    
        1. Take a full passage that is around 100 words (do not omit any
            sentences).
    
        2. Find the average sentence length (divide the number of words by
            the number of sentences).
    
        3. Count words with three or more syllables (complex words), not
            including proper nouns (for example, Djibouti), compound words,
            or common suffixes such as -es, -ed, or -ing as a syllable, or
            familiar jargon.
    
        4. Add the average sentence length and the percentage of complex
            words (ex., +13.37%, not simply + .1337)
    
        5. Multiply the result by 0.4
    
        The complete formula is as follows:
    
            ((words/sentence) + 100*(complex words/words))*0.4
    
        The formula can be easily modified to produce a Gunning-Fog index
        result with any length sample. Simply multiply the standard result
        by 100/(words in sample). The resultant formula wil be:
    
        ((words/sentence) + 100*(complex words/words))*0.4*100/(words in sample)
    
        While the index is a good indication of reading difficulty, it still
        has flaws. Not all multisyllabic words are difficult. For example, the
        word spontaneous is generally not considered to be a difficult word,
        even though it has four syllables.
    
    Automated Readability Index
    
        From http://en.wikipedia.org/wiki/Automated_Readability_Index
    
        To calculate the Automated Readability Index:
    
        1. Divide the number of characters by the number of words, and
            multiply by 4.71. This is #1.
    
        2. Divide the number of words by the number of sentences, and
            multiply by 0.5. This is #2.
    
        3. Add #1 and #2 together, and subtract 21.43.
    
        (4.71 * characters/word) + (0.5 * words/sentence) - 21.43
    
    Coleman-Liau Index
    
        From http://en.wikipedia.org/wiki/Coleman-Liau_Index
    
        1. Divide the number of characters by the number of words, and
            multiply by 5.89. This is #1.
    
        2. Divide (0.3 times the number of sentences) by 100 times the
            number of words. This is #2.
    
        3. Subtract #2 from #1 together, and subtract 15.8
    
        (5.89 * characters/word) - (0.3 * sentences)/(100 * words) -15.8
    
    Flesch-Kincaid Reading Ease
    
        From http://en.wikipedia.org/wiki/Flesch-Kincaid_Readability_Test
    
        One of the tests is known as the "Flesch-Kincaid Reading Ease" test.
        It scores passages on a scale of 0-100. Higher scores indicate
        material that is easier to read; lower numbers mark harder-to-read
        passages. The formula for the Flesch Reading Ease Score (FRES) test
        is:
    
            FRES = 206.835 - 1.015*ASL - 84.6*ASW
    
        where
    
            ASW = average number of syllables per word
                = (total syllables)/(total words)
    
            ASL = average sentence length
                = (total words)/(total sentences)
    
        As a rule of thumb, scores of 90-100 are considered easily
        understandable by an average 5th grader.  8th and 9th grade students
        could easily understand passages with a score of 60-70, and passage
        with results of 0-30 are best understood by college graduates.
        Reader's Digest magazine has a readability index of about 65, Time
        magazine scores about 52, and the Harvard Law Review has a general
        readability score in the low 30s.
    
        This test has become a U.S. governmental standard.  Many government
        agencies require documents or forms to meet specific readability
        levels.  Most states require insurance forms to score 40-50 on the
        test.  The U.S. Department of Defense uses the Reading Ease test as
        the standard test of readability for its documents and forms.  The
        test is so ubiquitous that it is bundled with the popular word
        processing programs KWord and Microsoft Word.
    
    Flesch-Kincaid Grade Level FKGL
    
        From http://en.wikipedia.org/wiki/Flesch-Kincaid_Readability_Test
    
        An obvious use for readability tests is in the field of education.
        The "Flesch-Kincaid Grade Level Formula" translates the 0-100 score
        to a U.S. grade level, making it easier for teachers, parents,
        librarians, and others to judge the readability level of various
        books and texts.  The grade level is calculated with the following
        formula:
    
            0.39*ASL + 11.8*ASW
    
        where
    
            ASW = average number of syllables per word
                = (total syllables)/(total words)
    
            ASL = average sentence length
                = (total words)/(total sentences)
    
        The result is a number that corresponds with a grade level. For
        example, a score of 6.1 would indicate that the text is
        understandable by an average student in 6th grade.
    
    SMOG Index
    
        From http://en.wikipedia.org/wiki/SMOG_Index
    
        McLaughlin, G. (1969), "SMOG grading: A new readability formula",
            Journal of Reading, 12 (8) 639-646
    
        The SMOG Index is a readability test designed to gauge the
        understandability of a text. Like the Flesch-Kincaid Grade Level,
        Gunning-Fog Index, Automated Readability Index, and Coleman-Liau
        Index, its output is an approximate representation of the U.S.
        grade level needed to comprehend the text.
    
        To calculate the SMOG Index:
    
        1. Count the number of complex words (words containing 3 or more
            syllables).
    
        2. Multiply the number of complex words by a factor of (30/number
            of sentences).
    
        3. Take the square root of the resultant number.
    
        4. Add 3 to the resultant number.
    
    FORCAST Readability Formula
    
        From http://agcomwww.tamu.edu/market/training/power/readabil.html
    
        FORCAST is a new readability formula designed especially for
        technical materials. It is not meant for traditional high school
        reading matter or for newspapers or magazines or books of fiction.
        It is simpler and faster to use than other readability formulas and,
        according to its authors, is more accurate for technical writing. It
        can be used to analyze a single passage, a group of passages, or a
        random series of selections from a large body of technical material.
    
        1. Count the number of one-syllable words in a 150-word passage.
    
        2. Divide that number by 10.
    
        3. Subtract the answer from 20.
    
        "The FORCAST Readability Formula." Pennsylvania State University
        Nutrition Center, Bridge to Excellence Conference, 1992.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Calculate various readability indices for a set of files
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from math import sqrt
    from pdb import set_trace as xx
    import getopt
    import os
    import pathlib
    import re
    import sys
if 1:   # Custom imports
    from wrap import dedent
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
    P = pathlib.Path
    ii = isinstance
    # If true, print out more details
    dbg = 0
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
          Prints readability statistics for text files.
        '''))
        if dbg:
            print(dedent(f'''
        C    = number of characters in words
        W    = number of words
        CW   = number of complex words (3 or more syllables)
        SY   = number of syllables
        SENT = number of sentences'''))
        print(dedent(f'''
          FKRE = Flesch-Kincaid Reading Ease
            0-100, higher numbers mean easier to read
        The following numbers are the approximate reading level in US grade level:
          FOG  = Gunning Fog Index
          ARI  = Automated Readability Index
          CL   = Coleman-Liau Index
          FKGL = Flesch-Kincaid Grade Level
          SMOG = SMOG Index
          FORC = FORCAST Readability Formula
        See the comments in the program code for formulas and references.
        ''', n=6))
        print(dedent(f'''
        Options
          -d    Turn on debug printing
          -p    Print to one decimal place (integer is default)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Debug output
        d["-p"] = False     # Print to 1 decimal place
        if len(sys.argv) < 2:
            Usage(1)
        try:
            opts, files = getopt.getopt(sys.argv[1:], "dhp", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dp"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        if d["-d"]:
            global dbg
            dbg = True
        return files
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
        return 0.4*(ASL + PCW)
    def AutomatedReadabilityIndex(characters, words, sentences):
        return 4.71*characters/words + 0.5*words/sentences - 21.43
    def ColemanLiauIndex(characters, words, sentences):
        return 5.89*characters/words - 0.3*sentences/(100*words) - 15.8
    def FleschKincaidReadingEase(words, syllables, sentences):
        ASW = syllables/words
        ASL = words/sentences
        return 206.835 - 1.015*ASL - 84.6*ASW
    def FleschKincaidGradeLevel(words, syllables, sentences):
        ASL = words/sentences
        ASW = syllables/words
        return 0.39*ASL + 11.8*ASW - 15.59
    def SMOGIndex(complex_words, sentences):
        return sqrt(30*complex_words/sentences) + 3
    def FORCASTReadabilityFormula(words, one_syllable_words):
        N = words/150
        return 20 - (one_syllable_words/N)/10
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
    def PrintHeader():
        if dbg:
            print("     C      W    CW     OS    SY  SENT   FOG   ARI",
                end=" ")
            print("   CL  FKRE  FKGL  SMOG  FORC")
        else:
            print("  FOG   ARI    CL  FKRE  FKGL  SMOG  FORC")
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
        return (characters, words, complex_words, one_syllable_words,
                syllables, sentences)
    def PrintResults(stats, file):
        (characters, words, complex_words, one_syllable_words, 
            syllables, sentences) = stats
        fog = GunningFogIndex(words, sentences, complex_words)
        ari = AutomatedReadabilityIndex(characters, words, sentences)
        cl = ColemanLiauIndex(characters, words, sentences)
        fkre = FleschKincaidReadingEase(words, syllables, sentences)
        fkgl = FleschKincaidGradeLevel(words, syllables, sentences)
        smog = SMOGIndex(complex_words, sentences)
        forc = FORCASTReadabilityFormula(words, one_syllable_words)
        if dbg:
            print("%6d %6d %5d %6d %5d %5d" % stats, end=" ")
        fmt = "%5.1f " * 7
        print(fmt % (fog, ari, cl, fkre, fkgl, smog, forc), end=" ")
        print(file)
if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    PrintHeader()
    for file in files:
        stats = CountStats(open(file).read())
        if not stats[-1]:
            print(f"No sentences in '{file}'")
            exit(1)
        PrintResults(stats, file)
