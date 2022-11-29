from skeletonize import affichage, skeletonizer
from freemanencoder import *

def main():
    skel = skeletonizer('bdd/04_2PS600_police12/00_resize/a/001.png')
    data = imgtoarray(skel)
    affichage('Skeletonize', skel)

main()