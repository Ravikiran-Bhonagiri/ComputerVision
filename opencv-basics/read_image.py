import cv2 as cv

img = cv.imread('Photos/cat.jpg')

cv.imshow('Cat', img)

cv.waitKey(0)

# read an image using opencv and display it and wait for a key press to close the window
# cv.waitKey(0) will wait for an infinite amount of time for a key press
# cv.waitKey(1) will wait for 1 millisecond for a key press
# cv.waitKey(2000) will wait for 2 seconds for a key press

