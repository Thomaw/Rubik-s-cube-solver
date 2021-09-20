import sys
import re
from PySide2.QtWidgets import *
from PySide2.QtGui import QScreen


# Fonction qui est appelée pour afficher la méthode de résolution sur un moniteur Arduino
def afficheur(q):
    class Configuration(QGroupBox):  # QGroupBox permet de créer un cadre avec un titre

        def __init__(self, widget):
            """
            La super fonction Python() nous permet de nous référer explicitement à la classe parente
            Ici Super nous permet d’interagir avec l'élément widget de notre classe
            """
            super().__init__(widget)

            # Définit un texte au début de l'interface graphique
            self.setTitle("Solution du Rubik's cube :")

            # Ajoute la possibilité d'éditer et afficher le texte dans une boite de dialogue
            self.desc = QTextEdit()
            self.desc.setFontPointSize(10.0)  # Définition de la taille de la police

            self.fields = QGridLayout()       # Permets de disposer les différents objets dans une grille

            self.fields.addWidget(self.desc)  # Ajoute à la grille l'afficheur de texte

            self.setLayout(self.fields)       # Mise en page de nos éléments définis ci-dessus

            # Change le texte de la boite de dialogue et le remplace par la méthode de résolution du cube
            self.desc.setText(txt)

    class Interface(QMainWindow):

        def __init__(self, parent=None):
            # Super nous permet d’interagir avec l'élément parent de notre classe
            super().__init__(parent)

            self.resize(650, 350)           # Redéfinition la taille de notre image
            self.setWindowTitle('Monitor')  # Définition de l'interface comme étant un "monitor"

            # On centre l'image lors de son affichage
            qr = self.frameGeometry()                    # Définit la géométrie de l'interface
            cp = QScreen().availableGeometry().center()  # Definit la position de l'écran sur le centre
            qr.moveCenter(cp)                            # On déplace le moniteur au centre de l'image

            # Création de la mise en page
            centralwidget = QWidget(self)

            # Permets de classer tous nos objets définis plus haut horizontalement
            centralLayout = QHBoxLayout(centralwidget)

            # Définit les objets de centralwidget comme au centre de l'interface
            self.setCentralWidget(centralwidget)

            # Ajoute tous les élements de notre class Configuration dans la class Interférence
            centralLayout.addWidget(Configuration(self))

    '''La fonction simplification ci-dessous ne va pas être expliqué. On peut simplement dire 
    que cette fonction celle-ci sert à enlever les imperfections que l'afficheur va lire. '''

    def simplification(txt):
        txt = (txt.replace("['", "")).replace("\\n]", "")
        txt = txt.replace('"', "")
        txt = (txt.replace(',,', ",")).replace("\\r\\n'", '\n')
        txt = txt.replace(", '\n,", "\n€")
        txt = txt.replace("\n, '", "\n")
        txt = (txt.replace(', \\r', '')).replace(',  ', '')
        txt = txt.replace("'\\r", '')
        txt = txt.replace('\\r', '')
        txt = re.sub("€'|€ '|€ ", '', txt)
        txt = txt.replace('\\n', '\n')

        txt = txt[:-1]
        txt = txt.replace('Transfert finish ...\n', '')
        txt = txt.replace('\n, ', '\n')
        return txt

    txt = simplification(q) # Simplifie le texte q

    app2 = QApplication()   # Création de l'application
    frame = Interface()     # Appelle la class Interface
    frame.show()            # Affiche la class Interface
    sys.exit(app2.exec_())  # Ferme l'application s'il y a appui sur le bouton de fermeture
