from skeletonize import affichage, skeletonizer
from freemanencoder import *

def main():
    skel = skeletonizer('bdd/04_2PS600_police12/00_resize/a/003.png')
    data = imgtoarray(skel)
    affichage('Skeletonize', skel)
    print(freeman(data))

main()