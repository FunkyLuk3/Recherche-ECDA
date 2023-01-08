import cv2
import numpy as np
import matplotlib.pyplot as plt
import string

def preprocess(image, plot_image):
    # niveaux de gris
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    if(plot_image):
        pltShowImage(image, "base")
    
    # filtre moyenneur et autres preprocessing à mettre ici
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
    kernel = np.ones((3,3),np.float32)
    
    image = cv2.dilate(image,kernel,iterations = 2)
    image = cv2.erode(image,kernel,iterations = 2)
    
    if(plot_image):
        pltShowImage(image, "base -> average-> thresholding -> closing")

    return image

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