import cv2
import numpy as np
import time
import os
import HandTrackingModule as htm

#######################
brushThickness = 25
eraserThickness = 100
#######################

folderPath = "Header"
myList = os.listdir(folderPath)
print(myList)
overlayList = []

for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    overlayList.append(image)
print(f"Loaded {len(overlayList)} header images")

header = overlayList[0]
drawColor = (255, 0, 255)  # Default drawing color (pink)

cap = cv2.VideoCapture(1)
cap.set(3, 1280)  # Width
cap.set(4, 720)  # Height

detector = htm.HandDetector(detection_conf=0.65, max_hands=1)
xp, yp = 0, 0  # Previous points for drawing
imgCanvas = np.zeros((720, 1280, 3), np.uint8)  # Canvas for drawing

while True:
    # 1. Import image
    success, img = cap.read()
    img = cv2.flip(img, 1)  # Flip image horizontally

    # 2. Find Hand Landmarks
    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)

    if len(lmList) != 0:
        # Tip of index and middle fingers
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip

        # 3. Check which fingers are up
        fingers = detector.fingers_up()

        # 4. Selection Mode (Two fingers up)
        if fingers[1] and fingers[2]:
            print("Selection Mode")
            if y1 < 125:
                # Check which header area is clicked
                if 250 < x1 < 450:
                    header = overlayList[0]
                    drawColor = (255, 0, 255)  # Pink
                elif 550 < x1 < 750:
                    header = overlayList[1]
                    drawColor = (255, 0, 0)  # Blue
                elif 800 < x1 < 950:
                    header = overlayList[2]
                    drawColor = (0, 255, 0)  # Green
                elif 1050 < x1 < 1200:
                    header = overlayList[3]
                    drawColor = (0, 0, 0)  # Eraser (black)
            cv2.rectangle(img, (x1, y1 - 25), (x2, y2 + 25), drawColor, cv2.FILLED)

        # 5. Drawing Mode (Index finger up)
        if fingers[1] and not fingers[2]:
            print("Drawing Mode")
            cv2.circle(img, (x1, y1), 15, drawColor, cv2.FILLED)  # Draw circle at index finger tip
            if xp == 0 and yp == 0:
                xp, yp = x1, y1

            if drawColor == (0, 0, 0):  # Eraser mode
                cv2.line(img, (xp, yp), (x1, y1), drawColor, eraserThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, eraserThickness)
            else:  # Drawing mode
                cv2.line(img, (xp, yp), (x1, y1), drawColor, brushThickness)
                cv2.line(imgCanvas, (xp, yp), (x1, y1), drawColor, brushThickness)

            xp, yp = x1, y1  # Update previous point

    else:
        xp, yp = 0, 0  # Reset previous points when hand is not detected

    # 6. Combine the image and the canvas
    imgGray = cv2.cvtColor(imgCanvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    img = cv2.bitwise_and(img, imgInv)
    img = cv2.bitwise_or(img, imgCanvas)

    # 7. Setting the header image
    img[0:125, 0:1280] = header

    # 8. Display
    cv2.imshow("Image", img)
    cv2.imshow("Canvas", imgCanvas)
    cv2.imshow("Inv", imgInv)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cap.release()
cv2.destroyAllWindows()