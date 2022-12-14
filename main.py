from skeletonize import plotDistancesStats
from freemanencoder import freemanLoop, freemanEditDistances
import matplotlib.pyplot as plt

def main():
    
    # folders
    numeric_folder = "01_Numeric_police12"
    scan1_folder = "03_PS600_police12"
    scan2_folder = "04_2PS600_police12"
    
    numeric_codes = freemanLoop(numeric_folder)
    scan1_codes = freemanLoop(scan1_folder)
    scan2_codes = freemanLoop(scan2_folder)
    
    dist_num_scan1 = freemanEditDistances(numeric_codes, scan1_codes)
    dist_num_scan2 = freemanEditDistances(numeric_codes, scan2_codes)
    
    fig, axs = plt.subplots(2)
    fig.suptitle('Distance par rapport aux caractères numériques\n(avec filtre moyenneur)')
    
    axs[0].set(ylabel='1 scan')
    axs[1].set(ylabel='2 scans')
        
    plotDistancesStats(dist_num_scan1, axs[0])
    plotDistancesStats(dist_num_scan2, axs[1])
    
    plt.show()
    

main()