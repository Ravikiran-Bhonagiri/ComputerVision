# read an image in python using opencv and display it and wait for a key press to close the window

import cv2 as cv

img = cv.imread('Photos/cat.jpg')

# convert the image to grayscale
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow('Cat', img)
cv.imshow('Gray', gray)

# blur the image
blur = cv.GaussianBlur(img, (3, 3), cv.BORDER_DEFAULT)
cv.imshow('Blur', blur)

# edge cascade
canny = cv.Canny(blur, 125, 175)
cv.imshow('canny edges', canny)

# dilating the image
dilated = cv.dilate(canny, (7,7), iterations=3)
cv.imshow('Dilated', dilated)

# eroding the image
eroded = cv.erode(dilated, (7,7), iterations=3)
cv.imshow('eroded', eroded)

# resize
resized = cv.resize(img, (500,500), interpolation=cv.INTER_CUBIC)
cv.imshow('resized', resized)


# cropped
cropped = img[50:200, 200:400]
cv.imshow('cropped', cropped)


cv.waitKey(0)