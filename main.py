from skeletonize import affichage, skeletonizer
from freemanencoder import *
import cv2

def main():
    skel = skeletonizer('bdd/04_2PS600_police12/00_resize/a/003.png')
    # skel = cv2.imread("test.png")
    data = imgtoarray(skel)
    # affichage('Skeletonize', skel)
    print(extremite(data))
    affichage('Skeletonize', skel)


main()