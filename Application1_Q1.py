"""
Provided code for Application portion of Module 1

Imports physics citation graph 
"""

# general imports
import urllib2

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(60)

import simpleplot
import math



###################################
# Code for loading citation graph

CITATION_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_phys-cite.txt"

def load_graph(graph_url):
    """
    Function that loads a graph given the URL
    for a text representation of the graph
    
    Returns a dictionary that models a graph
    """
    graph_file = urllib2.urlopen(graph_url)
    graph_text = graph_file.read()
    graph_lines = graph_text.split('\n')
    graph_lines = graph_lines[ : -1]
    
    print "Loaded graph with", len(graph_lines), "nodes"
    
    answer_graph = {}
    for line in graph_lines:
        neighbors = line.split(' ')
        node = int(neighbors[0])
        answer_graph[node] = set([])
        for neighbor in neighbors[1 : -1]:
            answer_graph[node].add(int(neighbor))

    return answer_graph

def compute_in_degrees(digraph):
    """computes the in-degrees for the nodes in the graph"""
    result = dict(zip(digraph.keys(), [0] * len(digraph)))
    for node in digraph.keys():
        for ajnode in digraph[node]:
            result[ajnode] += 1
    return result

def in_degree_distribution(digraph):
    """computes normalized distribution of the in-degrees"""
    degrees = compute_in_degrees(digraph)
    count_degrees = {}
    #normalize degree from beginning
    part = 1.0 / len(degrees)
    #unnormalized
    #part = 1
    for degree in degrees.keys():
        if degrees[degree] in count_degrees:
            count_degrees[degrees[degree]] += part
        else:
            count_degrees[degrees[degree]] = part
    return count_degrees

citation_graph = load_graph(CITATION_URL)
distr = in_degree_distribution(citation_graph)

print sum(distr.values())

plot = []
for x in distr.keys():
    if x > 0 and distr[x] > 0:
        plot.append([math.log(x, 10), math.log(distr[x], 10)])

simpleplot.plot_lines("Normalized in-degree distribution log/log graph", 600, 600, 
                      "log(in-degree) base 10", "log(probability) base 10", [plot])






