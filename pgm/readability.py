'''
Calculate readability statistics for a set of files
 
    I use this script to estimate the Flesch-Kincaid US grade level (FKGL)
    for the text files on the command line.  For my own writing, I aim to
    have an FKGL score of <= 8 for general writing and <= 12 for technical
    writing.
 
    Hemingway:  "I write one page of masterpiece to ninety-one pages of
    shit.  I try to put the shit in the wastebasket."
 
    Some references on writing:
        - Malcom Forbes, "How to Write a Business Letter"
        - Edward Thompson, "How to Write Clearly"
        - Kenneth Roman and Joel Raphaelson, "Writing That Works"
        - Strunk & White
        - Chicago Manual of Style


https://en.wikipedia.org/wiki/Readability#Using_the_readability_formulas
    
    Most experts agree that simple readability formulas like Flesch–Kincaid
    grade-level can be highly misleading. Even though the traditional
    features like the average sentence length have high correlation with
    reading difficulty, the measure of readability is much more complex.
    The artificial intelligence, data-driven approach (see above) was
    studied to tackle this shortcoming.

While I recognize the complexity of the task to "measure" readability, the
simplicity of the formulas like those used in this script are attractive
compared to the work needed to generate the AI tools mentioned in the
wikipedia article.

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
        # Calculate readability statistics for a set of files
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import getopt
        import math
        from pathlib import Path as P
        import re
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        import get
        # Load a dictionary of number of syllables if available (otherwise,
        # the number of syllables in each word will be found by the
        # function GuessSyllables.  Using this syllable dictionary speeds
        # this script up by about 4 times.
        try:
            from words_syllables import syllables as S, multiple_syllables as MS
            have_syllable_dict = True
        except ImportError:
            have_syllable_dict = False
    if 1:   # Global variables
        ii = isinstance
        common_abbreviations = set("mr mrs ms dr no mssr st ave".split())
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} file1 [file2...]
          Prints readability statistics for text files.  Use '-' for stdin.
          The Flesch-Kincaid grade level is printed by default for each
          file.  The exponent after the file name is the log of the file
          size rounded up.  Use -h to see more details.
        Options
          -a    Print all statistics
          -C    Colorize the statistics and print color key
          -c    Colorize the statistics
          -d    Turn on debug printing (shows more data)
          -e    Same as -d but uses an abbreviated number form (example:
                2.4³ means 2.4e3)
          -h    Print a manpage
          -p    Print to one decimal place (integer is default)
          -t    Run self-tests
          -z    Print approximate file size in subscripts after name
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Print all statistics
        d["-C"] = False     # Print color key
        d["-c"] = False     # Print in color
        d["-d"] = False     # Debug output
        d["-e"] = False     # Exponent notation
        d["-p"] = False     # Print to 1 decimal place
        d["-t"] = False     # Run self-tests
        d["-z"] = False     # Print file size
        try:
            opts, files = getopt.getopt(sys.argv[1:], "aCcdehptz")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("aCcdeptz"):
                d[o] = not d[o]
            elif o == "-h":
                Manpage()
        if d["-t"]:
            exit(SelfTests())
        if not files:
            Usage(1)
        if d["-C"]:
            d["-c"] = True
        if d["-e"]:
            d["-d"] = True
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
    def Manpage():
        print(dedent(f'''

        This script prints various readability estimates for the text files
        on the command line.  The estimates are
 
            FKGL    Flesch-Kincaid Grade Level
            FRES    Flesch-Kincaid Reading Ease (0-100, 100 easy)
            Fog     Gunning Fog Index
            ARI     Automated Readability Index
            CL      Coleman-Liau Index
            SMOG    SMOG Index
 
        Except for FRES, the estimates are in terms of the US school grade
        level (1-8 is grammar school, 9-12 is high school, 13-16 is college
        and > 16 is post-college-graduate).  The metrics are given as
        integers, which is appropriate since they are approximate
        estimates.  You can see one decimal place with the -p option.
 
        I have standardized on using the FKGL estimate to make decisions
        about readability of my writing.  I've found it to be a good tool
        when used on plain prose with on the order of 1000 words or more.
        Because it's a simple statistic, it's not difficult to construct
        pathological examples.  For example, on the above wikipedia page
        link, run this script on the Proust sentence and the FKGL will be
        233, indicating that this is poor writing from a readability
        standpoint (and the assessment is correct).  If you use it on plain
        ASCII prose in English, it gives good guidance.  
 
        These estimation tools are necessarily simple.  For example, if you
        randomly shuffled the letters in each word and somehow kept the
        number of syllables per word the same (the script uses a heuristic
        to calculate the number of syllables per word), the FKGL statistic
        would stay the same, but the text would be unreadable.
        Nevertheless, I've found the FKGL statistic works well for
        assessing plain prose in ASCII text form.

        If you use the -e option, you can see the characters, words, etc.
        given to 2 significant figures, making easier to estimate other
        statistics.
 
        Some FKGL examples
        ------------------
          E. R. Burroughs
             6 TheMucker.txt
             6 TheOakdaleAffair.txt
          Jane Austen
            12 Emma.txt
            12 Lady_Susan.txt
            13 Love_and_Friendship.txt
            12 Mansfield_Park.txt
            13 Northanger_Abbey.txt
            12 Persuasion.txt
            12 Pride_and_Prejudice.txt
            14 Sense_and_Sensibility.txt
          Agatha Christie
            6 Secret_Adversary.txt
            7 The_Mysterious_Affair_at_Styles.txt
          P. G. Wodehouse
            8 A_man_of_means.txt
            7 Adventures_of_Sally.txt
            7 Damsel_in_distress.txt
            7 Death_at_the_Excelsior.txt
            6 Love_among_the_chickens.txt
            6 My_Man_Jeeves.txt
            7 Psmith_in_the_city.txt
            8 Right_Ho_Jeeves.txt
            6 The_man_with_two_left_feet.txt
          Charles Dickens
             8 A_Christmas_Carol.txt
            10 A_House_to_Let.txt
            12 A_Message_from_the_Sea.txt
            10 A_Tale_of_Two_Cities.txt
            15 All_the_Year_Round.txt
            14 American_Notes.txt
            11 Bardell_v._Pickwick.txt
            11 Barnaby_Rudge.txt
            10 Bleak_House.txt
             9 Captain_Boldheart.txt
            10 David_Copperfield.txt
             9 Doctor_Marigold.txt
            11 Dombey_and_Son.txt
            11 George_Silvermans_Explanation.txt
            12 Great_English_Short-Story_Writers.txt
            11 Great_Expectations.txt
            10 Hard_Times.txt
             9 Holiday_Romance.txt
            10 Hunted_Down.txt
            11 Lazy_Tour_of_Two_Idle_Apprentices.txt
            11 Little_Dorrit.txt
            10 Martin_Chuzzlewit.txt
            14 Master_Humphreys_Clock.txt
            16 Mrs._Lirripers_Legacy.txt
            14 Mudfog_and_Other_Sketches.txt
             9 Mugby_Junction.txt
            13 Nicholas_Nickleby.txt
             9 No_Thoroughfare.txt
            11 Oliver_Twist.txt
            10 Our_Mutual_Friend.txt
            10 Perils_of_Certain_English_Prisoners.txt
            11 Reprinted_Pieces.txt
            15 Sketches_by_Boz.txt
            17 Sketches_of_Young_Couples.txt
            21 Sketches_of_Young_Gentlemen.txt
            12 Some_Christmas_Stories.txt
            11 Somebodys_Luggage.txt
            17 Sunday_under_Three_Heads.txt
             9 The_Battle_of_Life.txt
             8 The_Chimes.txt
             9 The_Cricket_on_the_Hearth.txt
            10 The_Haunted_Man_and_the_Ghosts_Bargain.txt
            12 The_Holly-Tree.txt
            12 The_Lamplighter.txt
            11 The_Lock_and_Key_Library.txt
            12 The_Magic_Fishbone.txt
            12 The_Old_Curiosity_Shop.txt
            12 The_Pickwick_Papers.txt
            12 The_Seven_Poor_Travellers.txt
            14 The_Uncommercial_Traveller.txt
            12 Three_Ghost_Stories.txt
             9 To_Be_Read_at_Dusk.txt
            12 Tom_Tiddlers_Ground.txt
            12 Wreck_of_the_Golden_Mary.txt
          Arthur Conan Doyle
             9 A_Desert_Drama.txt
             8 A_Duet.txt
             9 A_Visit_to_Three_Fronts.txt
             8 Beyond_the_City.txt
             8 Danger_and_Other_Stories.txt
             8 Lock_and_Key_Collection.txt
             8 Lupin_versus_Herlock_Sholmes.txt
            11 Masterpieces_of_Mystery.txt
             9 My_Friend_The_Murderer.txt
            10 pg9504.txt
            10 Rodney_Stone.txt
             8 Round_the_Red_Lamp.txt
             9 Short_stories_Freck_ed.txt
             9 Sir_Nigel.txt
            10 Tales_of_terror_and_mystery.txt
             7 The_Adventures_of_Gerard.txt
             9 The_Cabmans_Story.txt
            10 The_Captain_of_the_Polestar.txt
            12 The_Coming_of_the_Fairies.txt
             9 The_Croxley_Master.txt
             9 The_Dealings_of_Captain_Sharkey.txt
             9 The_Doings_Of_Raffles_Haw.txt
             9 The_Firm_of_Girdlestone.txt
            12 The_German_War.txt
            12 The_Great_Boer_War.txt
             9 The_Great_Keinplatz_Experiment.txt
             9 The_Great_Shadow.txt
             9 The_Green_Flag.txt
             9 The_Gully_of_Bluemansdyke.txt
             8 The_Last_Galley.txt
             9 The_Last_of_the_Legions.txt
             9 The_Man_from_Archangel.txt
            11 The_Mystery_of_Cloomber.txt
            12 The_New_Revelation.txt
             7 The_Parasite.txt
             9 The_Poison_Belt.txt
             9 The_Refugees.txt
            13 The_Vital_Message.txt
            10 The_White_Company.txt
            11 Through_the_Magic_Door.txt
            10 Troubled_marriages.txt
            10 Uncle_Bernac.txt
             9 A_Study_in_Scarlet.txt
             7 Adventure_of_the_Bruce-Partington_Plans.txt
             9 Adventure_of_the_Cardboard_Box.txt
             9 Adventure_of_the_Devils_Foot.txt
             6 Adventure_of_the_Dying_Detective.txt
             7 Adventure_of_the_Red_Circle.txt
             8 Adventure_of_Wisteria_Lodge.txt
             9 Adventures_of_Sherlock_Holmes.txt
             8 His_Last_Bow.txt
             9 Hound_of_the_Baskervilles.txt
             9 Memoirs_of_Sherlock_Holmes.txt
             8 Return_of_Sherlock_Holmes.txt
             8 Sign_of_the_Four.txt
             8 Valley_of_Fear.txt
          Science Fiction
             7 And_Thats_How_It_Was_Officer.txt
            11 Doc_Smith_-_Skylark_Three.txt
            11 Doc_Smith_-_Spacehounds_of_IPC.txt
             7 Doc_Smith_-_Subspace_Survivors.txt
            10 Doc_Smith_-_The_Skylark_of_Space.txt
            10 Doc_Smith_-_The_Vortex_Blaster.txt
            11 Doc_Smith_-_Triplanetary.txt
             6 Old_Rambling_House.txt
             6 Operation_Haystack.txt
             8 The_Time_Machine.txt
             9 The_War_of_the_Worlds.txt
          Mark Twain
            10 A_Connecticut_Yankee_in_King_Arthurs_Court.txt
            14 A_dogs_tale.txt
             9 Adventures_of_Huckleberry_Finn.txt
            10 Best_American_Short_Stories.txt
            10 Eves_diary.txt
            10 Extract_from_Captain_Stormfields_Visit_to_Heaven.txt
            10 Following_the_Equator.txt
            11 How_to_Tell_a_Story_and_Other_Essays.txt
            11 Innocents_Abroad.txt
            11 Life_on_the_Mississippi.txt
            10 Man_that_corrupted_Hadleyburg.txt
             9 Mark_Twains_speeches.txt
            10 Mysterious_Stranger.txt
            11 Personal_recollections_of_Joan_of_Arc.txt
            11 Prince_and_the_Pauper.txt
            10 The_30000_Dollar_Bequest_and_Other_Stories.txt
            10 The_gilded_age.txt
             8 Tom_Sawyer.txt
            10 Tragedy_of_Puddnhead_Wilson.txt
            11 Tramp_Abroad.txt
             8 What_Is_Man_and_Other_Essays.txt
          Jules Verne
             9 A_Journey_to_the_Centre_of_the_Earth.txt
            11 Abandoned.txt
            10 An_Antarctic_Mystery.txt
            11 Around_the_World_in_80_Days.txt
            11 Eight_Hundred_Leagues_on_the_Amazon.txt
            11 From_the_Earth_to_the_Moon.txt
            10 In_Search_of_the_Castaways.txt
            11 In_the_Year_2889.txt
            10 Robur_the_Conqueror.txt
             9 The_Master_of_the_World.txt
             9 The_Mysterious_Island.txt
             9 Twenty_Thousand_Leagues_Under_the_Sea.txt
          Andy Weir
            5 TheMartian.txt
 
            I wondered why "The Martian" had such a low readability score.
            Comparing the output of 'readability.py -e' for the Martian and
            Dickens' "Sunday_under_Three_Heads.txt" showed that the number
            of words per sentence for the Dickens writing was 3.4 times as
            large as the Martian novel:  
 
               Chars  Words CpxWrd OneSyl    Syl   Sent   FKGL 
                4.3⁵   1.0⁵   7.9³   7.1⁴   1.4⁵   9.2³      5 martian.txt
                5.2⁴   1.1⁴   1.3³   7.2³   1.7⁴   3.0²     17 Sunday_under_...

            The ASL for Martian is 1e5/9.2e3 = 10.9 versus 36.7 for Sunday.
            Multiplying by 0.39 to get the grade level (from the FKGL formula), we
            get 4 versus 14, explaining the observed difference.
 
        Other sources
        -------------
 
        https://pypi.org/project/py-readability-metrics
 
        '''))
        exit(0)
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
if 1:   # Core functionality
    def GuessSyllables(word):
        "Guess the number of syllables in a word"
        # Our basic way of guessing is to count the number of vowels
        # in a word.  We then subtract 1 for each diphthong we find,
        # and add 1 for anti-diphthongs (OK, that's probably not the
        # technical term).
        #
        # This function is from the pyflesch.py script written by Seb Bacon,
        # March 29, 2005,  You can find it at
        # http://freshmeat.net/projects/pyflesch/.  Update 10 Nov 2019:  This
        # URL is defunct.
        #
        # As of 3 Nov 2023, a web search turned up
        # https://github.com/sebbacon/pyflesch which uses a database of
        # words with number of syllables.
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
        if have_syllable_dict:
            if word in S:
                num = S[word]
            elif word in MS:
                num = MS[word][0]
            else:
                num = GuessSyllables(word)
        else:
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
        if d["-a"]:
            print(f"{'FRES':>6s}", end=" ")
            print(f"{'Fog':>6s}", end=" ")
            print(f"{'ARI':>6s}", end=" ")
            print(f"{'CL':>6s}", end=" ")
            print(f"{'SMOG':>6s}", end=" ")
        print()
        PrintHeader.hdr = True
    PrintHeader.hdr = False
    def AbbrExp(x, places=1):
        '''Return abbreviated exponential form for a number.  Example:
        The integer 142103 will be returned as 1.3⁵.
        '''
        ss = dict(zip("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
        m, e = f"{x:.{places}e}".split("e")
        k = [m]
        for i in str(int(e)):
            k.append(ss[i])
        u = ''.join(k)
        return u
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
            if d["-e"]:
                # Print abbreviated exponential form
                abbr = [AbbrExp(x) for x in stats]
                print("%7s %6s %6s %6s %6s %6s" % tuple(abbr), end=" ")
            else:
                print("%7d %6d %6d %6d %6d %6d" % tuple(stats), end=" ")
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
        if file == "-":
            sz = stdin_size
            print("<stdin>", end="")
        else:
            sz = get.GetFileSize(file)
            print(file, end="")
        if d["-z"]:  # Append an exponent to estimate the file size
            size = f"{sz:.0e}"
            m, e = size.split("e")
            ss = dict(zip("0123456789e", "₀₁₂₃₄₅₆₇₈₉ₑ"))
            k = [ss[m], ss["e"]]
            for i in str(int(e)):
                k.append(ss[i])
            print(''.join(k), end="")
        print()
        # Print color key if needed
        if d["-C"]:
            d["-c"] = True
            GetColor()
            PrintColorKey()

if __name__ == "__main__":
    d = {}      # Options dictionary
    files = ParseCommandLine(d)
    stdin_size = None
    for file in files:
        if file == "-":
            s = sys.stdin.read()
            stdin_size = len(s)
        else:
            s = open(file).read()
        stats = CountStats(s)
        stats[-1] = stats[-1] if stats[-1] else 1
        PrintResults(stats, file)
