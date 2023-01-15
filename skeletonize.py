import cv2
import numpy as np
import matplotlib.pyplot as plt
import string

def preprocess(image, plot_image, avg_filter, closing_amount):
    """Applique le pre-traitement sur une image

    Args:
        image (np.array): image a pre-traiter 
        plot_image (boolean): affiche ou non les etapes du pre-traitement dans les pyplot
        avg_filter (boolean): applique ou non le filtre moyenneur
        closing_amount (int): nombre de d'erosion/dilatation à appliquer

    Returns:
        np.array: image pre-traitee
    """
    # niveaux de gris
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if(plot_image):
        pltShowImage(image, "base")
    
    # filtre moyenneur
    if(avg_filter):
        kernel = np.ones((3,3),np.float32)/9
        image = cv2.filter2D(image,-1,kernel)
    
    if(plot_image):
        pltShowImage(image, "base -> average")
    
    # thresholding
    ret, image = cv2.threshold(image, 190, 255, cv2.THRESH_BINARY)
    
    if(plot_image):
        pltShowImage(image, "base -> average -> thresholding")
    
    # invert colors and have a 2D array of values between 0 and 1
    image = (255 - image)/255
    
    # closing
    if(closing_amount > 0):
        kernel = np.ones((3,3),np.float32)
        
        image = cv2.dilate(image,kernel,iterations = closing_amount)
        image = cv2.erode(image,kernel,iterations = closing_amount)
    
    if(plot_image):
        pltShowImage(image, "base -> average-> thresholding -> closing")

    return image

# fonction pour afficher dans un plot (sur spyder)
def pltShowImage(image, title):
    """Creer un pyplot et l'affiche 

    Args:
        image (np.array): image a afficher dans le pyplot
        title (str): titre du pyplot
    """
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

def  plotDistancesStats(distances, ax):
    letters = list(string.ascii_lowercase)      # toutes les lettres de l'alphabet
    
    moyennes = []
    
    for char in letters:
        m = 0
        long_moy = 0;
        for d, l in distances[char]:
            m += d
            long_moy += l
            
        m = float(m) / len(distances[char])
        long_moy = float(long_moy) / len(distances[char])
        moyennes.append(m/long_moy)
    
    ax.bar(letters, moyennes)

# copiée-collée https://www.geeksforgeeks.org/edit-distance-dp-5
def editDistance(str1, str2, m, n):
    """Calcule la distance Levenshtein entre 2 chaine de caractére 

    Args:
        str1 (str): Premiere chaine de caractere
        str2 (str): Deuxieme chaine de caractere
        m (int): Taille de la premiere chaine de caractere
        n (int): Taille de la deuxieme chaine de caractere

    Returns:
        int: Distance de Levenshtein entre les 2 chaines de caractere
    """
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