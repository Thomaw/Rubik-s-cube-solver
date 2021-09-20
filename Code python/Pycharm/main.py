# Bibliothèques nécessaires au fonctionnement de la commande principale

from methode_photographique import colorimetrie_via_photo
from Afficheur import *
from texte_optimisation import optimisation
from Cube_3D import Cube_3D
from communication import comm_arduino
from pre_implementation import pre_transfert_Arduino
from methode_manuelle import manual
from methode_video import visio

# On demande quelle méthode l'utilisateur souhaite utiliser
print('Veuillez entrer 1, 2 ou 3 : ')
print(' 1 pour la méthode manuelle')            # On utilise la méthode non automatisée
print(' 2 pour la méthode par photographie')    # On utilise la méthode semi-automatisée
print(' 3 pour la méthode avec la webcam')      # On utilise la méthode totalement automatisée

check = 1
# Le nombre rentré par l'utilisateur est associé à la variable ci-dessous
variable_a_demander = input()
if variable_a_demander == "1":                  # Si l'utilisateur souhaite la 1ère méthode
    master_list = manual()                      # On lance la méthode manuelle
elif variable_a_demander == "2":                # Si l'utilisateur souhaite la 2ème méthode
    master_list = colorimetrie_via_photo()      # On lance la méthode photographique
elif variable_a_demander == "3":                # Si l'utilisateur souhaite la 3ème méthode
    master_list = visio()                       # On lance la méthode via webcam
else:                                           # Sinon, on affiche un message d'erreur
    print('Erreur, veuillez relancer le programme')
    check = 0

if check == 1:
    # Puis, si cela est possible, on utilise une procédure pour simplifier la communication
    # qui va suivre avec Arduino
    final_tf, verification_cube_1 = pre_transfert_Arduino(master_list, variable_a_demander)

    # On transfère ensuite ce qui a été trouvé plus tôt puis on attend de recevoir
    # la méthode de résolution du cube
    resolution = comm_arduino(verification_cube_1, final_tf)
    # print("resolution")
    # print(resolution)
    # Une fois le cube résolu, on demande comment l'utilisateur souhaite l'afficher
    print(' \nVeuillez entrer 1 ou 2 : ', )    # Il existe deux méthodes d'affichage
    print(' 1 pour le moniteur')            # 1ère méthode: Affichage sur un moniteur
    print(' 2 pour le cube')                # 2ème méthode: Affichage 3D

    # Le nombre rentré par l'utilisateur est associé à la variable ci-dessous
    variable_a_demander2 = input()
    if variable_a_demander2 == "1":         # On utilise la méthode classique pour professionnel
        afficheur(str(resolution))          # On lance la fonction afficheur
    elif variable_a_demander2 == "2":       # On utilise la méthode classique pour amateur
        sol = optimisation(resolution)      # On commence par simplifier l'expression reçue avec la fonction adéquate
        #print(sol)                          # On affiche la solution dans le moniteur
        Cube_3D(sol)                        # On affiche en 3D la résolution
    else:                                   # Si l'utilisateur se trompe, on affiche un message d'erreur
        print('Erreur, veuillez relancer le programme')
