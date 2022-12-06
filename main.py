from skeletonize import plotDistancesStats
from freemanencoder import freeman_loop, freemanEditDistances


def main():
    r = freeman_loop()
    
    d = freemanEditDistances(r)
    
    plotDistancesStats(d)
    
    print('test')
    

main()