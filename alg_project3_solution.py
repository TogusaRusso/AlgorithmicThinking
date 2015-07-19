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


def slow_closest_pair(cluster_list, l_b, r_b):
    """
    Compute the distance between the closest pair of clusters in a list (slow)

    Input: cluster_list is the list of clusters
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    result = (float("inf"), -1, -1)
    if l_b == r_b:
        return result
    for idx1 in xrange(l_b, r_b):
        for idx2 in xrange(idx1 + 1, r_b + 1):
            current_d = pair_distance(cluster_list, idx1, idx2)
            if current_d < result:
                result = current_d
    return result



def fast_closest_pair(cluster_list, l_b, r_b, v_i):
    """
    Compute the distance between the closest pair of clusters in a list (fast)

    Input: cluster_list is list of clusters SORTED such that horizontal positions of their
    centers are in ascending order
    
    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] have minimum distance dist.       
    """
    num = r_b - l_b + 1
    if num <= 3:
        return slow_closest_pair(cluster_list, l_b, r_b)
    else:
        mid = int(math.floor(0.5 * (r_b + l_b)))
        v_i_l = [v_i[idx] for idx in xrange(len(v_i)) 
               if v_i[idx] < mid]
        v_i_r = [v_i[idx] for idx in xrange(len(v_i)) 
               if v_i[idx] >= mid]
        result = fast_closest_pair(cluster_list, l_b, mid - 1, v_i_l)
        new_res   = fast_closest_pair(cluster_list, mid, r_b, v_i_r)
        #new_res = (new_res[0], new_res[1] + mid, new_res[2] + mid)
        if new_res < result:
            result = new_res
        mid = 0.5 * (cluster_list[mid - 1].horiz_center() 
                     + cluster_list[mid].horiz_center())
        new_res   = closest_pair_strip(cluster_list, 
                                    mid, result[0], v_i)
        if new_res < result:
            result = new_res
    return result


def closest_pair_strip(cluster_list, horiz_center, half_width, v_i):
    """
    Helper function to compute the closest pair of clusters in a vertical strip
    
    Input: cluster_list is a list of clusters produced by fast_closest_pair
    horiz_center is the horizontal position of the strip's vertical center line
    half_width is the half the width of the strip (i.e; the maximum horizontal distance
    that a cluster can lie from the center line)

    Output: tuple of the form (dist, idx1, idx2) where the centers of the clusters
    cluster_list[idx1] and cluster_list[idx2] lie in the strip and have minimum distance dist.       
    """
    mid = [v_i[idx] for idx in xrange(len(v_i)) 
           if abs(cluster_list[v_i[idx]].horiz_center() 
                  - horiz_center) < half_width]
    #mid.sort(key = lambda idx: cluster_list[idx].vert_center())
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
    cluster_list.sort(key = lambda clu: clu.horiz_center())
    v_i = [idx for idx in xrange(num)]
    v_i.sort(key = lambda idx: cluster_list[idx].vert_center())
    while num > num_clusters:
        #if num % 50 == 0:
        #    print num_clusters, num 
        #cluster_list.sort(key = lambda clu: clu.horiz_center())
        idx = fast_closest_pair(cluster_list, 0, num - 1, v_i)
        #cluster_list[idx[1]].merge_clusters(cluster_list[idx[2]])
        #cluster_list.pop(idx[2])
        arrange_h(cluster_list, idx[1], idx[2])
        arrange(v_i, cluster_list, idx[1], idx[2])
        num -= 1
    return cluster_list

def arrange(v_i, cluster_list, idx1, idx2):
    pos = min(v_i.index(idx1), v_i.index(idx2))
    vert = cluster_list[idx1].vert_center()
    v_i.remove(idx1)
    v_i.remove(idx2)
    for idx in xrange(len(v_i)):
        if v_i[idx] > idx2:
            v_i[idx] -= 1
    while pos < len (v_i):
        if vert < cluster_list[pos].vert_center():
            break
        else:
            pos += 1
    v_i.insert(pos, idx1)

def arrange_h(cluster_list, idx1, idx2):
    pos = idx1
    cluster = cluster_list[idx1].copy()
    cluster = cluster.merge_clusters(cluster_list[idx2])
    horiz = cluster_list[idx1].horiz_center()
    cluster_list.pop(idx2)
    cluster_list.pop(idx1)
    while pos < len (cluster_list):
        if horiz < cluster_list[pos].horiz_center():
            break
        else:
            pos += 1
    cluster_list.insert(pos, cluster)

      
    


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

def compute_distortion(cluster_list, data_table):
    return sum([cluster.cluster_error(data_table) for cluster in cluster_list])




