from Modelisation_Point import Point
from Visualisation import Recorder



p1 = Point(0, 10)
p2 = Point(2, 8, pt_rat=p1)

visu = Recorder(Point.points_instancies)
visu.affiche_instant_t()