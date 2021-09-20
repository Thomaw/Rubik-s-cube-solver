import cv2
import numpy as np
import colorsys
import math


def visio():
    '''Initialisation de l'utilisation de la caméra'''
    cameratesting = True                # Autorisation d'utiliser la webcam
    colors_modification = True          # Autorisation de paramétrer les couleurs recherchées
    cam_port = 0                        # Le port d'entrée d'une webcam pour un ordinateur portable
                                        # Ce serait 1 si c'était une webcam externe

    cam = cv2.VideoCapture(cam_port)    # Création de l'objet caméra

    inter_color = []
    Color_list = []                     # Liste des couleurs reconnues
    number = 0                          # Compteur

    def empty_callback(x):              # Fonction inutile mais nécessaire pour la suite
        pass

    ## Création des fenêtres ##
    cv2.namedWindow('Image webcam', 0)                      # Création d'une fenêtre ajustable
    cv2.namedWindow('Image filtree', 0)                     # Création d'une fenêtre ajustable
    # Dimensionnement
    cv2.resizeWindow('Image webcam', 600, 600)              # Redimensionnement de l'image
    cv2.moveWindow('Image webcam', 750, 30)                 # Placement sur l'écran de l'image
    cv2.resizeWindow('Image filtree', 500, 500)             # Redimensionnement de l'image
    cv2.moveWindow('Image filtree', 240, 140)               # Placement sur l'écran de l'image

    # Positionnement des rectangles qui vont être placés sur l'image dans la fonction draw_current_stickers()
    xmax, ymax, size = 250, 200, 70
    current_stickers = [(xmax, ymax), (xmax + size, ymax), (xmax + 2 * size, ymax),
                        (xmax, ymax + size), (xmax + size, ymax + size), (xmax + 2 * size, ymax + size),
                        (xmax, ymax + 2 * size), (xmax + size, ymax + 2 * size), (xmax + 2 * size, ymax + 2 * size)]

    def draw_current_stickers(frame):
        """Dessine les 9 rectangles sur l'image."""
        for index, (x, y) in enumerate(current_stickers):       # Pour chaque position définie ci-dessus
            # Création d'un rectangle de couleur blanche
            cv2.rectangle(frame, (x, y), (x + 32, y + 32), (255, 255, 255), 2)


    # Positionnement de cube pour afficher les couleurs d'une image une fois enregistrée
    # Utilisé dans la fonction draw_blank_cube()
    blank_stickers = [(10, 10), (35, 10), (60, 10),
                      (10, 35), (35, 35), (60, 35),
                      (10, 60), (35, 60), (60, 60)]

    # Définition des couleurs recensées lors de l'enregistrement
    # Utilisé dans see_stickers()
    picture = [[0, 0, 0], [0, 0, 0], [0, 0, 0],
               [0, 0, 0], [0, 0, 0], [0, 0, 0],
               [0, 0, 0], [0, 0, 0], [0, 0, 0]]

    def see_stickers(frame):
        """Enregistrement des couleurs lues par la webcam"""

        for index, (x, y) in enumerate(current_stickers):        # Pour chaque position des rectangles
            # Sélectionne la couleur du pixel central sur l'image frame
            pix = frame[int(x - size / 2), int(y + size)]
            a, b, c = pix[0], pix[1], pix[2]                          # Création des trois couleurs RGB
            if number == 3 and x == xmax + size and y == ymax + size: # Cube centrale de la face blanche
                a, b, c = 255, 255, 255                               # Couleur blanche
            picture[index] = [int(a), int(b), int(c)]                 # Indexation des couleurs à un vecteur
            inter_color.append([a, b, c])                             # Indexation des couleurs à la liste intermédiaire

        # Retourne le cube (car la webcam nous force à faire tourner le cube pour voir la face)
        for ii in range(6, 9):
            for jj in range(0, 3):
                Color_list.append(inter_color[ii - 3*jj])        # Indexation des couleurs à la liste finale
        # print("a=", Color_list)

        # Transposition dans l'affichage des cubes en haut à gauche
        picture[1], picture[3] = picture[3], picture[1]
        picture[2], picture[6] = picture[6], picture[2]
        picture[5], picture[7] = picture[7], picture[5]

        inter_color.clear()     # Réinitialisation des couleurs trouvées

    def draw_blank_cube(frame):
        """Affichage des couleurs vues par l'ordinateur."""
        for index, (x, y) in enumerate(blank_stickers):       # Pour chaque position des rectangles
            # Affiche à l'utilisateur les couleurs enregistrées sur les rectangles en haut à gauche
            cv2.rectangle(frame, (x, y), (x + 20, y + 20), picture[index], -1)
            cv2.imshow('Image webcam', frame)

    # Méthode d'arrêt de l'application
    stop_application = False

    def save_face(frame, stop_application):
        # On regarde si l'on a appuyé 7 fois sur le bouton d'enregistrement
        if number != 7:
            # Si ce n'est pas le cas, on affiche le nombre d'images enregistrées
            cv2.putText(frame, "Save Face = {}/6".format(number),
                        (20, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        else:
            # Si c'est le cas, on arrête le programme
            stop_application = True

        return stop_application

    def_centers = ['yellow', 'blue', 'white','red', 'green', 'orange', 'all']
    # Définition des couleurs que l'on recherche ainsi que ses bornes limites par défaut
    def_colors = ['blue', 'yellow', 'orange', 'red', 'green', 'white']
    Lower = [[89, 178, 51], [21, 110, 117], [0, 110, 125], [150, 120, 0], [50, 150, 100], [100, 0, 150]]  # hsv
    Upper = [[118, 255, 194], [45, 255, 255], [17, 255, 255], [200, 255, 255], [100, 255, 220], [150, 50, 255]]  # hsv

    # Méthode de filtrage de l'image de la webcam
    def filtrage(Lower, Upper):
        lower_hsv_bleu = np.array(Lower[0])                             # Minimum admissible pour la couleur bleue
        upper_hsv_bleu = np.array(Upper[0])                             # Maximum admissible pour la couleur bleue
        # Vérifie si les éléments de l'image sont dans les limites imposées par la couleur bleue
        mask_bleu = cv2.inRange(hsv, lower_hsv_bleu, upper_hsv_bleu)

        # Modification de l'image à travers le masque bleu
        # Permets de ne garder que les pixels de l'image qui sont bleus
        midframe_bleu = cv2.bitwise_and(frame, frame, mask=mask_bleu)

        for i in range(1, 6):
            lower_hsv_z =  np.array(Lower[i])                            # Minimum admissible pour la couleur i
            upper_hsv_z = np.array(Upper[i])                             # Maximum admissible pour la couleur i
            # Vérifie si les éléments de l'image sont dans les limites imposées par la couleur i
            mask_z = cv2.inRange(hsv, lower_hsv_z, upper_hsv_z)
            # Modification de l'image à travers le masque de l'image i
            midframe_z = cv2.bitwise_and(frame, frame, mask=mask_z)
            # Ajoute les pixels de la couleur i, aux autres pixels déjà trouvés
            midframe_bleu = cv2.bitwise_or(midframe_bleu, midframe_z)

        # Une fois sortie de la boucle, on se retrouve avec un filtre contenant les 6 couleurs
        # du rubik's Cube. Il ne reste qu'à l'afficher sur une autre image afin de voir le résultat
        frame2 = midframe_bleu
        return frame2

    # Début du programme
    while cameratesting:

        _, frame = cam.read()                       # Capture une image vidéo à partir de l'objet de la caméra
        frame = cv2.flip(frame, 1)                  # Rotation de la caméra
        draw_current_stickers(frame)                # Affiche les rectangles au milieu de l'image
        draw_blank_cube(frame)                      # Affiche les rectangles vierges sur le côté de l'image
        stop_application = save_face(frame, stop_application)   # Regarde le nombre d'enregistrement

        if stop_application == True:                # Si 7 appuis
            break                                   # Arrêt du programme

        cv2.putText(frame, "Save {} center".format(def_centers[number]),
                    (380, 460), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

        cv2.imshow('Image webcam', frame)         # Affiche sur la fenêtre l'image de la webcam
        key = cv2.waitKey(10)                       # Définis la durée d'affichage d'une image en millisecondes

        if key % 256 == 27:                         # Si l'on appui sur "échap"
            print("Arrêt du programme...")          # Affichage de arrêt du programme
            break                                   # Arrêt du programme

        elif key % 256 == 32:                       # Si l'on appui sur "Espace"
            number += 1                             # Incrémente le compteur
            print('Enregistrement image ...')       # Affiche que l'on a enregistré une image
            see_stickers(frame2)                    # Lis les couleurs sur l'image filtrée

        elif key == ord('c'):                       # Si l'on appui sur "c"
            if number > 0:                          # Si une image a déjà été enregistrée
                print('Suppression image ...')      # Affiche que l'on supprime une image
                number -= 1                         # Décrémente le compteur
                Color_list = Color_list[:-9]        # Décrémente la liste finale

        elif key == ord('d'):                       # Si l'on appui sur "d"
            print('Réinitialisation des images ...')# Affichage de la suppression des images
            number = 0                              # Réinitialisation du compteur
            Color_list = []                         # Réinitialisation des couleurs

        elif key == ord('z'):                       # Si l'on appui sur "z"
            cv2.namedWindow('Calibrage cube', 0) # Création d'une nouvelle fenêtre
            # Dimensionnement de l'image
            cv2.resizeWindow('Calibrage cube', 300, 300)
            cv2.moveWindow('Calibrage cube', 0, 0)
            cl = 0

            for i in range(0, 6):   # Pour chaque couleur

                '''Création de six curseurs pour régler chacun des paramètres d'une image en HSV
                    - Hmin et Hmax
                    - Smin et Smax
                    - Vmin et Vmax'''

                cv2.createTrackbar('H Upper', "Calibrage cube", Upper[i][0], 179, empty_callback)
                cv2.createTrackbar('H Lower', "Calibrage cube", Lower[i][0], 179, empty_callback)
                cv2.createTrackbar('S Upper', "Calibrage cube", Upper[i][1], 255, empty_callback)
                cv2.createTrackbar('S Lower', "Calibrage cube", Lower[i][1], 255, empty_callback)
                cv2.createTrackbar('V Upper', "Calibrage cube", Upper[i][2], 255, empty_callback)
                cv2.createTrackbar('V Lower', "Calibrage cube", Lower[i][2], 255, empty_callback)

                # Tant que l'on modifie les couleurs
                while colors_modification:
                    _, frame = cam.read()                   # On lit ce que voit la webcam
                    # On enlève l'affichage réelle pour se concentrer sur l'image filtrée
                    cv2.destroyWindow('Image webcam')

                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)        # Conversion des couleurs de l'image en HSV
                    lower_hsv = np.array(Lower[i])                      # Limite inférieure de notre couleur
                    upper_hsv = np.array(Upper[i])                      # Limite supérieure de notre couleur

                    # Regarde quel pixel est dans les limites de la couleur i
                    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
                    # Garde l'image de la couleur i uniquement
                    frame2 = cv2.bitwise_and(frame, frame, mask=mask)

                    # Affichage de quelle couleur nous calibrons
                    cv2.putText(frame2, "Calibrating {} colors".format(def_colors[i]),
                                (60, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

                    cv2.imshow('Image filtree', frame2)                 # Affiche l'image
                    key = cv2.waitKey(10)                               # Temps d'affichage d'une image

                    '''On récupère ce que l'utilisateur définit comme limite de la couleur en question
                    et affiche en temps réel l'image modifiée filtrée'''
                    Upper[i][0] = cv2.getTrackbarPos('H Upper', 'Calibrage cube')
                    Lower[i][0] = cv2.getTrackbarPos('H Lower', 'Calibrage cube')
                    Upper[i][1] = cv2.getTrackbarPos('S Upper', 'Calibrage cube')
                    Lower[i][1] = cv2.getTrackbarPos('S Lower', 'Calibrage cube')
                    Upper[i][2] = cv2.getTrackbarPos('V Upper', 'Calibrage cube')
                    Lower[i][2] = cv2.getTrackbarPos('V Lower', 'Calibrage cube')

                    if key % 256 == 27:         # Si l'on appui sur "échap"
                        cl = 1                  # Variable d'arrêt sur 1
                        break                   # casse la boucle

                    if key == ord('y'):         # Si l'on appui sur "y"
                        break                   # Passe à la couleur suivante

                if cl == 1:                     # Si l'on souhaitait arrêter le programme
                    cl = 0                      # Variable d'arrêt sur 0
                    break                       # Arrêt du calibrage

            cv2.destroyWindow('Calibrage cube')  # Arrêt de l'affichage de la fenêtre de modification

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)  #  génère une version hsv de l'image de la webcam
        # Applique notre filtrage pour les limites définit dans la partie calibrage
        frame2 = filtrage(Lower, Upper)
        draw_current_stickers(frame2)                        # Affiche les rectangles sur l'image filtrée
        cv2.imshow('Image filtree', frame2)                  # Affiche la nouvelle image filtrée

    '''Une fois les couleurs identifiées, fermeture des fenêtres'''
    cv2.destroyWindow('Calibrage cube')
    cv2.destroyWindow('Image webcam')
    cv2.destroyWindow('Image filtree')

    Color_list = Color_list[0:54]
    # Création d'une nouvelle liste
    final_color = []

    """
    Dans la suite, on cherche à identifier les couleurs que la webcam a extraites
    Pour cela, on va d'abord regarder les limites inférieures et supérieures de chaque couleur;
    
    Puis, nous allons créer la couleur voulue à partir de la moyenne de ces deux limites (il est donc 
    important de définir de la façon la plus précise possible les limites de chaque couleur)
    """
    Middle = [0, 0, 0, 0, 0, 0]                                         # Nouvelle valeur des couleurs

    for i in range(0, 6):
        h1, s1, v1 = Lower[i][0], Lower[i][1], Lower[i][2]              # Valeurs minimales de la couleur
        h2, s2, v2 = Upper[i][0], Upper[i][1], Upper[i][2]              # Valeurs maximales de la couleur

        h3, s3, v3 = (h1 + h2) / 2, (s1 + s2) / 2, (v1 + v2) / 2        # Moyennage 1/2 (lower + upper)
        r3, g3, b3 = colorsys.hsv_to_rgb(h3 / 180, s3 / 255, v3 / 255)  # Conversion en RGB
        Middle[i] = [b3 * 255, g3 * 255, r3 * 255]                      # Modification de l'échelle

    '''
    La fonction ci-dessous donne la méthode pour trouver la bonne couleur lue 
    Pour cela, on utilise les distances entre chaque couleur. Plus la distance entre deux couleurs
    est faible et plus les deux images se rapprochent
    '''
    def verif_norme_2():
        d = [0, 0, 0, 0, 0, 0]  # Vecteur distance

        for i in range(0, 6):   # Pour chauqe couleur
            c = Middle[i]       # On prend la valeur de la couleur
            r = math.sqrt((c[0] - Color_in_list[0]) ** 2 +
                          (c[1] - Color_in_list[1]) ** 2 +
                          (c[2] - Color_in_list[2]) ** 2)   # Calcul de la distance
            d[i] = r            # implémentation de la distance dans un vecteur

        for j in range(0, 6):                       # Pour chaque couleur
            if min(d) == d[j]:                      # Si la position j est le minimum de d
                final_color.append(def_colors[j])   # La bonne couleur est la couleur de la position j
                break

    for m in range(0, len(Color_list)): # Pour toutes les couleurs de la liste
        Color_in_list = Color_list[m]
        verif_norme_2()                 # Détermine la couleur de chaque pixel

    print(final_color)

    return final_color
