#Uses python3
import sys
import math
from itertools import combinations
from collections import defaultdict

def get_edge_weights(points):

    edges = list(combinations(points, 2))
    
    dist = lambda x1, y1, x2, y2 : math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

    weights = [dist(p1.x, p1.y, p2.x, p2.y) for (p1, p2) in edges]
 
    return [(edge, weight) for (edge, weight) in zip(edges, weights)]
    
class Point():
    def __init__(self, x, y, id_):
        self.x = x
        self.y = y
        self.id_ = id_
        # self.parent = parent

    def find(self):
        return self.id_

class Cluster():
    
    def __init__(self, points, root):
        self.points = points
        self.root = root
        self.rank = 1

    def merge(self, cluster):

        if cluster.rank < self.rank:
            to_remove = cluster.root.find()
            # hang cluster under self
            # no change in ranks
            # remove cluster
            for p in cluster.points:
                p.id_ = self.root.find()
                self.points.append(p)


        elif cluster.rank > self.rank:

            # rank of cluster > self, hang self under cluster
            # remove self

            to_remove = self.root.find()
            for p in self.points:
                p.id_ = cluster.root.find()
                cluster.points.append(p)

        
        else:
            # ranks are equal, hang cluster under self but increment self.rank
            # remove cluster
            to_remove = cluster.root.find()

            for p in cluster.points:
                p.id_ = self.root.find()
              
                self.points.append(p)

            self.rank += 1

        return to_remove

   
def get_shortest_road(clusters, points, edges):

    res = 0

    # iterate until a single set is left i.e all the points are connected
    while len(clusters) > 1:

        # the best edge is one with minimum weight
        best_edge = min(edges, key=lambda x:x[1])
        
        ((p1, p2), w) = best_edge

        id1, id2 = p1.find(), p2.find()

        if id1 != id2:
            # p1 and p2 are not in the same disjoint set -> they are not connected -> this edge will not form a cycle
            
            # merge the two sets and add the edge weight to result
            to_remove = clusters[id1].merge(clusters[id2])
            
            res += w
            
            # remove the set that was 'hung' under the other
            del clusters[to_remove]

        # remove this edge in any case -> either it was found to form a cycle, or it was used to connect two vertices
        edges.remove(best_edge)

    return res


if __name__ == '__main__':
    input = sys.stdin.read()
    data = list(map(int, input.split()))
    n = data[0]

    points = list()
    i = 0

    for (x, y) in zip(data[1::2], data[2::2]):
        
        points.append(Point(x, y, i))
        i += 1

    # get all possible edges and their respective distances for the set of points
    edges = get_edge_weights(points)
    
    # initialise a singleton set for each point (thus root is the point)
    clusters = {i : Cluster([points[i]], root=points[i]) for i in range(len(points))}


    print(get_shortest_road(clusters, points, edges))


