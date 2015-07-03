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
import random



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

def normalize_distribution(degrees):
    """computes normalized distribution of the in-degrees"""
    count_degrees = {}
    #normalize degree from beginning
    #part = 1.0 / len(degrees)
    #unnormalized
    part = 1
    for degree in degrees.keys():
        if degrees[degree] in count_degrees:
            count_degrees[degrees[degree]] += part
        else:
            count_degrees[degrees[degree]] = part
    return count_degrees

def make_er_graph(num_nodes, p):
    """returns a complete directed graph"""
    graph = {}
    edges = set(range(num_nodes))
    for node in xrange(num_nodes):
        graph[node] = set([])
        for ajnode in edges.difference(set([node])):
            if random.random() < p:
                graph[node].update(set([ajnode]))
    return graph

def combination(n, k):
    result = 1.0
    st1 = n
    st2 = k
    while st1 > k:
        result *= st1
        st1 -= 1
        if st2 > 1:
            result = result / st2
            st2 -= 1
    while st2 > 1:
        result = ttt = DPATrial(3)
print ttt.run_trial(3)
print ttt.run_trial(3)
print ttt.run_trial(3)result / st2
        st2 -= 1
    return result


def sim_er_degree_log(n, p):
    result = {}
    #print p
    p_log = math.log(1-p) * (n -1)
    mult_log = math.log(p / (1-p))
    prob = p_log
    for k in xrange(0, n - 2):
        result[k] = p_log
        p_log += mult_log + math.log((n - 1) - k ) - math.log(k + 1)
    result[n - 1] = p_log
    return result

def average_out_degree(graph):
    sum = 0
    n = 0.0
    for node in graph:
        n += 1.0
        sum += len(graph[node])
    return sum / n 
        

citation_graph = load_graph(CITATION_URL)
print len(citation_graph.keys())
print average_out_degree(citation_graph)

#distr1 = in_degree_distribution(citation_graph)
graph1 = make_er_graph(1000, 0.5)
distr1 = in_degree_distribution(graph1)
#er_graph = make_er_graph(len(citation_graph) // 50, 0.5)
#distr2 = in_degree_distribution(er_graph)
#print sim_er_degree(, 0.5)
#print normalize_distribution(sim_er_degree(len(citation_graph), 0.5))
distr2 = sim_er_degree_log(1000, 0.5)



low = min(distr1.values())

plot1 = []
for x in distr1.keys():
    if x > 0 and distr1[x] > 0:
        plot1.append([math.log(x), math.log(distr1[x])])
plot2 = []
for x in distr2.keys():
    if x > 0 and distr2[x] > math.log(low):
        plot2.append([math.log(x), 
                     distr2[x]])

simpleplot.plot_lines("Distribution for random graph and binomial distribution for n = 1000 p = 0.5 ", 600, 600, 
                      "log(in-degree) base e", "log(probability) base e", [plot1, plot2])






