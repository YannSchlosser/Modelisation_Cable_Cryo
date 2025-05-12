from Modelisation_Point import Point
import numpy as np

class Cable:

    def __init__(self, liste_des_points, masse=1):
        """
        Instancie un cable compose de point. Toutes les unites sont en metres et kilogrammes
        """
        
        # Tous les points utilises pour representer le cable
        self.liste_points = liste_des_points.copy()
        self.nb_points = len(self.liste_points)

        # Masse du cable
        self.masse_cable = masse

        # Applique une masse a chaque points
        for point in self.liste_points:
            point.masse = self.masse_cable / self.nb_points

    def simulation_chute(self, t0, tfin, dt, recorder=None):

        if not recorder is None:
            t = t0
            while t <= tfin:
                recorder.record_etat(t)
                self.simulation_1_iteration(dt)
                t += dt

        else: 
            t = t0
            while t < tfin:
                self.simulation_1_iteration(dt)
                t += dt

    def simulation_1_iteration(self, dt):

        for point in self.liste_points:

            if not point.fige:

                # Calcul des effets de gravite
                force_gravite = np.zeros((2, 1))
                force_gravite[1] = -point.gravite()

                # Calcul de la tension au point de gauche et de droite
                force_tension_points_voisins = point.tension(constante_raideur=2000)
                # if point.indice_point == 2:
                #     print(point.x, point.y)

                # Somme des forces
                somme_forces = force_tension_points_voisins + force_gravite

                # Integration de l'acceleration
                point.vx = float(point.vx + somme_forces[0] / point.masse * dt)
                point.vy = float(point.vy + somme_forces[1] / point.masse * dt)

                # Integration de la vitesse
                point.x = point.x + point.vx * dt
                point.y = point.y + point.vy * dt

if __name__ == "__main__":
    
    p1 = Point(0, 10)
    p2 = Point(2, 8, p1)

    c = Cable(Point.points_instancies, masse=10)
    print(p1.masse)
