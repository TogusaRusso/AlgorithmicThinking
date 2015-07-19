"""
Student template code for Project 3
Student will implement five functions:

slow_closest_pair(cluster_list)
fast_closest_pair(cluster_list)
closest_pair_strip(cluster_list, horiz_center, half_width)
hierarchical_clustering(cluster_list, num_clusters)
kmeans_clustering(cluster_list, num_clusters, num_iterations)

where cluster_list is a 2D list of clusters in the plane
"""

import math
import alg_cluster
import random
import time

# CodeSkulptor import
import simpleplot
import codeskulptor
codeskulptor.set_timeout(600)




######################################################
# Code for closest pairs of clusters

def pair_distance(cluster_list, idx1, idx2):
    """
    Helper function that computes Euclidean distance between two clusters in a list

    Input: cluster_list is list of clusters, idx1 and idx2 are integer indices for two clusters
    
    Output: tuple (dist, idx1, idx2) where dist is distance between
    cluster_list[idx1] and cluster_list[idx2]
    """
    return (cluster_list[idx1].distance(cluster_list[idx2]), min(idx1, idx2), max(idx1, idx2))


def slow_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    result = (float("inf"), -1, -1)
    nnn = len(cluster_list)
    if nnn == 1:
        return result
    for idx1 in xrange(nnn - 1):
        for idx2 in xrange(idx1 + 1, nnn):
            current_d = pair_distance(cluster_list, idx1, idx2)
            if current_d < result:
                result = current_d
    return result



def fast_closest_pair(cluster_list):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    num = len(cluster_list)
    if num <= 3:
        return slow_closest_pair(cluster_list)
    else:
        mid = int(math.floor(0.5 * num))
        p_l = [cluster_list[idx] for idx in xrange(mid)]
        p_r = [cluster_list[idx] for idx in xrange(mid, num)]
        result = fast_closest_pair(p_l)
        new_res   = fast_closest_pair(p_r)
        new_res = (new_res[0], new_res[1] + mid, new_res[2] + mid)
        if new_res < result:
            result = new_res
        mid = 0.5 * (p_l[-1].horiz_center() 
                     + p_r[0].horiz_center())
        new_res   = closest_pair_strip(cluster_list, 
                                    mid, result[0])
        if new_res < result:
            result = new_res
    return result


def closest_pair_strip(cluster_list, horiz_center, half_width):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    mid = [idx for idx in xrange(len(cluster_list)) 
           if abs(cluster_list[idx].horiz_center() 
                  - horiz_center) < half_width]
    mid.sort(key = lambda idx: cluster_list[idx].vert_center())
    num = len(mid)
    result = (float("inf"), -1, -1)
    for idx1 in xrange(num - 1):
        for idx2 in xrange(idx1 + 1, min(idx1 + 4, num)):
            current_d = pair_distance(cluster_list, mid[idx1], mid[idx2])
            if current_d < result:
                result = current_d
    if result[1] > result[2]:
        result = (result[0], result[2], result[1])
    return result
            
 
    
######################################################################
# Code for hierarchical clustering


def hierarchical_clustering(cluster_list, num_clusters):
    """
    Compute a hierarchical clustering of a set of clusters
    Note: the function may mutate cluster_list
    
    Input: List of clusters, integer number of clusters
    Output: List of clusters whose length is num_clusters
    """
    num = len(cluster_list)
    while num > num_clusters:	
        cluster_list.sort(key = lambda clu: clu.horiz_center())
        idx = fast_closest_pair(cluster_list)
        cluster_list[idx[1]].merge_clusters(cluster_list[idx[2]])
        cluster_list.pop(idx[2])
        num -= 1
    return cluster_list


######################################################################
# Code for k-means clustering

    
def kmeans_clustering(cluster_list, num_clusters, num_iterations):
    """
    Compute the k-means clustering of a set of clusters
    Note: the function may not mutate cluster_list
    
    Input: List of clusters, integers number of clusters and number of iterations
    Output: List of clusters whose length is num_clusters
    """

    # position initial clusters at the location of clusters with largest populations
    num = len(cluster_list)
    
    points = [idx for idx in xrange(num)]
    points.sort(reverse = True, key = lambda idx: 
                cluster_list[idx].total_population())
    points = [[cluster_list[points[idx]].horiz_center(),
               cluster_list[points[idx]].vert_center()] 
              for idx in xrange(num_clusters)]
    clusters = [-1 for _ in xrange(num)]
    population = [0 for _ in xrange(num_clusters)]
    for _ in xrange(num_iterations):
        for cidx in xrange(num):
            mind = (float("inf"), -1, -1)
            for idx in xrange(num_clusters):
                dist = cluster_point_distance(cluster_list,
                                              points, 
                                              cidx, idx)
                if mind > dist:
                    mind = dist
            clusters[cidx] = mind[2]
        for idx in xrange(num_clusters):
            points[idx][0] = 0.0
            points[idx][1] = 0.0
            population[idx] = 0
        for cidx in xrange(num):
            idx = clusters[cidx]
            cpopul = cluster_list[cidx].total_population()
            population[idx] += cpopul
            points[idx][0] += cluster_list[cidx].horiz_center() * cpopul
            points[idx][1] += cluster_list[cidx].vert_center()  * cpopul
        for idx in xrange(num_clusters):
            points[idx][0] /= population[idx]
            points[idx][1] /= population[idx]
    result = [0 for _ in xrange(num_clusters)]
    for cidx in xrange(num):
        idx = clusters[cidx]
        if result[idx] == 0:
            result[idx] = cluster_list[cidx].copy()
        else:
            result[idx].merge_clusters(cluster_list[cidx])
    return result

def cluster_point_distance(cluster_list, points, cidx, idx):
    """
    Helper function that computes Euclidean distance between cluster and point

    Input: cluster_list is list of clusters, points is list of points,
    cidx1 and idx are integer indices for cluster and point
    
    Output: tuple (dist, cidx, idx) where dist is distance between
    cluster_list[cidx] and points[idx]
    """
    d_x = cluster_list[cidx].horiz_center() - points[idx][0]
    d_y = cluster_list[cidx].vert_center()  - points[idx][1]
    return (math.sqrt(d_x ** 2 + d_y ** 2), cidx, idx)

def gen_random_clusters(num_clusters):
    """
    creates a list of clusters where each cluster 
    in this list corresponds to one randomly generated point 
    """
    result = []
    for idx in xrange(num_clusters):
        h_p = 2 * random.random() - 1
        v_p = 2 * random.random() - 1
        result.append(alg_cluster.Cluster(set([idx]), h_p, v_p, 1, .001))
    return result

slow = []
fast = []
for n in xrange(2, 200):
    cluster_list = gen_random_clusters(n)
    #presort the list
    cluster_list.sort(key = lambda clu: clu.horiz_center())
    t_time = 0.0
    for _ in xrange(5):
        ptime = time.time()
        slow_closest_pair(cluster_list)
        t_time += time.time() - ptime
    slow.append([n, t_time / 5])
    t_time = 0.0
    for _ in xrange(5):
        ptime = time.time()
        fast_closest_pair(cluster_list)
        t_time += time.time() - ptime
    fast.append([n, t_time / 5])
    #print n, slow[-1][1], fast[-1][1]
    
simpleplot.plot_lines("Running time of closest pair functions (CodeSkulptor)",
                      800, 600, "Number of clusters n (2 - 200)", "Running times (seconds)",
                      [slow, fast], False,
                      ["Slow closest pair (brute force)", "Fast closest pair (presorted)"])
    



