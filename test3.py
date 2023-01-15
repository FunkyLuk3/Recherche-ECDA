# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 10:32:06 2023

@author: Adam
"""

import cv2
import numpy as np

path = "C:/Users/Adam/Desktop/m.png"
savepath = "C:/Users/Adam/Desktop/d99.png"

image = cv2.imread(path)

print(image.shape)
h, w, c = image.shape

resized_image = np.zeros((100,100,3))
resized_image.fill(255)
print(resized_image.shape)

# offsets
x_offset = int((100-w)/2)
y_offset = int((100-h)/2)

print(x_offset, y_offset)

# place the letter on the resized bg
resized_image[y_offset:y_offset + h, x_offset:x_offset+w] = image

cv2.imwrite('resized_m.png', resized_image)