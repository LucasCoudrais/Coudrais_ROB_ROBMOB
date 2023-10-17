__author__ = 'Jacques saraydaryan'

from global_planner_short_path_student.ShortPathMethods.AbstractShortPath import AbstractShortPath
import math
import rclpy
from visualization_msgs.msg import MarkerArray


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


class AStar(AbstractShortPath):
    SLEEP_TIME_BEFORE_NEXT_ITERATION = 0.1
    MAP_OBSTACLE_VALUE = -100

    def __init__(self):
        print('')

    def goto(self, source, target, matrix, pub_marker, marker_container):        
        # In djikstra computation start from the source
        start = {'x': source['x'], 'y': source['y']}
        end = {'x': target['x'], 'y': target['y']}

        fscore = {}

        gscore = {}
        gscore[str(start['x']) + '_' + str(start['y'])] = 0

        prev = {}
        prev[str(start['x']) + '_' + str(start['y'])] = None

        frontier = []
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                # all nodes receive a score of INF
                fscore[str(i) + '_' + str(j)] = 9999
                # all nodes are added to the list to process
                frontier.append({'x': i, 'y': j})
        fscore[str(start['x']) + '_' + str(start['y'])] = 0

        # While their is no data to process, another condition could be while goal is not reached
        while len(frontier) != 0:
            # get the point of the FIFO and remove it from the frontier
            current = self.minScore(fscore, frontier)
            fscore.pop(str(current['x']) + '_' + str(current['y']))
            
            # create visual info
            self.createClosedMarkerPt(current, marker_container)

            # for all neighbors of the current point
            for next in self.getNeighbors(current, matrix):
                h = math.sqrt(math.pow(end['x'] - next['x'], 2) + math.pow(end['y'] - next['y'], 2))
                if(str(next['x']) + '_' + str(next['y']) not in gscore):
                    self.createFontierUnitMarkerPt(next, marker_container)
                    # Add the Neighbor to be processed
                    if matrix[next['y']][next['x']] != self.MAP_OBSTACLE_VALUE:
                        gscore[str(next['x']) + '_' + str(next['y'])] = gscore[str(current['x']) + '_' + str(current['y'])] + matrix[next['y']][next['x']]
                        fscore[str(next['x']) + '_' + str(next['y'])] = gscore[str(next['x']) + '_' + str(next['y'])] + round(h)

                    # Add the previous reference of the current Neighbor
                    prev[str(next['x']) + '_' + str(next['y'])] = str(current['x']) + '_' + str(current['y'])
                    if next['x'] == end['x'] and next['y'] == end['y']:
                        frontier = []
                        break

            # publish the visual markers
            pub_marker.publish(marker_container)
            # wait before next iteration
            time.sleep(self.SLEEP_TIME_BEFORE_NEXT_ITERATION)

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

    def minScore(self, fscore, frontier):
        """ Return the node that has the lowest score, information return like u={'x':5,'y':3}"""
        min = 9999
        min_coord = ''
        for n in frontier:
            if fscore[str(n['x']) + '_' + str(n['y'])] < min:
                min = fscore[str(n['x']) + '_' + str(n['y'])]
                min_coord = n
        return min_coord
