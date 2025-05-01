# Usage:
# echo "your sentence here" | python3 autoglosser.py --igtdef <igt file> --biltrans <directory of bilingual transducer> --morph <directory of monolingual transducer>
#
#
#

import subprocess
import sys

# common symbols
gloss = {
    # parts of speech
    "n": ["",""],
    "prn": ["",""],
    "vblex": ["",""],
    "v": ["",""],
    "vaux": ["",""],
    "adj": ["",""],
    "adv": ["",""],
    "adv": ["",""],
    "pr": ["",""],
    "num": ["",""],
    "cnjcoo": ["",""],
    # gender
    "f": ["","F"],
    "m": ["","M"],
    "nt": ["","N"],
    # number
    "sg": ["","SG"],
    "pl": ["","PL"],
    "du": ["","DU"],
    # person
    "p1": ["","1"],
    "p2": ["","2"],
    "p3": ["","3"],
    # pronoun types
    "pers": ["",""],
    "rel": ["","REL"],
    "dem": ["","DEM"],
    "ind": ["","NDEF"],
    "def": ["","DEF"],
    "itg": ["","INT"],
    "pos": ["","POSS"],
    "ref": ["","REFL"],
    # case
    "nom": ["","NOM"],
    "acc": ["","ACC"],
    "dat": ["","DAT"],
    "gen": ["","GEN"],
    "voc": ["","VOC"],
    "abl": ["","ABL"],
    "erg": ["","ERG"],
    "abs": ["","ABS"],
    # TMA
    "pres": ["","PRS"],
    "past": ["","PST"],
    "fut": ["","FUT"],
    "imp": ["","IMP"],
    "impf": ["","NPFV"],
    "perf": ["","PFV"],
    # other stuff
    "inf": ["","INF"],
    "neg": ["","NEG"],
    "ger": ["","GER"]
}

# read the options
igtdef = ""
biltrans = ""
morph = ""
i = 1
while i < len(sys.argv):
    if sys.argv[i] == "--igtdef":
        i += 1
        igtdef = sys.argv[i]
    if sys.argv[i] == "--biltrans":
        i += 1
        biltrans = sys.argv[i]
    if sys.argv[i] == "--morph":
        i += 1
        morph = sys.argv[i]
    i += 1
    
if not igtdef or not biltrans or not morph:
    print("ERROR: options not supplied")
    sys.exit(1)


input_str = sys.stdin.read()
input_str = input_str.strip()
print(input_str)


# print(gloss.get("inf")[1])

# result = subprocess.run("echo \"" + input_t + "\" | apertium -d . wuu-zho-biltrans", shell=True, capture_output=True, text=True)