from skimage import measure
from copy import deepcopy, copy

import numpy as np
import math
import cv2

def imgtoarray(imagename):
    data = []
    nbrligne = 0
    numpydata = np.array(imagename)
    for ligne in numpydata:
        data.append([])
        for pixel in range(len(ligne)):
            data[nbrligne].append(ligne[pixel][1])
        nbrligne += 1
    return data