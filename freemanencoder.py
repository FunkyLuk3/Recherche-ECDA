from skimage.morphology import skeletonize
from skeletonize import preprocess, editDistance
from serifs import deleteSerifs, voisin2

import cv2
import numpy as np
import string


                
                
def extremite(image, visited):
    """Renvoie la premiere extremite du l'image. 
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
    """Encodage de freeman squelettise

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


def freeman(image_path, avg_filter, closing_amount, remove_serifs):
    """Encodage de freeman

    Args:
        image_path (str): le path (chemin) de l'image sur laquel on applique freeman
        vg_filter (boolean): applique ou non le filtre moyenneur
        closing_amount (int): nombre de d'erosion/dilatation à appliquer
        remove_serif (boolean): applique ou non la fonction qui retire les sérifs

    Returns:
        str: encodage de l'image
    """
    
    image = cv2.imread(image_path)
    if image.size == 0:
        print("Une erreur est survenue au moment d'ouvrir l'image.")
        quit()
    
    # preprocessing
    image = preprocess(image, False, avg_filter, closing_amount)
    
    # skeletonization
    skel = skeletonize(image)
    
    if remove_serifs:
        deleteSerifs(skel, 10)
    
    # Affichage du squelette
    #affichage(aff,  "Skeleton")             # afficher dans une fenetre à part
    #pltShowImage(skel, "Skeleton")        # afficher dans les plots de spyder

    # freeman encoding
    return freeman_from_skel(skel)

def freemanLoop(folder, avg_filter, closing_amount, remove_serifs):
    """Encodage de freeman sur tous les elements d'un dossier

    Args:
        folder (str): nom du dossier
        vg_filter (boolean): applique ou non le filtre moyenneur
        closing_amount (int): nombre de d'erosion/dilatation à appliquer
        remove_serif (boolean): applique ou non la fonction qui retire les sérifs

    Returns:
        char[]: liste des encodage de chaque image du dossier
    """
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
            
            results[char].append(freeman(image_path, avg_filter, closing_amount, remove_serifs))
                
    return results

def freemanEditDistances(freeman_codes1, freeman_codes2):
    """Calcule la distance entre 2 dictionnaire de codes de Freeman
       Les codes de freeman sont ceux de lettres de l'alphabet 

    Args:
        freeman_codes1 (char[]): Dictionnaire de code de freeman 
        freeman_codes2 (char[]): Dictionnaire de code de freeman 

    Returns:
        int{}: Distance entre freeman_codes1 et freeman_codes2
    """
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