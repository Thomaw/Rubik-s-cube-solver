import matplotlib.pyplot as plt
from class_quaternion import *


class Cube:
    # Définition du cube
    '''
    Pour créer un rubik's cube, il nous faut les éléments suivants:
    - Cube noir
    - stickers de couleurs pour simuler les cubes des faces
    '''

    base_face = np.array([[1, 1, 1], [1, -1, 1], [-1, -1, 1],
                          [-1, 1, 1], [1, 1, 1], [0, 0, 0],
                          [0, 0, 0], [0, 0, 0], [0, 0, 0]])  # Face unité

    # Permet de créer les petits cubes qui iront sur chaque face
    d1, d2, d3 = 0.95, 0.9, 1.001
    # Positionnement planaire des points permettant de créer un sticker
    base_sticker = np.array([[d1, d2, d3], [d2, d1, d3], [-d2, d1, d3],
                             [-d1, d2, d3], [-d1, -d2, d3], [-d2, -d1, d3],
                             [d2, -d1, d3], [d1, -d2, d3], [d1, d2, d3]])

    x, y, z = np.eye(3)  # Matrice I (3*3)

    # Définition des rotations nécessaires pour le positionnement dans l'espace des faces et stickers
    rots = [Quaternion.from_v_theta(np.eye(3)[0], theta) for theta in (np.pi / 2, -np.pi / 2)]
    rots += [Quaternion.from_v_theta(np.eye(3)[1], theta) for theta in (np.pi / 2, -np.pi / 2, np.pi, 2 * np.pi)]

    # On créer ensuite chaque élément nécessaire définit dans la partie théorique
    def __init__(self, cube=None):
        self.face_colors = ["#00008f", "#009f0f", "#cf0000", "#ff6f00", "w", "#ffcf00"]
        self.colors = []          # Définition des couleurs
        self.centre_face = []     # Définition des centres des faces
        self.faces = []           # Définition des faces
        self.centre_sticker = []  # Définition des centres des stickers
        self.sticker = []         # Définition des stickers
        self.initialisation()     # Appelle de la procédure d'initialisation

    def initialisation(self):
        # Création des déplacements 3D des différentes parties du cube
        translations = np.array([[[-1 + (i + 0.5) * 2. / 3, -1 + (j + 0.5) * 2. / 3, 0]]
                                 for i in range(3)
                                 for j in range(3)])

        # Création d'un facteur d'échelle permettant de réduire certaines imperfections
        facteur = np.array([1. / 3, 1. / 3, 1])

        # Placement des points :
        for i in range(6):
            # Création de la matrice de rotation pour la face i
            M = self.rots[i].as_rotation_matrix()

            '''Création de la rotation des différentes parties du cube 
                               - Faces
                               - stickers 
                               - centre des faces
                               - centre des stickers
                            '''
            faces_t = np.dot(facteur * self.base_face + translations, M.T)
            sticker_t = np.dot(facteur * self.base_sticker + translations, M.T)
            centre_face_t = np.dot(np.array([0, 0, 1]) + translations, M.T)
            centre_sticker_t = np.dot(np.array([0, 0, 1.001]) + translations, M.T)

            # Création des couleurs de chaque face
            colors_i = i*np.ones(9, dtype=int)

            centre_face_t = centre_face_t.reshape(-1, 3)
            centre_sticker_t = centre_sticker_t.reshape(-1, 3)

            # Ajout des positions finales aux listes correspondantes
            self.faces.append(faces_t)
            self.centre_face.append(centre_face_t)
            self.sticker.append(sticker_t)
            self.centre_sticker.append(centre_sticker_t)
            self.colors.append(colors_i)

        # Mise en forme du résultat
        self.centre_face = np.vstack(self.centre_face)
        self.faces = np.vstack(self.faces)
        self.centre_sticker = np.vstack(self.centre_sticker)
        self.sticker = np.vstack(self.sticker)
        self.colors = np.concatenate(self.colors)

    def Affichage(self):
        ''' Implémentation d'une figure'''
        fig = plt.figure()                  # création figure
        fig.add_axes(Interaction(self))     # Ajout de la classe qui va suivre dans la figure
        return fig


class Interaction(plt.Axes):
    ''' Classe permettant de modéliser le cube'''

    def __init__(self, cube=None, rect=[0, 0.1, 1, 0.9], **kwargs):
        fig = plt.gcf() # Affichage d'une interface pour les figures

        # Paramétrages de la figure
        kwargs.update(dict(aspect='equal', xlim=(-2.0, 2.0), ylim=(-2.0, 2.0)))
        super(Interaction, self).__init__(fig, rect, **kwargs)

        self.cube = cube   # Variable représentant le cube
        self._draw_cube()  # Met à jour l'affichage du cube

    def _project(self, pts):
        '''Fonction permettant de projeter les points par rapport à la vue de l'utilisateur'''
        return project_points(pts, Quaternion.from_v_theta((1, -1, 0), -np.pi / 6), (0, 0, 10), [0, 1, 0])

    def _draw_cube(self):
        '''Fonction pour dessiner le cube dans une figure'''

        # Projete les points de chaque élément défini dans la classe cube et l'associe à
        # sa variable éqivalente dans cette classe.
        sticker = self._project(c.sticker)[:, :, :2]
        faces = self._project(c.faces)[:, :, :2]
        centre_face = self._project(c.centre_face[:, :3])
        c.centre_sticker = self._project(c.centre_sticker[:, :3])

        c.colors = np.asarray(self.cube.face_colors)[c.colors]
        face_ordre = -centre_face[:, 2]
        sticker_ordre = -c.centre_sticker[:, 2]

        # Pour chaque face et sticker:
        for i in range(0,54):
            # Création du polygone associé à la face et au stickers i
            fp = plt.Polygon(faces[i], facecolor='black', zorder=face_ordre[i])
            sp = plt.Polygon(sticker[i], facecolor=c.colors[i], zorder=sticker_ordre[i])

            # Implémentation de ceux-ci dans la figure
            self.add_patch(fp)
            self.add_patch(sp)


c = Cube()     # Récupération de l'ojet Cube()
c.Affichage()  # Crée et positionne la figure
plt.show()     # Affiche la figure
