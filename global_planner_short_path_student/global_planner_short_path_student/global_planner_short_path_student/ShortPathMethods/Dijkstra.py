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

    def createFontierUnitMarker(self, v, marker_container):
        pass

    def createClosedMarker(self, u, marker_container):
        pass

    def goto(self, source, target, matrix, pub_marker, marker_container):
        prev = {}
        ### TODO
        ###########################################################
        ################### Function Paramters ###################
        ###########################################################
        ### source: coordinate of the robot position source['x'] return the x position, source['y'] return the y position
        ###
        ### target: coordinate of the target position target['x'] return the x position, target['y'] return the y position
        ###
        ### matrix: rescaled map (including obstacles) matrix[i][j] return the value of the cell i,j of the matrix
        ###
        ### elf.MAP_OBSTACLE_VALUE: value of an obstacle into the matrix (-100)
        ###
        ### pub_marker: marker publisher to visualize information into rviz (usage pub_marker.publish(marker_container) )
        ###
        ### marker_container: marker container where where new marker are added as point
        ###
        ###########################################################
        ################### Function Toolboxes ###################
        ###########################################################
        #   # create a visual information
        #   self.createFontierUnitMarker(v, marker_container)
        #
        #    # publish visual information
        #    pub_marker.publish(marker_container)
        #
        #    # create a visual information
        #    self.createClosedMarker(u, marker_container)
        #
        #
        #                       TODO
        #
        #
        ### prev:  disctionary holding node precedence
        ### CAUTION prev dictionary has to be completed as follow:
        ###
        ### prev[str(v['x']) + '_' + str(v['y'])] = str(u['x']) + '_' + str(u['y'])
        ###
        ### where v['x'] return the x position of the node v in the resized map
        ### where v['y'] return the y position of the node v in the resized map
        #return prev
        
        # In djikstra computation start from the source
        start = {'x': source['x'], 'y': source['y']}

        # FIFO that store data to process
        frontier = list()
        # Initialized with the first point
        frontier.append(start)
        # Dictionary that holds local precedence of each point
        # came_from = {}
        # came_from[str(start['x']) + '_' + str(start['y'])] = None
        processed = {}
        processed[str(start['x']) + '_' + str(start['y'])] = None

        # it = 0

        # While their is no data to process, another condition could be while goal is not reached
        while not frontier.__len__() == 0:
            # get the point of the FIFO and remove it from the frontier
            current = frontier[0]
            # create visual info
            self.createClosedMarker(current, marker_container)

            # for all neighbors of the current point
            for next in self.getNeighbors(current, matrix):
                # counter of number of iteration, only to see computation size
                # it = it + 1

                # check that the current Neighbor has not be processed
                if str(next['x']) + '_' + str(next['y']) not in processed:
                    # create visual info
                    self.createFontierUnitMarker(next, marker_container)
                    # Add the Neighbor to be processed in th FIFO
                    frontier.insert(???, next)

                    # Add the previous reference of the current Neighbor
                    processed[str(next['x']) + '_' + str(next['y'])] = str(current['x']) + '_' + str(current['y'])

            # publish the visual markers
            pub_marker.publish(marker_container)
            #marker_array = MarkerArray()
            # wait before next iteration
            time.sleep(self.SLEEP_TIME_BEFORE_NEXT_ITERATION)
        # print('end of wave front it:' + str(it))
        pub_marker.publish(marker_container)

        # return the dictionary of precedence
        return processed
    
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
