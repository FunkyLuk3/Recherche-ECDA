from skimage.morphology import skeletonize
from skimage.util import invert

import cv2
import numpy as np
import matplotlib.pyplot as plt
import string

def preprocess(image):
    # niveaux de gris
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # filtre moyenneur et autres preprocessing à mettre ici
    
    
    
    # thresholding
    ret, image = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    
    # invert colors and have a 2D array of values between 0 and 1
    image = (255 - image)/255
    
    return image

def skeletonizer(imagepath):
    """Squeletisation d'une image

    Args:
        imagename (str): chemin de l'image à squeletiser
    """
    img = cv2.imread(imagepath)
    imginvert = invert(img)
    ret, binaryimg = cv2.threshold(imginvert, 228, 255, cv2.THRESH_BINARY)
    
    return skeletonize(binaryimg)

# fonction pour afficher dans un plot (sur spyder)
def pltShowImage(image, title):
    plt.title(title + " - " + str(image.shape))
    if len(image.shape) <= 2 :
        plt.imshow(image, cmap="gray")
    else:
        plt.imshow(image)
    plt.show()

# fonction pour afficher dans une fenêtre
def affichage(image, windowname):
    """Affichage d'une image
    Args:
        windowname (str): nom de la fenetre d'affichage
        img (var): nom de la variable ou est stockée l'image à afficher
    """
    #cv2.namedWindow(windowname, cv2.WINDOW_NORMAL)
    cv2.imshow("", image)
    cv2.destroyAllWindows()

def plotDistancesStats(distances):
    letters = list(string.ascii_lowercase)      # toutes les lettres de l'alphabet
    
    moyennes = []
    
    for char in letters:
        m = 0
        for d in distances[char]:
            m += d
        m = float(m) / 10
        moyennes.append(m)
    
    plt.bar(letters,moyennes)
    plt.show()

# fonction qui calcule la différence entre deux string
# honteusement copiée-collée
def editDistance(str1, str2, m, n):
    # Create a table to store results of subproblems
    dp = [[0 for x in range(n + 1)] for x in range(m + 1)]
 
    # Fill d[][] in bottom up manner
    for i in range(m + 1):
        for j in range(n + 1):
 
            # If first string is empty, only option is to
            # insert all characters of second string
            if i == 0:
                dp[i][j] = j    # Min. operations = j
 
            # If second string is empty, only option is to
            # remove all characters of second string
            elif j == 0:
                dp[i][j] = i    # Min. operations = i
 
            # If last characters are same, ignore last char
            # and recur for remaining string
            elif str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
 
            # If last character are different, consider all
            # possibilities and find minimum
            else:
                dp[i][j] = 1 + min(dp[i][j-1],        # Insert
                                   dp[i-1][j],        # Remove
                                   dp[i-1][j-1])      # Replace
 
    return dp[m][n]