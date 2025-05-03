# Usage:
# echo "your sentence here" | python3 autoglosser.py --igtdef <igt file> --biltrans <bilingual transducer binary file> --morph <directory of monolingual transducer>
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
    "mf": ["",""],
    "nt": ["","N"],
    # number
    "sg": ["","SG"],
    "pl": ["","PL"],
    "sp": ["",""],
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

puncts = ["<sent>", "<cm>", "<lquot>", "<rquot>", "<lpar>", "<rpar>", "<guio>", "<apos>", "<quot>", "<percent>", "lquest", "clb", "punct"]


# read the options

lang = ""
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
    print("Usage:")
    print("echo \"your sentence here\" | python3 autoglosser.py --igtdef <igt file> --biltrans <bilingual transducer binary file> --morph <directory of monolingual transducer>")
    sys.exit(1)

# read the sentence to be glossed

input_str = sys.stdin.read()
input_str = input_str.strip()

result = subprocess.run("echo \"" + input_str + "\" | lt-proc " + morph, shell=True, capture_output=True, text=True)

words = result.stdout.split("$")

for i in range(len(words)):
    if words[i].rfind("/") != -1:
        words[i] = words[i][words[i].rfind("/")+1:]

def is_punctuation(str):
    for t in puncts:
        if t in str:
            return True
    return False

words = [x for x in words if not is_punctuation(x) and not x == '\n']

words_s = []
for i in range(len(words)):
    words_s.append(words[i].split("<"))
    for j in range(1,len(words_s[i])):
        words_s[i][j] = words_s[i][j][:-1]

# print(words)
# print(words_s)

# process stuff

glossed = []
for i in range(len(words_s)):
    glossed_word = ""
    for j in range(len(words_s[i])):
        if j == 0:
            result = subprocess.run("echo \"" + words[i] + "\" | lt-proc " + biltrans, shell=True, capture_output=True, text=True)
            temp = result.stdout[result.stdout.find("/")+1:]
            if temp.find("<") != -1:
                temp = temp[:temp.find("<")]
                glossed_word = temp.replace(" ", "-")
            else:
                glossed_word = "<" + words_s[i][0] + ">"
        else:
            if words_s[i][j] in gloss:
                if gloss.get(words_s[i][j])[0]:
                    glossed_word = gloss.get(words_s[i][j])[0] + "." + glossed_word
                if gloss.get(words_s[i][j])[1]:
                    glossed_word = glossed_word + "." + gloss.get(words_s[i][j])[1]
    #fix some stuff
    glossed_word = glossed_word.replace("1.SG", "1SG")
    glossed_word = glossed_word.replace("2.SG", "2SG")
    glossed_word = glossed_word.replace("3.SG", "3SG")
    glossed_word = glossed_word.replace("1.PL", "1PL")
    glossed_word = glossed_word.replace("2.PL", "2PL")
    glossed_word = glossed_word.replace("3.PL", "3PL")
    glossed.append(glossed_word)

# output

for i in range(len(words_s)):
    print(words_s[i][0] + " ", end='')

print()

for i in range(len(words_s)):
    print(glossed[i] + " ", end='')

print()
