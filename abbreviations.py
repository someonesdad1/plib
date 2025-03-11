'''

Todo:
    - Harvest from https://en.wikipedia.org/wiki/Lists_of_abbreviations
    
Determine if a string is an English abbreviation (case ignored)
  Use:  from abbreviations import IsAbbreviation
        IsAbbreviation(w: str) -> bool
        
Source:  I put together this list over a period of time from a variety of
searches and manual construction.  The typical method is to search for a
string in text that ends in "." that's not a word in a dictionary.
    
'''
_pgminfo = '''
<oo desc
    Module to help find abbreviations and acronyms and construct a glossary.
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat util oo>
<oo test none oo>
<oo todo oo>
'''
if 1:  # Header
    if 1:  # Imports
        from collections import defaultdict
    if 1:  # Custom imports
        from columnize import Columnize
if 1:  # Utility functions to vet data
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
            print("-" * 70)
            print(f"Missing in '{name}'")
            for line in Columnize(not_found, indent="  "):
                print(line)
    def _CanonicalizeData():
        '''Print IsAbbrevation.data in sorted form.'''
        # Build dictionary keyed by first letter of abbreviation
        items = defaultdict(list)
        for i in sorted(IsAbbreviation.data.split()):
            fl = i[0]
            items[fl].append(i)
        # Print the data
        for fl in items:
            print(" ".join(sorted(items[fl])))
            print()
if 1:  # Core functionality
    def IsAbbreviation(w, no_period=False, full=False):
        '''Returns True if w is an abbreviation; case is ignored.  
    
        no_period:  If True, all '.' characters are removed from w and the abbreviations.
    
        full:  If True the set is enhanced by abbreviations that can also be words that
        end a sentence.
        '''
        if not hasattr(IsAbbreviation, "abbrev"):
            # Cache our set of abbreviation strings
            data = '''
            
                a.c. a.d. a.k.a. a.m. a.s.a.p. abbr. abbrev. abol.  aborig.
                abr. abr. abstr. acad. acc. acct. accts. addr. adj.  adjs.
                adm. admon. adv. advb. amer. anal. anat. annot. anon.  apoc.
                app. appl. approx. appt. apr. apt. arb. arch. assoc.  astr.
                astrol. astron. att. attrib. aug. auth. ave.
                
                b. b.c. b.c.e. b.o. b.t.u. b.y.o.b. betw. bibliog. biochem.
                biog. biogr. biol. bk. bks. blvd. bot. brit. bur.
                
                c. c.e. c.e.o. c.o.d. c.p.u. ca. cal. calc. calif. camb.  cap.
                capt. cath. cent. ceram. cert. certif. cf. ch. chap.  char.
                chas. chem. chr. chron. chronol. circ. cl. cmdr. co.
                col. coll. colloq. com. comm. comp. compl. conc.  concr. conf.
                conj. consol. const. constr. cont. contrib.  conv. convtrov.
                coron. corp. corr. corresp. cp. cpd. cpl.  cr. crim. crit. ct.
                cycl.
                
                d.a. d.c. d.i.y. d.o.a. dan. dat. deb. dec. def. deliv. dem.
                dep. dept. deriv. derog. descr. devel. dial. dict. diff.
                dis. disc. dist. div. dr.
                
                e. e.g. e.s.p. e.t.a. e.v.p. ea. eccl. eccles. ecol. econ.
                ed. educ. edw. electr. elem. emph. encycl. eng. enq. entom.
                equip. esp. esq. est. et.al. et.seq. etc. etym. etymol. euphem.
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
                
                m. m.d. m.p. mach. mag. magn. maj. manuf. mar. masc.  mass.
                meas. mech. med. messrs. mil. min. misc. mlle. mlles.  mme.
                mmes. mo. mon. mr. mrs. ms. mss. mssrs. mt. mtg. myth.
                
                n. n.b. n.e. n.s.w. n.w. n.y. n.z. narr. nat. naut. nav.
                nec. neurol. nom. nov. nucl.
                
                o.d. o.e.d. o.k. o.t. obj. obs. observ. occas. oct. 
                offic. opp. opt. ord. org. orig. oz.
                
                p. p.a. p.e. p.m. p.o. p.s. perf. pers. ph.d.
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
                
                v. v.p. v.r. va. vac. var. vbl. veg. vet. vet. vic.
                viz. voc. vol. vols. vs. vulg.
                
                w. w.c. w.m.d. wed. wk. wkly. wks. writ.
                
                yearbk. yng. yr. yrs.
                
                zeitschr. zool.
                
            '''
            IsAbbreviation.abbrev = set(data.split())
            IsAbbreviation.abbrev_noperiod = set(i.replace(".", "") for i in IsAbbreviation.abbrev)
        if full and not hasattr(IsAbbreviation, "full"):
            # The following abbreviations can also be words that end
            # a sentence; you can exclude them if you wish by setting the
            # keyword full to False.
            s = set(
                '''
                    
                add. admin. am. ann. art. bull. class. conn. dim. fig.
                math. mod. no. off. pa. pass. path. pop. sept. sing. west.
                wed. sat. sun.
                
                '''.split())
            IsAbbreviation.full = s
            IsAbbreviation.full_noperiod = set(i.replace(".", "") for i in s)
        if no_period:
            if full and w.strip().lower() in IsAbbreviation.full_noperiod:
                return True
            return w.strip().lower() in IsAbbreviation.abbrev_noperiod
        else:
            if full and w.strip().lower() in IsAbbreviation.full:
                return True
            return w.strip().lower() in IsAbbreviation.abbrev

if __name__ == "__main__":
    if 1:  # Custom modules
        from lwtest import run, Assert
    def Test_IsAbbreviation():
        f = IsAbbreviation
        Assert(IsAbbreviation("zeitschr."))
        Assert(IsAbbreviation("ZeiTscHr."))
        Assert(IsAbbreviation("ZEITSCHR."))
        Assert(not IsAbbreviation("zzeitschr."))
        # Test full
        Assert(not IsAbbreviation("sun."))
        Assert(IsAbbreviation("sun.", full=True))
        # Test no_period
        Assert(IsAbbreviation("zeitschr", no_period=True))
        Assert(IsAbbreviation("ZeiTscHr", no_period=True))
        Assert(IsAbbreviation("ZEITSCHR", no_period=True))
        Assert(not IsAbbreviation("zzeitschr", no_period=True))
        # Test full
    exit(run(globals(), halt=1)[0])
