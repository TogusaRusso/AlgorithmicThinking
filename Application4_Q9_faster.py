"""
Provide code and solution for Application 4
"""

DESKTOP = True

import math
import random
import urllib2
import time
import Project4 as student

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
    conv = {}
    for word in word_set:
        for pos in xrange(len(word) + 1):
            keyword = word[:pos] + word[pos+1:]
            conv[keyword] = conv.get(keyword, set([word]))
            conv[keyword].add(word)
    return conv

def new_keys_dict(word_dict):
    """
    Return set of all conversions of the sets of words
    """
    conv = {}
    for word in word_dict.keys():
        for pos in xrange(len(word) + 1):
            keyword = word[:pos] + word[pos+1:]
            conv[keyword] = conv.get(keyword, set([]))
            conv[keyword].update(word_dict[word])
    return conv

def distance(word1, word2, s_m):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    a_m = student.compute_alignment_matrix(word1, word2, s_m, True)
    score = student.compute_global_alignment(word1, word2, s_m, a_m)
    changes = len(word1) + len(word2) - score[0]
    return changes

def check_spelling(checked_word, dist, word_dict, s_m):
    """
    Gets checked_word, converts it to set,
    then generates conversions dist times.
    Returns intersection of conversions set and
    dictionary set.
    """
    checked_set = set([checked_word])
    for _ in xrange(dist):
        checked_set = new_keys(checked_set).keys()
    result_set = set([])
    for word in checked_set:
        if word in word_dict:
            result_set.update(word_dict[word])
    result = []
    for word in result_set:
        if distance(checked_word, word, s_m) <= dist:
            result.append(word)
    return result

timer = time.time()
words = set(read_words(WORD_LIST_URL))
new_words = new_keys(words)
print len(new_words)
new_words = new_keys_dict(new_words)
print len(new_words)
#print new_keys_dict(new_keys(["cat"]))
alphabet = "abcdefghijklmnopqrstuvwxyz"
s_m = student.build_scoring_matrix(alphabet, 2, 1, 0)
print "Generating took ", time.time() - timer
timer = time.time()
print "humble", len(check_spelling("humble", 2,  new_words, s_m))
print "Time :", time.time() - timer
timer = time.time()
print "firefly", len(check_spelling("firefly", 2, new_words, s_m))
print "Time :", time.time() - timer
timer = time.time()
print "fireflyfosjfoijsfoidsj", len(check_spelling("fireflyfosjfoijsfoidsj", 2, new_words, s_m))
print "Time :", time.time() - timer
