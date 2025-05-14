import numpy as np

class Point:

    # Pour suivre tous les points instancies
    points_instancies = []

    def __init__(self, x_ini=0, y_ini=0, vx_ini=0, vy_ini=0, pt_rat=None, is_fige=False):
        """
        Instanciation d'un point. Mesures en metres et en kilogrammes.
        """

        # Coordonnees initiales
        self.x = x_ini
        self.y = y_ini
        self.vx = vx_ini
        self.vy = vy_ini

        # Vecteur force : somme des forces
        self.somme_des_forces = np.zeros((2, 1))

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

        # Vecteurs de tensions avec les points voisins - pour la visualisation
        self.vecteur_gauche = np.zeros((2, 1))
        self.vecteur_droite = np.zeros((2, 1))

        # Donne un indice au pointt et l'ajoute a la liste des points instancies
        self.indice_point = len(Point.points_instancies)
        Point.points_instancies.append(self)

    def calcul_energie(self, y=None, vx=None, vy=None):

        g = 9.81   # m/s^2 - acceleration due à la gravite

        if y is None and vx is None and vy is None:
            energie_cinetique = 1/2 * self.masse * np.linalg.norm(np.asarray([self.vx, self.vy]))**2
            energie_potentielle = self.masse * self.y * g
        
        else:
             energie_cinetique = 1/2 * self.masse * np.linalg.norm(np.asarray([vx, vy]))**2
             energie_potentielle = self.masse * y * g

        return energie_cinetique, energie_potentielle

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

        return force_tension_point_gauche + force_tension_point_droite
    
    def update_cinematique(self, dt):

        # Integration de l'acceleration
        # self.vx = float(self.vx + self.somme_des_forces[0] / self.masse * dt)
        # self.vy = float(self.vy + self.somme_des_forces[1] / self.masse * dt)

        # Integration de la vitesse
        # self.x = self.x + self.vx * dt
        # self.y = self.y + self.vy * dt

        self.rk4(dt)


    def rk4_step(self, dt):
        # Initialisation des variables temporaires
        k1_v = np.zeros((len(Point.points_instancies), 2))
        k1_x = np.zeros((len(Point.points_instancies), 2))
        k2_v = np.zeros((len(Point.points_instancies), 2))
        k2_x = np.zeros((len(Point.points_instancies), 2))
        k3_v = np.zeros((len(Point.points_instancies), 2))
        k3_x = np.zeros((len(Point.points_instancies), 2))
        k4_v = np.zeros((len(Point.points_instancies), 2))
        k4_x = np.zeros((len(Point.points_instancies), 2))
        
        # Sauvegarde des états initiaux
        x_temp = np.array([[p.x, p.y] for p in Point.points_instancies])
        v_temp = np.array([[p.vx, p.vy] for p in Point.points_instancies])

        # Étape 1 : Calcul de k1
        for i, point in enumerate(Point.points_instancies):
            if not point.fige:
                # Calcul des forces
                force_gravite = np.array([0, -point.gravite()])
                force_tension = point.tension().flatten()

                # Accélération
                a = (force_gravite + force_tension) / point.masse

                # k1
                k1_v[i] = a
                k1_x[i] = v_temp[i]

        # Étape 2 : Calcul de k2
        for i, point in enumerate(Point.points_instancies):
            if not point.fige:
                # Mise à jour temporaire des positions et vitesses
                point.x = x_temp[i, 0] + 0.5 * dt * k1_x[i, 0]
                point.y = x_temp[i, 1] + 0.5 * dt * k1_x[i, 1]
                point.vx = v_temp[i, 0] + 0.5 * dt * k1_v[i, 0]
                point.vy = v_temp[i, 1] + 0.5 * dt * k1_v[i, 1]

                # Calcul des forces
                force_gravite = np.array([0, -point.gravite()])
                force_tension = point.tension().flatten()

                # Accélération
                a = (force_gravite + force_tension) / point.masse

                # k2
                k2_v[i] = a
                k2_x[i] = np.array([point.vx, point.vy])

        # Étape 3 : Calcul de k3
        for i, point in enumerate(Point.points_instancies):
            if not point.fige:
                # Mise à jour temporaire des positions et vitesses
                point.x = x_temp[i, 0] + 0.5 * dt * k2_x[i, 0]
                point.y = x_temp[i, 1] + 0.5 * dt * k2_x[i, 1]
                point.vx = v_temp[i, 0] + 0.5 * dt * k2_v[i, 0]
                point.vy = v_temp[i, 1] + 0.5 * dt * k2_v[i, 1]

                # Calcul des forces
                force_gravite = np.array([0, -point.gravite()])
                force_tension = point.tension().flatten()

                # Accélération
                a = (force_gravite + force_tension) / point.masse

                # k3
                k3_v[i] = a
                k3_x[i] = np.array([point.vx, point.vy])

        # Étape 4 : Calcul de k4
        for i, point in enumerate(Point.points_instancies):
            if not point.fige:
                # Mise à jour temporaire des positions et vitesses
                point.x = x_temp[i, 0] + dt * k3_x[i, 0]
                point.y = x_temp[i, 1] + dt * k3_x[i, 1]
                point.vx = v_temp[i, 0] + dt * k3_v[i, 0]
                point.vy = v_temp[i, 1] + dt * k3_v[i, 1]

                # Calcul des forces
                force_gravite = np.array([0, -point.gravite()])
                force_tension = point.tension().flatten()

                # Accélération
                a = (force_gravite + force_tension) / point.masse

                # k4
                k4_v[i] = a
                k4_x[i] = np.array([point.vx, point.vy])

        # Mise à jour finale des positions et vitesses
        for i, point in enumerate(Point.points_instancies):
            if not point.fige:
                point.vx = v_temp[i, 0] + (dt / 6) * (k1_v[i, 0] + 2*k2_v[i, 0] + 2*k3_v[i, 0] + k4_v[i, 0])
                point.vy = v_temp[i, 1] + (dt / 6) * (k1_v[i, 1] + 2*k2_v[i, 1] + 2*k3_v[i, 1] + k4_v[i, 1])

                point.x = x_temp[i, 0] + (dt / 6) * (k1_x[i, 0] + 2*k2_x[i, 0] + 2*k3_x[i, 0] + k4_x[i, 0])
                point.y = x_temp[i, 1] + (dt / 6) * (k1_x[i, 1] + 2*k2_x[i, 1] + 2*k3_x[i, 1] + k4_x[i, 1])

    def rk4(self, dt):

        # TODO: pour l'instant l'acceleration se compose de gravite + tension des points voisins, donc rien qui ne depende du temps ni de la vitesse
        # cependant lorsqu'il y aura des ajouts de frottement et autres forces, il faudra verifier la construction du modele RK4 car les composantes
        # k sont construites avec des instants ou vitesses futurs
        # Idem pour la vitesse

        acceleration = self.somme_des_forces / self.masse
        
        # Integration de l'acceleration pour obtenir la vitesse
        k1_v = dt * acceleration
        k2_v = dt * acceleration
        k3_v = dt * acceleration
        k4_v = dt * acceleration

        self.vx = float( self.vx + (1 / 6) * (k1_v[0] + 2*k2_v[0] + 2*k3_v[0] + k4_v[0]) )
        self.vy = float( self.vy + (1 / 6) * (k1_v[1] + 2*k2_v[1] + 2*k3_v[1] + k4_v[1]) )

        # self.vx = self.vx + acceleration[0] * dt
        # self.vy = self.vy + acceleration[1] * dt


        # Integration de la vitesse pour obtenir la position
        k1_x = dt * np.array([self.vx, self.vy])

        vx = self.vx + 0.5 * dt * k1_x[0]
        vy = self.vy + 0.5 * dt * k1_x[1]
        k2_x = dt * np.array([vx, vy])

        vx = self.vx + 0.5 * dt * k2_x[0]
        vy = self.vy + 0.5 * dt * k2_x[1]
        k3_x = dt * np.array([self.vx, self.vy])

        vx = self.vx + dt * k3_x[0]
        vy = self.vy + dt * k3_x[1]
        k4_x = dt * np.array([self.vx, self.vy])

        self.x = float( self.x + (1 / 6) * (k1_x[0] + 2*k2_x[0] + 2*k3_x[0] + k4_x[0]) )
        self.y = float( self.y + (1 / 6) * (k1_x[1] + 2*k2_x[1] + 2*k3_x[1] + k4_x[1]) )


        # self.x = self.x + self.vx * dt
        # self.y = self.y + self.vy * dt




if __name__ == "__main__":
    
    p1 = Point(0, 10)
    p2 = Point(2, 8, pt_rat=p1)

    print(p1.x)
    print(p1.indice_point, p2.indice_point)

