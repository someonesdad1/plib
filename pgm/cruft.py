"""
Generate n sentences of gibberish
    Python implementation of consult-o-matic at http://hewgill.com/.

    Example output:
        Of course, the highly factual report is further compounded when
        taking into account the subsystem compatibility testing.
        Similarly, the incorporation of additional mission constraints
        greatly reduces the complexity of the total system rationale.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Python script to generate meaningless gibberish
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import sys
    import textwrap
    from random import choice as ch
if 1:  # Custom imports
    from wrap import dedent, wrap
if 1:  # Global variables
    e1 = (
        "In particular,",
        "On the other hand,",
        "However,",
        "Similarly,",
        "As a resultant implication,",
        "In this regard,",
        "Based on integral subsystem considerations,",
        "For example,",
        "Thus,",
        "With respect to specific goals,",
        "Interestingly enough,",
        "Without going into the technical details,",
        "Of course,",
        "To approach true user-friendliness,",
        "In theory,",
        "It is assumed that",
        "Conversely,",
        "We can see, in retrospect,",
        "It is further assumed that",
        "Further,",
        "In summary,",
        "It should be noted that",
        "To further describe and annotate,",
        "Specifically,",
        # My additions
        "Not withstanding negative thinking,",
        "Should a level 8 approach be inappropriate,",
        "Forgetting for a moment our logic,",
        "Though highly interesting,",
        "Though somewhat abstract,",
        "In a somewhat contravariant viewpoint,",
        "In actual fact,",
    )
    e2 = (
        "a large proportion of interface coordination communication",
        "a constant flow of effective communication",
        "the characterization of specific criteria",
        "initiation of critical subsystem development",
        "the fully integrated test program",
        "the product configuration baseline",
        "any associated supporting element",
        "the incorporation of additional mission constraints",
        "the independent functional principle",
        "the interrelation of system and/or subsystem technologies",
        "the product assurance architecture",
        # My additions
        "a number of the alternative hypotheses",
        "the legerdemain of the true genius",
        "the highly factual report",
        "the dimly-seen goal",
    )
    e3 = (
        "must utilize and be functionally interwoven with",
        "maximizes the probability of project success, yet minimizes cost and",
        "increases time required for",
        "adds explicit performance limits to",
        "necessitates that urgent consideration be applied to",
        "requires considerable systems analysis and trade-off studies to arrive at",
        "is further compounded when taking into account",
        "presents extremely interesting challenges to",
        "recognizes other systems' importance and the necessity for",
        "effects a significant implementation of",
        "adds overriding performance constraints to",
        "mandates staff-meeting-level attention to",
        "is functionally equivalent and parallel to",
        # My additions
        "increases the space required for",
        "increases the money required for",
        "reduces the space required for",
        "reduces the money required for",
        "allows total commitment to",
        "reduces the complexity of",
        "greatly reduces the complexity of",
        "somewhat reduces the complexity of",
        "increases the complexity of",
        "greatly increases the complexity of",
        "somewhat increases the complexity of",
    )
    e4 = (
        "the sophisticated hardware.",
        "the anticipated fourth-generation equipment.",
        "the subsystem compatibility testing.",
        "the structural design, based on system engineering concepts.",
        "the preliminary qualification limit.",
        "the evolution of specifications over a given time period.",
        "the philosophy of commonality and standardization.",
        # "the greater fight-worthiness concept.",
        "any discrete configuration mode.",
        "the management-by-contention principle.",
        "the total system rationale.",
        "possible bidirectional logical relationship approaches.",
        "the postulated use of dialog management technology.",
        "the overall negative profitability.",
        # My additions
        "the overall positive profitability.",
        "the slavish use of resources.",
        "the arcane technologies required.",
        "numerous alternative approaches.",
        "the canonical and well-accepted approach.",
        "a rigorous truth overlooked by the majority.",
        "a rigorous falsehood missed by most people.",
        "the complex social impedance.",
        "the ornithated transductor architecture.",
        "the negative impedance converter.",
        "an empirically-driven approach.",
        "an analytical formulation.",
        "a classical problem-solving approach.",
        "a parametric social-dynamics approach.",
        "a non-parametric socio-economic approach.",
    )
if 1:  # Utility

    def Usage(d, status=1):
        name = sys.argv[0]
        print(
            dedent(f"""
    Usage:  {name} [options] n
      Generate n sentences of gibberish.
    """)
        )
        exit(status)

    def ParseCommandLine(d):
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o in ("-h", "--help"):
                Usage(d, status=0)
        if not args:
            Usage(d, status=1)
        return int(args[0])


if __name__ == "__main__":
    d = {}  # Options dictionary
    n = ParseCommandLine(d)
    result = []
    for i in range(n):
        result.append(" ".join([ch(e1), ch(e2), ch(e3), ch(e4)]))
    print(wrap(" ".join(result)))
