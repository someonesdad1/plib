'''
IsAbbreviation(w: str) -> bool
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Provides the function IsAbbreviation() which will return True if the 
    # string argument is an abbreviation.  Case is ignored.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass

if 1:   # Imports
    from collections import defaultdict
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from columnize import Columnize
def IsAbbreviation(w):
    'Returns True if w is an abbreviation; case is ignored'
    if not hasattr(IsAbbreviation, "abbrev"):
        IsAbbreviation.data = '''

            a.c. a.d. a.k.a. a.m. a.s.a.p. abbr. abbr. abbrev. abol.
            aborig. abr. abr. abstr. acad. acc. acct. accts. addr. adj.
            adjs. adm. admon. adv. advb. amer. anal. anat. annot. anon.
            apoc. app. appl. approx. appt. apr. apt. arb. arch. assoc.
            astr. astrol. astron. att. attrib. aug. auth. ave.

            b. b.c. b.c.e. b.o. b.t.u. b.y.o.b. betw. bibliog. biochem.
            biog. biogr. biol. bk. bks. blvd. bot. brit. bur.

            c. c.e. c.e.o. c.o.d. c.p.u. ca. cal. calc. calif. camb.
            cap. capt. cath. cent. ceram. cert. certif. cf. ch. chap.
            char. chas. chem. chr. chron. chronol. circ. cl. class.
            cmdr. co. col. coll. colloq. com. comm. comp. compl. conc.
            concr. conf. conj. consol. const. constr. cont. contrib.
            conv. convtrov. coron. corp. corp. corr. corresp. cp. cpd.
            cpl. cr. crim. crit. ct. cycl.

            d.a. d.c. d.i.y. d.o.a. dan. dat. deb. dec. def. deliv. dem.
            dep. dept. deriv. derog. descr. devel. dial. dict. diff.
            dis. disc. dist. div. dr.

            e. e.g. e.s.p. e.t.a. e.v.p. ea. eccl. eccles. ecol. econ.
            ed. educ. edw. electr. elem. emph. encycl. eng. enq. entom.
            equip. esp. est. et.al. et.seq. etc. etym. etymol. euphem.
            eval. exc. exch. exec. exper.

            f. f.b.i. fab. fam. famil. feb. fem. ff. fl. floz. fr. freq.
            fri. fut.

            g.i. gal. gen. geo. geog. geogr. geol. geom. ger. gov. govt.
            gr.

            h. h.p. handbk. hebr. hist. hort. hosp. hr. hrs. hydrol.

            i.d. i.e. i.q. i.u.d. ib. ibid. illustr. impt. inc. ind.
            indef. indir. industr. infl. inorg. inq. inst. instr. intr.
            intro. introd. inv. invoc. ir. irreg. ital.

            j.d. jan. jap. jr. jrnl. jud. judg. jul. jun. jurisd.
            jurispr.

            l. lab. lang. langs. lat. lb. lbf. lett. lex. libr. lit. ll.
            ln. lt. ltd.

            m. m. m.d. m.p. mach. mag. magn. maj. manuf. mar. masc.
            mass. meas. mech. med. messrs. mil. min. misc. mlle. mlles.
            mme. mmes. mo. mon. mr. mrs. ms. mss. mssrs. mt. mtg. myth.

            n. n.b. n.e. n.s.w. n.w. n.y. n.z. narr. nat. naut. nav.
            nec. neurol. nom. nov. nucl.

            o.d. o.e.d. o.k. o.t. obj. obs. observ. occas. oct. off.
            offic. opp. opt. ord. org. orig. oz.

            p. p.a. p.e. p.m. p.o. p.s. pass. path. perf. pers. ph.d.
            pharm. phil. philos. phys. pict. pl. plur. pm. poet. pol.
            polit. poss. posth. postm. pp. ppb. ppl. ppm. pr. pract.
            prec. pred. pref. prep. pres. pres. prim. princ. priv. prob.
            prob. proc. prod. prof. pron. prop. prov. pt. pt. publ. pvt.

            q. q.e.d. q.v. qt. quot.

            r. r.a.f. r.c. r.n. r.s.v.p. rad. rd. re. rec. ref. rel.
            rep. repr. ret. rev.

            s. s.e. s.t.p. s.u.v. s.v. s.v.p. s.w. s.w. sat. sci. sep.
            sess. sgt. sim. soc. sp. spec. sr. ss. st. st. stat. str.
            subj. subord. subscr. subst. symp. syst.

            t. t.b. taxon. techn. technol. tel. telegr. teleph. temp.
            theol. thu. tr. trad. trans. transl. trav. treas. trib.
            trig. trop. tue. typog.

            u.k. u.s. u.s.a. u.s.a.f. u.s.c.g. u.s.m.c. u.s.n. u.s.s.r.
            univ. unkn. unoffic. usu.

            v. v.p. v.p. v.r. va. vac. var. vbl. veg. vet. vet. vic.
            viz. voc. vol. vols. vs. vulg.

            w. w.c. w.m.d. wed. wk. wkly. wks. writ.

            yearbk. yng. yr. yrs.

            zeitschr. zool.

        '''
        IsAbbreviation.abbrev = set(IsAbbreviation.data.split())
        if 1:
            # The following abbreviations can also be words that end
            # a sentence; you can exclude them if you wish.
            IsAbbreviation.abbrev.update(set('''
                add. admin. am. ann. art. bull. conn. dim. fig. math. mod.
                no. pa. pop. sept. sing. west. wed. sat. sun.
            '''.split()))
    return w.strip().lower() in IsAbbreviation.abbrev
IsAbbreviation("")      # Load IsAbbreviation.abbrev
if 1:   # Utility functions to vet data
    def _Missing(name, s):
        '''Print out abbreviations from s that are missing from
        IsAbbreviation.abbrev.
        '''
        not_found = []
        for line in s.strip().split("\n"):
            abbr = line.split("|")[0].strip().lower()
            if not abbr.endswith("."):
                continue
            if abbr not in IsAbbreviation.abbrev:
                not_found.append(abbr)
        if not_found:
            print("-"*70)
            print(f"Missing in '{name}'")
            for line in Columnize(not_found, indent="  "):
                print(line)
    def _CanonicalizeData():
        '''Print IsAbbrevation.data in sorted form.
        '''
        # Build dictionary keyed by first letter of abbreviation
        items = defaultdict(list)
        for i in sorted(IsAbbreviation.data.split()):
            fl = i[0]
            items[fl].append(i)
        # Print the data
        for fl in items:
            print(' '.join(sorted(items[fl])))
            print()
if __name__ == "__main__": 
    if 1:   # Custom modules
        from wrap import dedent
        from lwtest import run, raises, assert_equal, Assert
    def Test_IsAbbreviation():
        f = IsAbbreviation
        Assert(f("zeitschr."))
        Assert(f("ZeiTscHr."))
        Assert(f("ZEITSCHR."))
        Assert(not f("zzeitschr."))
    exit(run(globals(), halt=1)[0])
