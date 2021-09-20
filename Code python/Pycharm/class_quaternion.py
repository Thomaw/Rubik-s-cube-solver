import numpy as np


class Quaternion:
    """ Classe pour les rotations 3D via les quaternions """

    @classmethod
    def from_v_theta(cls, v, theta):
        """ Fonction pour passer de v et thêta au quaternion normalisé """
        v = np.asarray(v)                                                # Convertis l'entrée (int) en (array)
        v = v * np.sin(theta / 2) / np.sqrt(np.sum(v * v))               # v = v*sin(x/2) / ||v||
        x = np.ones(4)                                                   # x = [1, 1, 1, 1]
        x[0], x[1], x[2], x[3] = np.cos(theta / 2), v[0], v[1], v[2]     # x = [x[0], v[0], v[1], v[2]]
        return cls(x)

    def __init__(self, x):
        self.x = np.asarray(x)                    # Convertis l'entrée (int) en (array)

    ''' Fonction pour permettre la multipliaction de deux quaternions. 
        Permet la rotation du cube en utilisant la souris '''
    def __mul__(self, other):
        sxr = self.x.reshape(4, 1)                # sxr est x définit en colonne
        oxr = other.x.reshape(1, 4)               # oxr est x définit en ligne
        prod = sxr * oxr                          # Matrice [4,4] produit de sxr et oxr

        # Produit final
        ret = np.array([(prod[0, 0] - prod[1, 1] - prod[2, 2] - prod[3, 3]),
                        (prod[0, 1] + prod[1, 0] + prod[2, 3] - prod[3, 2]),
                        (prod[0, 2] - prod[1, 3] + prod[2, 0] + prod[3, 1]),
                        (prod[0, 3] + prod[1, 2] - prod[2, 1] + prod[3, 0])]).T
        return self.__class__(ret)

    ''' Fonction pour passer du quaternion normalisé à v et thêta '''
    def as_v_theta(self):
        x = self.x.reshape(4, -1)                 # Décompose x en chacun de ses éléments puis le transpose

        # Calcul de theta
        norm = np.sqrt((x ** 2).sum(0))           # calcul de la norme de x
        theta = 2 * np.arccos(x[0] / norm)        # Calcul de thêta

        # Calcul de v
        v = np.array(x[1:])                       # Création de v. Sélectionne les 3 derniers éléments de x
        v /= np.sqrt(np.sum(v ** 2))              # Normalise v (v est une matrice ligne)
        v = v.T                                   # Transpose v (v est à présent une colonne)
        return v, theta

    """ Renvoie la matrice de rotation du quaternion normalisé """
    def as_rotation_matrix(self):
        v, theta = self.as_v_theta()              # Convertis x en v et thêta
        v = v.T                                   # Transpose v

        c = np.cos(theta)                         # cos(theta)
        c1 = 1. - c                               # 1 - cos(theta)
        s = np.sin(theta)                         # sin(theta)

        # Matrice de rotation
        mat = np.array([[v[0] ** 2 * c1 + c, v[0] * v[1] * c1 - v[2] * s, v[0] * v[2] * c1 + v[1] * s],
                        [v[1] * v[0] * c1 + v[2] * s, v[1] ** 2 * c1 + c, v[1] * v[2] * c1 - v[0] * s],
                        [v[2] * v[0] * c1 - v[1] * s, v[2] * v[1] * c1 + v[0] * s, v[2] ** 2 * c1 + c]]).T
        return mat.reshape(3, 3)

    def rotate(self, points):
        M = self.as_rotation_matrix()             # M reçoit la rotation de la matrice
        return np.dot(points, M.T)                # Produit scalaire entre les points et la matrice de rotation


def project_points(points, q, view, vertical=None):
    if vertical is None:
        vertical = [0, 1, 0]                      # Définis l'axe vertical par défaut
    view = np.asarray(view)                       # Convertis l'entrée (int) en array

    xdir = np.cross(vertical, view).astype(float) # Création du nouveau vecteur unitaire correspondant à l'horizontale
    xdir /= np.sqrt(np.dot(xdir, xdir))           # Normalisation

    ydir = np.cross(view, xdir)                   # Création du nouveau vecteur unitaire correspondant à la verticale
    ydir /= np.sqrt(np.dot(ydir, ydir))           # Normalisation

    zdir = view / np.sqrt(np.dot(view, view))     # Création du nouveau vecteur unitaire correspondant à la côte

    R = q.as_rotation_matrix()                    # Rotation des points

    # Projeté des points sur la vue
    dpoint = np.dot(points, R.T) - view
    dpoint_view = np.dot(dpoint, view).reshape(dpoint.shape[:-1] + (1,))
    dproj = -dpoint * np.dot(view, view) / dpoint_view

    trans = list(range(1, dproj.ndim)) + [0]
    return np.array([np.dot(dproj, xdir), np.dot(dproj, ydir), -np.dot(dpoint, zdir)]).transpose(trans)
