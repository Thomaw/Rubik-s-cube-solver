from tkinter import *

'''Définition de la première méthode d'implémentation du cube'''
def manual():
    # Création d'une fenêtre tkinter ainsi que de ces paramètres
    fenetre = Tk()
    fenetre.configure(bg='white')
    fenetre.title("Gui rubik's Cube")

    # Création de la solution sous forme d'une liste
    rubik = []

    # Création de la liste des couleurs en hexadécimale, des noms des couleurs et des noms de chaque face:
    colors = ["#FFFF00", "#0000FF", "#FFFFFF", "#FF0000", "#008000", "#FF7F00"]
    letters = ['yellow', 'blue', 'white', 'red', 'green', 'orange']
    position = ['Face jaune', 'Face bleue', 'Face blanche', 'Face rouge', 'Face verte', 'Face orange']

    # Création de la matrice 3*3 représentant la couleur de chaque cube d'une face
    count = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    lamb = 100      # Constant

    '''Création d'un "canvas" sur la fenêtre tkinter
    Un canvas est une zone rectangulaire destinée à contenir des dessins ou d’autres figures complexes'''
    Terrain = Canvas(fenetre, height=4 * lamb, width=3 * lamb)
    Terrain.pack()      # Organise les widgets définis plus haut

    # Création des rectangles sur le "Terrain"
    carreau = [[Terrain.create_rectangle(i * lamb, j * lamb, (i + 1) * lamb, (j + 1) * lamb, fill="#FFFF00")
                for i in range(3)] for j in range(3)]

    # Définition des couleurs de chaque carreau d'une face
    face = ['yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow']

    def name_face():
        '''Création d'un rectangle dans le "Terrain" avec comme paramètre:
        - fill : couleur du fond passif du rectangle (lorsque la souris n'est pas sur le bouton)
        - activefill : couleur du fond actif du rectangle (lorsque la souris est sur le bouton)
        - outline : Contour du rectangle
        - width : largeur du rectangle
        '''
        Terrain.create_rectangle(115, 325, 185, 375, fill="#F0F0F0", activefill="#F0F0F0",outline="#F0F0F0", width=5)
        # On crée un texte sur le rectangle avec comme texte le nom de la face
        Terrain.create_text(150, 350, text=position[len(rubik)])

    # Cas où l'utilisateur clic
    def clic(event):
        # Position du clic
        j = event.x // lamb                     # en x
        i = event.y // lamb                     # en y
        count[i][j] = (count[i][j] + 1) % 6     # Incrémente de 1 la position (x,y) du cube
        Terrain.itemconfigure(carreau[i][j], fill=colors[count[i][j]])  # Modifie la couleur en fonction de count
        face[i * 3 + j] = letters[count[i][j]]  # Modifie le nom de la face en fonction de count

    # Lit la fonction clic avec le lorsque l'on relâche le bouton de la souris
    Terrain.bind('<ButtonRelease>', clic)

    # Pour réinitialiser la face en cours
    def restart_face():
        for i in range(3):
            for j in range(3):
                # Réinitialise les couleurs de la face
                Terrain.itemconfigure(carreau[i][j], fill=colors[len(rubik)])
                count[i][j] = len(rubik)                # Modifie la couleur de la matrice
                face[3 * i + j] = letters[len(rubik)]   # Modifie la couleur de la face

        return count

    # Crée un bouton dans la fenêtre ayant comme nom "Restart" avec comme fonction
    # associé "restart_face"
    Restart_bouton = Button(fenetre, text='Restart', command=restart_face)
    Restart_bouton.place(x=50, y=375) # Positionnement du bouton

    # Pour sauvegarder une face
    def save():
        rubik.append(face[0:9])     # Ajout des 9 noms de la face à la solution
        if len(rubik) == 6:         # Si on a enregistré 6 fois
            fenetre.quit()          # On quitte la fenêtre
        else:                       # Sinon
            name_face()             # On appelle la procédure name_face()
            for i in range(3):
                for j in range(3):
                    Terrain.itemconfigure(carreau[i][j], fill=colors[len(rubik)]) # Modifie la couleur
                    count[i][j] = len(rubik)                        # Modifie la couleur de la matrice
                    face[3 * i + j] = letters[len(rubik)]           # Modifie le nom de la face en fonction de count

    # Crée un bouton dans la fenêtre ayant comme nom "Save" avec comme fonction
    # associée "save"
    Save_bouton = Button(fenetre, text='Save', command=save)
    Save_bouton.place(x=135, y=375) # Positionnement du bouton

    # Définition pour réinitialiser l'entièreté de la méthode
    def restart_all():
        rubik.clear()       # Clear la solution
        restart_face()      # Réinitialise la face
        Terrain.create_rectangle(115, 325, 185, 375, fill="#F0F0F0", activefill="#F0F0F0",
                                 outline="#F0F0F0", width=5)        # Réinitialise le rectangle créé
        Terrain.create_text(150, 350, text=position[len(rubik)])    # Réinitialise le nom de la face

    # Crée un bouton dans la fenêtre ayant comme nom "Restart all" avec comme fonction
    # associée "restart_all"
    Restart_all_Bouton = Button(fenetre, text='Restart all', command=restart_all)
    Restart_all_Bouton.place(x=200, y=375) # Positionnement du bouton

    # Appelle de la procédure name_face()
    name_face()
    fenetre.mainloop()
    fenetre.destroy()

    # On crée une nouvelle solution
    linear_rubik = []
    for i in range(6):
        q = rubik[i]            # Pour chaque élément de la solution
        linear_rubik.extend(q)  # On ajoute les éléments un par un à la nouvelle solution

    return linear_rubik
