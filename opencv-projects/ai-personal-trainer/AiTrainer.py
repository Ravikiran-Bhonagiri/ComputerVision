import cv2
import numpy as np
import time
import PoseModule as pm

# Load video
cap = cv2.VideoCapture("AiTrainer/curls.mp4")
detector = pm.PoseDetector()  # Assuming your module uses class `PoseDetector()`
count = 0  # Count for repetitions
dir = 0  # 0 for down, 1 for up (tracking direction of movement)
pTime = 0  # Previous time for FPS calculation

while True:
    success, img = cap.read()
    if not success:
        print("Video ended or cannot read video file.")
        break

    # Resize the image for consistency
    img = cv2.resize(img, (1280, 720))

    # Detect pose
    img = detector.find_pose(img, draw=False)  # Draw is False to avoid clutter
    lmList = detector.find_position(img, draw=False)  # Get landmark positions

    if len(lmList) != 0:
        # Right arm angle calculation
        angle = detector.find_angle(img, 12, 14, 16)  # Right shoulder, elbow, wrist

        # Left arm (optional)
        # angle = detector.find_angle(img, 11, 13, 15, draw=False)  # Left shoulder, elbow, wrist

        # Normalize angle to percentage
        per = np.interp(angle, (210, 310), (0, 100))  # Percentage for curl movement
        bar = np.interp(angle, (220, 310), (650, 100))  # Bar height for UI feedback

        # Check if curl is complete
        color = (255, 0, 255)
        if per == 100:
            color = (0, 255, 0)  # Green when fully curled
            if dir == 0:
                count += 0.5  # Increment half curl (moving up)
                dir = 1
        if per == 0:
            color = (0, 255, 0)  # Green when fully extended
            if dir == 1:
                count += 0.5  # Increment half curl (moving down)
                dir = 0

        print(f"Reps: {count}")

        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)  # Outer bar
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), color, cv2.FILLED)  # Filled bar
        cv2.putText(img, f'{int(per)}%', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)  # Background for count
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

    # Calculate and display FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime) if cTime - pTime > 0 else 0
    pTime = cTime
    cv2.putText(img, f'FPS: {int(fps)}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    # Display the output
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
        break

cap.release()
cv2.destroyAllWindows()
