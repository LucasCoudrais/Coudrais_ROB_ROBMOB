turtlebot_simulator
===================

Launchers for Gazebo simulation of the TurtleBot

- see [how to start simulation](./simulation/gazebo/gazebo_sim_nav/Readme.md)
- see [Ros Navigation Stack Pratical Work](./simulation/gazebo/gazebo_sim_nav/Tp.md)
- see [Ros Navigation Stack Local Planner Pratical Work](./turtlebot_gazebo/Tp2.md)

# Réponse question Partie 1 

# 1.3

`What happened when the robot move ? Why ?`
- on voit que son laser scan tout l'environnement et le garde en mémoire, le but est d'explorer tout ce qui est possible pour mapper l'environnement

`What happened when your robot tries to map long corridor ? Explain`
- etant donné qu'il est difficile que l'odométrie soit representative de la realisté et qu'on ne soit dans un environnement sans trop de distinction, le rabot va se decaler par rapport a son environnement reel, si on croise une angle ou une partie distincitve de jjuste une ligne droire, le robot va se recalibrer

# 1.4
`Open the myMap.yaml and explain each lines`
- Voici notre fichier `myMap.yaml` : 
```
image: map.pgm
mode: trinary
resolution: 0.05
origin: [-16.5, -8.92, 0]
negate: 0
occupied_thresh: 0.65
free_thresh: 0.25
```

TODO

# 2.1 
`What is the difference between local and global_costmap, What is the purpose of each costmap ?`
- local c'est les cout de la map local qui suit le robot, faite pour repondre si jamais on voit des obstable qui ne sont pas prevu ou present dans la global. Global on s'en sert pour y mettre les murs et obstacle connu. et aussi pour faire les itinéraire.

```
In the global costmap explain the following:

    update_frequency
    resolution: 0.05
    static_layer
```
- TODO

`What happened when the robot tries to cross a door ? Why ?`
- il rentre totalement dans le mur car le robot se deplace comme s'il etait aussi epais qu'un point et donc le tour du robot qui est autour du point peut totalement rentre dans un mur comme s'il nexistait pas jusqu'a ce que point rencontre un mur mais du coup ca bug. il faut inflate les murs

# 3.2 
`What happened with the new configuration ? Explain the different robot trajectories ?`
- il prend mtn en compte la taille du robot relle, on grossit les murs artificiellement de la taille du robot pour eviter qu'il rentre dedans. du coup il rentre pas dedans et ca bug plus quand il longe les mur ou passe une porte 

`Explain the impact of the parameters. (see ROS1 inflate layer)`
- robot_radius: 0.22 => Taille limite du robot   
inflation_radius: 0.33 => Taille du grossissement, c'est une marge mais pas une limite en soit

`In gazebo, add an obstacle in front of the robot. Try to send an order of navigation through rviz. What happen ? Why ?`
- il ne longe plus les murs et ne rentre plus dans les porte, comme on a grossit les murs, encore mieux, on a prevu une marge selon des parametre qui fait que le robot pourra coller les murs, mais il evitera de le faire car ce coutera plus cher de froler les murs inflate dans son algo d'intineraire global map

# 4.2
```
Find the definition of each parameter (ROS2 Nav2,ROS1 obstacle layer):

    obstacle_layer:
    combination_method
        track_unknown_space
    Sensor management parameter
        observation_sources
        max_obstacle_height
        obstacle_max_range
        raytrace_max_range

    Which kind of information is used as observation source ? Is there any alternative ?
```
- TODO 

# 4.3 
`Try to send an order of navigation through rviz. What happen ? Why ?`
- il passe totalement a travers meme s'il le voit bien avec le laser. du coup ca le pousse

# 4.5 
`Try to send an order of navigation through rviz. What happen ? Why ?`
- on rajoute l'inflate des murs aux obstacles, mais du coup il s'arrete simplement aux obstacle et ne parvient pas a le contourner et donc pas a aller au goal 

# 4.5bis
`Make the test again has explain in 4.5, What happens ? Why ?`
- 4.5 bis ca remarche pas il fonce dedans=> changement de priorité, l'inflate layer a besoin de connaitre les obstable pour fonctionner hors la on fait l'inflate avant les obstacle donc l'innflate ne va pas inflate les obstacles

# 4.6
`Does the global planner take into account the obstacle ? Why ?`
- je crois que a ce moement la ca change rien

`What happen ? Why ?`
- 

`How is it possible to fix that ?`
- 

# 6.3
`What happen ? Why ? what is the difference with the new /global_costmap/costmap into rviz ? Why ?`
- oui car on rajoute le local map dans le global ce qui permet de prendre en compte les obstacles imprevu dans le calcul de l'itinéraire donc mtn on le contourne bien 

# 7.2
`What happened ? why ?`
- comme on scan avec un laser qui tire une ligne 2D sur une ligne horizontale a une certaine verticalité. donc on ne voit que les pied de la table et pasd u tout le dessus. On prend bien compteces obstable et du coup on passe entre les pieds.

`What can you conclude ?`
- C'est cool mais dans certain cas on pourrait avoir envie de savoir les truc au dessus de nous

# 7.3 
`What is the difference between voxel_layer and obstacle_layer ?`
- on prend applatit le trrain 3d en 2D du coup, passer sous la table est considérer comme etant un obstacle. il faut bien mettre des bon parametre pour prendre ca en compte quand on est pas trop pres no trop loin.

# 7.4
`What happened ? why ?`
- On prend bien en compte le dessus de la table comme etant un opbstable, mais on bvoit seulement le devant quand on est un peu loin et seulement le derriere quanjd on est un peu pres. Quand on va sur l'obstacle, on s'arrete et le BT fait que l'obstacle est recalculer et comme on estr dessous le scan 3D ne voit plus le dessus de la table car trop pres du ocup on ne voit plus que les pied et du coup on passe a traver a pres s'etre arreter 

# Bonus compréhension behavior tree
Pour l'abre de comportement en gros il dit que des qu'on crash et donc qu'on rentre sous la table, on clear la local costet on refait, vu qu'on fait quand on est osus la talble, l'angle de la diago est trop bas donc on ne voit le dessus de la talbe. On ne voit pas le dessus si on est trop proche pour ca et si on est trop loin a cause des valeurs voxel.