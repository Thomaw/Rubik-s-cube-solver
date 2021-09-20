import matplotlib.pyplot as plt
from matplotlib import widgets
from class_quaternion import *
plt.rcParams['toolbar'] = 'None'        # Pas de toolbar pour l'affichage via matplotlib


def Cube_3D(txt4):

    class Cube:
        # Définition du cube
        '''
        Pour créer un rubik's cube, il nous faut les éléments suivants:
        - Cube noir
        - stickers de couleurs pour simuler les cubes d'une face
        '''
        base_face = np.array([[1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1], [1, 1, 1]]) # Face unité
        d1, d2, d3 = 0.95, 0.9, 1.001   # Dimensionnement

        # Positionnement planaire des points permettant de créer un sticker
        base_sticker = np.array([[d1, d2, d3], [d2, d1, d3], [-d2, d1, d3],
                                 [-d1, d2, d3], [-d1, -d2, d3], [-d2, -d1, d3],
                                 [d2, -d1, d3], [d1, -d2, d3], [d1, d2, d3]])

        x, y, z = np.eye(3)  # Matrice I (3*3)

        # Définition des rotations nécessaires pour le positionnement dans l'espace des faces et stickers
        rots = [Quaternion.from_v_theta(np.eye(3)[0], theta) for theta in (np.pi / 2, -np.pi / 2)]
        rots += [Quaternion.from_v_theta(np.eye(3)[1], theta) for theta in (np.pi / 2, -np.pi / 2, np.pi, 2 * np.pi)]

        # Définition des mouvements possibles et des conséquences de ceux-ci
        facesdict = dict(F=z, B=-z, R=x, L=-x, U=y, D=-y)

        def __init__(self):
            # couleurs des faces  bleu, vert, rouge, orange, blanc, jaune
            self.face_colors = ["#00008f", "#009f0f", "#FF0000", "#EF7401", "#FFFFFF", "#FFCF00"]

            self._move_list = []            # Liste des mouvements que devra faire l'utilisateur
            self.colors = []                # Définition des couleurs
            self.face_centroids = []        # Définition des faces centrales
            self.faces = []                 # Définition des autres faces
            self.sticker_centroids = []     # Définition des faces centrales des stickers
            self.stickers = []              # Définition des autres faces des stickers
            self._initialize_arrays()       # Appelle de la procédure _initialize_arrays

        def _initialize_arrays(self):
            '''initialise le cube'''

            # Création des déplacements 3D des différentes parties du cube
            translations = np.array([[[-1 + (i + 0.5) * 2./3, -1 + (j + 0.5) * 2./3, 0]]
                                     for i in range(3)
                                     for j in range(3)])

            # Création d'un facteur d'échelle permettant de réduire certaines imperfections
            factor = np.array([1./3, 1./3, 1])

            for i in range(6):
                # Création de la matrice de rotation
                M = self.rots[i].as_rotation_matrix()

                '''Création de la rotation des différentes parties du cube 
                   - Faces
                   - stickers 
                   - centre des faces
                   - centre des stickers
                '''
                faces_t = np.dot(factor * self.base_face + translations, M.T)
                stickers_t = np.dot(factor * self.base_sticker + translations, M.T)
                face_centroids_t = np.dot(np.array([0, 0, 1]) + translations, M.T)
                sticker_centroids_t = np.dot(np.array([0, 0, 1.001])  + translations, M.T)

                # Création des couleurs de chaque face
                colors_i = i*np.ones(9, dtype=int)

                face_centroids_t = face_centroids_t.reshape(-1, 3)
                sticker_centroids_t = sticker_centroids_t.reshape(-1, 3)

                # Ajout dans les listes des positions de chaque élément
                self.faces.append(faces_t)
                self.face_centroids.append(face_centroids_t)
                self.stickers.append(stickers_t)
                self.sticker_centroids.append(sticker_centroids_t)
                self.colors.append(colors_i)

            ''' Reconstruire les tableaux divisés par "vsplit.
                Séparer un tableau en plusieurs sous-réseaux verticalement (par rangée).
             
            Examples
            --------
            >>> a = np.array([1, 2, 3])
            >>> np.vstack((a,b))
            array([[1],
                   [2],
                   [3]])
            '''
            # Mise en forme du résultat
            self._face_centroids = np.vstack(self.face_centroids)
            self._faces = np.vstack(self.faces)
            self._sticker_centroids = np.vstack(self.sticker_centroids)
            self._stickers = np.vstack(self.stickers)
            self._colors = np.concatenate(self.colors)

        def rotate_face(self, f, n=1, layer=0):
            """Rotation des faces lors des mouvements"""

            # Ajoute un mouvemement à la liste des mouvements
            self._move_list.append((f, n, layer))

            # Recherche de l'axe de rotation souhaité par le mouvement
            v = self.facesdict[f]

            # Applique une rotation par rapport à cet axe
            # Rotation de pi/2 car cela représente 90°
            r = Quaternion.from_v_theta(v, n*np.pi/2)

            # Définit la matrice de rotation par cet axe
            M = r.as_rotation_matrix()

            self._face_centroids = self._face_centroids[:, :3]

            # Méthode pour tourner que les cubes nécessaires
            proj = np.dot(self._face_centroids, v) # 54*1
            flag = ((proj > 0.9 - (layer + 1) * 2./3) & (proj < 1.1 - layer * 2./3)) # 54*1

            # Rotation des éléments à tourner
            for x in [self._stickers, self._sticker_centroids, self._faces, self._face_centroids]:
                x[flag] = np.dot(x[flag], M.T)

        def rotate_cube(self, f, sens):
            """Rotation du cubes lors des mouvements cw ou ccw"""
            # Définition du sens de rotation
            if sens == 'CW':
                z = 1
            elif sens == 'CCW':
                z = -1

            # Rotation des trois couches des faces (ce qui représente tout le cube)
            for i in range(0, 3):
                self.rotate_face(f, z, layer=i)

        def draw_interactive(self):
            '''Affichage 3D du cube'''
            fig = plt.figure(figsize=(10, 6))           # Définit la figure et sa taille
            fig.add_axes(InteractiveCube(self))         # Ajoute le cube sur la figure
            fig.canvas.manager.window.move(250, 50)     # Déplace en (x,y) la figure
            return fig

    class InteractiveCube(plt.Axes):

        def __init__(self, cube=None, fig=None, rect=None, **kwargs):
            if rect is None:
                rect = [-0.15, 0.1, 1, 0.9]
            if fig is None:
                fig = plt.gcf()

                # Gère les paramètres de la figure
                kwargs.update(dict(aspect=kwargs.get('aspect', 'equal'),
                                   xlim=kwargs.get('xlim', (-2.0, 2.0)),
                                   ylim=kwargs.get('ylim', (-2.0, 2.0)),
                                   frameon=kwargs.get('frameon', False),
                                   xticks=kwargs.get('xticks', []),
                                   yticks=kwargs.get('yticks', [])))
                super(InteractiveCube, self).__init__(fig, rect, **kwargs)

            self.cube = cube
            self.compteur = -1
            self.arret = False
            self.kpress = False        # permet de vérifier si on a déjà appuyé sur une touche du clavier

            self._start_rot = Quaternion.from_v_theta((1, -1, 0), -np.pi / 6)  # définie la vue initiale

            # désactiver les événements du clavier par défaut
            callbacks = fig.canvas.callbacks.callbacks
            del callbacks['key_press_event']

            # Internal state variable
            self._button1 = False                # Vrai quand le bouton est appuyé
            self._event_xy = None                # Position (x,y) de l'évènement de la souris

            self._current_rot = self._start_rot  # Etat de rotation actuel
            self._face_polys = None              # Création des faces
            self._sticker_polys = None           # Création des stickers

            self._draw_cube()                    # Met à jour l'affichage du cube

            # Connecter les événements GUI
            self.figure.canvas.mpl_connect('button_press_event', self._mouse_press)    # Connexion appui bouton souris
            self.figure.canvas.mpl_connect('button_release_event', self._mouse_release)# Connexion relaché bouton souris
            self.figure.canvas.mpl_connect('motion_notify_event', self._mouse_motion)  # Connexion déplacement souris
            self.figure.canvas.mpl_connect('key_press_event', self._key_press)         # Connexion appui clavier
            self._initialize_widgets()                                                 # Connexion des widgets définis

        def _initialize_widgets(self):
            self._ax_reset = self.figure.add_axes([0.25, 0.05, 0.2, 0.075])    # Positionnement bouton 'Reset View'
            self._btn_reset = widgets.Button(self._ax_reset, 'Reset View')     # Création bouton 'Reset View
            self._btn_reset.on_clicked(self._reset_view)                       # Ajout de la focntion associé au bouton

            self._ax_view = self.figure.add_axes([0.65, 0.73, 0.15, 0.075])    # Positionnement bouton 'Vue du dessus'
            self._btn_dessus = widgets.Button(self._ax_view, 'Vue du dessus')  # Création bouton 'Vue du dessus'
            self._btn_dessus.on_clicked(self._Vue_de_dessus)                   # Ajout de la focntion associé au bouton

            self._ax_view = self.figure.add_axes([0.81, 0.73, 0.15, 0.075])    # Positionnement bouton 'Vue du dessous'
            self._btn_dessous = widgets.Button(self._ax_view, 'Vue du dessous')# Création bouton 'Vue du dessous'
            self._btn_dessous.on_clicked(self._Vue_de_dessous)                 # Ajout de la focntion associé au bouton

            self._ax_view = self.figure.add_axes([0.65, 0.63, 0.15, 0.075])    # Positionnement bouton 'Vue du droite'
            self._btn_droite = widgets.Button(self._ax_view, 'Vue de droite')  # Création bouton 'Vue du droite'
            self._btn_droite.on_clicked(self._Vue_de_droite)                   # Ajout de la focntion associé au bouton

            self._ax_view = self.figure.add_axes([0.81, 0.63, 0.15, 0.075])    # Positionnement bouton 'Vue du gauche'
            self._btn_gauche = widgets.Button(self._ax_view, 'Vue de gauche')  # Création bouton 'Vue du gauche'
            self._btn_gauche.on_clicked(self._Vue_de_gauche)                   # Ajout de la focntion associé au bouton

            self._ax_view = self.figure.add_axes([0.65, 0.53, 0.15, 0.075])    # Positionnement bouton 'Vue arrière'
            self._btn_arriere = widgets.Button(self._ax_view, 'Vue arrière')   # Création bouton 'Vue arrière'
            self._btn_arriere.on_clicked(self._Vue_arriere)                    # Ajout de la focntion associé au bouton

            self._ax_view = self.figure.add_axes([0.81, 0.53, 0.15, 0.075])    # Positionnement bouton 'Vue avant'
            self._btn_avant = widgets.Button(self._ax_view, 'Vue avant')       # Création bouton 'Vue avant'
            self._btn_avant.on_clicked(self._Vue_avant)                        # Ajout de la focntion associé au bouton

            # Affichage du texte 'Vues possibles'
            props = dict(boxstyle='round', facecolor='wheat', alpha=1.5)       # Paramètres du texte
            self.text(2.9, 1.5, 'Vues possibles', fontsize=14, verticalalignment='top', bbox=props)

            # Ajouter bouton avancer et reculer
            self._ax_move = self.figure.add_axes([0.65, 0.1, 0.15, 0.075])     # Positionnement bouton 'Avancer'
            self._btn_avancer = widgets.Button(self._ax_move, 'Avancer')       # Création bouton 'Avancer'
            self._btn_avancer.on_clicked(self._Vue_avancer)                    # Ajout de la focntion associé au bouton

            self._ax_move = self.figure.add_axes([0.81, 0.1, 0.15, 0.075])     # Positionnement bouton 'Reculer'
            self._btn_reculer = widgets.Button(self._ax_move, 'Reculer')       # Création bouton 'Reculer'
            self._btn_reculer.on_clicked(self._Vue_reculer)                    # Ajout de la focntion associé au bouton

            # Affichage du texte 'Mouvements possibles'
            self.text(2.55, -1.3, 'Mouvements possibles', fontsize=14,
                      verticalalignment='top', bbox=props)

        def _project(self, pts):
            return project_points(pts, self._current_rot, (0, 0, 10), [0, 1, 0])

        def _draw_cube(self):
            stickers = self._project(c._stickers)[:, :, :2]
            faces = self._project(c._faces)[:, :, :2]
            face_centroids = self._project(c._face_centroids[:, :3])
            c.sticker_centroids = self._project(c._sticker_centroids[:, :3])

            c.colors = np.asarray(self.cube.face_colors)[c._colors]
            face_zorders = -face_centroids[:, 2]
            sticker_zorders = -c.sticker_centroids[:, 2]

            if self._face_polys is None:
                # appel initial : création d'objets polygonaux et ajout aux axes
                self._face_polys = []
                self._sticker_polys = []

                for i in range(54):
                    fp = plt.Polygon(faces[i], facecolor='black', zorder=face_zorders[i])
                    sp = plt.Polygon(stickers[i], facecolor=c.colors[i], zorder=sticker_zorders[i])

                    self._face_polys.append(fp)
                    self._sticker_polys.append(sp)
                    self.add_patch(fp)
                    self.add_patch(sp)
            else:
                # appel suivant : mise à jour des objets polygonaux
                for i in range(len(c.colors)):
                    self._face_polys[i].set_xy(faces[i])
                    self._face_polys[i].set_zorder(face_zorders[i])

                    self._sticker_polys[i].set_xy(stickers[i])
                    self._sticker_polys[i].set_zorder(sticker_zorders[i])

            self.figure.canvas.draw()

        def rotate(self, rot):
            self._current_rot = self._current_rot * rot

        def rotate_face(self, face, turns=1):
            self.kpress = True                              # Si une touche a été appuyé, interdit de réappuyer
            for j in range(2):
                for i in range(5):
                    self.cube.rotate_face(face, turns / 10) # Tourne progressivemene le cube
                    self._draw_cube()                       # L'affiche en temps réel

                    # Met une pause entre chaque rotation pour bien voir le mouvement
                    plt.pause(0.02)
            self.kpress = False                             # Autorise à nouveau d'appuyer sur une touche

        '''Création des fonctions que l'on utilise dans nos boutons'''
        def _reset_view(self, *args):                       # Fonction d'affichage de la vue 3D initiale
            self._current_rot = self._start_rot             # La position devient la position de départ
            self._draw_cube()                               # Affichage du cube

        def _Vue_de_dessus(self, *args):                                        # Vue face du dessus
            self._current_rot = Quaternion.from_v_theta((1, 0, 0), -np.pi / 2)  # Positionnement du cube
            self._draw_cube()                                                   # Affichage du cube

        def _Vue_de_dessous(self, *args):                                       # Vue face du dessous
            self._current_rot = Quaternion.from_v_theta((1, 0, 0), np.pi / 2)   # Positionnement du cube
            self._draw_cube()                                                   # Affichage du cube

        def _Vue_de_droite(self, *args):                                        # Vue face de droite
            self._current_rot = Quaternion.from_v_theta((0, 1, 0), np.pi / 2)   # Positionnement du cube
            self._draw_cube()                                                   # Affichage du cube

        def _Vue_de_gauche(self, *args):                                        # Vue face de gauche
            self._current_rot = Quaternion.from_v_theta((0, 1, 0), -np.pi / 2)  # Positionnement du cube
            self._draw_cube()                                                   # Affichage du cube

        def _Vue_arriere(self, *args):                                          # Vue face arrière
            self._current_rot = Quaternion.from_v_theta((0, 1, 0), np.pi)       # Positionnement du cube
            self._draw_cube()                                                   # Affichage du cube

        def _Vue_avant(self, *args):                                            # Vue face avant
            self._current_rot = Quaternion.from_v_theta((0, 1, 0), 2 * np.pi)   # Positionnement du cube
            self._draw_cube()                                                   # Affichage du cube

        def _Vue_avancer(self, *args):          # Fonction pour faire avancer de 1 étape la résolution du cube
            if not self.kpress:                 # Si aucune rotation est en cours
                InteractiveCube.avancer(self)   # Utilise la procédure avancer
                self._draw_cube()               # Affichage du cube

        def _Vue_reculer(self, *args):          # Fonction pour faire reculer de 1 étape la résolution du cube
            if not self.kpress:                 # Si aucune rotation est en cours
                InteractiveCube.reculer(self)   # Utilise la procédure reculer
                self._draw_cube()               # Affichage du cube

        def _key_press(self, event):            # Si un appui sur une touhe du clavier
            if not self.kpress :                # Si aucune rotation est en cours
                if event.key == 'right':        # Appui sur la flèche de droite
                    self.rotate(Quaternion.from_v_theta((0, -1, 0), 0.05))      # Déplacement sur la droite de la vue
                elif event.key == 'left':                                       # Appui sur la flèche de gauche
                    self.rotate(Quaternion.from_v_theta((0, -1, 0), -0.05))     # Déplacement sur la gauche de la vue
                elif event.key == 'up':                                         # Appui sur la flèche du dessus
                    self.rotate(Quaternion.from_v_theta((1, 0, 0), 0.05))       # Déplacement sur le dessus de la vue
                elif event.key == 'down':                                       # Appui sur la flèche du dessous
                    self.rotate(Quaternion.from_v_theta((1, 0, 0), -0.05))      # Déplacement sur le dessous de la vue

                elif event.key.upper() == 'A':    # Appui sur la touche A du clavier
                    InteractiveCube.avancer(self) # Utilise la procédure avancer

                elif event.key.upper() == 'B':    # Appui sur la touche B du clavier
                    InteractiveCube.reculer(self) # Utilise la procédure reculer

            self._draw_cube()                     # Affichage du cube

        def avancer(self):
            if self.arret:                        # si le dernier mouvement était un 'Avancer'
                self.compteur += 1                # Incrémentation du compteur

            if len(Cube.move_list) > self.compteur > -1:                   # Si le compteur est positif
                # On sélectionne la longueur du mouvement n°compteur
                h = len(Cube.move_list[self.compteur])
                if h == 1:                                                 # Si le mouvement a une taille de "1"
                    self.rotate_face(Cube.move_list[self.compteur], 1)     # Mouvements possibles (R, L, U, D, F, B)
                elif h == 2:                                               # Si le mouvement a une taille de "2"
                    self.rotate_face(Cube.move_list[self.compteur][0], -1) # Mouvements possibles (R',L',U',D',F',B')
                elif h == 7:                                               # Si le mouvement a une taille de "7"
                    c.rotate_cube(Cube.move_list[self.compteur][6], 'CW')  # Mouvements possibles ( CW on U, CW on U)
                elif h == 8:                                               # Si le mouvement a une taille de "8"
                    c.rotate_cube(Cube.move_list[self.compteur][7], 'CCW') # Mouvements possibles ( CCW on U, CCW on U)

            if len(Cube.move_list) < self.compteur + 1:  # Si le dernier mmt de la liste a déjà été éfféctué
                self.compteur = len(Cube.move_list) - 1  # On réinitialise le compteur sur le nombre de coup effectué
            self.arret = True                            # Signifie que le dernier appui était sur le bouton 'Avancer'

        def reculer(self):
            if not self.arret:                # si le dernier mouvement était un 'Reculer'
                self.compteur -= 1            # Décrémentation du compteur

            # Même raisonnement que précédemment mais dans le cas inverser car l'on souhaite soustraire un mouvement
            if len(Cube.move_list) > self.compteur > -1:
                h = len(Cube.move_list[self.compteur])
                if h == 1:
                    self.rotate_face(Cube.move_list[self.compteur], -1)    # Mouvements possibles (R',L',U',D',F',B')
                elif h == 2:
                    self.rotate_face(Cube.move_list[self.compteur][0], 1)  # Mouvements possibles (R,L,U,D,F,B)
                elif h == 7:
                    c.rotate_cube(Cube.move_list[self.compteur][6], 'CCW') # Mouvements possibles (CCW on U,CCW on U)
                elif h == 8:
                    c.rotate_cube(Cube.move_list[self.compteur][7], 'CW')  # Mouvements possibles (CW on U,CW on U)

            if self.compteur <= 0:  # Si 1er mvt de la liste déjà éfféctué
                self.compteur = 0   # Remise à zéro du compteur
            self.arret = False      # Signifie que le dernier appui était sur le bouton 'Reculer'

        def _mouse_press(self, event):
            """Fonction pour appuyer sur le bouton de la souris"""
            self._event_xy = (event.x, event.y)         # Récupère la position (x,y) du clic
            if event.button == 1:                       # Si appuie sur la souris
                self._button1 = True                    # Le bouton est alors vue comme appuyé

        def _mouse_release(self, event):
            """Fonction pour le relâchement du bouton de la souris"""
            self._event_xy = None                       # Enlève la position du clic
            if event.button == 1:                       # Si relaché du bouton de la souris
                self._button1 = False                   # Le bouton est alors vue comme non appuyé

        def _mouse_motion(self, event):
            """Fonction pour le mouvement de la souris"""
            # Si le bouton a été appuyé (donc l'utilisateur maintient le bouton de la souris)
            if self._button1:
                dx = event.x - self._event_xy[0]        # On calcul le déplacement en x
                dy = event.y - self._event_xy[1]        # On calcul le déplacement en y
                self._event_xy = (event.x, event.y)     # On définit la nouvelle position du clic

                rot1 = Quaternion.from_v_theta((1, 0, 0), 0.01 * dy)
                rot2 = Quaternion.from_v_theta((0, -1, 0), 0.01 * dx)
                self.rotate(rot1 * rot2)
                self._draw_cube()                       # Met à jour l'affichage du cube

    def anti_resolution(texte):
        '''Cette fonction affiche le cube non résolu dans la position qu'il est dans les mains de l'utilisateur'''
        texte.reverse()                             # Retourne la méthode de résolution

        # Applique les mouvements de résolution à l'envers
        for mvt in texte:
            h = len(mvt)
            if h == 1:                              # Si la taille du mouvement est de 1 (R, L, U, D, F, B)
                c.rotate_face(mvt, -1)              # mouvement inverse (R', L', U', D', F', B')
            elif h == 2:                            # Si la taille du mouvement est de 2 (R', L', U', D', F', B')
                c.rotate_face(mvt[0], 1)            # mouvement inverse (R, L, U, D, F, B)
            elif h == 7:                            # Si la taille du mouvement est de 7 ( CW on F,  CW on U)
                c.rotate_cube(f=mvt[6], sens='CCW') # mouvement inverse ( CCW on F,  CCW on U)
            elif h == 8:                            # Si la taille du mouvement est de 8 ( CCW on F,  CCW on U)
                c.rotate_cube(f=mvt[7], sens='CW')  # mouvement inverse ( CW on F,  CW on U)
        texte.reverse()                             # Retourne le texte

    c = Cube()              # Récupération de l'ojet Cube()
    Cube.move_list = txt4   # Mouvement de résolution du cube
    anti_resolution(txt4)   # Affiche le cube non résolu de l'utilisateur
    c.draw_interactive()    # Crée et positionne la figure
    plt.show()
