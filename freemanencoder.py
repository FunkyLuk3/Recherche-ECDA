from skimage.morphology import skeletonize
from skeletonize import preprocess, editDistance

import cv2
import numpy as np
import string

def imgtoarray(imagename):
    """Transforme une image en tableau

    Args:
        imagename (var): nom de la variable ou est stocker l'image à afficher

    Returns:
        array: tableau contenant les pixels de l'image
    """
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
    """Detecte les voisins d'un pixel

    Args:
        tabimage (array): tableau contenant les pixels de l'image
        x (int): coordonnee du pixel
        y (int): coordonnee du pixel

    Returns:
        array: liste des voisins du pixel
    """
    v0 = (tabimage[x-1][y-1], x-1, y-1)
    v1 = (tabimage[x][y-1] , x, y-1)
    v2 = (tabimage[x+1][y-1], x+1, y-1)
    v3 = (tabimage[x+1][y], x+1, y)
    v4 = (tabimage[x+1][y+1], x+1, y+1)
    v5 = (tabimage[x][y+1], x, y+1)
    v6 = (tabimage[x-1][y+1], x-1, y+1)
    v7 = (tabimage[x-1][y], x-1, y)
    
    return [v0,v1,v2,v3,v4,v5,v6,v7]

def voisin2(image, x, y):
    """Detecte les voisins d'un pixel

    Args:
        tabimage (array): tableau contenant les pixels de l'image
        x (int): coordonnee du pixel
        y (int): coordonnee du pixel

    Returns:
        array: liste des voisins du pixel
    """
    height, width = image.shape
    
    # les changements de coordonnées à chaque étape
    dx_list = [0,    1,    1,    0,    0,   -1,   -1,    0]
    dy_list = [1,    0,    0,   -1,   -1,    0,    0,    1]
    
    # la liste qui contient les voisins dans l'ordre
    voisins = []
    
    # les coordonnées du premier voisins sont celles juste au dessus du pixel
    x -= 1
    
    for i in range(len(dx_list)):
        if x >= height or x < 0 or y >= width or y < 0:     # si les coordonnées du voisin sont hors de l'image, on met le voisin à "None"
            voisins.append(None)
        else:
            voisins.append((image[x,y], x, y))
        x += dx_list[i]
        y += dy_list[i]
    
    return voisins

def extremite(tabimage):
    """Renvoi la premiere extremite du l'image

    Args:
        tabimage (array): tableau contenant les pixels de l'image

    Returns:
        tuple: les coordonnees de la premiere extremite
    """
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
                
                
def extremite2(image, visited):
    """Renvoi la premiere extremite du l'image. 
    Le deuxième argument permet de se limiter aux pixels nons visitéés de l'image, afin de faire des appels successifs à freeman2

    Args:
        image (np.array)   : tableau contenant les pixels de l'image
        visited (np.array) : tableau de booléens indiquant si le pixel a déjà été visité

    Returns:
        tuple: les coordonnees de la premiere extremite
               s'il ne reste pas de pixels à visiter dans l'image, renvoie le couple (None, None)
    """
    height, width = image.shape
    
    nb_voisins = np.full((height, width), np.inf)
    
    # on fait le compte des voisins non visités pour tous les pixels non visités du squelette
    for x in range(height):
        for y in range(width):
            if image[x, y] != 0 and not visited[x,y]:
                voisins = voisin2(image, x, y)
                nb_voisins[x,y] = 0
                for v in voisins:
                    if v != None:
                        (valeur, vx, vy) = v
                        if valeur != 0 and not visited[vx,vy]:
                            nb_voisins[x,y] += 1
    
    # idéalement on renvoie les coordonnées d'un pixel extrémité, sinon le premier
    min_nb_voisins = np.inf
    x_min, y_min = (None, None)
    for x in range(height):
        for y in range(width):
            if nb_voisins[x,y] == 1:
                return x,y
            elif nb_voisins[x,y] < min_nb_voisins:
                min_nb_voisins = nb_voisins[x,y]
                x_min, y_min = (x,y)
    
    return (x_min, y_min)

def freeman_from_skel(skel):
    """Encodage de freeman

    Args:
        tabimage (array): tableau contenant les pixels de l'image

    Returns:
        str: encodage de l'image
    """
    code = ""
    height, width = skel.shape

    visited = np.full((height, width), False)
    x, y = extremite2(skel, visited)                    # les coordonnées du pixel extremité
    
    end = False
    while not end:
        visited[x, y] = True
        voisins = voisin2(skel, x, y)
        for i, v in enumerate(voisins) :
            if v != None:
                (valeur, vx, vy) = v
                if valeur != 0 and not visited[vx, vy] :
                    x, y = (vx, vy)
                    code += str(i)
                    break
            
            if i == 7:              # ici, on a pas trouvé de voisin pour continer le long du squelette
                x, y = extremite2(skel, visited)
        if x == None:
            end = True
            
    return code


def freeman(image_path):
    image = cv2.imread(image_path)
    
    # preprocessing
    image = preprocess(image)
    
    # skeletonization
    skel = skeletonize(image)
    
    # Affichage du squelette
    #affichage(aff,  "Skeleton")             # afficher dans une fenetre à part
    #pltShowImage(skel, "Skeleton")        # afficher dans les plots de spyder

    # freeman encoding
    return freeman_from_skel(skel)

def freeman_loop():
    
    base_path = "C:/Users/Adam/Documents/01 - Lyon 2/Recherche/ressources/Datasets/dataset_caracters"
    scans_folders = ["03_PS600_police12", "04_2PS600_police12"]
    letters = list(string.ascii_lowercase)      # toutes les lettres de l'alphabet
    
    results = []
    
    # loop over all images
    for f_i,folder in enumerate(scans_folders):
        results.append({})
        for char in letters:
            print(f_i, " - ", char)
            results[f_i][char] = []
            
            for i in range(1,11):
                file_name = ""
                if i == 10:
                    file_name = "0" + str(i) + ".png"
                else:
                    file_name = "00" + str(i) + ".png"
                
                image_path = base_path + "/" +  folder + "/00_resize/" + char + "/" + file_name
                
                results[f_i][char].append(freeman(image_path))
                
    return results

def freemanEditDistances(freeman_codes):
    letters = list(string.ascii_lowercase)      # toutes les lettres de l'alphabet
    
    distances = {}
    
    for char in letters:
        distances[char] = []
        for i in range(10):
            freeman_code_1S = freeman_codes[0][char][i]
            freeman_code_2S = freeman_codes[1][char][i]
            
            dist = editDistance(freeman_code_1S, freeman_code_2S, len(freeman_code_1S), len(freeman_code_2S))
            distances[char].append(dist)
    
    return distances