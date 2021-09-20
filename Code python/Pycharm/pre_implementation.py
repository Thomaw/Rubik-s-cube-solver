
def pre_transfert_Arduino(master_list, variable_a_demander):
    '''Vérification des résultats'''

    # Avant de transmettre les données à Arduino, il faut quand même vérifier qu'elles ont un sens
    # Pour cela, on crée une fonction qui associe à chaque couleur un nombre
    def ft_color(ch):
        switcher = {
            'blue': 1,
            'yellow': 2,
            'orange': 3,
            'green': 4,
            'red': 5,
            'white': 6,
        }
        return switcher.get(ch)

    # Puis on crée une liste permettant de compter le nombre de mêmes couleurs dans la liste principale
    verification_cube_1 = [0, 0, 0, 0, 0, 0]

    # On crée ensuite un nombre qui sera le nombre final à transmettre à Arduino
    final_tf = 0

    # La liste principale est actuellement une liste de 6 sous-listes contenant chacune 9 éléments
    # Nous allons donc regarder dans chaque élément de ces sous-listes, quelle couleur nous avons
    if variable_a_demander == "2":
        for s_list in master_list:
            for ss_list in s_list:
                zz = ft_color(ss_list)         # On associe à la couleur ss_list le nombre associé dans le switch
                final_tf = 10 * final_tf + zz  # On ajoute le chiffre unité du nombre à transmettre
                # On ajoute +1 à la position dans verification_cube_1 de la couleur associée
                verification_cube_1[zz - 1] += 1

    elif variable_a_demander == "1" or variable_a_demander == "3":
        for s_list in master_list:
            zz = ft_color(s_list)               # On associe à la couleur ss_list le nombre associé dans le switch
            final_tf = 10 * final_tf + zz       # On ajoute le chiffre unité du nombre à transmettre
            # On ajoute +1 à la position dans verification_cube_1 de la couleur associée
            verification_cube_1[zz - 1] += 1

    return final_tf, verification_cube_1
