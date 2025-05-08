# Usage:
# echo "your sentence here" | python3 autoglosser.py --igtdef <igt file> --inputlang <ISO code>  --glosslang <ISO code> --biltrans <bilingual transducer directory>
#
#
#

import subprocess
import sys
from itertools import combinations

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
    "f": ["",".F"],
    "m": ["",".M"],
    "mf": ["",""],
    "nt": ["",".N"],
    # person number
    "p1.sg": ["",".1SG"],
    "p2.sg": ["",".2SG"],
    "p3.sg": ["",".3SG"],
    "p1.pl": ["",".1PL"],
    "p2.pl": ["",".2PL"],
    "p3.pl": ["",".3PL"],
    # pronoun types
    "pers": ["",""],
    "rel": ["",".REL"],
    # "dem": ["",".DEM"],
    "ind": ["",".NDEF"],
    "def": ["",".DEF"],
    "itg": ["",".INT"],
    "pos": ["",".POSS"],
    "ref": ["",".REFL"],
    # case
    "nom": ["",".NOM"],
    "acc": ["",".ACC"],
    "dat": ["",".DAT"],
    "gen": ["",".GEN"],
    "voc": ["",".VOC"],
    "abl": ["",".ABL"],
    "erg": ["",".ERG"],
    "abs": ["",".ABS"],
    # TMA
    "pres": ["",".PRS"],
    "past": ["",".PST"],
    "fut": ["",".FUT"],
    "imp": ["",".IMP"],
    "impf": ["",".NPFV"],
    "perf": ["",".PFV"],
    # other stuff
    "inf": ["",".INF"],
    "neg": ["",".NEG"],
    "ger": ["",".GER"]
}

puncts = ["sent", "cm", "lquot", "rquot", "lpar", "rpar", "guio", "apos", "quot", "percent", "lquest", "clb", "punct"]


# read the options

input_lang = ""
gloss_lang = ""
igtdef = ""
biltrans = ""
i = 1
while i < len(sys.argv):
    if sys.argv[i] == "--igtdef":
        i += 1
        igtdef = sys.argv[i]
    if sys.argv[i] == "--biltrans":
        i += 1
        biltrans = sys.argv[i]
    if sys.argv[i] == "--inputlang":
        i += 1
        input_lang = sys.argv[i]
    if sys.argv[i] == "--glosslang":
        i += 1
        gloss_lang = sys.argv[i]
    i += 1
    
if not biltrans or not input_lang or not gloss_lang:
    print("ERROR: options not supplied")
    print("Usage:")
    print("echo \"your sentence here\" | python3 autoglosser.py --igtdef <igt file> --inputlang <ISO code>  --glosslang <ISO code> --biltrans <bilingual transducer directory>")
    sys.exit(1)

# read igt file

if igtdef:
    f = open(igtdef)
    for x in f:
        line = x.split()
        if line[0] != "lemma":
            if line[0] == "-":
                line[0] = ""
            if line[1] == "-":
                line[1] = ""
            if line[2] == "-":
                line[2] = ""
            if line[3] == "-":
                line[3] = ""
            if line[4] == "-":
                line[4] = ""
            if not line[0] and not line[1]:
                gloss.update({line[2] : [line[3], line[4]]})
            elif not line[0] and not line[2]:
                gloss.update({line[1] : [line[3], line[4]]})
            elif not line[1] and not line[2]:
                gloss.update({line[0] : [line[3], line[4]]})
            elif not line[0]:
                gloss.update({line[1]+"."+line[2] : [line[3], line[4]]})
            elif not line[1]:
                gloss.update({line[0]+"."+line[2] : [line[3], line[4]]})
            elif not line[2]:
                gloss.update({line[0]+"."+line[1] : [line[3], line[4]]})
            else:
                gloss.update({line[0]+"."+line[1]+"."+line[2] : [line[3], line[4]]})

# read the sentence to be glossed

input_str = sys.stdin.read()
input_str = input_str.strip()

result = subprocess.run("echo \"" + input_str + "\" | apertium -d " + biltrans + " " + input_lang + "-" + gloss_lang + "-biltrans", shell=True, capture_output=True, text=True)

words = result.stdout.split("$")

tags = []
glossed = []

for i in range(len(words)):
    tags.append(words[i][words[i].find("^")+1:words[i].find("/")-1].lower())
    tags[i] = tags[i].replace(">","")
    glossed.append(words[i][words[i].find("/")+1:].lower())
    glossed[i] = glossed[i][:glossed[i].find("<")]


def is_punctuation(str):
    for t in puncts:
        if t in str:
            return True
    return False


i = 0
while i < len(tags):
    if is_punctuation(tags[i]) or not tags[i]:
        del tags[i]
        del glossed[i]
        i -= 1
    i += 1

tags_s = []
for i in range(len(tags)):
    tags_s.append(tags[i].split("<"))
    tags_s[i][0] = tags_s[i][0].replace(" ","-")
    glossed[i] = glossed[i].replace(" ","-")

# print(words)
# print(tags)
print(tags_s)
print(glossed)

# sys.exit(0)


# process stuff

def get_sublists(lst):
    lst.reverse()
    res = [list(combinations(lst, r)) for r in range(1, len(lst) + 1)]
    res = [list(sublist) for g in res for sublist in g]
    ans = []
    for x in res:
        sbl2str = ""
        for k in x:
            sbl2str = k + "." + sbl2str
        ans.append(sbl2str[:-1])
    ans.reverse()
    lst.reverse()
    return ans

def remove_processed(lst,str):
    items = str.split(".")
    for x in items:
        lst.remove(x)

for i in range(len(glossed)):
    #other stuff
    stuff = tags_s[i]
    while stuff:
        sbl = get_sublists(stuff)
        stop = True
        for j in sbl:
            if j in gloss:
                if gloss.get(j)[0]:
                    glossed[i] = gloss.get(j)[0] + glossed[i]
                if gloss.get(j)[1]:
                    glossed[i] = glossed[i] + gloss.get(j)[1]
                remove_processed(stuff,j)
                stop = False
                break
        if stop:
            break
    #fix some stuff
    glossed[i] = glossed[i].replace("1.SG", "1SG")
    glossed[i] = glossed[i].replace("2.SG", "2SG")
    glossed[i] = glossed[i].replace("3.SG", "3SG")
    glossed[i] = glossed[i].replace("1.PL", "1PL")
    glossed[i] = glossed[i].replace("2.PL", "2PL")
    glossed[i] = glossed[i].replace("3.PL", "3PL")
    glossed[i] = glossed[i].replace("][", ".")

# output

# for i in range(len(tags_s)):
#     print(tags_s[i][0] + " ", end='')

# print()

print(input_str)

for i in range(len(glossed)):
    print(glossed[i] + " ", end='')

print()

