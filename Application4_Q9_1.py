"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2
import time

if not DESKTOP:
    import codeskulptor
    codeskulptor.set_timeout(300)
    

# URLs for data files
WORD_LIST_URL = "http://storage.googleapis.com/codeskulptor-assets/assets_scrabble_words3.txt"



###############################################
# provided code


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


def new_keys(word):
    """
    Return set of all conversions of the sets of words
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    replaces   = [a + c + b[1:] for a, b in splits for c in alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in alphabet]
    return set(deletes + replaces + inserts)

def check_spelling(checked_word, dist, word_set):
    """
    Gets checked_word, converts it to set,
    then generates conversions dist times.
    Returns intersection of conversions set and
    dictionary set.
    """
    checked1 = new_keys(checked_word)
    checked2 = set(e2 for e1 in checked1 for e2 in new_keys(e1) if e2 in word_set)
    checked_set= checked1.union(checked2).union(set([checked_word]))
    return list(word_set.intersection(checked_set))

words = set(read_words(WORD_LIST_URL))

timer = time.time()
print check_spelling("humble", 2, words)
print time.time() - timer

timer = time.time()
print check_spelling("firefly", 2, words)
print time.time() - timer
