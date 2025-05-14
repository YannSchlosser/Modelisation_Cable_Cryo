import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import matplotlib.transforms as mtransforms

class Recorder:

    def __init__(self, liste_de_pts):
        
        # Liste des points instancies
        self.liste_points = liste_de_pts.copy()

        # Variable de memoire --> indice du point : liste des ses etats au travers de la simulation
        self.raz_memoire()

    def affiche_instant_t(self, x_range=None, y_range=None):

        plt.figure()

        # Recuperation des coordonnees des points
        liste_x, liste_y = [], []
        for point in self.liste_points:
            liste_x.append(point.x)
            liste_y.append(point.y)

        plt.scatter(liste_x, liste_y)

        # Ajustement de la fenetre si demande
        if not x_range is None:
            plt.xlim(x_range)
        if not y_range is None:
            plt.ylim(y_range)
        
        plt.show()

    def raz_memoire(self):
        
        self.memoire = {point.indice_point:{"x":[], "y":[], "vx":[], "vy":[],
                                            "vecteur_tension_gauche":[], "vecteur_tension_droite":[]} for point in self.liste_points}
        self.memoire["temps"] = []

    def record_etat(self, t):

        self.memoire["temps"].append(t)
        for point in self.liste_points:
            self.memoire[point.indice_point]["x"].append(point.x)
            self.memoire[point.indice_point]["y"].append(point.y)
            self.memoire[point.indice_point]["vx"].append(point.vx)
            self.memoire[point.indice_point]["vy"].append(point.vy)

            self.memoire[point.indice_point]["vecteur_tension_gauche"].append(point.vecteur_gauche)
            self.memoire[point.indice_point]["vecteur_tension_droite"].append(point.vecteur_droite)

    def calibrage_animation(self, duree_simu):
        """
        Vient calibrer le temps (ms) entre deux frames pour les animations 
        et quelles images doivent etre selectionnees pour avoir 58fps temps reel sur les animations
        """

        self.nb_frame_simu = len(self.memoire["temps"])

        # Cas ou on a pas assez ou juste assez d'image pour avoir les 58fps
        if self.nb_frame_simu/duree_simu <= 58:
            self.intervale_frame = (duree_simu * 1000) / self.nb_frame_simu          # On met un ecart de : temps (ms) / nb_frame entre chaque frame
            self.frame_modulo = None            # On garde toutes les frames

        # On a plus de 58fps, il faut donc trier les images et juster l'intervale entre deux frames
        else:
            nb_frame_sec = self.nb_frame_simu / duree_simu       # Nombre de frame par seconde (non triee)
            self.frame_modulo = int(nb_frame_sec / 58)           # On va afficher 1 frame toute les frame_modulo frames
            self.intervale_frame = 17                       # 58 fps represente un ecart de 17ms entre deux frames

    def func_animation(self, figure, update, init):

        # Dans le cas ou on garde toutes les frames
        if self.frame_modulo is None:
            ani = animation.FuncAnimation(figure, update, frames=self.nb_frame_simu, interval=self.intervale_frame, init_func=init, blit=False)
            
        # Dans le cas ou on doit trier les frames
        else:
            ani = animation.FuncAnimation(figure, update, frames=range(0, self.nb_frame_simu, self.frame_modulo), 
                                          interval=self.intervale_frame, init_func=init, blit=False)
            
        return ani

    def animation_cable(self, figure, axe, see_past=False):

        # Fonction d'initialisation
        def init():
            for line in lines:
                line.set_data([], [])
            return lines

        # Fonction de mise a jour
        def update(frame):
            if see_past:
                for i, point in enumerate(self.liste_points):
                    lines[i].set_data(self.memoire[point.indice_point]["x"][:frame], self.memoire[point.indice_point]["y"][:frame])
            else:
                for i, point in enumerate(self.liste_points):
                    lines[i].set_data(self.memoire[point.indice_point]["x"][frame], self.memoire[point.indice_point]["y"][frame])

            title.set_text("Temps : {}".format(round(self.memoire["temps"][frame], 2)))

            return lines

        # Configuration du graphique
        axe.set_xlim(min(min(self.memoire[p.indice_point]["x"]) for p in self.liste_points) - 1,
                    max(max(self.memoire[p.indice_point]["x"]) for p in self.liste_points) + 1)
        axe.set_ylim(min(min(self.memoire[p.indice_point]["y"]) for p in self.liste_points) - 1, 
                     max(max(self.memoire[p.indice_point]["y"]) for p in self.liste_points) + 1)
        axe.set_xlabel('Position X')
        axe.set_ylabel('Position Y')
        axe.set_title('Simulation de la chute du câble')
        axe.set_aspect('equal')  # Maintien de l'aspect ratio
        axe.grid()

        title = axe.text(0.5, 1.5, "", bbox={'facecolor':'w', 'alpha':0.5, 'pad':5}, transform=axe.transAxes, ha="center")
        lines = [axe.plot([], [], marker='o')[0] for _ in self.liste_points]
        
        return self.func_animation(figure, update=update, init=init)
    
    def animation_vecteur_tension(self, figure, axe, indice_du_point):
        """
        Objectif : visualiser 1 ou plusieurs vecteur de tension de 1 ou plusieurs points (a finir)
        """

        # Fonction d'initialisation
        def init():
            for arrow in arrows:
                arrow.set_visible(False)
            return arrows

        # Fonction de mise a jour
        def update(frame):
            if len(self.memoire[indice_du_point]["vecteur_tension_gauche"]) != 0:
                arrows[0].xy = self.memoire[indice_du_point]["vecteur_tension_gauche"][frame]
                arrows[0].set_visible(True)

            if len(self.memoire[indice_du_point]["vecteur_tension_droite"]) != 0:
                arrows[1].xy = self.memoire[indice_du_point]["vecteur_tension_droite"][frame]
                arrows[1].set_visible(True)
            
            return arrows
        
        # Creation des fleches et de leur patchs pour la legende
        arrow_patches = [mpatches.FancyArrowPatch((0, 0), (1, 1), label=f'Vecteur tension gauche', mutation_scale=10, color="g"),
                         mpatches.FancyArrowPatch((0, 0), (1, 1), label=f'Vecteur tension droite', mutation_scale=10, color="r")] 
        arrows = [axe.annotate("", xy=(0, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="g", linewidth=3)),
                  axe.annotate("", xy=(0, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="r", linewidth=3))]

        # Configuration du graphique
        axe.set_xlim([-1, 1])
        axe.set_ylim([-1, 1])
        axe.grid()
        axe.legend(handles=arrow_patches, loc='upper right')
        
        return self.func_animation(figure, update=update, init=init)

    def animation_energie_systeme(self, figure, axe):
        """
        Visualisation de l'energie totale du systeme : Energie potentielle + Energie cinematique
        """

        # Fonction d'initialisation
        def init():
            plot_energie_syst.set_data([], [])
            return plot_energie_syst

        # Fonction de mise a jour
        def update(frame):
            energie_systeme = 0
            for p in self.liste_points:
                if not p.fige:
                    energie_cine, energie_pot = p.calcul_energie(y=self.memoire[p.indice_point]["y"][frame],
                                                                vx=self.memoire[p.indice_point]["vx"][frame],
                                                                vy=self.memoire[p.indice_point]["vy"][frame])
                    energie_systeme += energie_cine + energie_pot
            trace_energie_systeme[frame] = energie_systeme

            plot_energie_syst.set_data(range(frame + 1), trace_energie_systeme[:frame + 1])
            plot_energie_syst.set_visible(True)
            
            return plot_energie_syst

        # Configuration du graphique
        energie_ini_systeme = 0
        for p in self.liste_points:
            if not p.fige:
                energie_cine, energie_pot = p.calcul_energie()
                energie_ini_systeme += energie_cine + energie_pot
        axe.set_ylim([0.9 * energie_ini_systeme, 1.1 * energie_ini_systeme])
        axe.set_xlim([0, len(self.memoire[0]["x"])])

        axe.grid()
        axe.set_xlabel("Frame")
        axe.set_title("Energie du système (J)")
        # axe.legend(handles=arrow_patches, loc='upper right')

        trace_energie_systeme = [None for _ in range(self.nb_frame_simu)]
        plot_energie_syst = axe.plot([], [], marker='o')[0]
        
        return self.func_animation(figure, update=update, init=init)
        


    


if __name__ == "__main__":
    
    r = Recorder([])

    memoire = {i:[] for i in range(5)}
    print(memoire)
    l = [0, 1, 2, 3, 4, 5, 6, 7]
