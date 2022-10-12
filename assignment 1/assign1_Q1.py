
import math
from math import sqrt
from sympy import Point, Line,Segment
 
# line from two points
def line_between_two_points(p1, p2):
    line = Line(p1, p2)
    line_equation = line.equation()
    return line
  
#  Compute distance between two points
def distance_between_points(p1,p2):
    p1 = Point(p1)
    p2 = Point(p2)
    distance = sqrt(((p1[0]-p2[0])**2 )+ ((p1[1]-p2[1])**2))
    return distance
   
# Compute perpendicular distance between a point and a line segment
def distance_from_point_to_line(x, p1, p2):
    seg = Segment(p1, p2)
    return seg.distance(x)

# Compute distance between a point and a Polygon
def distance_from_point_to_polygon(p1, polygon):
    return polygon.distance(p1)
  
# Compute tangent vector to a polygon
def tangents_to_polygon(p1, polygon):
  line_from_point_to_polygon = []
  tangent = []

  # getting lines from x to vertices of polygon
  for i in range(0, len(polygon.vertices)):
    line_from_point_to_polygon.append(Line(p1, polygon.vertices[i]))
  
  # if the line intersects the polygon only once it is a tangent
  for i in range(0, len(line_from_point_to_polygon)):
      if len(line_from_point_to_polygon[i].intersection(polygon)) == 1:
        tangent.append(line_from_point_to_polygon[i])

# Find intersection of two polygons
def intersection_polygon(poly1, poly2):
  return poly1.intersection(poly2)






