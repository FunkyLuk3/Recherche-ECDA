from skimage.morphology import skeletonize
from skimage.util import invert

import cv2

def skeletonizer(imagepath):
    """Squeletisation d'une image

    Args:
        imagename (str): chemin de l'image à squeletiser
    """
    img = cv2.imread(imagepath)
    imginvert = invert(img)
    ret, binaryimg = cv2.threshold(imginvert, 228, 255, cv2.THRESH_BINARY)
    
    return skeletonize(binaryimg)

def affichage(windowname, img):
    """Affichage d'une image
    Args:
        windowname (str): nom de la fenetre d'affichage
        img (var): nom de la variable ou est stocker l'image à afficher
    """
    cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)
    cv2.imshow('Skeletonize',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

