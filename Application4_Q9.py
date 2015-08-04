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


def new_keys(word_set):
    """
    Return set of all conversions of the sets of words
    """
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    conv = set([])
    for word in word_set:
        for pos in xrange(len(word) + 1):
            conv.add(word[:pos] + word[pos+1:])
            for char in alphabet:
                conv.add(word[:pos] + char + word[pos+1:])
                conv.add(word[:pos] + char + word[pos:])
    return conv


def check_spelling(checked_word, dist, word_set):
    """
    Gets checked_word, converts it to set,
    then generates conversions dist times.
    Returns intersection of conversions set and
    dictionary set.
    """
    checked_set = set([checked_word])
    for _ in xrange(dist):
        checked_set = new_keys(checked_set)
    return list(word_set.intersection(checked_set))

words = set(read_words(WORD_LIST_URL))

timer = time.time()
check_spelling("humble", 2, words)
print "humble", time.time() - timer
timer = time.time()
check_spelling("firefly", 2, words)
print "firefly", time.time() - timer
timer = time.time()
check_spelling("fireflyfosjfoijsfoidsj", 2, words)
print "fireflyfosjfoijsfoidsj ", time.time() - timer
