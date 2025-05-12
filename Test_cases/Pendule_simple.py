import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
sys.path.append("/Users/yannschlosser/Desktop/Entrainement Python/Modelisation_Cable_Cryo/")

from Modelisation_Point import Point
from Modelisation_Cable import Cable
from Visualisation import Recorder


"""
Les points sont places a 10m de hauteur, le premier point est fixe, le deuxieme est a 10m sur sa droite et libre de mouvement
Le cas test vise a reproduire le mouvement d'un pendule simple
"""

############# DEFINITION DES POINTS #############
p1 = Point(0, 10, is_fige=True)
p2 = Point(10, 10, pt_rat=p1)
p3 = Point(20, 10, pt_rat=p2)
#################################################

#############  DEFINITION DU CABLE  #############
c = Cable(Point.points_instancies, masse=10)
#################################################

#############  DEFINITION RECORDER  #############
r = Recorder(Point.points_instancies)
#################################################


########### Demarrage de la simulation ###########
c.simulation_chute(t0=0, tfin=5, dt=0.01, recorder=r)
##################################################

r.calibrage_animation(duree_simu=5)

# Configuration de la figure
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
ax, ax2 = axes[0], axes[1]

ani1 = r.animation_cable(fig, axes[0], see_past=False)
# ani2 = r.animation_vecteur_tension(fig, axes[1], indice_du_point=1)

# Affichage de l'animation
plt.show()


# Sauvegarde du GIF
# ani.save('simulation.gif', writer='pillow')
