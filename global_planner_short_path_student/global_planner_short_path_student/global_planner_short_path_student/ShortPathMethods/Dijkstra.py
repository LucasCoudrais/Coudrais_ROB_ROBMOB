__author__ = 'Jacques saraydaryan'

from global_planner_short_path_student.ShortPathMethods.AbstractShortPath import AbstractShortPath
from visualization_msgs.msg import MarkerArray
import math
import rclpy


# import sys
# sys.path.append('../')

import time
from nav_msgs.msg import OccupancyGrid
from visualization_msgs.msg import Marker
from visualization_msgs.msg import MarkerArray
from geometry_msgs.msg import Point, PoseStamped, PointStamped

import numpy as np
import heapq
from queue import Queue, LifoQueue, PriorityQueue
import time

class Dijsktra(AbstractShortPath):
    SLEEP_TIME_BEFORE_NEXT_ITERATION = 0.01
    MAP_OBSTACLE_VALUE = -100

    def __init__(self):
        print('')

    def goto(self, source, target, matrix, pub_marker, marker_container):        
        # In djikstra computation start from the source
        start = {'x': source['x'], 'y': source['y']}

        frontier = []
        frontier.append(Queue())
        frontier[0].put(start)
        # Dictionary that holds local precedence of each point
        prev = {}
        prev[str(start['x']) + '_' + str(start['y'])] = None
        poids = {}
        poids[str(start['x']) + '_' + str(start['y'])] = 0

        # While their is no data to process, another condition could be while goal is not reached
        while not frontier.__len__() == 0:
            # get the point of the FIFO and remove it from the frontier
            current = frontier[0].get()
            # create visual info
            self.createClosedMarkerPt(current, marker_container)

            # for all neighbors of the current point
            for next in self.getNeighbors(current, matrix):
                # counter of number of iteration, only to see computation siz

                # check that the current Neighbor has not be prev
                if (str(next['x']) + '_' + str(next['y']) not in prev or 
                    poids[str(next['x']) + '_' + str(next['y'])] < poids[str(current['x']) + '_' + str(current['y'])] + matrix[next['y']][next['x']]):
                    # create visual info
                    self.createFontierUnitMarkerPt(next, marker_container)
                    # Add the Neighbor to be processed
                    if matrix[next['y']][next['x']] != self.MAP_OBSTACLE_VALUE:
                        for i in range(matrix[next['y']][next['x']] + 1):
                            if frontier.__len__() <= i + 1:
                                frontier.append(Queue())
                            frontier[matrix[next['y']][next['x']] + 1].put(next)

                    # Add the previous reference of the current Neighbor
                    prev[str(next['x']) + '_' + str(next['y'])] = str(current['x']) + '_' + str(current['y'])
                    poids[str(next['x']) + '_' + str(next['y'])] = poids[str(current['x']) + '_' + str(current['y'])] + matrix[next['y']][next['x']]

            # publish the visual markers
            pub_marker.publish(marker_container)
            # wait before next iteration
            time.sleep(self.SLEEP_TIME_BEFORE_NEXT_ITERATION)

            if frontier[0].empty():
                frontier.pop(0)
        # print('end of wave front it:' + str(it))
        pub_marker.publish(marker_container)

        # return the dictionary of precedence
        return prev
    
    def getNeighbors(self, currentNode, matrix):
        """ Compute Neighbors of the current point, Return the list of the point neighbors in Cfree"""
        x_c = currentNode['x']
        y_c = currentNode['y']
        neighbors = []
        self.checkAndAdd(neighbors, x_c + 1, y_c, matrix)
        self.checkAndAdd(neighbors, x_c, y_c + 1, matrix)
        self.checkAndAdd(neighbors, x_c - 1, y_c, matrix)
        self.checkAndAdd(neighbors, x_c, y_c - 1, matrix)
        return neighbors

    def checkAndAdd(self, neighbors, x, y, matrix):
        """ Check that the candidate neighbor is valid == not an obstacle, in current bound, add the nieghbor node to the node list"""
        if (x > 0 and x < len(matrix) and y > 0 and y < len(matrix[0])):
            if (matrix[y][x] != self.MAP_OBSTACLE_VALUE):
                neighbors.append({'x': x, 'y': y})
        return neighbors
