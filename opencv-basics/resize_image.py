# write code to resize an image in python using opencv

import cv2 as cv

img = cv.imread('Photos/cat.jpg')

cv.imshow('Cat', img)

# write function to resize image

def rescaleFrame(frame, scale=0.75):
    # images, videos and live video
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    
    dimensions = (width, height)
    
    return cv.resize(frame, dimensions, interpolation=cv.INTER_AREA)

# write function to change resolution for live video

def changeRes(width, height):
    # live video
    capture.set(3, width)
    capture.set(4, height)


resized_image = rescaleFrame(img)

cv.imshow('Image', resized_image)

cv.waitKey(0)


capture = cv.VideoCapture('Videos/dog.mp4')

while True:
    isTrue, frame = capture.read()
    frame_resized = rescaleFrame(frame)

    cv.imshow('Video', frame)
    cv.imshow('Video Resized', frame_resized)

    if cv.waitKey(20) & 0xFF==ord('d'):
        break
    
capture.release()
cv.destroyAllWindows()



