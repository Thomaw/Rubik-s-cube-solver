# Bibliothèques nécessaires au fonctionnement du programme

import cv2 as cv
import numpy as np
from imutils import contours
import glob

'''
L'idée d'utilisation du programme est le suivant:
 - On rentre dans un dossier les images du cube qui doit être résolu
 - L'algorithme reconnaît les couleurs sur chaque face du cube
 - Une fois les six faces reconnues, il envoie les données à Arduino qui résout le cube
 - Le programme lit alors la méthode de résolution et l'affiche sur un afficheur
'''


def colorimetrie_via_photo():
    # Permets de lire l'intégralité des images d'un fichier (ici Cube_2) sous la forme d'un jpg
    fold = [cv.imread(file) for file in glob.glob(r"Cube_2\*.jpg")]
    # Création de la liste finale, celle qui permettra d'obtenir toutes les couleurs du cube
    master_list = []

    # Création d'un compteur
    counter = 0

    '''
    Création de la gamme de couleurs de notre rubik's cube
    Celles-ci sont de la forme HSV. Cette forme est expliquée par la suite 
    '''
    colors = {
        'blue': ([100, 120, 150], [140, 255, 255]),  # limite RGB de la couleur bleue
        'yellow': ([21, 110, 117], [45, 255, 255]),  # limite RGB de la couleur jaune
        'orange': ([0, 110, 125], [17, 255, 255]),   # limite RGB de la couleur orange
        'red': ([150, 120, 0], [200, 255, 255]),     # limite RGB de la couleur rouge
        'green': ([50, 150, 100], [100, 255, 220]),  # limite RGB de la couleur verte
        'white': ([100, 0, 150], [150, 50, 255])     # limite RGB de la couleur blanche
    }

    # Pour chaque image dans le dossier
    for image in fold:

        # Initialisation de toutes les variables importantes:
        final_color = []
        response = []
        position = []

        image = cv.resize(image, (600, 600))  # L'image est réajustée
        cv.imshow('image', image)             # Affichage de l'image
        original = image.copy()               # L'image est ensuite copiée

        '''
         On utilise ensuite la fonction d'Open CV qui s'appelle cvtColor:
         Cette fonction permet de convertir une image d'un espace couleur à un autre
         Dans notre cas, nous allons convertir la couleur de l'image de la méthode RGB (ou BGR selon le sens d'étude)
         en HSV
    
         La particularité de cette transformation est la suivante:
         - En RGB, les couleurs sont définies par les trois couleurs pouvant aller de 0 à 255 
         - En HSV, les couleurs sont définies par:
            - la teinte (allant de 0 à 179)
            - la saturation (allant de 0 à 255)
            - une valeur (allant de 0 à 255)
    
            COLOR_BGR2HSV est une variable déjà définie dans cv pour la conversion des couleurs de BGR à HSV
        '''
        image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
        # Création d'une matrice nulle nommée mask de taille de l'image
        mask = np.zeros(image.shape, dtype=np.uint8)

        '''
        A présent que nous avons défini l'ensemble des couleurs de l'image et l'échelle HSV de
        chaque couleur du cube, il faut à présent un moyen pour comparer les couleurs de l'image
        avec les couleurs prédéfinies.
    
        Pour cela, nous allons utiliser la fonction getStructuringElement d'Open CV.
        Celle-ci permet de modifier la morphologie d'une image en lui appliquant un filtre de convolution.
        C'est-à-dire que l'image sera convoluée avec un noyau pour former une nouvelle image
    
        Plus précisément, celle-ci fonctionne de la manière suivante:
        getStructuringElement(formes, noyau), avec la forme souhaitée et le noyau souhaité.
        '''

        '''
        Avec cette fonction, nous allons créer deux filtres: un grand et un petit.
        L'idée derrière ces deux filtres est de pouvoir trouvé de manière efficace les cubes 
        d'une face d'un RUbik's Cube. Il nous faut donc des filtres qui soient carrés ou rectangulaires.
        Cependant il n'existe que 3 types de formes possibles:
        - MORPH_RECT
        - MORPH_CROSS
        - MORPH_ELLIPSE
    
        Par chance, nous souhaitons un rectangle, nous allons donc choisir MORPH_RECT
        kernel = getStructuringElement(shape, size)  
        '''
        big_kernel = cv.getStructuringElement(cv.MORPH_RECT, (7, 7))
        small_kernel = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))

        # Pour chacune des couleurs dans la liste
        for color, (lower, upper) in colors.items():
            '''On définit deux tableaux pour les couleurs HSV minimales et maximales
            Ces tableaux auront des variables internes de type uint8'''
            lower = np.array(lower, dtype=np.uint8)
            upper = np.array(upper, dtype=np.uint8)

            # On commence par vérifier si les éléments de l'image sont dans les bornes de couleurs définies plus haut
            color_mask = cv.inRange(image, lower, upper)

            ''' morphologyEx(src, op, kernel,iterations=None) 
            Si op est cv.MORPH_OPEN:effectue une ouverture, c'est-à-dire une érosion suivie d'une dilatation ce qui 
            permet d'éliminer le bruit de fond.
    
            Si op est cv.MORPH_CLOSE: effectue une fermeture, c'est-à-dire une dilatation suivie d'une érosion ce qui 
            permet d'éliminer le bruit de fond noir dans les parties blanches.
            '''

            color_mask = cv.morphologyEx(color_mask, cv.MORPH_OPEN, big_kernel, iterations=1)
            color_mask = cv.morphologyEx(color_mask, cv.MORPH_CLOSE, small_kernel, iterations=5)
            # Fusion des matrices
            color_mask = cv.merge([color_mask, color_mask, color_mask])

            # Applique la porte logique ou au masque par rapport à la couleur du masque
            # Ajoute progressivement les couleurs sur le filtre
            mask = cv.bitwise_or(mask, color_mask)
            cv.imshow('mask', mask)

        gray = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)

        '''findContours(image, mode, method)
    
        4 méthodes:
        - CHAIN_APPROX_NONE = 1
        - CHAIN_APPROX_SIMPLE = 2
    
        - CHAIN_APPROX_TC89_KCOS = 4
        - CHAIN_APPROX_TC89_L1 = 3'''
        cnts = cv.findContours(gray, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # Permets de lister les contours du plus haut au plus bas
        (cnts, _) = contours.sort_contours(cnts[0], method="top-to-bottom")

        row = []
        cube_rows = []
        # Trie les contours de gauche à droite
        for (i, c) in enumerate(cnts, 1):
            row.append(c)
            if i % 3 == 0:
                (cnts, _) = contours.sort_contours(row, method="left-to-right")
                cube_rows.append(cnts)
                row.clear()

        '''Dans la partie qui suit, on définit les couleurs des rectangles ainsi
        que le nombre de rectangles dans la figure '''
        number = 0
        for row in cube_rows:
            for c in row:
                '''
                On définit les caractéristiques des rectangles:
                - position par rapport au haut
                - position par rapport à la droite
                - largeur du rectangle
                - Longueur du rectangle
                '''
                x, y, w, h = cv.boundingRect(c)
                # Récupère la couleur centrale du pixel de l'image[abscisse,ordonné]
                pix = image[int(x + h / 2), int(y + w / 2)]
                position.append([x, y])  # ajoute la position du rectangle à la liste des rectangles
                cv.rectangle(original, (x, y), (x + w, y + h), (36, 255, 12), 4)  # Trace le rectangle associé

                # On cherche à présent à trouver le texte associé aux couleurs trouvées ci-dessus
                for color, (lower, upper) in colors.items():  # Pour chaque couleur
                    lower = np.array(lower, dtype=np.uint8)
                    upper = np.array(upper, dtype=np.uint8)
                    for i in range(0, 3):
                        # Définis si la couleur est comprise entre les deux limites et
                        # Associe un tableau de "True" ou "False"
                        response.append(lower[i] <= pix[i] <= upper[i])

                    # Si les trois réponses sont vraies
                    if response[0] == True and response[1] == True and response[2] == True:
                        final_color.append(color)  # Ajoute la couleur au vecteur des couleurs finales
                    response.clear()  # Réinitialise la réponse

                    # Affichage du nombre du i ème rectangle trouvé
                    cv.putText(original, "cube {}".format(number + 1), (int(x + h / 4), y - 5), cv.FONT_HERSHEY_SIMPLEX,
                               0.7,
                               (255, 255, 255), 3)

                number += 1  # Incrémente le compteur

        '''
        Position des cubes                      Position des couleurs associées à ces cubes
        0   1   2                                0   3   6
        3   4   5                                1   4   7
        6   7   8                                2   5   8
        '''
        # Les trois lignes ci-dessous permettent donc de transposer la liste des noms
        final_color[1], final_color[3] = final_color[3], final_color[1]
        final_color[2], final_color[6] = final_color[6], final_color[2]
        final_color[5], final_color[7] = final_color[7], final_color[5]

        '''
        Vérification d'une erreur:
        La face blanche du Rubik's Cube a une face centrale particulière qui pourrait
        déstabiliser l'algorithme. Pour outrepasser ce problème, il nous suffit de dire
        que ce cube central est nécessairement de couleur blanche
        '''
        if counter == 2:
            final_color[4] = 'white'

        # On affiche ensuite les noms des couleurs sur les cubes
        number = 0  # Définition d'un compteur
        for r in position:  # Pour chaque rectangle trouvé plus haut
            # Affiche le texte final_color[number] associé à la couleur
            # du cube (p + 50, q + 75) sur l'image originale
            cv.putText(original, final_color[number], (r[0] + 50, r[1] + 75), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0),
                       2)
            number += 1

        counter += 1  # imcrémentation du compteur

        # Affichage des résultats
        cv.imshow('original', original)  # Affiche l'image avec le masque
        cv.waitKey()  # Attends qu'une touche du clavier ait été appuyée pour s'arrêter
        master_list.append(final_color)  # Ajoute la liste des couleurs de la face à la liste principale

    # Une fois les six faces étudiées
    cv.destroyAllWindows()  # Ferme toutes les fenêtres
    # cv.waitKey()

    return master_list
