import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)

    if len(lmList) != 0:
        # Left Leg
        left_knee_angle = detector.findAngle(img, 23, 25, 27)
        left_leg_angle = detector.findAngle(img, 25, 27, 29)

        # Right Leg
        right_knee_angle = detector.findAngle(img, 24, 26, 28)
        right_leg_angle = detector.findAngle(img, 26, 28, 30)

        # Check for plank position
        if left_knee_angle > 200 and right_knee_angle > 200:
            color = (0, 255, 0)
            text = "Plank"
        else:
            color = (255, 0, 255)
            text = "Not Plank"

        cv2.putText(img, text, (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, color, 5)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
