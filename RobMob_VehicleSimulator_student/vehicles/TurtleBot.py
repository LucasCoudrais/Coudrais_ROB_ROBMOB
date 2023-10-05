#!/usr/bin/env python  

__author__ = 'Lucas Coudrais'

from math import cos, sin, tan, pi, sqrt, atan2, fmod, fabs, copysign
import turtle  
import time

from vehicles.Vehicle import Vehicle
from PathTools import PathTools



class TurtleBot(Vehicle):

    # def __init__(self, x=0, y=0, theta=0, Ks=0.1, Kv=2, L=1.8, steering_max_angle = pi/8, dt = 0.003):
    def __init__(self, x=0, y=0, theta=0, Ks=16, Kv=1, T=0.3, dt = 0.003):
        self.x = x          # x position
        self.y = y          # y position
        self.theta = theta  # theta orientation
        self.Ks = Ks        # Steering proportionnal coefficient
        self.Kv = Kv        # Velocity proportionnal coefficient
        # self.L = L          # Distance between front and back wheel
        self.T = T          # Distance between front and back wheel
        # self.steering_max_angle = steering_max_angle  # How much you can turn the front wheel
        self.dt = dt                # Time of one code cycle
        self.throttle_min = 400     # Min saturation throttle based of euclidan distance
        self.throttle_max = 500000    # Max saturation throttle based of euclidan distance


    def model(self, Vl, Vr):
        """  TurtleBot model
                           ___________________
                          |                   |
                          |                   |---> x           
                   Vr --->|                   |    
                          |      Bicycle      |
                          |                   |---> y
                          |       Model       |                        
                   Vl --->|                   |   
                          |                   |---> theta      
                          |___________________|          
        """        
        # Vl = min(Vl, self.throttle_max)
        # Vr = min(Vr, self.throttle_max)
        # g = min(guidon, self.steering_max_angle) 
        v = (Vl+Vr)/2
        w = (Vr-Vl)/self.T
        dt = self.dt

        x_p = v * cos(self.theta)
        y_p = v * sin(self.theta)
        theta_p = w

        self.x = self.x + x_p*dt
        self.y = self.y + y_p*dt
        self.theta = self.theta + theta_p*dt

        return self.x, self.y, self.theta


    def toPoint(self, x, y, eps=0.5):
        """ Move to a point (x, y)

            Parameters:
            x (int): x coordinate to reach in the map
            y (int): y coordinate to reach in the map
            eps (float): epsilon below which we consider the goal is reached

            Returns:
            float: Returning throttle value (corresponding to euclidian distance vehicle-->goal) 

        """        
        Ks = self.Ks
        Kv = self.Kv          
        eucli_throttle = eps
        while eucli_throttle >= eps:

            eucli_throttle = sqrt( (x-self.x)**2 + (y-self.y)**2 )
            steering = atan2(  (y-self.y)  , (x-self.x) )

            throttle_gain = max(min(eucli_throttle * Kv, self.throttle_max), self.throttle_min)
            steering_gain = sin(PathTools().shortestAngleDiff(steering, self.theta)) * Ks
            # v = max(min(eucli_throttle * Kv, self.throttle_max), self.throttle_min)
            # s = PathTools().shortestAngleDiff(steering, self.theta) * Ks

            Vl = throttle_gain - steering_gain
            Vr = throttle_gain + steering_gain
        
            self.model(Vl, Vr)

            yield eucli_throttle


    def turn(self, phi, eps_angle=0.1):

        s = 1

        while fabs(s) > eps_angle:

            # v = 10 # Trick... Because a bicyle/car CAN'T turn without linear velocity
            s = PathTools().shortestAngleDiff(phi, self.theta) 

            self.model(-s, s)

            yield s            


    
    # def toPose(self, x, y, theta):

    #     pass





    