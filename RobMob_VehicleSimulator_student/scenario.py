#!/usr/bin/env python  

__author__ = 'Raphael Leber'

from vehicles.Bicycle import Bicycle
from VehicleSimulator import *

# create simulator instance
vs = VehicleSimlulator()

# create vehicle instance
bicycle = Bicycle()

# Choose one particular vehicle
vs.selectVehicle(bicycle)

# --- SCENARIO ---
vs.toPoint( *BLUE )
vs.toPoint( *GREEN )
vs.toPoint( *PURPLE )
vs.turn( pi/4 )

# End of Scenario
vs.frame.mainloop()

