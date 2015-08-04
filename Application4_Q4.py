"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2

if DESKTOP:
    import matplotlib.pyplot as plt
    import Project4 as student
else:
    import simpleplot
    import user40_iIrfXkomzJ_9 as student
    import codeskulptor
    codeskulptor.set_timeout(300)
    

# URLs for data files
PAM50_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_PAM50.txt"
HUMAN_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_HumanEyelessProtein.txt"
FRUITFLY_EYELESS_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_FruitflyEyelessProtein.txt"
CONSENSUS_PAX_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_ConsensusPAXDomain.txt"
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code

def read_scoring_matrix(filename):
    """
    Read a scoring matrix from the file named filename.  

    Argument:
    filename -- name of file containing a scoring matrix

    Returns:
    A dictionary of dictionaries mapping X and Y characters to scores
    """
    scoring_dict = {}
    scoring_file = urllib2.urlopen(filename)
    ykeys = scoring_file.readline()
    ykeychars = ykeys.split()
    for line in scoring_file.readlines():
        vals = line.split()
        xkey = vals.pop(0)
        scoring_dict[xkey] = {}
        for ykey, val in zip(ykeychars, vals):
            scoring_dict[xkey][ykey] = int(val)
    return scoring_dict




def read_protein(filename):
    """
    Read a protein sequence from the file named filename.

    Arguments:
    filename -- name of file containing a protein sequence

    Returns:
    A string representing the protein
    """
    protein_file = urllib2.urlopen(filename)
    protein_seq = protein_file.read()
    protein_seq = protein_seq.rstrip()
    return protein_seq


def read_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    # load assets
    word_file = urllib2.urlopen(filename)
    
    # read in files as string
    words = word_file.read()
    
    # template lines and solution lines list of line string
    word_list = words.split('\n')
    print "Loaded a dictionary with", len(word_list), "words"
    return word_list

def generate_null_distribution(seq_x, seq_y, scoring_matrix, num_trials):
    scoring_distribution = {}
    for i in xrange(num_trials):
        rand_y = list(seq_y)
        random.shuffle(rand_y)
        a_m = student.compute_alignment_matrix(seq_x, rand_y, scoring_matrix, False)
        alignment = student.compute_local_alignment(seq_x, rand_y, scoring_matrix, a_m)
        score = alignment[0]
        scoring_distribution[score] = scoring_distribution.get(score, 0) + 1
        print i
        #print alignment[1]
        #print alignment[2]
    return scoring_distribution

human = read_protein(HUMAN_EYELESS_URL)
fruitfly = read_protein(FRUITFLY_EYELESS_URL)
s_m = read_scoring_matrix(PAM50_URL)

distribution = generate_null_distribution(human, fruitfly, s_m, 1000)
print distribution
d_l = distribution.items()
x_l = []
y_l = []
x_t = []
bar_width = 1
for v in d_l:
    x_l.append(v[0])
    y_l.append(v[1] / 1000.0)
    x_t.append(v[0] + bar_width / 2)


plot = plt.bar(x_l, y_l, bar_width)
#plot = plt.hist(x_l)
plt.title("Normilized scores distribution")
plt.ylabel("Fraction on total trials (N = 1000)")
plt.xlabel("Scores of local alignment")
#plt.xticks(x_t, x_l)
plt.show()
