from skimage import measure
from copy import deepcopy, copy
from math import inf

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
    v1 = (tabimage[x-1][y-1], x-1, y-1)
    v2 = (tabimage[x][y-1] , x, y-1)
    v3 = (tabimage[x+1][y-1], x+1, y-1)
    v4 = (tabimage[x+1][y], x+1, y)
    v5 = (tabimage[x+1][y+1], x+1, y+1)
    v6 = (tabimage[x][y+1], x, y+1)
    v7 = (tabimage[x-1][y], x-1, y)
    
    return [v1,v2,v3,v4,v5,v6,v7]

def extremite(tabimage):
    width = len(tabimage)
    height = len(tabimage[0])

    
    for ligne in range(height):
        for pixel in range(width):
            if tabimage[ligne][pixel] != 0:
                listvoisin = voisin(tabimage, ligne, pixel)
                nb_voisins = 0
                for (valeur, vx, vy) in listvoisin:
                    if valeur != 0:
                        nb_voisins += 1
                if nb_voisins == 1:
                    return (ligne, pixel)
                    
def freeman(tabimage):
    width = len(tabimage)
    height = len(tabimage[0])
    start = extremite(tabimage)
    print(start)
    visited = [[False for i in range(width)] for j in range(height)]
    end = False
    code = ""
    while not end:
        voisins = voisin(tabimage, start[0], start[1])
        for i,(valeur, vx, vy) in enumerate(voisins):
            if valeur != 0 and not visited[vx][vy]:
                visited[start[0]][start[1]] = True
                start = (vx, vy)
                code += str(i)
                break
            if visited[vx][vy]:
                end = True
    return code
