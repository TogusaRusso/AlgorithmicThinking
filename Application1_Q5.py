"""
Provided code for application portion of module 1

Helper class for implementing efficient version
of DPA algorithm
"""

# general imports
import random
import math
import simpleplot

# Set timeout for CodeSkulptor if necessary
import codeskulptor
codeskulptor.set_timeout(1200)




class DPATrial:
    """
    Simple class to encapsulate optimized trials for DPA algorithm
    
    Maintains a list of node numbers with multiple instances of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a DPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]
        


    def run_trial(self, num_nodes):
        """
        Conduct num_node trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that the number of instances of
        each node number is in the same ratio as the desired probabilities
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for dummy_idx in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors
    
def make_complete_graph(num_nodes):
    """returns a complete directed graph"""
    graph = {}
    edges = set(range(num_nodes))
    for node in xrange(num_nodes):
        graph[node] = edges.difference(set([node]))
    return graph
    
def create_DPA_graph(n, m):
    graph = make_complete_graph(m)
    dpa = DPATrial(m)
    for node in xrange(m, n):
        graph[node] = dpa.run_trial(m)
    return graph

def average_out_degree(graph):
    sum = 0
    n = 0.0
    for node in graph:
        n += 1.0
        sum += len(graph[node])
    return sum / n 

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


graph = create_DPA_graph(27770, 13)
print len(graph.keys())
print average_out_degree(graph)

distr = in_degree_distribution(graph)

plot = []
for x in distr.keys():
    if x > 0 and distr[x] > 0:
        plot.append([math.log(x, 10), math.log(distr[x], 10)])
        
simpleplot.plot_lines("Distribution for DPA random graph for n = 27700, m = 13 ", 600, 600, 
                      "log(in-degree) base 10", "log(probability) base 10", [plot])


        
   


    

