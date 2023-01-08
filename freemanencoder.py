from skimage.morphology import skeletonize
from skeletonize import preprocess, editDistance

import cv2
import numpy as np
import string

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
                
                
def extremite(image, visited):
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
    x, y = extremite(skel, visited)                    # les coordonnées du pixel extremité
    
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
                x, y = extremite(skel, visited)
        if x == None:
            end = True
            
    return code


def freeman(image_path):
    image = cv2.imread(image_path)
    
    # preprocessing
    image = preprocess(image, False)
    
    # skeletonization
    skel = skeletonize(image)
    
    # Affichage du squelette
    #affichage(aff,  "Skeleton")             # afficher dans une fenetre à part
    #pltShowImage(skel, "Skeleton")        # afficher dans les plots de spyder

    # freeman encoding
    return freeman_from_skel(skel)

def freemanLoop(folder):
    
    base_path = "bdd/dataset_caracters"
    letters = list(string.ascii_lowercase)      # toutes les lettres de l'alphabet
    
    results = {}
    
    # loop over all images
    for char in letters:
        print(folder, "/", char)
        results[char] = []
        
        for i in range(1,11):
            file_name = ""
            if i == 10:
                file_name = "0" + str(i) + ".png"
            else:
                file_name = "00" + str(i) + ".png"
            
            image_path = base_path + "/" +  folder + "/00_resize/" + char + "/" + file_name
            
            results[char].append(freeman(image_path))
                
    return results

def freemanEditDistances(freeman_codes1, freeman_codes2):
    letters = list(string.ascii_lowercase)      # toutes les lettres de l'alphabet
    
    distances = {}
    
    for char in letters:
        distances[char] = []
        for i in range(len(freeman_codes1[char])):
            freeman_code_1S = freeman_codes1[char][i]
            freeman_code_2S = freeman_codes2[char][i]
            
            dist = editDistance(freeman_code_1S, freeman_code_2S, len(freeman_code_1S), len(freeman_code_2S))
            distances[char].append((dist, len(freeman_code_1S)))
    
    return distances

#formule dans le document 1608-1613
def crossingNumber(skeleton, x, y):
    height, width = skeleton.shape
    
    CN = 0
    
    if skeleton[x,y] == 0:
        return CN
    else:
        #les huits voisins
        voisins = voisin2(skeleton, x, y)
        #on ajoute le premier à la fin de la liste
        voisins.append(voisins[0])
        
        v = (0, 1)[voisins[0][0] == 255]
        CN = 0
        
        for i in range(1,len(voisins)):
            vp = 0
            
            if voisins[i] != None:
                vp = (0, 1)[voisins[i][0] == 255]
            
            # v et vp valent 1 si ce sont des pixels du squelette, sinon 0
            CN += abs(vp - v)/2
            
            v = vp
        
    return CN

#renvoie les jonctions du squelette
def junctions(skeleton):
    height, width = skeleton.shape
    
    junction_list= []
    
    for x in range(height):
        for y in range(width):
            if skeleton[x,y] == 255:
                CN = crossingNumber(skeleton, x, y)
                
                if CN != 2:
                    junction_list.append((x,y,CN))
    
    return junction_list

def removeLine(skeleton, start, end):
    x,y = start
    while (x,y) != end:
        voisins = voisin2(skeleton, x, y)
        
        for val, vx, vy in voisins:
            if val == 255:
                skeleton[x,y] = 0
                x,y = vx, vy
                break

def deleteSerifs(skeleton, radius_sq):
    junct = junctions(skeleton)
    
    for i,j1 in enumerate(junct):
        for k, j2 in enumerate(junct):
            if i != k and ((j1[2] == 1.0) ^ (j2[2] == 1.0)):       # On ne compare que les jonctions dictinctes, et uniquement si une seule d'entre elle est une extrémité
                dx = j1[0] - j2[0]
                dy = j1[1] - j2[1]
                dist_sq = dx*dx + dy+dy
                
                if dist_sq > radius_sq:
                    start = j1[0], j1[1]
                    end = j2[0], j2[1]
                    
                    # On les inverse si start n'est pas l'extrémité
                    if j1[2] != 1.0:
                        start, end  = end, start
                    
                    removeLine(skeleton, start, end)