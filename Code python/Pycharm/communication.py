import serial
import time


def comm_arduino(verification_cube_1, final_tf):
    communication_open = 1
    '''
     On vérifie ensuite si dans la liste de vérification, nous avons
     bien chaque élément égal à 9. Si ce n'est pas le cas, cela signifie qu'il y a un 
     problème et la communication avec Arduino devient impossible
    '''

    for nb in verification_cube_1:
        if nb != 9:                         # S'il n'y a pas 9 fois la même couleur, il y a une erreur
            communication_open = 0          # Rend impossible la communication avec Arduino
            print("Impossible de résoudre le cube, veuillez réessayer !")

    # Création d'une liste permettant d'afficher les résultats d'Arduino
    resolution = []

    # Communication avec Arduino
    if communication_open == 1:
        print("Transfert commencé...")      # Affiche que le transfert a commencé
        ser = serial.Serial('COM6', 9600)   # Associe à ser le monopole sur le com6
        # ATTENTION: Rends impossible la communication depuis Arduino
        time.sleep(2)                       # délai de 2 secondes

        cube = str(final_tf)  # Nombre à transférer

        for i in range(len(cube)):
            ser.write(str.encode(cube[i]))  # Ecrit dans le moniteur série d'Arduino le chiffre n°i de ce nombre
            time.sleep(0.1)                 # délai de 0.1 secondes

        # Une fois la transmission terminée
        while True:
            b = ser.readline()              # Lecture du moniteur série
            string_n = b.decode()           # Convertit ce qui est lu sur le moniteur série
            string_m = string_n.rstrip()    # Enlève les \r et \n créés
            resolution.append(string_n)     # Ajoute à la liste les instructions reçues
            time.sleep(0.01)                # délai de 0.01 secondes

            if (string_m == "Done!"):       # Si l'on lit le terme "Done!"
                print("Transfert terminé...")
                # Le programme Arduino est terminé, plus besoin de lire ce qui se passe
                # dans le moniteur série
                break

    return resolution
