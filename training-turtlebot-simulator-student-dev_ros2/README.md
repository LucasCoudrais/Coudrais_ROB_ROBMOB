turtlebot_simulator
===================

Launchers for Gazebo simulation of the TurtleBot

- see [how to start simulation](./simulation/gazebo/gazebo_sim_nav/Readme.md)
- see [Ros Navigation Stack Pratical Work](./simulation/gazebo/gazebo_sim_nav/Tp.md)
- see [Ros Navigation Stack Local Planner Pratical Work](./turtlebot_gazebo/Tp2.md)

# Répose question Partie 1 

- robot_radius: 0.22 => Taille limite du robot   
inflation_radius: 0.33 => Taille du grossissement, c'est une marge mais pas une limite en soit


4.5 bis ca remarche pas il fonce dedans=> changement de priorité

Pour l'abre de comportement en gros il dit que des qu'on crash et donc qu'on rentre sous la table, on clear la local costet on refait, vu qu'on fait quand on est osus la talble, l'angle de la diago est trop bas donc on ne voit le dessus de la talbe. On ne voit pas le dessus si on est trop proche pour ca et si on est trop loin a cause des valeurs voxel.