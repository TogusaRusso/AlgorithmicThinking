"""
Provided code for Application portion of Module 2
"""

# general imports
import urllib2
import random
import time
import math
import poc_queue

# CodeSkulptor import
import simpleplot
import codeskulptor
codeskulptor.set_timeout(600)

# Desktop imports
#import matplotlib.pyplot as plt


############################################
# Provided code

def copy_graph(graph):
    """
    Make a copy of a graph
    """
    new_graph = {}
    for node in graph:
        new_graph[node] = set(graph[node])
    return new_graph

def delete_node(ugraph, node):
    """
    Delete a node from an undirected graph
    """
    neighbors = ugraph[node]
    ugraph.pop(node)
    for neighbor in neighbors:
        ugraph[neighbor].remove(node)
    
def targeted_order(ugraph):
    """
    Compute a targeted attack order consisting
    of nodes of maximal degree
    
    Returns:
    A list of nodes
    """
    # copy the graph
    new_graph = copy_graph(ugraph)
    
    order = []    
    while len(new_graph) > 0:
        max_degree = -1
        for node in new_graph:
            if len(new_graph[node]) > max_degree:
                max_degree = len(new_graph[node])
                max_degree_node = node
        
        neighbors = new_graph[max_degree_node]
        new_graph.pop(max_degree_node)
        for neighbor in neighbors:
            new_graph[neighbor].remove(max_degree_node)

        order.append(max_degree_node)
    return order

def fast_targeted_order(ugraph):
    new_graph = copy_graph(ugraph)
    n = len(new_graph)
    degree_sets = [set([]) for _ in xrange(n)]
    for node in new_graph:
        d = len(new_graph[node])
        degree_sets[d].add(node)
    #print degree_sets
    attack_order = []
    for k in xrange(n - 1, -1, -1):
        #print degree_sets[k], degree_sets
        while len(degree_sets[k]) > 0:
            max_degree_node = degree_sets[k].pop()
            for node in new_graph[max_degree_node]:
                d = len(new_graph[node])
                degree_sets[d].remove(node)
                degree_sets[d-1].add(node)
            attack_order.append(max_degree_node)
            delete_node(new_graph, max_degree_node)
    return attack_order
            
        
        
    


##########################################################
# Code for loading computer network graph

NETWORK_URL = "http://storage.googleapis.com/codeskulptor-alg/alg_rf7.txt"


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

class UPATrial:
    """
    Simple class to encapsulate optimizated trials for the UPA algorithm
    
    Maintains a list of node numbers with multiple instance of each number.
    The number of instances of each node number are
    in the same proportion as the desired probabilities
    
    Uses random.choice() to select a node number from this list for each trial.
    """

    def __init__(self, num_nodes):
        """
        Initialize a UPATrial object corresponding to a 
        complete graph with num_nodes nodes
        
        Note the initial list of node numbers has num_nodes copies of
        each node number
        """
        self._num_nodes = num_nodes
        self._node_numbers = [node for node in range(num_nodes) for dummy_idx in range(num_nodes)]
        #print self._node_numbers


    def run_trial(self, num_nodes):
        """
        Conduct num_nodes trials using by applying random.choice()
        to the list of node numbers
        
        Updates the list of node numbers so that each node number
        appears in correct ratio
        
        Returns:
        Set of nodes
        """
        
        # compute the neighbors for the newly-created node
        new_node_neighbors = set()
        for _ in range(num_nodes):
            new_node_neighbors.add(random.choice(self._node_numbers))
        
        # update the list of node numbers so that each node number 
        # appears in the correct ratio
        self._node_numbers.append(self._num_nodes)
        for dummy_idx in range(len(new_node_neighbors)):
            self._node_numbers.append(self._num_nodes)
        self._node_numbers.extend(list(new_node_neighbors))
        
        #update the number of nodes
        self._num_nodes += 1
        return new_node_neighbors

def make_complete_graph(num_nodes):
    """returns a complete graph"""
    graph = {}
    edges = set(range(num_nodes))
    for node in xrange(num_nodes):
        graph[node] = edges.difference(set([node]))
    return graph

def make_ER_graph(num_nodes, p):
    """returns a ER undirected graph"""
    graph = {}
    #edges = set(range(num_nodes))
    for node in xrange(num_nodes):
        graph[node] = set([])
    for node1 in xrange(num_nodes - 1):
        for node2 in xrange(node1 + 1 , num_nodes):
            if random.random() < p:
                graph[node1].add(node2)
                graph[node2].add(node1)
    return graph


    
def create_UPA_graph(n, m):
    graph = make_complete_graph(m)
    upa = UPATrial(m)
    for node in xrange(m, n):
        graph[node] = set([])
    for node in xrange(m, n):
        for snode in upa.run_trial(m):
            graph[node].add(snode)
            graph[snode].add(node)
    return graph

def average_out_degree(graph):
    sum = 0
    n = 0.0
    for node in graph:
        n += 1.0
        sum += len(graph[node])
    return sum / n 

def edges(graph):
    return sum(map(len, graph.values())) / 2

def random_order(graph):
    nodes = graph.keys()
    #print nodes
    random.shuffle(nodes)
    print nodes
    return nodes

def bfs_visited(ugraph, start_node):
    """Takes the undirected graph ugraph and 
    the node start_node and returns the set 
    consisting of all nodes that are visited 
    by a breadth-first search that starts at start_node"""
    queue =  poc_queue.Queue()
    visited = set([start_node])
    queue.enqueue(start_node)
    while queue:
        current_node = queue.dequeue()
        for neighbor in ugraph[current_node]:
            if not neighbor in visited:
                visited.add(neighbor)
                queue.enqueue(neighbor)
    return visited

def cc_visited(ugraph):
    """Takes the undirected graph ugraph and returns
    a list of sets, where each set consists of
    all the nodes (and nothing else) in
    a connected component, and there is
    exactly one set in the list for
    each connected component in ugraph and nothing else"""
    remaining_nodes = set(ugraph.keys())
    cc_vis = []
    while remaining_nodes:
        node = remaining_nodes.pop()
        visited = bfs_visited(ugraph, node)
        cc_vis.append(visited)
        remaining_nodes.difference_update(visited)
    return cc_vis

def largest_cc_size(ugraph):
    """ Takes the undirected graph ugraph and returns
    the size (an integer) of the largest connected
    component in ugraph"""
    cc_vis = cc_visited(ugraph)
    if cc_vis:
        return max(map(len, cc_vis))
    else:
        return 0

def compute_resilience(ugraph, attack_order):
    """ Takes the undirected graph ugraph,
    a list of nodes attack_order and iterates
    through the nodes in attack_order.
    For each node in the list, the function
    removes the given node and its edges
    from the graph and then computes the size
    of the largest connected component for
    the resulting graph """
    graph = copy_graph(ugraph)
    resilience = [largest_cc_size(graph)]
    for attack_node in attack_order:
        #print attack_node
        delete_node(graph, attack_node)
        current_resilience = largest_cc_size(graph)
        resilience.append(current_resilience)
        #print current_resilience
    return resilience



"""
network = load_graph(NETWORK_URL)
network_size = len(network.keys())
print network_size, average_out_degree(network), edges(network)
p = (2.0 * edges(network)) / (network_size * (network_size - 1))
print p
p = 0.00397
er_graph = make_ER_graph(network_size, p)
#print er_graph
print len(er_graph.keys()), edges(er_graph)

#print er_graph[1262]
upa_graph = create_UPA_graph(network_size, 3)
print len(upa_graph.keys()), edges(upa_graph)
print fast_targeted_order(er_graph)
"""
m = 5
n2times = []
ntimes = []
for n in xrange(10, 1000, 10):
    upa_graph = create_UPA_graph(n, m)
    ptime = time.time()
    targeted_order(upa_graph)
    n2times.append([n, time.time() - ptime])
    ptime = time.time()
    fast_targeted_order(upa_graph)
    ntimes.append([n, time.time() - ptime])
    #print n, n2time, ntime
    
simpleplot.plot_lines("Targeted order computing time (CodeSkulptor)",
                      800, 600, "Number of nodes n", "Running times (seconds)",
                      [n2times, ntimes], False,
                      ["Targeted order, O(n^2)", "Fast targeted order, O(n)"])
    

"""
#print network
attack_order = random_order(network)[:network_size / 2]
#print attack_order
print "Network"
resilience_network = compute_resilience(network, attack_order)
print "ER"
attack_order = random_order(er_graph)[:network_size / 2]
resilience_er = compute_resilience(er_graph, attack_order)
print "UPA"
attack_order = random_order(upa_graph)[:network_size / 2]
resilience_upa = compute_resilience(upa_graph, attack_order)
plot_network = [[idx, resilience_network[idx]] for idx in range(len(resilience_network))]
plot_er =  [[idx, resilience_er[idx]] for idx in range(len(resilience_er))]
plot_upa =  [[idx, resilience_upa[idx]] for idx in range(len(resilience_upa))]
plot_x2 = [[idx, network_size - idx] for idx in range(network_size / 2)]
plot_x1 = [[idx, 0.75 * (network_size - idx)] for idx in range(network_size / 2)]
simpleplot.plot_lines("Graph resilience", 800, 600,
            "Nodes removed", "Size of the largest connect component",
                      [plot_network, plot_er, plot_upa, plot_x2, plot_x1], 
            False, ["Network example", "ER graph, p = 0.00397", "UPA graph, m = 3", "X", "0.75 * X"])
"""






