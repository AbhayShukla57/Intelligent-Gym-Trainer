import cv2
import numpy as np
import time
import PoseModule as pm

cap = cv2.VideoCapture(0)
detector = pm.poseDetector()
count = 0
dir = 0
pTime = 0
while True:
    success, img = cap.read()
    img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img, False)
    lmList = detector.findPosition(img, False)
    
    if len(lmList) != 0:
        # Left leg
        left_knee_angle = detector.findAngle(img, 23, 25, 27)
        left_hip_angle = detector.findAngle(img, 23, 24, 25)
        
        # Right leg
        right_knee_angle = detector.findAngle(img, 24, 26, 28)
        right_hip_angle = detector.findAngle(img, 24, 23, 26)
        
        # Check for lunges
        if left_hip_angle > 80 and right_hip_angle > 80:
            if left_knee_angle < 110 and right_knee_angle < 110:
                count += 0.5
        
        # Draw Curl Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)