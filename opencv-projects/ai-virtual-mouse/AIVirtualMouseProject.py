import cv2
import numpy as np
import HandTrackingModule as htm
import time
import autopy

##########################
wCam, hCam = 640, 480  # Camera dimensions
frameR = 100  # Frame reduction for smoother control
smoothening = 7  # Smoothing factor to avoid jitter
##########################

pTime = 0  # Previous time for FPS calculation
plocX, plocY = 0, 0  # Previous location of the cursor
clocX, clocY = 0, 0  # Current location of the cursor

cap = cv2.VideoCapture(1)
cap.set(3, wCam)  # Set width
cap.set(4, hCam)  # Set height
detector = htm.HandDetector(max_hands=1)  # Initialize hand detector
wScr, hScr = autopy.screen.size()  # Get screen width and height
# print(wScr, hScr)

while True:
    # 1. Find hand landmarks
    success, img = cap.read()
    if not success:
        break

    img = detector.find_hands(img)
    lmList, bbox = detector.find_position(img)

    # 2. Get the tip of the index and middle fingers
    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Index finger tip
        x2, y2 = lmList[12][1:]  # Middle finger tip
        # print(x1, y1, x2, y2)

        # 3. Check which fingers are up
        fingers = detector.fingers_up()
        # print(fingers)

        cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)

        # 4. Only index finger up: Moving mode
        if fingers[1] == 1 and fingers[2] == 0:
            # 5. Convert coordinates
            x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
            y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))

            # 6. Smoothen values
            clocX = plocX + (x3 - plocX) / smoothening
            clocY = plocY + (y3 - plocY) / smoothening

            # 7. Move mouse
            autopy.mouse.move(wScr - clocX, clocY)
            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            plocX, plocY = clocX, clocY

        # 8. Both index and middle fingers up: Clicking mode
        if fingers[1] == 1 and fingers[2] == 1:
            # 9. Find distance between fingers
            length, img, lineInfo = detector.find_distance(8, 12, img)
            # print(length)

            # 10. Click mouse if distance is short
            if length < 40:
                cv2.circle(img, (lineInfo[4], lineInfo[5]), 15, (0, 255, 0), cv2.FILLED)
                autopy.mouse.click()

    # 11. Frame rate
    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime - pTime > 0 else 0
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    # 12. Display
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
