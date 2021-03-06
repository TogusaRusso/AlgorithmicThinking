"""
Provide code and solution for Application 4
"""

DESKTOP = False

import math
import random
import urllib2

if DESKTOP:
    import matplotlib.pyplot as plt
    import user40_iIrfXkomzJ_9 as student
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

human = "HSGVNQLGGVFVNGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATPEVVSKIAQYKRECPSIFAWEIRDRLLSEGVCTNDNIPSVSSINRVLRNLASEKQQ"
fruitfly = "HSGVNQLGGVFVGGRPLPDSTRQKIVELAHSGARPCDISRILQVSNGCVSKILGRYYETGSIRPRAIGGSKPRVATAEVVSKISQYKRECPSIFAWEIRDRLLQENVCTNDNIPSVSSINRVLRNLAAQKEQQ"
s_m = read_scoring_matrix(PAM50_URL)
consensus = read_protein(CONSENSUS_PAX_URL)

a_m = student.compute_alignment_matrix(human, consensus, s_m, True)
alignment = student.compute_global_alignment(human, consensus, s_m, a_m)
print "Score    :", alignment[0]
print "Human    :", alignment[1]
print "Consensus:", alignment[2]
percent = 0
for i in xrange(len(alignment[1])):
    if alignment[1][i] == alignment[2][i]:
        percent += 1
print "Percent  :", 100.0 * percent / len(alignment[1])

a_m = student.compute_alignment_matrix(fruitfly, consensus, s_m, True)
alignment = student.compute_global_alignment(fruitfly, consensus, s_m, a_m)
print "Score    :", alignment[0]
print "Fruitfly :", alignment[1]
print "Consensus:", alignment[2]
percent = 0
for i in xrange(len(alignment[1])):
    if alignment[1][i] == alignment[2][i]:
        percent += 1
print "Percent  :", 100.0 * percent / len(alignment[1])

       


