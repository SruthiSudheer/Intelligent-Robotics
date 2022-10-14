
from sympy import Polygon, Point, Line, Segment2D, Point2D, Line2D
import sys

def visibility_graph(start_point, destination, polygons):
    points = [start_point, destination]
    for p in polygons:
        points.extend(p.vertices) # storing vertices of polygon
    points = list(set(points)) # storing unique vertices only
    points.sort(key=lambda v: v.args[0]) # sorting by x-coordinate

    edges = []
    for p in polygons:
        edges.extend(p.sides) # storing polygon edges

    visible_graph = []
    for p in range(len(points)-1):
        for q in range(p+1, len(points)):
            line = Line(points[p], points[q]) # drawing lines from one point to another including start_point, destination and unique polygon vertices

            valid = True
            for e in edges:
                intersection = e.intersect(line)
                if intersection.is_empty:   # the lines drawn doesn not intersect the polygons
                    continue

                elif type(intersection) is Segment2D:   # the lines drawn is coincident to the polygon edge
                    continue

                elif not list(intersection)[0] in e.args: # the x-coordinate of the intersection is not the x-coordinate of the edge end points
                    valid = False
                    break
                
            if valid:
                visible_graph.append((points[p], points[q])) # storing the valid lines from p to q
    return set(visible_graph)


class Graph(): 
    def __init__(self, vertices):
        self.V = vertices
        self.graph = [[0 for column in range(vertices)]
                      for row in range(vertices)]
 
    def printSolution(self, dist):
        print("Vertex \tDistance from Source")
        for node in range(self.V):
            print(node, "\t", dist[node])

    def minDistance(self, dist, sptSet): # finding the vertex with minimum distance value, from the set of vertices not yet included in shortest path tree
 
        # Initialize minimum distance for next node
        min = sys.maxsize
 
        # Search not nearest vertex not in the shortest path tree
        for u in range(self.V):
            if dist[u] < min and sptSet[u] == False:
                min = dist[u]
                min_index = u
 
        return min_index
 
 # main
    def dijkstra(self, src): 
        dist = [sys.maxsize] * self.V
        dist[src] = 0
        sptSet = [False] * self.V
 
        for cout in range(self.V):
            x = self.minDistance(dist, sptSet) # Picking the minimum distance vertex from the set of vertices not yet seen
            sptSet[x] = True # Putting the minimum distance vertex in theshortest path tree

            #Updating dist value of the adjacent vertices of the picked vertex only if 
            #the current distance is greater than new distance and 
            #the vertex in not in the shortest path tree
            for y in range(self.V):
                if self.graph[x][y] > 0 and sptSet[y] == False and \
                        dist[y] > dist[x] + self.graph[x][y]:
                    dist[y] = dist[x] + self.graph[x][y]
 
        self.printSolution(dist)

destination = (0,2,0)
start_point = (0.5,-1,0)

polygons = [poly1,poly2]
visible_graph = visibility_graph(start_point, destination, polygons)

if __name__ == "__main__":         
    g = visible_graph
    g.dijkstra(0)
