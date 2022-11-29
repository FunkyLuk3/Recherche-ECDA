from skeletonize import affichage, skeletonizer
import cv2

def main():
    skel = skeletonizer('bdd/04_2PS600_police12/00_resize/a/001.png')
    affichage('Skeletonize', skel)

main()