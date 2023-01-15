from skeletonize import plotDistancesStats
from freemanencoder import freemanLoop, freemanEditDistances, freeman
import matplotlib.pyplot as plt

def processAllDataset(avg_filter, closing_amount, remove_serifs):
    # folders
    numeric_folder = "01_Numeric_police12"
    scan_folders = ["02_PS300_police12","03_PS600_police12","04_2PS600_police12"]
    plot_names = ["1 scan 300 dpi", "1 scan 600 dpi", "2 scan 600 dpi"]
    
    numeric_codes = freemanLoop(numeric_folder, avg_filter, closing_amount, remove_serifs)
    scan_codes = []
    for folder in scan_folders:
        scan_codes.append(freemanLoop(folder, avg_filter, closing_amount, remove_serifs))
    
    distances = []
    for codes in scan_codes:
        distances.append(freemanEditDistances(numeric_codes, codes))

    fig, axs = plt.subplots(len(distances))
    
    for i in range(len(distances)):
        axs[i].set(ylabel=plot_names[i])
      
    for i,dist in enumerate(distances):
        plotDistancesStats(dist, axs[i])

    plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.3,
                    hspace=0.8)
    plt.show()
    
def processSingleImage(avg_filter, closing_amount, remove_serifs):
    # choix du chemin de l'image
    image_path = str(input("Chemin de l'image (un chemin invalide ferme le programme) :"))
    
    code = freeman(image_path, avg_filter, closing_amount, remove_serifs)
    
    return code
    
    

def optionSelection():
    avg_filter = True
    closing_amount = 2
    remove_serifs = True
    
    print("Choix des options :")
    
    # choix du filtre 
    while True:
        try:
            avg_choice = str(input("Filtre moyenneur (o/n) ? "))
        except ValueError:
            print("Entrée invalide, réessayez.")
            continue
        else:
            if avg_choice.lower() == "o":
                avg_filter = True
                break
            elif avg_choice.lower() == "n":
                avg_filter = False
                break
            else:
                print("Entrée invalide, réessayez.")
                continue
    
    # choix de la quantité de fermeture
    while True:
        try:
            closing_amount = int(input("Combien d'érosion/dilatation ? "))
        except ValueError:
            print("Entrée invalide, réessayez (il faut un entier).")
            continue
        else:
            break
    
    # choix pour les serifs
    while True:
        try:
            serif_choice = str(input("Retirer les sérifs (o/n) ? "))
        except ValueError:
            print("Entrée invalide, réessayez.")
            continue
        else:
            if serif_choice.lower() == "o":
                remove_serifs = True
                break
            elif serif_choice.lower() == "n":
                remove_serifs = False
                break
            else:
                print("Entrée invalide, réessayez.")
                continue
        
    return avg_filter, closing_amount, remove_serifs

def main():
    
    choice = 0
    while True:
        try:
            print("Choix du programme à lancer :")
            print("\t - analyse du dataset entier (1)")
            print("\t - application sur une seule image au choix (2)")

            choice = int(input())
        except ValueError:
            print("Entrée invalide, réessayez.")
            continue
        else:
            if choice == 1 or choice == 2:
                break
            else:
                print("Entrée invalide, réessayez.\n")
                continue
    
    # on séléctionne les options indépendemment du choix fait
    avg_filter, closing_amount, remove_serifs = optionSelection()

    if choice == 1: 
        processAllDataset(avg_filter, closing_amount, remove_serifs)
    elif choice == 2:
        # une seule image
        print("Note : il est préférable que l'image soit un caractère noir sur fond blanc. \nIl n'y a pas de limite de taille, mais le pre-traitement est calibré sur des images de taille 100x100.")
        
        print("Encodage de Freeman de l'image : " + str(processSingleImage(avg_filter, closing_amount, remove_serifs)))
    

main()