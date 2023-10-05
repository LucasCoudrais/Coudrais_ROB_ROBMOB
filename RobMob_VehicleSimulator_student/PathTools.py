#!/usr/bin/env python  

__author__ = 'Raphael Leber'

from math import pi, sqrt, fmod, fabs


class PathTools():

    def __init__(self):
        pass

    def shortestAngleDiff(self, th1, th2):
        """
            Returns the shortest angle between 2 angles in the trigonometric circle
        """        
        anglediff = fmod( (th1 - th2), 2*pi)

        if anglediff < 0.0:
            if fabs(anglediff) > (2*pi + anglediff) :
                anglediff = 2*pi + anglediff
        else:
            if anglediff > fabs(anglediff - 2*pi) :
                anglediff = anglediff - 2*pi

        return anglediff
