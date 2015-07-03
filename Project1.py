"""Project 1 - Degree distributions for graphs"""

#define graphs

EX_GRAPH0 = {0: set([1, 2]), 1: set([]), 2: set([])}
EX_GRAPH1 = {0: set([1, 4, 5]), 1: set([2, 6]), 2: set([3]),
             3: set([0]), 4: set([1]), 5: set([2]), 
             6: set([])}
EX_GRAPH2 = {0: set([1, 5, 4]), 1: set([2, 6]), 
             2: set([3, 7]), 3: set([7]), 4: set([1]), 
             5: set([2]), 6: set([]), 7: set([3]), 
             8: set([1, 2]), 9: set([0, 3, 4, 5, 6, 7])}

def make_complete_graph(num_nodes):
    """returns a complete directed graph"""
    graph = {}
    edges = set(range(num_nodes))
    for node in xrange(num_nodes):
        graph[node] = edges.difference(set([node]))
    return graph

def compute_in_degrees(digraph):
    """computes the in-degrees for the nodes in the graph"""
    result = dict(zip(digraph.keys(), [0] * len(digraph)))
    for node in digraph.keys():
        for ajnode in digraph[node]:
            result[ajnode] += 1
    return result

def in_degree_distribution(digraph):
    """computes unnormalized distribution of the in-degrees"""
    degrees = compute_in_degrees(digraph)
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