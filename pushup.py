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
        # Right Arm
        angle1 = detector.findAngle(img, 12, 14, 16)
        # Left Arm
        angle2 = detector.findAngle(img, 11, 13, 15, False)
        per1 = np.interp(angle1, (210, 310), (0, 100))
        per2 = np.interp(angle2, (210, 310), (0, 100))
        
        # Calculate the distance between the left and right hands
        left_hand_x, left_hand_y = lmList[11][1], lmList[11][2]
        right_hand_x, right_hand_y = lmList[14][1], lmList[14][2]
        hand_dist = np.sqrt((right_hand_x - left_hand_x)**2 + (right_hand_y - left_hand_y)**2)

        # Calculate the distance between the shoulder joints
        shoulder_left_x, shoulder_left_y = lmList[12][1], lmList[12][2]
        shoulder_right_x, shoulder_right_y = lmList[9][1], lmList[9][2]
        shoulder_dist = np.sqrt((shoulder_right_x - shoulder_left_x)**2 + (shoulder_right_y - shoulder_left_y)**2)

        # Check for the push-ups
        color = (255, 0, 255)
        if per1 >= 80 and per2 >= 80 and hand_dist < shoulder_dist/2:
            color = (0, 255, 0)
            if dir == 0:
                count += 1
                dir = 1
        if per1 <= 20 and per2 <= 20:
            color = (0, 255, 0)
            if dir == 1:
                dir = 0
        print(count)

        # Draw Bar
        cv2.rectangle(img, (1100, 100), (1175, 650), color, 3)
        cv2.rectangle(img, (1100, 100), (1175, int(100+(per1+per2)/2)), color, cv2.FILLED)
        cv2.putText(img, f'{int((per1+per2)/2)} %', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, color, 4)

        # Draw Push-Up Count
        cv2.rectangle(img, (0, 450), (250, 720), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, str(int(count)), (45, 670), cv2.FONT_HERSHEY_PLAIN, 15, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

    cv2.imshow("Image", img)
    cv2.waitKey(1)
