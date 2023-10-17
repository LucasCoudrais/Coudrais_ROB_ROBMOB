turtlebot_simulator
===================

Launchers for Gazebo simulation of the TurtleBot

- see [how to start simulation](./simulation/gazebo/gazebo_sim_nav/Readme.md)
- see [Ros Navigation Stack Pratical Work](./simulation/gazebo/gazebo_sim_nav/Tp.md)
- see [Ros Navigation Stack Local Planner Pratical Work](./turtlebot_gazebo/Tp2.md)

# Réponse question Partie 1 

# 1.3

`What happened when the robot move ? Why ?`
- Le robot scanne son environnement avec son laser et le conserve en mémoire. Le but est d'explorer autant que possible pour cartographier l'environnement.

`What happened when your robot tries to map long corridor ? Explain`
- Étant donné que l'odométrie peut ne pas représenter avec précision la réalité dans un environnement sans nombreuses caractéristiques distinctives, le robot peut dévier de son environnement réel. S'il rencontre un angle ou une partie distincte, qui soit plus distinguable que juste une ligne droite, le robot pourra se recalibrer.

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
- L'image 'map.pgm' est la carte utilisée, le mode 'trinary' indique la manière dont la carte est encodée. La résolution est de 0,05 mètres par pixel, et l'origine est située à [-16,5, -8,92, 0].

# 2.1 
`What is the difference between local and global_costmap, What is the purpose of each costmap ?`
- La local costmap représente les coûts dans la carte locale autour du robot, conçue pour répondre aux obstacles imprévus non présents dans la carte globale. La global costmap sert à cartographier les murs et les obstacles connus, ainsi qu'à planifier des itinéraires.

```
In the global costmap explain the following:

    update_frequency
    resolution: 0.05
    static_layer
```
- La fréquence de mise à jour détermine à quelle fréquence la carte globale est mise à jour. La résolution de 0,05 mètres par pixel définit la précision de la carte. La couche statique gère les obstacles fixes.

`What happened when the robot tries to cross a door ? Why ?`
- Il entre complètement dans le mur car le robot se déplace comme s'il était aussi mince qu'un point. Par conséquent, l'empreinte du robot peut se superposer complètement à un mur comme s'il n'existait pas jusqu'à ce que le point rencontre un mur, provoquant un bug. Il est nécessaire de gonfler les murs de la taille du rayon du robot pour simuler une limite jusqu'ou le robot ne doit pas trop s'approcher du mur pour ne pas rentrer dedans.

# 3.2 
`What happened with the new configuration ? Explain the different robot trajectories ?`
- Il tient désormais compte de la taille réelle du robot, en gonflant artificiellement les murs de la taille du robot pour éviter les collisions. Par conséquent, il ne heurte plus les murs et ne reste pas bloqué en frolant les murs ou en passant par une porte.

`Explain the impact of the parameters. (see ROS1 inflate layer)`
- robot_radius : 0,22 => La taille maximale du robot, valeur de gonflement des murs, les cout dans cette zone est alors un obstacle.
- inflate_radius : 0,33 => La taille d'inflation, une marge mais pas une limite en soi. pour le robot. Cela represente une zone a plus fort cout pour les algos. Cela agit comme une fonction decroissante par rapport ala distance du mur gonflé. Le coeff de cette decroissance depend du facteur que l'on peut changer aussi.

`In gazebo, add an obstacle in front of the robot. Try to send an order of navigation through rviz. What happen ? Why ?`
- Il ne longe plus les murs ni n'entre dans les portes. En gonflant les murs, le robot évite de coller aux murs et suit un chemin qui évite tout contact avec les obstacles gonflés dans son algorithme de planification de trajectoire globale.

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
- obstacle_layer : Couche gérant les obstacles dans la navigation.

- combination_method : Méthode de combinaison des informations des capteurs pour construire une carte d'obstacles.

- - track_unknown_space : Suivre les espaces inconnus en plus des obstacles.

- Sensor management parameter (Paramètre de gestion des capteurs) :

- - observation_sources : Sources de données des capteurs utilisées pour construire la carte d'obstacles.
- - max_obstacle_height : Hauteur maximale des obstacles pris en compte.
- - obstacle_max_range : Portée maximale des capteurs pour détecter les obstacles.
- - raytrace_max_range : Portée maximale pour le traçage des rayons.

# 4.3 
`Try to send an order of navigation through rviz. What happen ? Why ?`
- Le robot passe à travers les obstacles, même s'il peut les voir clairement avec le laser il ne s'arrete pas ou ne les contourne pas. Du coup cela engendre une collisison et le robot continue sa route et pousse l'obstacle.

# 4.5 
`Try to send an order of navigation through rviz. What happen ? Why ?`
- En ajoutant l'inflation des murs aux obstacles, le robot s'arrête lorsqu'il rencontre un obstacle inattendu, ce qui l'empêche de naviguer jusqu'à la destination, il reste bloqué devant l'obstacle inattendu.

# 4.5bis
`Make the test again has explain in 4.5, What happens ? Why ?`
- Le robot entre toujours en collision avec l'obstacle et le pousse. La priorité est modifiée, et la couche d'inflation doit connaître les obstacles pour fonctionner correctement. Dans ce cas, l'inflation est appliquée avant de considérer les obstacles, donc la couche d'inflation ne gonfle pas les obstacles.

# 4.6
`Does the global planner take into account the obstacle ? Why ?`
- (Aucune différence observé il me semble)

`What happen ? Why ?`
- (Aucune différence observé il me semble)

`How is it possible to fix that ?`
- (Aucune différence observé il me semble)

# 6.3
`What happen ? Why ? what is the difference with the new /global_costmap/costmap into rviz ? Why ?`
- Il prend en compte les obstacles imprévus dans le calcul de l'itinéraire en ajoutant la carte locale à la carte globale. Maintenant, il navigue efficacement autour d'eux car la globale recalcule l'itnieraire en ayant connaissance des nouveau obstacle et donc recalcul l'itinéraire en prenant en compte ces nouveaux obstacle.

# 7.2
`What happened ? why ?`
- Le robot scanne avec un laser 2D qui projette une ligne horizontalement avec une certaine verticalité. En conséquence, il ne voit que les pieds de la table et pas le dessus. Il évite bien les pieds de la table mais ne sait pas qu'il y a une table au dessus de lui.

`What can you conclude ?`
- C'est efficace, mais dans certains cas, nous pourrions souhaiter détecter des objets au-dessus de nous.

# 7.3 
`What is the difference between voxel_layer and obstacle_layer ?`
- La couche voxel aplati le terrain 3D en 2D, pour que passer sous la table soit considéré comme un obstacle. Des paramètres appropriés sont nécessaires pour en tenir compte lorsque le robot n'est ni trop près ni trop loin.

# 7.4
`What happened ? why ?`
- Le dessus de la table est considéré comme un obstacle, mais on ne voit que le debut lorsque le robot est à distance et la fin lorsque le robot est proche. Lorsque le robot s'approche de l'obstacle, il s'arrête. L'arbre de comportement recalcule alors l'obstacle, et comme la numérisation 3D ne voit plus le dessus de la table à cause de la proximité, il ne voit que les pieds, ce qui fait que le robot passe à travers après s'être arrêté.

# Bonus compréhension behavior tree
Dans l'arbre de comportement, il est défini que quand on heurte un obstacle, on clear la map et on refait tout. Ainsi lorsque le robot heurte et passe sous la table, il efface la carte et la réévalue. Lorsqu'il est sous la table, l'angle diagonal est trop bas pour voir le dessus de la table, ce qui provoque des problèmes. Il ne voit pas le dessus s'il est trop près ou trop loin en raison des valeurs voxel.