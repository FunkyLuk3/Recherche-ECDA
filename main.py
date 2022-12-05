from skeletonize import affichage, skeletonizer
from freemanencoder import *
import cv2

def main():
<<<<<<< HEAD
    skel = skeletonizer('bdd/04_2PS600_police12/00_resize/a/003.png')
    # skel = cv2.imread("test.png")
    data = imgtoarray(skel)
    # affichage('Skeletonize', skel)
    print(extremite(data))
    affichage('Skeletonize', skel)

=======
    skel = skeletonizer('bdd/01_Numeric_police12/00_resize/e/001.png')
    data = imgtoarray(skel)
    print(freeman(data))
    affichage('Skeletonize', skel)
>>>>>>> 41ee510fc32f5d47901389733607eb53cb74e756

main()