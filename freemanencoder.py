from skimage import measure
from copy import deepcopy, copy

import numpy as np

def imgtoarray(imagename):
    data = []
    nbrligne = 0
    numpydata = np.array(imagename)
    for ligne in numpydata:
        data.append([])
        for pixel in range(len(ligne)):
            data[nbrligne].append(ligne[pixel][1])
        nbrligne += 1
    return data

def voisin(tabimage, x, y):
    v1 = tabimage[x-1][y-1]
    v2 = tabimage[x][y-1]
    v3 = tabimage[x+1][y-1]
    v4 = tabimage[x+1][y]
    v5 = tabimage[x+1][y+1]
    v6 = tabimage[x][y+1]
    v7 = tabimage[x-1][y]
    
    return [v1,v2,v3,v4,v5,v6,v7]

def freeman(tabimage):
    code = ''
    for ligne in range(len(tabimage)):
        for pixel in range(len(ligne)):
            if tabimage[ligne][pixel] != 0:
                listvoisin = voisin(tabimage, ligne, pixel)
                for i in range(listvoisin):
                    if voisin[i] != 0:
                        code += str(i+1)