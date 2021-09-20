import re

'''
Cette fonction va nous permettre de simplifier la réception du message Arduino
avant de le transmettre à l'afficheur

Cette fonction ne sera pas expliquée en détail, car c'est simplement une modification longue et sinueuse
du message Arduino ayant pour objectif principal d'enlever les imperfections pour créer quelques choses 
de facile à comprendre pour l'utilisateur
'''


def optimisation(liste):
    def simplification(txt):
        txt = (txt.replace("['", "")).replace("\\n]", "")
        txt = txt.replace('"', "")
        txt = (txt.replace(',,', ",")).replace("\\r\\n'", '\n')
        txt = txt.replace(", '\n,", "\n€")
        txt = txt.replace("\n, '", "\n")
        txt = (txt.replace(', \\r', '')).replace(',  ', '')
        txt = txt.replace("'\\r", '')
        txt = txt.replace('\\r', '')
        txt = ((txt.replace("€'", "")).replace("€ '", "")).replace("€ ", "")
        txt = txt.replace('\\n', '\n')
        txt = txt[:-1]
        txt = txt.replace('Transfert terminé ...\n', '')
        return txt

    def Convert(alpha):
        li = list(alpha.split(" "))
        return li

    txt = str(liste)
    txt2 = Convert(txt)
    txt3, txt4 = [], []

    for s_list in txt2:
        q = (((str(s_list).replace('[', '')).replace(']', '')).replace('(', '')).replace(')', '')
        if len(q) > 10:
            q = "Solving"

        q = re.sub('Face:|Fix|Cross|Instance|1:|2:|3:|Corners|bring|yellow|piece|up:|Done|\'Transfert|finish|'
                   'Add|Edges|edges|White|Top:|Finish|Face|Green|Right:|Left:|Solving|Cube:|Superflip'
                   'Cross:|Solved|PLL:|inside|First|Layer|not|Second|Whole|:|last|OLL|The|is', '', q)

        if len(q) > 0:
            txt3.append(q)

    # "  CW Rotation: "
    # "  CCW Rotation: "
    mx = len(txt3)
    for i in range(0, mx):
        if txt3[i] == "B,":
            txt3[i] = 'B,'

        if len(txt3[i]) == 4 and txt3[i][1] == "B":
            txt3[i] = "B'"

        if txt3[i] == 'Flip':
            if txt3[i + 1] == 'CCW':

                # "[Cube Flip: CCW on F]"
                if txt3[i + 3] == 'F' or txt3[i + 3] == 'F,':
                    for j in range(i, i + 5):
                        txt3[j] = ''
                    txt3[i - 1] = 'CCW on F'

                # "[Cube Flip: CCW on U]"
                elif txt3[i + 3] == 'U' or txt3[i + 3] == 'U,':
                    for j in range(i, i + 5):
                        txt3[j] = ''
                    txt3[i - 1] = 'CCW on U'

            elif txt3[i + 1] == 'CW':
                # "[Cube Flip: CW on F]"
                if txt3[i + 3] == 'F' or txt3[i + 3] == 'F,':
                    for j in range(i, i + 5):
                        txt3[j] = ''
                    txt3[i - 1] = 'CW on F'

                # "[Cube Flip: CW on U]"
                elif txt3[i + 3] == 'U' or txt3[i + 3] == 'U,':
                    for j in range(i, i + 5):
                        txt3[j] = ''
                    txt3[i - 1] = 'CW on U'

        elif (txt3[i] == 'CW' or txt3[i] == 'CCW') and txt3[i + 1] == 'Rotation':
            txt3[i] = ''
            txt3[i + 1] = ''

    for s_list in txt3:
        s_list = s_list.replace(',', '')
        if len(str(s_list)) > 0 and str(s_list)[0] in 'BCDLURF':
            txt4.append(s_list)

    del txt4[-1]
    return txt4
