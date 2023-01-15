# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 21:13:24 2023

@author: Adam
"""


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
        
        v = (0, 1)[voisins[0][0] != 0]
        CN = 0
        
        for i in range(1,len(voisins)):
            vp = 0
            
            if voisins[i] != None:
                vp = (0, 1)[voisins[i][0] != 0]
            
            # v et vp valent 1 si ce sont des pixels du squelette, sinon 0
            CN += abs(vp - v)/2
            
            v = vp
        
    return CN

#renvoie les jonctions du squelette
def possibleSerifs(skeleton):
    height, width = skeleton.shape
    
    # les potentiels sérifs sont caractérisés par leur point de départ : l'extrémité
    p_serifs= []
    
    for x in range(height):
        for y in range(width):
            if skeleton[x,y] != 0:
                CN = crossingNumber(skeleton, x, y)
                
                if CN == 1.0:               # un CN de 1.0 indique uen extrémité
                    p_serifs.append((x,y))
    
    return p_serifs

def removeSerif(skeleton, start, size_max):
    x,y = start
    
    # première boucle qui sert à savoir si c'est bien un sérif (extrémité de taille <= size_max)
    serif_pixels = []
    end_reached = False
    while len(serif_pixels) <= size_max and not end_reached:
        serif_pixels.append((x,y))
        
        # on regarde les voisins pour savoir dans quelle direction la suite du squelette est
        voisins = voisin2(skeleton, x, y)

        for v in voisins:
            if v != None:
                val, vx, vy = v
                
                if val != 0 and (vx, vy) not in serif_pixels:
                    CN = crossingNumber(skeleton, vx, vy)
                    if CN == 2.0:                       # si c'est un pixel du squelette, avec CN == 2.0 (ligne)
                        x,y = vx, vy
                    elif CN == 1.0:                     # si c'est un pixel du squelette, avec CN == 1.0 (extrémité)
                        end_reached = True
                        # dans ce cas de figure, on ajoute quand même le pixel à la liste
                        serif_pixels.append((vx, vy))
                    else:                               # autre cas de CN (intersections)
                        end_reached = True
                    
                    break
    
    # on a maintenant la liste des pixels du sérif
    # on retire le sérif du squelette si sa longueur est valide (taille <= size_max)
    if len(serif_pixels) <= size_max:
        for (x,y) in serif_pixels:
            skeleton[x,y] = 0


def deleteSerifs(skeleton, size_max):
    p_serifs = possibleSerifs(skeleton)
    
    for s in p_serifs:
        removeSerif(skeleton, s, size_max)