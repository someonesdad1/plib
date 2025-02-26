"""
Library to calculate common readability estimates

ToDo
    - Needed options
        - Warn when a file contains non-ASCII characters
        - ASCIIfy the file's data
        - Remove a set of words from a file or sequence
        - Change ';' to '.'.  In most prose, this is probably appropriate
          unless it's usage like 'France, 3; UK, 2;...'.  Note that speech
          never uses a semicolon.
    - Colorize the results for grade level.  There are two target
      audiences:
        - Educated adults (e.g., has a college degree)
            - purl:  easy (<= grade 7)
            - grnl:  standard (<= grade 8-10)
            - yell:  medium (<= grade 11-12)
            - ornl:  medium-hard (<= grade 13-16)   College
            - redl:  hard (> grade 16)              Graduate school
        - Average adult
            - purl:  easy (<= grade 5)
            - grnl:  standard (<= grade 6-8)
            - yell:  medium (<= grade 9-10)
            - ornl:  medium-hard (<= grade 11-12)
            - redl:  hard (> grade 12)
    - Include in the manpage the scores from a number of popular texts such
      as pnp, Tom Sawyer, etc.
        - 22 Jul 2021:  "Pride and Prejudice" has a FKGL of around 12th
          grade, senior in high school.  "Tom Sawyer" is about 8th grade
          level.  A surprise was Andy Weir's "The Martian" is about 5th
          grade level.  It's an eminently readable book and I wouldn't have
          guessed it would have such a low readability score.  It's
          probably a combination of lots of short sentences and avoiding
          the use of long words.
    - This should be both my readability script and a library.
        - Default
            - Fog
            - FKGL
        - Optional
            - ARI
            - CL
            - FRES
            - SMOG
        - Consider an option that prints out x where x =
          math.ceil(log(characters)) and x is a superscript after the file
          name.

Observations
    - I tried to use a Readability class, but performance fell by about a
      factor of 2 or more, so I retained the function-based approach.
    - Readability is a complicated topic and can be pretty subjective, as
      it depends on many things.
      https://scholarworks.wmich.edu/cgi/viewcontent.cgi?referer=https://en.wikipedia.org/&httpsredir=1&article=1792&context=reading_horizons
      explains some of the complexities.  For my needs, I've found that the
      Flesch-Kincaid grade level is easy to compute and works well for the
      documents I evaluate and write.  These documents are aimed at
      educated adults, often with a technical background.
    - 10 Nov 2019:  I spent time producing the words_syllables.py script,
      which is basically what used to be in the old words.py file from
      about 15 years ago; it's made from a CMU corpus in the NLTK (see the
      script /pylib/pgm/words_syllables_make.py).  The dictionary lookup of
      the number of syllables decreased the run time on
      /ebooks/kindle/Twain/*.txt from 52.4 s to 6.6 s, so having the
      dictionaries is worth the half second or so they take to load.
    - 22 Sep 2010
        - Added test of GuessSyllables().  Changed output to just print
          nearest integer; this better reflects the approximate nature of
          the numbers.
        - You should be cautious in applying the results of a program like
          this.  Reading scores are only rough guides; they cannot measure
          many things that are relevant to reading comprehension.  If you
          don't believe this, the clearest argument I can give you is to
          have you randomly shuffle the words in each sentence of a
          document.  Virtually all documents will now be unintelligible,
          yet the typical readability scores will be unchanged.  These
          scores know nothing about semantics or syntax, the
          formatting/font of the text, how nice it's visually organized, or
          the background and interest of the reader.  These (and many
          other) things are relevent to reading comprehension, yet are
          obviously beyond the ken of a computer program.
    - I use this script as a guide to how well I am writing
        - My writing targets in grade level
            - General reader:  8
            - Technical document for educated readers:  12
        - It took me many years to get out of the habit of writing with the
          style I learned in academia.  This was OK in graduate school, but
          in the real, practical world, it turns readers off and lowers
          comprehension.
        - A core realization in my industrial career was that I needed to
          get my message across to busy executives and decision makers in
          half a page of paper with easy-to-read prose.  Put the gory
          details in an appendix.
        - Read good references on clear writing
            - Malcom Forbes "How to Write a Business Letter"
            - "How to Write Clearly" by Edward Thompson, Editor-in-Chief,
              Reader's Digest
            - "Writing that Works" by Kenneth Roman and Joel Raphaelson
            - Strunk & White
            - Chicago Manual of Style
            - Getting the details right means you care about the craft of
              writing and your reader
        - Hemingway:  "I write one page of masterpiece to ninety-one pages
          of shit.  I try to put the shit in the wastebasket."

Algorithms
    - Gunning Fog Index
        - From http://en.wikipedia.org/wiki/Gunning_Fog_Index
        - Method
            - 1. Take a full passage that is around 100 words (do not omit
              any sentences).
            - 2. Find the average sentence length (divide the number of
              words by the number of sentences).
            - 3. Count words with three or more syllables (complex words),
              not including proper nouns (for example, Djibouti), compound
              words, or common suffixes such as -es, -ed, or -ing as a
              syllable, or familiar jargon.
            - 4. Add the average sentence length and the percentage of
              complex words (ex., +13.37%, not simply + .1337)
            - 5. Multiply the result by 0.4
            - The formula is 0.4*((words/sentence) + 100*(complex
              words/words))
        - While the index is a good indication of reading difficulty, it
          still has flaws.  Not all multisyllabic words are difficult. For
          example, the word spontaneous is generally not considered to be a
          difficult word, even though it has four syllables.
    - Automated Readability Index
        - From http://en.wikipedia.org/wiki/Automated_Readability_Index
        - Method
            - 1. Divide the number of characters by the number of words,
              and multiply by 4.71. This is A.
            - 2. Divide the number of words by the number of sentences, and
              multiply by 0.5. This is B.
            - 3. Add A and B together, and subtract 21.43.
            - Index = (4.71*characters/word) + (0.5*words/sentence) - 21.43
    - Coleman-Liau Index
        - From http://en.wikipedia.org/wiki/Coleman-Liau_Index
        - Method
            - 1. Divide the number of characters by the number of words,
              and multiply by 5.89. This is #1.
            - 2. Divide (0.3 times the number of sentences) by 100 times
              the number of words. This is #2.
            - 3. Subtract #2 from #1 together, and subtract 15.8
            - Index = (5.89*characters/word) - (0.3*sentences)/(100*words)
              - 15.8
    - Flesch Reading Ease Score = FRES
        - From http://en.wikipedia.org/wiki/Flesch-Kincaid_Readability_Test
        - Scores passages on a scale of 0-100 (can be > 100 and < 0 for
          pathological cases). Higher scores indicate material that is
          easier to read; lower numbers mark harder-to-read passages.
            - Formula:  FRES = 206.835 - 1.015*ASL - 84.6*ASW
        - where
            - ASW = average number of syllables per word (total
              syllables)/(total words)
            - ASL = average sentence length = (total words)/(total
              sentences)
        - Interpretation
            - > 90:  understandable by 5th grade
            - 60-70:  understandable by 8th and 9th grades
            - 0-30:  understandable by college graduates
            - Reader's Digest:  65
            - Time magazine:  52
            - Harvard Law Review:  low 30's
        - Has become a US governmental standard.  Many government agencies
          require documents or forms to meet specific readability levels.
          Most states require insurance forms to score 40-50 on the test.
          The US DoD uses the Reading Ease test as the standard test of
          readability for its documents and forms.
    - Flesch-Kincaid Grade Level = FKGL
        - From http://en.wikipedia.org/wiki/Flesch-Kincaid_Readability_Test
        - An obvious use for readability tests is in the field of
          education.  The "Flesch-Kincaid Grade Level Formula" translates
          the 0-100 score to a US grade level, making it easier for
          teachers, parents, librarians, and others to judge the
          readability level of various books and texts.
        - Method
            - GL = 0.39*ASL + 11.8*ASW
            - where
                - ASW = average number of syllables per word = (total
                  syllables)/(total words)
                - ASL = average sentence length = (total words)/(total
                  sentences)
        - The result is a number that corresponds with a grade level. For
          example, a score of 6.1 would indicate that the text is
          understandable by an average student in 6th grade.
    - SMOG Index
        - From http://en.wikipedia.org/wiki/SMOG_Index
        - McLaughlin, G. (1969), "SMOG grading: A new readability formula",
          Journal of Reading, 12 (8) 639-646
        - The SMOG Index is a readability test designed to gauge the
          understandability of a text. Like the Flesch-Kincaid Grade Level,
          Gunning-Fog Index, Automated Readability Index, and Coleman-Liau
          Index, its output is an approximate representation of the US
          grade level needed to comprehend the text.
        - Method
            - 1. Count the number of complex words (words containing 3 or
              more syllables).
            - 2. Multiply the number of complex words by a factor of
              (30/number of sentences).
            - 3. Take the square root of the resultant number.
            - 4. Add 3 to the resultant number.
    - FORCAST Readability Formula
        - From http://agcomwww.tamu.edu/market/training/power/readabil.html
        - FORCAST is a new readability formula designed especially for
          technical materials. It is not meant for traditional high school
          reading matter, newspapers, magazines, or books of fiction.  It
          is simpler and faster to use than other readability formulas and,
          according to its authors, is more accurate for technical writing.
          It can be used to analyze a single passage, a group of passages,
          or a random series of selections from a large body of technical
          material.
        - Method
            - 1. Count the number of one-syllable words in a 150-word
              passage.
            - 2. Divide that number by 10.
            - 3. Subtract the answer from 20.
        - "The FORCAST Readability Formula." Pennsylvania State University
          Nutrition Center, Bridge to Excellence Conference, 1992.

"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2005, 2023 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Calculate various readability indices for a set of files
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from math import sqrt
        import getopt
        import os
        from pathlib import Path as P
        import re
        import string
        import sys
        from collections import namedtuple
    if 1:  # Custom imports
        import get
        import dpstr
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from lwtest import Assert

        if 1:
            import debug

            debug.SetDebugger()
        common_abbreviations = set("mr mrs ms dr no mssr st ave".split())
        # Load a dictionary of number of syllables if available (otherwise,
        # the number of syllables in each word will be found by the function
        # GuessSyllables.  The words_syllables module contains two
        # dictionaries that greatly speed up getting the number of syllables
        # per word.  See the docstring.
        try:
            from words_syllables import syllables as S, multiple_syllables as MS
        except ImportError:
            pass
    if 1:  # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        ii = isinstance
        # If true, print out more details
        dbg = 0
        # Named tuple to hold textual information
        TextInfo = namedtuple(
            "TextInfo",
            """
            characters
            words
            complex_words
            one_syllable_words
            syllables
            sentences
            wordlist
            """,
        )
        # Named tuple for readability estimates
        ReadabilityTuple = namedtuple(
            "Readability",
            """
            FK_ease
            FK_grade
            DaleChall
            """,
        )
        # Colors
        t.dbg = t("lill")
        t.err = t("redl")
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} file1 [file2...]
          Prints readability statistics for text files.
        """)
        )
        if dbg:
            print(
                dedent(f"""
        C    = number of characters in words
        W    = number of words
        CW   = number of complex words (3 or more syllables)
        SY   = number of syllables
        SENT = number of sentences""")
            )
        print(
            dedent(
                f"""
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
        """,
                n=6,
            )
        )
        print(
            dedent(f"""
        Options
          -d    Turn on debug printing
          -p    Print to one decimal place (integer is default)
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-d"] = False  # Debug output
        d["-p"] = False  # Print to 1 decimal place
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


if 1:  # Manpage

    def Manpage():
        print(
            dedent(f"""

        Readability Estimates
        ---------------------

            For an introduction, see https://en.wikipedia.org/wiki/Readability.  This
            module contains a class Readability that can take input from files or
            streams that results in plain ASCII text with words separated by
            whitespace.  The text is analyzed for number of characters, words,
            sentences, syllables per word, and complex words.  These numbers are used
            to calculate various estimates of how readable a selection of text is.
            Because this is based on only the text content, the visual layout of the
            text is ignored.

            I recommend you experiment with the different methods and decide on which
            tools best meet your needs.  Reading the above wikipedia page should give
            enough background on the methods.

        Opinions
        --------

            My primary use of a few of these formulas is to assess the approximate
            reading level of my written material.  I went through a typical academic
            curriculum, doing research and writing reports and papers.
            Unfortunately, many such writers can produce nearly unreadable text.
            This is easily seen when reading research literature.  When I worked in
            R&D at HP, a good friend who was an executive politely told me I wrote
            too many words and used too many unfamiliar words.  This almost
            guaranteed the memos and reports I wrote to influence decision makers were
            not read.  Later, when I was in management, I noticed the same behavior
            in my department, so I studied books aimed at helping professionals to
            write better.  It took effort and study to unlearn the stilted academic
            habits we all had.  But it helped us write a bit better for our
            business environment.
            
            The main lesson my friend taught me was that decision makers (executives,
            managers, senior-level technical staff) are overloaded with reading
            material.  If you can't get them the core message in half a sheet of
            paper, they likely won't read the rest of your material.  If you want to
            make an impact, keep the executive summary short and provide the details
            in an appendix.

            After retiring, I would occasionally do consulting work for an electronic
            test company, writing and editing user manuals and marketing
            communications.  This further showed the need for more careful writing,
            so I routinely used the precursor of this library to analyze every piece
            of writing I was responsible for.  It must have helped, as they used my
            writing services for over a decade.

            I settled on the Flesch-Kincaid grade level (FKGL) in integer form as the
            most practical guide to reading ease.  I read somewhere that "Reader's
            Digest" had a FKGL of around 8th grade and I used this as a target for
            most of my writing.  

        Examples
        --------

            I ran the readability.py script on the following software license texts:

                afl3       Academic Free License 3.0
                apache2    Apache License 2.0
                bsd3       BSD 3-clause license
                ccsa4      Creative Commons Attribution-ShareAlike 4.0
                gpl2       GNU Public License version 2
                gpl3       GNU Public License version 3
                lgpl3      Lesser GNU Public License version 3
                mit        MIT License
                nposl3     Non-Profit Open Software License 3.0
                osl3       Open Software License 3.0
                pd         Public domain release
                wol        Wide-open License

            and got the following results:

                FOG   ARI    CL  FKRE  FKGL  SMOG
                 20    17    14    28    16    17  aa.afl3
                 21    18    15    24    17    18  aa.apache2
                 23    20    17    17    18    19  aa.bsd3
                 16    12    15    33    13    14  aa.ccsa4
                 17    16    12    41    15    15  aa.gpl2
                 19    17    13    34    16    16  aa.gpl3
                 20    17    12    33    17    16  aa.lgpl3
                 21    20    16    22    18    18  aa.mit
                 24    21    14    19    20    20  aa.nposl3
                 24    21    14    19    20    20  aa.osl3
                 20    17    14    30    17    17  aa.pd
                 17    17    18    25    16    15  aa.wol

            These were likely all written by lawyers and would all be considered 
            difficult documents for the general reader by virtue of their FKRE being
            about 30 or less.

            As an example of a hard-to-read page because of the medical terminology,
            run the script on the page
            https://en.wikipedia.org/wiki/Cholangiocarcinoma.  This gave a Fog of 35
            and a FKGL of 32.

        Reference data
        --------------

        https://outreach.ou.edu/educational-services/education/edutas/comp-center-landing-page/knowledgebases/program-evaluation-knowledgebase/task-1-write-report/fog-index/
            - Discusses Gunning Fog and Flesch-Kincaid grade level
            - Gives the Fog following grade levels for these magazines:
                - 6     Comic books
                - 7     True Confessions
                - 8     Ladies' Home Journal
                - 9     Reader's Digest
                - 10    Newsweek
                - 11    Time, Harper's
                - 12    Atlantic Monthly
            - Points out the FOG index indicates how easy the writing is to
              read.  The Flesch formulas are supposed to do the same, but
              since we learn to read more difficult words before we
              understand them, the Fog index is two grades higher than the
              Flesch metric.
            - Most newspapers write at 8-10 grade Fog level or 5-8 grade
              reading ease (Flesch).  The rationale is that the newspaper
              won't be read if a person has to labor over it as if doing
              school research.

        https://www.wyliecomm.com/2021/11/measure-reading-levels-with-readability-indexes/
            - Flesch reading ease
                - reading_ease = 206.835 – (1.015*words_per_sentence) – (84.6*syllables_per_word)
                - Scores range from 0 to 100 usually, although you can
                  construct pathological cases that result in numbers
                  outside this range
                - Scores (% is number of adults who can read at this level)
                    - > 90  Very easy, 4th grade level, 93%
                    - > 80  Easy, 5th grade level, 91%
                    - > 70  Fairly easy, 6th grade level, 83%
                    - > 50  Fairly hard, some high school, 54%
                    - > 30  Hard, High school or some college, 33%
                    - < 30  Very hard, college, 4.5%
                - Aim for 60 or higher.  To increase, reduce length of
                  sentences and words.
            - Flesch-Kincaid grade level
                - FKGL = (0.39*average_number_of_words_per_sentence)
                        + (11.8*average_number_of_syllables_per_word) – 15
                - Standard for DoD, IRS, SS Administration.  Many states
                  require insurance policies and other documents at 9th
                  grade level or less.
                - Scores (% is number of adults who can read at this level)
                    - 4:    very easy, 93
                    - 5:    easy, 91
                    - 6:    fairly easy, 88
                    - 7-8:  standard, 83
                    - Some high school:  fairly hard, 83
                    - High school or some college:  hard, 33
                    - College:  very hard, 4.5
                - Aim for 8th grade or lower
            - Gunning Fog level
                - Their formula is wrong
                - Fog index is approximate grade level (shoot for <= 9)
                - Scores (magazines at that level)
                    - 6:    People, Parade
                    - 7:    TV Guide, Bible, Mark Twain
                    - 8:    Ladies' Home Journal
                    - 9:    Reader's Digest
                    - 10:   National Geographic
                    - 11-12:   Harper's, Time, Atlantic Monthly, Newsweek, WSJ
                    - 13-15:   None
                    - 16:   College senior, standard medical consent forms
                    - 17-20:   Academic journals
                    - 20+:   US government information
        """)
        )
        exit(0)


if 1:  # Basic routines

    def GuessSyllables(word, letters_only=False):
        """Guess the number of syllables in a word.

        If letters_only is True, then an exception is raised if any
        punctuation characters are found in the word.  This is intended to
        ensure that you're not e.g. examining program code.

        From pyflesch.py script by Seb Bacon.  Downloaded 5 Feb 2023
        https://github.com/sebbacon/pyflesch/blob/master/pyflesch.py.
        I have edited the algorithm.
        """
        # Our basic way of guessing is to count the number of vowels
        # in a word.  We then subtract 1 for each dipthong we find,
        # and add 1 for anti-dipthongs (OK, that's probably not the
        # technical term).
        #
        syl = 0
        subtract_syl = [
            "cial",
            "tia",
            "cius",
            "cious",
            "giu",  # belgium!
            "ion",
            "iou",
            "sia$",
            ".ely$",  # absolutely! (but not ely!)
            "ea.",
            "oa.",
            "enced$",
        ]
        add_syl = [
            "ia",
            "riet",
            "dien",
            "iu",
            "io",
            "ii",
            "[aeiouym]bl$",  # -Vble, plus -mble
            "[aeiou]{3}",  # agreeable
            "^mc",
            "ism$",  # -isms
            "([^aeiouy])\1l$",  # middle twiddle battle bottle, etc.
            "[^l]lien",  # alien, salient [1]
            "^coa[dglx].",  # [2]
            "[^gq]ua[^auieo]",  # I think this fixes more than it breaks
            "dnt$",  # couldn't
        ]
        word = word.lower()
        word = word.replace("'", "")  # fold contractions
        word = word.replace('"', "")  # remove double quotes from around word
        word = word.replace("'", "")  # (DP added) Remove single quotes from around word
        word = re.sub("e$", "", word)
        # Check for non-letters if necessary
        if letters_only:
            if dpstr.Remove(word, string.ascii_lowercase):
                raise ValueError(f"'{word}' contains non-letters")
        spl = re.split("[^aeiouy]+", word)
        while "" in spl:  # Remove any empty strings
            spl.remove("")
        for rx in subtract_syl:
            if re.match(rx, word):
                syl -= 1
        for rx in add_syl:
            if re.match(rx, word):
                syl += 1
        if len(word) == 1:  # 'x'
            syl += 1
        syl += len(spl)
        return syl if syl else 1

    def EndOfSentence(word):
        "Return 1 if the word is the end of a sentence"
        if not word:
            raise Exception("Empty word")
        last_char = word[-1]
        end_of_sentence_chars = ".!?"
        non_word_chars = ",;:-" + end_of_sentence_chars
        if last_char not in end_of_sentence_chars:
            return False
        word = word[:-1]
        # Remove all non-word characters
        while len(word) and word[-1] in non_word_chars:
            word = word[:-1]
        word = word.lower()
        return False if word in common_abbreviations else True

    def StripNonletters(word):
        """Remove letters not in "abcdefghijklmnopqrstuvwxyz" from the end
        of the word.  Note this ignores non-letters in the middle of the
        word.

        Example:  "object.data!" will return "object.data".  With
        non-letter data in the middle of a word, it's likely the word came
        from program code or a mistake.
        """
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
            print("     C      W    CW     OS    SY  SENT   FOG   ARI", end=" ")
            print("   CL  FKRE  FKGL  SMOG  FORC")
        else:
            print("  FOG   ARI    CL  FKRE  FKGL  SMOG  FORC")

    def PrintResults(stats, file):
        (characters, words, complex_words, one_syllable_words, syllables, sentences) = (
            stats
        )
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

    def GetTextInfo(text):
        """For a string of text, return a TextInfo namedtuple."""
        Assert(ii(text, str))
        # Operate on only lowercase strings.  Note this means we won't
        # ignore proper nouns (these could be confused with the words at
        # the beginning of a sentence if you assume a proper noun begins
        # with a capital letter).
        text = text.lower()
        # Veriables for counts
        characters, words, complex_words, one_syllable_words = 0, 0, 0, 0
        syllables, sentences = 0, 0
        # Split the text into words
        wordlist = get.GetWords(text)
        for word in wordlist:
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
        s = [
            characters,
            words,
            complex_words,
            one_syllable_words,
            syllables,
            sentences,
            wordlist,
        ]
        for i in s[:-1]:
            Assert(i >= 0)
        return TextInfo(*s)


if 1:  # Readability metric algorithms

    def GunningFogIndex(words, sentences, complex_words):
        ASL = words / sentences
        PCW = 100 * complex_words / words
        return 0.4 * (ASL + PCW)

    def ARI(characters, words, sentences):
        """Automated readability index for English text.

        See https://en.wikipedia.org/wiki/Automated_readability_index.  An
        advantage of this metric is that it is easy to calculate.  The
        returned value is interpreted as a US grade level.  Note this is
        slightly different than the metric defined in the wikipedia page.
        """
        ari = 4.71 * characters / words + 0.5 * words / sentences - 21.43
        # Subtract 1 so that a returned value of 1 indicates first grade.
        ari -= 1
        # Provide some reality checks
        if ari < 0:
            raise ValueError("ARI is < 0")
        return ari

    def ColemanLiauIndex(characters, words, sentences):
        """Return an estimate of the US grade level.

        See https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index.
        Formula is
            CL = 0.0588*L - 0.296*S - 15.8
        where
            L = 100*characters/words
            S = 100*sentences/words
        """
        return 5.89 * characters / words - 0.3 * sentences / (100 * words) - 15.8

    def FleschKincaidReadingEase(words, syllables, sentences):
        ASW = syllables / words
        ASL = words / sentences
        return 206.835 - 1.015 * ASL - 84.6 * ASW

    def FleschKincaidGradeLevel(words, syllables, sentences):
        ASL = words / sentences
        ASW = syllables / words
        return 0.39 * ASL + 11.8 * ASW - 15.59

    def SMOGIndex(complex_words, sentences):
        return sqrt(30 * complex_words / sentences) + 3

    def FORCASTReadabilityFormula(words, one_syllable_words):
        N = words / 150
        return 20 - (one_syllable_words / N) / 10


if 0:  # Dale-Chall stuff (not working yet)
    """https://en.wikipedia.org/wiki/Dale%E2%80%93Chall_readability_formula
    makes the point that "Regular plurals of nouns, regular past tense
    forms, progressive forms of verbs etc have to be added" to the
    basic list of words.  The formula is also ambiguous as to what
    exactly "words" means:  is it all the words in the document or the
    set of unique words?  I'd need the original reference to determine
    this.  Hence, this stuff is commented out until this is resolved.
    """

    def DaleChall(text, textinfo):
        "Return score from Dale-Chall formula"
        easywords = DaleChallWords()
        ti = textinfo
        words, sentences, wordlist = ti.words, ti.sentences, ti.wordlist
        # Note:  wordlist is changed to a set so that difficult words are
        # only counted once.
        wordlist = set(wordlist)
        if not sentences:
            sentences += 1
        # Count difficult words.
        difficult_words = 0
        for word in wordlist:
            if word not in easywords:
                difficult_words += 1
        # Calculate statistic
        pct = 100 * difficult_words / len(wordlist)
        score = 0.1579 * pct + 0.0496 * (words / sentences)
        final_score = score + 3.6365 if pct > 5 else score
        if 1:
            t.print(f"{t.dbg}words                = {words}")
            t.print(f"{t.dbg}sentences            = {sentences}")
            t.print(f"{t.dbg}difficult words      = {difficult_words}")
            t.print(f"{t.dbg}% of difficult words = {pct}")
            t.print(f"{t.dbg}raw score            = {score}")
            t.print(f"{t.dbg}score                = {final_score}")
        return final_score

    def DaleChallGrade(score):
        "Return grade level associated with score"
        Assert(score >= 0)
        if score <= 4.9:
            return 4
        elif score <= 5.9:
            return 6
        elif score <= 6.9:
            return 8
        elif score <= 7.9:
            return 10
        elif score <= 8.9:
            return 12
        elif score <= 9.9:
            return 15
        else:
            return 16

    def DaleChallWords(to_lower=True):
        """Return a set of words from the Dale-Chall list of words.  If
        to_lower is True, convert the words to lowercase.  See
        https://www.readabilityformulas.com/articles/dale-chall-readability-word-list.php
        for a discussion.  This list of words represent those that about
        80% of 4th graders will understand.
        """
        if not hasattr(DaleChallWords, "words"):
            # 5 Feb 2023 2950 words from
            # http://countwordsworth.com/download/DaleChallEasyWordList.txt
            data = """
    
                a able aboard about above absent accept accident account ache aching acorn acre across act acts add address admire adventure afar afraid after afternoon afterward afterwards again against age aged ago agree ah ahead aid aim air airfield airplane airport airship airy alarm alike alive all alley alligator allow almost alone along aloud already also always am America American among amount an and angel anger angry animal another answer ant any anybody anyhow anyone anything anyway anywhere apart apartment ape apiece appear apple April apron are aren't arise arithmetic arm armful army arose around arrange arrive arrived arrow art artist as ash ashes aside ask asleep at ate attack attend attention August aunt author auto automobile autumn avenue awake awaken away awful awfully awhile ax axe baa babe babies back background backward backwards bacon bad badge badly bag bake baker bakery baking ball balloon banana band bandage bang banjo bank banker bar barber bare barefoot barely bark barn barrel base baseball basement basket bat batch bath bathe bathing bathroom bathtub battle battleship bay be beach bead beam bean bear beard beast beat beating beautiful beautify beauty became because become becoming bed bedbug bedroom bedspread bedtime bee beech beef beefsteak beehive been beer beet before beg began beggar begged begin beginning begun behave behind being believe bell belong below belt bench bend beneath bent berries berry beside besides best bet better between bib bible bicycle bid big bigger bill billboard bin bind bird birth birthday biscuit bit bite biting bitter black blackberry blackbird blackboard blackness blacksmith blame blank blanket blast blaze bleed bless blessing blew blind blindfold blinds block blood bloom blossom blot blow blue blueberry bluebird blush board boast boat bob bobwhite bodies body boil boiler bold bone bonnet boo book bookcase bookkeeper boom boot born borrow boss both bother bottle bottom bought bounce bow bowl bow-wow box boxcar
                boxer boxes boy boyhood bracelet brain brake bran branch brass brave bread break breakfast breast breath breathe breeze brick bride bridge bright brightness bring broad broadcast broke broken brook broom brother brought brown brush bubble bucket buckle bud buffalo bug buggy build building built bulb bull bullet bum bumblebee bump bun bunch bundle bunny burn burst bury bus bush bushel business busy but butcher butt butter buttercup butterfly buttermilk butterscotch button buttonhole buy buzz by bye cab cabbage cabin cabinet cackle cage cake calendar calf call caller calling came camel camp campfire can canal canary candle candlestick candy cane cannon cannot canoe can't canyon cap cape capital captain car card cardboard care careful careless carelessness carload carpenter carpet carriage carrot carry cart carve case cash cashier castle cat catbird catch catcher caterpillar catfish catsup cattle caught cause cave ceiling cell cellar cent center cereal certain certainly chain chair chalk champion chance change chap charge charm chart chase chatter cheap cheat check checkers cheek cheer cheese cherry chest chew chick chicken chief child childhood children chill chilly chimney chin china chip chipmunk chocolate choice choose chop chorus chose chosen christen Christmas church churn cigarette circle circus citizen city clang clap class classmate classroom claw clay clean cleaner clear clerk clever click cliff climb clip cloak clock close closet cloth clothes clothing cloud cloudy clover clown club cluck clump coach coal coast coat cob cobbler cocoa coconut cocoon cod codfish coffee coffeepot coin cold collar college color colored colt column comb come comfort comic coming company compare conductor cone connect coo cook cooked cooking cookie cookies cool cooler coop copper copy cord cork corn corner correct cost cot cottage cotton couch cough could couldn't count counter country county course court cousin cover cow coward cowardly cowboy cozy crab crack cracker
                cradle cramps cranberry crank cranky crash crawl crazy cream creamy creek creep crept cried croak crook crooked crop cross crossing cross-eyed crow crowd crowded crown cruel crumb crumble crush crust cry cries cub cuff cup cuff cup cupboard cupful cure curl curly curtain curve cushion custard customer cut cute cutting dab dad daddy daily dairy daisy dam damage dame damp dance dancer dancing dandy danger dangerous dare dark darkness darling darn dart dash date daughter dawn day daybreak daytime dead deaf deal dear death December decide deck deed deep deer defeat defend defense delight den dentist depend deposit describe desert deserve desire desk destroy devil dew diamond did didn't die died dies difference different dig dim dime dine ding-dong dinner dip direct direction dirt dirty discover dish dislike dismiss ditch dive diver divide do dock doctor does doesn't dog doll dollar dolly done donkey don't door doorbell doorknob doorstep dope dot double dough dove down downstairs downtown dozen drag drain drank draw drawer draw drawing dream dress dresser dressmaker drew dried drift drill drink drip drive driven driver drop drove drown drowsy drub drum drunk dry duck due dug dull dumb dump during dust dusty duty dwarf dwell dwelt dying each eager eagle ear early earn earth east eastern easy eat eaten edge egg eh eight eighteen eighth eighty either elbow elder eldest electric electricity elephant eleven elf elm else elsewhere empty end ending enemy engine engineer English enjoy enough enter envelope equal erase eraser errand escape eve even evening ever every everybody everyday everyone everything everywhere evil exact except exchange excited exciting excuse exit expect explain extra eye eyebrow fable face facing fact factory fail faint fair fairy faith fake fall false family fan fancy far faraway fare farmer farm farming far-off farther fashion fast fasten fat father fault favor favorite fear feast feather February fed feed feel feet fell fellow felt fence
                fever few fib fiddle field fife fifteen fifth fifty fig fight figure file fill film finally find fine finger finish fire firearm firecracker fireplace fireworks firing first fish fisherman fist fit fits five fix flag flake flame flap flash flashlight flat flea flesh flew flies flight flip flip-flop float flock flood floor flop flour flow flower flowery flutter fly foam fog foggy fold folks follow following fond food fool foolish foot football footprint for forehead forest forget forgive forgot forgotten fork form fort forth fortune forty forward fought found fountain four fourteen fourth fox frame free freedom freeze freight French fresh fret Friday fried friend friendly friendship frighten frog from front frost frown froze fruit fry fudge fuel full fully fun funny fur furniture further fuzzy gain gallon gallop game gang garage garbage garden gas gasoline gate gather gave gay gear geese general gentle gentleman gentlemen geography get getting giant gift gingerbread girl give given giving glad gladly glance glass glasses gleam glide glory glove glow glue go going goes goal goat gobble God god godmother gold golden goldfish golf gone good goods goodbye good-by goodbye good-bye good-looking goodness goody goose gooseberry got govern government gown grab gracious grade grain grand grandchild grandchildren granddaughter grandfather grandma grandmother grandpa grandson grandstand grape grapes grapefruit grass grasshopper grateful grave gravel graveyard gravy gray graze grease great green greet grew grind groan grocery ground group grove grow guard guess guest guide gulf gum gun gunpowder guy ha habit had hadn't hail hair haircut hairpin half hall halt ham hammer hand handful handkerchief handle handwriting hang happen happily happiness happy harbor hard hardly hardship hardware hare hark harm harness harp harvest has hasn't haste hasten hasty hat hatch hatchet hate haul have haven't having hawk hay hayfield haystack he head headache heal health healthy heap
                hear hearing heard heart heat heater heaven heavy he'd heel height held hell he'll hello helmet help helper helpful hem hen henhouse her hers herd here here's hero herself he's hey hickory hid hidden hide high highway hill hillside hilltop hilly him himself hind hint hip hire his hiss history hit hitch hive ho hoe hog hold holder hole holiday hollow holy home homely homesick honest honey honeybee honeymoon honk honor hood hoof hook hoop hop hope hopeful hopeless horn horse horseback horseshoe hose hospital host hot hotel hound hour house housetop housewife housework how however howl hug huge hum humble hump hundred hung hunger hungry hunk hunt hunter hurrah hurried hurry hurt husband hush hut hymn I ice icy I'd idea ideal if ill I'll I'm important impossible improve in inch inches income indeed Indian indoors ink inn insect inside instant instead insult intend interested interesting into invite iron is island isn't it its it's itself I've ivory ivy jacket jacks jail jam January jar jaw jay jelly jellyfish jerk jig job jockey join joke joking jolly journey joy joyful joyous judge jug juice juicy July jump June junior junk just keen keep kept kettle key kick kid kill killed kind kindly kindness king kingdom kiss kitchen kite kitten kitty knee kneel knew knife knit knives knob knock knot know known lace lad ladder ladies lady laid lake lamb lame lamp land lane language lantern lap lard large lash lass last late laugh laundry law lawn lawyer lay lazy lead leader leaf leak lean leap learn learned least leather leave leaving led left leg lemon lemonade lend length less lesson let let's letter letting lettuce level liberty library lice lick lid lie life lift light lightness lightning like likely liking lily limb lime limp line linen lion lip list listen lit little live lives lively liver living lizard load loaf loan loaves lock locomotive log lone lonely lonesome long look lookout loop loose lord lose loser loss lost lot loud love lovely lover low luck lucky
                lumber lump lunch lying ma machine machinery mad made magazine magic maid mail mailbox mailman major make making male mama mamma man manager mane manger many map maple marble march March mare mark market marriage married marry mask mast master mat match matter mattress may May maybe mayor maypole me meadow meal mean means meant measure meat medicine meet meeting melt member men mend meow merry mess message met metal mew mice middle midnight might mighty mile milk milkman mill miler million mind mine miner mint minute mirror mischief miss Miss misspell mistake misty mitt mitten mix moment Monday money monkey month moo moon moonlight moose mop more morning morrow moss most mostly mother motor mount mountain mouse mouth move movie movies moving mow Mr.  Mrs.  much mud muddy mug mule multiply murder music must my myself nail name nap napkin narrow nasty naughty navy near nearby nearly neat neck necktie need needle needn't Negro neighbor neighborhood neither nerve nest net never nevermore new news newspaper next nibble nice nickel night nightgown nine nineteen ninety no nobody nod noise noisy none noon nor north northern nose not note nothing notice November now nowhere number nurse nut oak oar oatmeal oats obey ocean o'clock October odd of off offer office officer often oh oil old old-fashioned on once one onion only onward open or orange orchard order ore organ other otherwise ouch ought our ours ourselves out outdoors outfit outlaw outline outside outward oven over overalls overcoat overeat overhead overhear overnight overturn owe owing owl own owner ox pa pace pack package pad page paid pail pain painful paint painter painting pair pal palace pale pan pancake pane pansy pants papa paper parade pardon parent park part partly partner party pass passenger past paste pasture pat patch path patter pave pavement paw pay payment pea peas peace peaceful peach peaches peak peanut pear pearl peck peek peel peep peg pen pencil penny people pepper peppermint perfume
                perhaps person pet phone piano pick pickle picnic picture pie piece pig pigeon piggy pile pill pillow pin pine pineapple pink pint pipe pistol pit pitch pitcher pity place plain plan plane plant plate platform platter play player playground playhouse playmate plaything pleasant please pleasure plenty plow plug plum pocket pocketbook poem point poison poke pole police policeman polish polite pond ponies pony pool poor pop popcorn popped porch pork possible post postage postman pot potato potatoes pound pour powder power powerful praise pray prayer prepare present pretty price prick prince princess print prison prize promise proper protect proud prove prune public puddle puff pull pump pumpkin punch punish pup pupil puppy pure purple purse push puss pussy pussycat put putting puzzle quack quart quarter queen queer question quick quickly quiet quilt quit quite rabbit race rack radio radish rag rail railroad railway rain rainy rainbow raise raisin rake ram ran ranch rang rap rapidly rat rate rather rattle raw ray reach read reader reading ready real really reap rear reason rebuild receive recess record red redbird redbreast refuse reindeer rejoice remain remember remind remove rent repair repay repeat report rest return review reward rib ribbon rice rich rid riddle ride rider riding right rim ring rip ripe rise rising river road roadside roar roast rob robber robe robin rock rocky rocket rode roll roller roof room rooster root rope rose rosebud rot rotten rough round route row rowboat royal rub rubbed rubber rubbish rug rule ruler rumble run rung runner running rush rust rusty rye sack sad saddle sadness safe safety said sail sailboat sailor saint salad sale salt same sand sandy sandwich sang sank sap sash sat satin satisfactory Saturday sausage savage save savings saw say scab scales scare scarf school schoolboy schoolhouse schoolmaster schoolroom scorch score scrap scrape scratch scream screen screw scrub sea seal seam search season seat second secret see
                seeing seed seek seem seen seesaw select self selfish sell send sense sent sentence separate September servant serve service set setting settle settlement seven seventeen seventh seventy several sew shade shadow shady shake shaker shaking shall shame shan't shape share sharp shave she she'd she'll she's shear shears shed sheep sheet shelf shell shepherd shine shining shiny ship shirt shock shoe shoemaker shone shook shoot shop shopping shore short shot should shoulder shouldn't shout shovel show shower shut shy sick sickness side sidewalk sideways sigh sight sign silence silent silk sill silly silver simple sin since sing singer single sink sip sir sis sissy sister sit sitting six sixteen sixth sixty size skate skater ski skin skip skirt sky slam slap slate slave sled sleep sleepy sleeve sleigh slept slice slid slide sling slip slipped slipper slippery slit slow slowly sly smack small smart smell smile smoke smooth snail snake snap snapping sneeze snow snowy snowball snowflake snuff snug so soak soap sob socks sod soda sofa soft soil sold soldier sole some somebody somehow someone something sometime sometimes somewhere son song soon sore sorrow sorry sort soul sound soup sour south southern space spade spank sparrow speak speaker spear speech speed spell spelling spend spent spider spike spill spin spinach spirit spit splash spoil spoke spook spoon sport spot spread spring springtime sprinkle square squash squeak squeeze squirrel stable stack stage stair stall stamp stand star stare start starve state station stay steak steal steam steamboat steamer steel steep steeple steer stem step stepping stick sticky stiff still stillness sting stir stitch stock stocking stole stone stood stool stoop stop stopped stopping store stork stories storm stormy story stove straight strange stranger strap straw strawberry stream street stretch string strip stripes strong stuck study stuff stump stung subject such suck sudden suffer sugar suit sum summer sun Sunday
                sunflower sung sunk sunlight sunny sunrise sunset sunshine supper suppose sure surely surface surprise swallow swam swamp swan swat swear sweat sweater sweep sweet sweetness sweetheart swell swept swift swim swimming swing switch sword swore table tablecloth tablespoon tablet tack tag tail tailor take taken taking tale talk talker tall tame tan tank tap tape tar tardy task taste taught tax tea teach teacher team tear tease teaspoon teeth telephone tell temper ten tennis tent term terrible test than thank thanks thankful Thanksgiving that that's the theater thee their them then there these they they'd they'll they're they've thick thief thimble thin thing think third thirsty thirteen thirty this thorn those though thought thousand thread three threw throat throne through throw thrown thumb thunder Thursday thy tick ticket tickle tie tiger tight till time tin tinkle tiny tip tiptoe tire tired title to toad toadstool toast tobacco today toe together toilet told tomato tomorrow ton tone tongue tonight too took tool toot tooth toothbrush toothpick top tore torn toss touch tow toward towards towel tower town toy trace track trade train tramp trap tray treasure treat tree trick tricycle tried trim trip trolley trouble truck true truly trunk trust truth try tub Tuesday tug tulip tumble tune tunnel turkey turn turtle twelve twenty twice twig twin two ugly umbrella uncle under understand underwear undress unfair unfinished unfold unfriendly unhappy unhurt uniform United States unkind unknown unless unpleasant until unwilling up upon upper upset upside upstairs uptown upward us use used useful valentine valley valuable value vase vegetable velvet very vessel victory view village vine violet visit visitor voice vote wag wagon waist wait wake waken walk wall walnut want war warm warn was wash washer washtub wasn't waste watch watchman water watermelon waterproof wave wax way wayside we weak weakness weaken wealth weapon wear weary weather weave web we'd wedding
                Wednesday wee weed week we'll weep weigh welcome well went were we're west western wet we've whale what what's wheat wheel when whenever where which while whip whipped whirl whisky whiskey whisper whistle white who who'd whole who'll whom who's whose why wicked wide wife wiggle wild wildcat will willing willow win wind windy windmill window wine wing wink winner winter wipe wire wise wish wit witch with without woke wolf woman women won wonder wonderful won't wood wooden woodpecker woods wool woolen word wore work worker workman world worm worn worry worse worst worth would wouldn't wound wove wrap wrapped wreck wren wring write writing written wrong wrote wrung yard yarn year yell yellow yes yesterday yet yolk yonder you you'd you'll young youngster your yours you're yourself yourselves youth you've
    
            """.strip()
            if to_lower:
                data = data.lower()
                DaleChallWords.words = set(data.split())
        return DaleChallWords.words


if 1:  # Test routines

    def TestGunningFogIndex():
        raise Exception("Needs to be written")

    def TestCL():
        # Text from # https://en.wikipedia.org/wiki/Coleman%E2%80%93Liau_index
        text = """
            Existing computer programs that measure readability are based
            largely upon subroutines which estimate number of syllables,
            usually by counting vowels. The shortcoming in estimating
            syllables is that it necessitates keypunching the prose into
            the computer.  There is no need to estimate syllables since
            word length in letters is a better predictor of readability
            than word length in syllables.  Therefore, a new readability
            formula was computed that has for its predictors letters per
            100 words and sentences per 100 words. Both predictors can be
            counted by an optical scanning device, and thus the formula
            makes it economically feasible for an organization such as the
            U.S. Office of Education to calibrate the readability of all
            textbooks for the public school system. """
        # The CL index should be (0.0588*537 - 0.296*4.20 - 15.8 = 14.5
        # There are L = letters/words*100 = 537
        # S = sentences/words*100 = 4.20

    def TestText():
        # 49% through Tom Sawyer
        return """About midnight Joe awoke, and called the boys.  There was a brooding
            oppressiveness in the air that seemed to bode something.  The boys
            huddled themselves together and sought the friendly companionship of the
            fire, though the dull dead heat of the breathless atmosphere was
            stifling.  They sat still, intent and waiting.  The solemn hush
            continued.  Beyond the light of the fire everything was swallowed up in
            the blackness of darkness.  Presently there came a quivering glow that
            vaguely revealed the foliage for a moment and then vanished.  By and by
            another came, a little stronger.  Then another.  Then a faint moan came
            sighing through the branches of the forest and the boys felt a fleeting
            breath upon their cheeks, and shuddered with the fancy that the Spirit
            of the Night had gone by.  There was a pause.  Now a weird flash turned
            night into day and showed every little grass-blade, separate and
            distinct, that grew about their feet.  And it showed three white,
            startled faces, too.  A deep peal of thunder went rolling and tumbling
            down the heavens and lost itself in sullen rumblings in the distance.  A
            sweep of chilly air passed by, rustling all the leaves and snowing the
            flaky ashes broadcast about the fire.  Another fierce glare lit up the
            forest and an instant crash followed that seemed to rend the tree-tops
            right over the boys' heads.  They clung together in terror, in the thick
            gloom that followed.  A few big rain-drops fell pattering upon the
            leaves."""

    def Test_GuessSyllables_function():
        """22 Sep 2010 DP:  this function provides a check of the
        GuessSyllables() function's output.  The word_syllables dictionary from
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
        the time and only off by one syllable 16% of the time.  I think
        this is excellent performance for a relatively simple algorithm.
        """
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
            print(i, "%.2f%%" % (100.0 * d[i] / n))


if 1:  # Library functions

    def GunningFogIndex(textinfo):
        """Returns a number indicating the approximate US grade level
        necessary to read a text selection.  See
        https://en.wikipedia.org/wiki/Gunning_fog_index for details.

            - words is the word count
            - sentences is the number of sentences
            - complex_words are words of >= 3 syllables

        The above web page's algorithm says to ignore proper nouns, jargon,
        or compound words.  It also says to ignore common suffixes such as
        -es, -ed, -ing, etc.  I've chosen to ignore this because it would
        require more sophisticated linguistic data, so the measure returned
        here may not match other sources.
        """
        ti = textinfo
        average_sentence_length = ti.words / ti.sentences
        percent_complex_words = 100 * ti.complex_words / ti.words
        return 0.4 * (average_sentence_length + percent_complex_words)


s = TestText()
ti = GetTextInfo(s)
print(GunningFogIndex(ti))
exit()

if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    header = False
    for file in files:
        file_data = open(file).read()
        textinfo = GetTextInfo(file_data)
        if 0:
            print(textinfo)
        if not textinfo.characters:
            t.print(f"{t.err}Error:  No text in '{file}'", file=sys.stderr)
        else:
            if not header:
                PrintHeader()
                header = True
            PrintResults(textinfo, file)
