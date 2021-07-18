'''
A "personality" test that someone emailed me.
    I have no idea where it originated.  The questions and answers are
    rot13 encoded so you can't easily peek at them.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import random
    import codecs
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    questions = (
        (
            "Jura qb lbh srry lbhe orfg?",
            (
                "Va gur zbeavat",
                "Qhevat gur nsgreabba naq rneyl riravat",
                "Yngr ng avtug"
            ),
            (2, 4, 6)
        ),
        (
            "Lbh hfhnyyl jnyx",
            (
                "snveyl snfg, jvgu ybat fgrcf",
                "snveyl snfg, ohg jvgu fubeg, dhvpx fgrcf",
                "yrff snfg, urnq hc, ybbxvat gur jbeyq va gur snpr",
                "yrff snfg, urnq qbja"
                "irel fybjyl"
            ),
            (6, 4, 7, 2, 1)
        ),
        (
            "Jura gnyxvat gb crbcyr, lbh",
            (
                "fgnaq jvgu lbhe nezf sbyqrq",
                "unir lbhe unaqf pynfcrq",
                "unir bar be obgu lbhe unaqf ba lbhe uvcf",
                "gbhpu be chfu gur crefba gb jubz lbh ner gnyxvat",
                "cynl jvgu lbhe rne, gbhpu lbhe puva, be fzbbgu lbhe unve"
            ),
            (4, 2, 5, 7, 6)
        ),
        (
            "Jura erynkvat, lbh fvg jvgu",
            (
                "lbhe xarrf orag naq lbhe yrtf arngyl fvqr ol fvqr",
                "lbhe yrtf pebffrq",
                "lbhe yrtf fgergpurq bhg be fgenvtug",
                "jvgu bar yrt pheyrq haqre lbh"
            ),
            (4, 6, 2, 1)
        ),
        (
            "Jura fbzrguvat ernyyl nzhfrf lbh, lbh ernpg jvgu",
            (
                "n ovt, nccerpvngvir ynhtu",
                "n ynhtu, ohg abg n ybhq bar",
                "n dhvrg puhpxyr",
                "n furrcvfu fzvyr"
            ),
            (6, 4, 3, 2)
        ),
        (
            "Jura lbh tb gb n cnegl be fbpvny tngurevat, lbh",
            (
                "znxr n ybhq ragenapr fb rirelbar abgvprf lbh",
                "znxr n dhvrg ragenapr, ybbxvat nebhaq sbe fbzrbar lbh xabj",
                "znxr dhvrgrfg ragenapr cbffvoyr naq gel gb fgnl haabgvprq"
            ),
            (6, 4, 2)
        ),
        (
            "Lbh ner jbexvat uneq, pbapragengvat uneq. Lbh ner\n" +
            "     vagreehcgrq. Lbh:",
            (
                "jrypbzr gur oernx",
                "srry rkgerzryl veevgngrq",
                "inel orgjrra gurfr gjb rkgerzrf"
            ),
            (6, 2, 4)
        ),
        (
            "Juvpu bs gur sbyybjvat pbybef qb lbh yvxr zbfg?",
            (
                "erq be benatr",
                "oynpx",
                "lryybj be yvtug oyhr",
                "terra",
                "qnex oyhr be checyr",
                "juvgr",
                "oebja be tenl"
            ),
            (6, 7, 5, 4, 3, 2, 1)
        ),
        (
            "Jura lbh ner va orq ng avtug, va gubfr ynfg srj\n" +
            "     zbzragf orsber tbvat gb fyrrc, lbh yvr",
            (
                "fgergpurq bhg ba lbhe onpx",
                "fgergpurq bhg snpr qbja ba lbhe fgbznpu",
                "ba lbhe fvqr, fyvtugyl pheyrq",
                "jvgu lbhe urnq ba bar nez",
                "jvgu lbhe urnq haqre gur pbiref"
            ),
            (7, 6, 4, 2, 1)
        ),
        (
            "Lbh bsgra qernz gung lbh ner",
            (
                "snyyvat",
                "svtugvat be fgehttyvat",
                "frnepuvat sbe fbzrguvat be fbzrobql",
                "sylvat be sybngvat",
                "Lbh hfhnyyl unir n qernzyrff fyrrc",
                "Lbhe qernzf ner nyjnlf cyrnfnag"
            ),
            (4, 2, 3, 5, 5, 1)
        ),
    )
    analyses = (
        (
            (61, 100),
    '''Bguref frr lbh nf fbzrbar gurl fubhyq "unaqyr jvgu  pner."
    Lbh ner bsgra frra nf inva, frys-pragrerq, naq rkgerzryl
    qbzvanag.  Bguref znl nqzver lbh naq jvfu gurl pbhyq or zber
    yvxr lbh, ohg gurl qba'g nyjnlf gehfg lbh naq urfvgngr gb
    orpbzr gbb qrrcyl vaibyirq jvgu lbh.'''
        ),
        (
            (51, 60),
    '''Lbhe sevraqf frr lbh nf na rkpvgvat, uvtuyl ibyngvyr, engure
    vzchyfvir crefbanyvgl; n angheny yrnqre, dhvpx gb znxr
    qrpvfvbaf (gubhtu abg nyjnlf gur evtug barf).  Gurl frr lbh
    nf obyq naq iragherfbzr, fbzrbar jub jvyy gel na nqiragher.
    Gurl rawbl orvat va lbhe pbzcnal orpnhfr bs gur rkpvgrzrag
    lbh enqvngr.'''
        ),
        (
            (41, 50),
    '''Bguref frr lbh nf serfu, yviryl, punezvat, nzhfvat,
    cenpgvpny, naq nyjnlf vagrerfgvat; fbzrbar jub vf pbafgnagyl
    gur pragre bs nggragvba, ohg fhssvpvragyl jryy-onynaprq abg
    gb yrg vg tb gb lbhe urnq.  Gurl frr lbh nyfb nf xvaq,
    pbafvqrengr, naq haqrefgnaqvat; fbzrbar jub jvyy purre gurz
    hc naq uryc gurz bhg.'''
        ),
        (
            (31, 40),
    '''Bgure crbcyr frr lbh nf frafvoyr, pnhgvbhf, pnershy, naq
    cenpgvpny. Gurl frr lbh nf pyrire, tvsgrq, be gnyragrq, ohg
    zbqrfg. Abg n crefba jub znxrf sevraqf gbb dhvpxyl be gbb
    rnfvyl, ohg fbzrbar jub vf rkgerzryl yblny gb gur sevraqf
    lbh qb znxr naq jub rkcrpgf gur fnzr yblnygl va erghea.
    Gubfr jub ernyyl trg gb xabj lbh ernyvmr gung vg gnxrf n ybg
    gb funxr lbhe gehfg va lbhe sevraqf, ohg, rdhnyyl, gung vg
    gnxrf lbh n ybat gvzr gb trg bire vg vs gung gehfg vf
    oebxra.'''
        ),
        (
            (21, 30),
    '''Lbhe sevraqf frr lbh nf cnvafgnxvat naq shffl.  Gurl frr lbh
    nf irel, irel pnhgvbhf naq rkgerzryl pnershy, n fybj naq
    fgrnql cybqqre.  Vg jbhyq ernyyl fhecevfr gurz vs lbh rire
    qvq fbzrguvat vzchyfviryl be ba gur fche bs gur zbzrag. Gurl
    rkcrpg lbh gb rknzvar  rirelguvat pnershyyl sebz rirel fvqr
    naq gura, hfhnyyl qrpvqr ntnvafg vg. Gurl guvax guvf
    ernpgvba ba lbhe cneg vf pnhfrq cnegyl ol lbhe pnershy
    angher naq cnegyl ol ynmvarff.'''
        ),
        (
            (0, 20),
    '''Crbcyr guvax lbh ner ful, areibhf, naq vaqrpvfvir, fbzrbar
    jub arrqf gb or ybbxrq nsgre, jub nyjnlf jnagf fbzrbar ryfr
    gb znxr gur qrpvfvbaf naq jub qbrfa'g jnag gb trg vaibyirq
    jvgu nalbar be nalguvat.  Gurl frr lbh nf n jbeevre, jub
    frrf ceboyrzf gung qba'g rkvfg. Fbzr crbcyr guvax lbh'er
    obevat.  Bayl gur crbcyr jub xabj lbh jryy xabj gung lbh
    nera'g.'''
        ),
    )
    Letters = ("a", "b", "c", "d", "e", "f", "g")
def Print(s):
    print(codecs.decode(s, "rot13"))
def PrintQuestion(question_index, count):
    letters = []
    for char in Letters:
        letters.append(codecs.decode(char, "rot13"))
    question, answers, weights = questions[question_index]
    Print("%2d.  %s" % (count, question))
    for index in range(len(answers)):
        Print("       (%c) %s" % (letters[index], answers[index]))
def UpdateScore(answer, question_index, score):
    question, answers, weights = questions[question_index]
    return score + weights[answer]
def GetAnswer(question_index):
    question, answers, weights = questions[question_index]
    letters = Letters[:len(answers)]
    while True:
        try:
            answer = input("-> ").lower()
        except Exception:
            print()
            exit(1)
        if answer not in letters:
            print("   Not a valid answer -- try again")
            continue
        else:
            for i in range(len(letters)):
                if answer == letters[i]:
                    return i
            raise "Logic error"
def PrintResults(score):
    print()
    for index in range(len(analyses)):
        low, high = analyses[index][0]
        analysis = analyses[index][1]
        if score >= low and score <= high:
            print("Score =", score)
            Print(analysis)
            return
    raise Exception("Score didn't match anything")
if __name__ == "__main__": 
    count = 1
    indices = list(range(0, len(questions)))
    random.shuffle(indices)
    score = 0
    for index in indices:
        PrintQuestion(index, count)
        if 1:
            answer = GetAnswer(index)
        else:
            # Use for testing
            answer = 0
        score = UpdateScore(answer, index, score)
        count += 1
    PrintResults(score)
