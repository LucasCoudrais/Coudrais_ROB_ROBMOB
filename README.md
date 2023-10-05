# Local planer
## Envoyer une liste de way point
- Pour envoyer un goal simplement envoyer le message donné au service de notre noeud avec les TODO correctement complétés
- Pour que notre algo prenne en compte une liste de way point, il faut cette fois envoyer un message différent a un autre service.
- Le message pourrait etre tres tres complexe, pour cela lancer le noeud `testPathGenerator` qui va envoyer une liste de way point a notre place.
- Ne pas oublier pour cette partie la de lancer les autre noeud ros dont avait besoin pour le global planner
- - Le noeud de map server  
- - Le noeud de navigation