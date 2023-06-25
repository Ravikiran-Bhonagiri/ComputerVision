# read an image in python using opencv 

import cv2 as cv
import numpy as np

img = cv.imread('Photos/park.jpg')

cv.imshow('park', img)

# translation
def translate_image(img, x, y):
    trans_matrix = np.float32([[1,0,x],[0,1,y]])
    dimensions = (img.shape[1], img.shape[0])
    return cv.warpAffine(img, trans_matrix, dimensions)

# -x --> left
# -y --> up
# x --> right
# y --> down

translate_img = translate_image(img, 100, 200)

# Rotation
def rotate(img, angle, rotPoint=None):
    (height, width) = img.shape[:2]

    if rotPoint is None:
        rotPoint = (width//2, height//2)

    rotMat = cv.getRotationMatrix2D(rotPoint, angle, 1.0)
    dimensions = (width, height)

    return cv.warpAffine(img, rotMat, dimensions)

rotated = rotate(img, 45)
cv.imshow('Rotated', rotated)


# Resizing
resized = cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow("resized", resized)


# Flipping
flip = cv.flip(img, 0) ## 0 1, -1
cv.imshow('Flip', flip)


# cropping
cropped = img[200:400, 300:400]
cv.imshow('Cropped', cropped)


cv.waitKey(0)