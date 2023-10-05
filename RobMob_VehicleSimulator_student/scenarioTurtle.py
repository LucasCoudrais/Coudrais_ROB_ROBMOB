#!/usr/bin/env python  

__author__ = 'Lucas Coudrais'

from vehicles.TurtleBot import TurtleBot
from VehicleSimulator import *

# create simulator instance
vs = VehicleSimlulator()

# create vehicle instance
turtlebot = TurtleBot()

# Choose one particular vehicle
vs.selectVehicle(turtlebot)

# --- SCENARIO ---
vs.toPoint( *BLUE )
vs.toPoint( *GREEN )
vs.toPoint( *PURPLE )
vs.turn( pi/4 )

# End of Scenario
vs.frame.mainloop()

