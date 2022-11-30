from skeletonize import affichage, skeletonizer
from freemanencoder import *

def main():
    skel = skeletonizer('bdd/01_Numeric_police12/00_resize/e/001.png')
    data = imgtoarray(skel)
    print(freeman(data))
    affichage('Skeletonize', skel)

main()