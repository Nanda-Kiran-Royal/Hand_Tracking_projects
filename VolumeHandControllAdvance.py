
import cv2 as cv
import time
import numpy as np
import HandTrackingModule as htm
import math
import osascript
from cvzone.HandTrackingModule import HandDetector
import cvzone

####################
wCam, hCam = 640, 480
####################

cap = cv.VideoCapture(0)
pTime = 0
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(detectionCon=0.8,maxHands=1)
minVol = 0
maxVol = 100
vol = 0
volBar = 400
volPer = 0
colVol = (255,0,0)

def findDistance(p1, p2, img, draw):
    pass


# target_volume = 50
# vol = "set volume output volume " + str(target_volume)
# osascript.osascript(vol)

while True:
    success, img = cap.read()
    img = cv.flip(img, 1)
    hands, img = detector.findHands(img, flipType=False)
    if hands:
        # Hand1
        hand1 = hands[0]
        lmList1 = hand1["lmList"]  ## 21 landmarks of hand
        bbox1 = hand1['bbox']  ## Bounding Box info x,y,w,h
        centerPoint1 = hand1['center']
        handType1 = hand1['type']
        palm_area = (bbox1[2] * bbox1[3]) // 200
        print(palm_area)
        # print(lmList[4],lmList[8])
        if 85 < palm_area < 145:
            print('yes')
            x1, y1 = lmList1[4][0], lmList1[4][1]
            x2, y2 = lmList1[8][0], lmList1[8][1]
            # xt1,yt1 =
            # xt2,yt2 =
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv.circle(img, (x1, y1), 10, (255, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), 10, (255, 0, 255), cv.FILLED)
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)
            print(length)

            ## Hand Range is 15 250]
            ## VOlue range is 0 100

            vol = np.interp(length, [8, 152], [minVol, maxVol])
            volBar = np.interp(length, [8, 150], [450, 150])
            volPer = np.interp(length, [8, 150], [minVol, maxVol])

            smoothness = 5
            volPer = smoothness * round(volPer / smoothness)


            fingers1 = detector.fingersUp(hand1)
            print(fingers1)


            if not fingers1[4]:
                volume = "set volume output volume " + str(volPer)
                osascript.osascript(volume)
                cv.circle(img, ((x1+x2)//2, (y1+y2)//2), 10, (0, 255, 0), cv.FILLED)
                colVol = (0,255,0)
            else :
                colVol = (255,0,0)

            # print(vol, length)





    cv.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 3)
    cv.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv.FILLED)
    cv.putText(img, f'{int(volPer)} %', (40, 450), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

    curVol = (osascript.osascript('get volume settings')[1][14:17])
    cv.putText(img, f'Curr Vol:{(curVol)}', (30, 40), cv.FONT_HERSHEY_SIMPLEX, 1, colVol, 2)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv.putText(img, f'FPS:{int(fps)}', (400, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv.imshow('Img', img)

    cv.waitKey(1)
