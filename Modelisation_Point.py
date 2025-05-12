import numpy as np

class Point:

    # Pour suivre tous les points instancies
    points_instancies = []

    def __init__(self, x_ini=0, y_ini=0, vx_ini=0, vy_ini=0, pt_rat=None, is_fige=False):
        """
        Instanciation d'un point. Mesures en metres et en kilogrammes.
        """

        self.vecteur_gauche = np.zeros((2, 1))
        self.vecteur_droite = np.zeros((2, 1))

        # Coordonnees initiales
        self.x = x_ini
        self.y = y_ini
        self.vx = vx_ini
        self.vy = vy_ini

        # Point auquel celui ci est rattaché, et calcul de leur distance qui restera fixe
        self.point_de_gauche = pt_rat
        self.point_de_droite = None
        if not pt_rat is None:
            self.point_de_gauche.point_de_droite = self
            self.distance_pt_gauche = np.linalg.norm(np.asarray([self.x, self.y]) - 
                                                     np.asarray([self.point_de_gauche.x, self.point_de_gauche.y]))

        # Permet de savoir si ce point est bloque (ne subira pas de deplacement)
        self.fige = is_fige

        # Masse associee au point
        self.masse = None

        # Donne un indice au pointt et l'ajoute a la liste des points instancies
        self.indice_point = len(Point.points_instancies)
        Point.points_instancies.append(self)

    def gravite(self):

        g = 9.81   # m/s^2 - acceleration due à la gravite
        acceleration_gravite = self.masse * g

        return acceleration_gravite
    
    def tension(self, constante_raideur=500):

        force_tension_point_gauche = np.zeros((2, 1))
        force_tension_point_droite = np.zeros((2, 1))
        p1 = np.asarray([self.x, self.y]).reshape(2, 1)

        if not self.point_de_gauche is None:
            p2 = np.asarray([self.point_de_gauche.x, self.point_de_gauche.y]).reshape(2, 1)
            distance_p1_p2 = np.linalg.norm(p2 - p1)
            force_tension_point_gauche += constante_raideur * (distance_p1_p2 - self.distance_pt_gauche) * (p2 - p1) / distance_p1_p2
            # force_tension_point_gauche *= self.point_de_gauche.masse * force_tension_point_gauche

            self.vecteur_gauche = (p2 - p1) / distance_p1_p2

        if not self.point_de_droite is None:
            p2 = np.asarray([self.point_de_droite.x, self.point_de_droite.y]).reshape(2, 1)
            distance_p1_p2 = np.linalg.norm(p2 - p1)
            force_tension_point_droite += constante_raideur * (distance_p1_p2 - self.point_de_droite.distance_pt_gauche) * (p2 - p1) / distance_p1_p2
            # force_tension_point_droite *= self.point_de_droite.masse * force_tension_point_droite

            self.vecteur_droite = (p2 - p1) / distance_p1_p2

        # if self.indice_point == 1:
        #     print(force_tension_point_gauche, force_tension_point_droite)

        return force_tension_point_gauche + force_tension_point_droite



if __name__ == "__main__":
    
    p1 = Point(0, 10)
    p2 = Point(2, 8, pt_rat=p1)

    print(p1.x)
    print(p1.indice_point, p2.indice_point)

