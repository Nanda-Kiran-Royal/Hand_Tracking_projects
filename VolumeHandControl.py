import platform

system_platform = platform.system()

if system_platform == "Windows":
    print("Running on a Windows system")

    import cv2
    import time
    import numpy as np
    import HandTrackingModule as htm
    import math
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    ################################
    wCam, hCam = 640, 480
    ################################

    cap = cv2.VideoCapture(1)
    cap.set(3, wCam)
    cap.set(4, hCam)
    pTime = 0

    detector = htm.handDetector(detectionCon=0.7)

    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(
        IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    # volume.GetMute()
    # volume.GetMasterVolumeLevel()
    volRange = volume.GetVolumeRange()
    minVol = volRange[0]
    maxVol = volRange[1]
    vol = 0
    volBar = 400
    volPer = 0
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            # print(lmList[4], lmList[8])

            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
            cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)
            # print(length)

            # Hand range 50 - 300
            # Volume Range -65 - 0

            vol = np.interp(length, [50, 300], [minVol, maxVol])
            volBar = np.interp(length, [50, 300], [400, 150])
            volPer = np.interp(length, [50, 300], [0, 100])
            print(int(length), vol)
            volume.SetMasterVolumeLevel(vol, None)

            if length < 50:
                cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)

        cv2.rectangle(img, (50, 150), (85, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)

        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, f'FPS: {int(fps)}', (40, 50), cv2.FONT_HERSHEY_COMPLEX,
                    1, (255, 0, 0), 3)

        cv2.imshow("Img", img)
        cv2.waitKey(1)


elif system_platform == "Darwin":
    print("Running on a macOS system")
    import cv2 as cv
    import time
    import numpy as np
    import HandTrackingModule as htm
    import math
    import osascript

    ####################
    wCam, hCam = 640, 480
    ####################

    cap = cv.VideoCapture(0)
    pTime = 0
    cap.set(3, wCam)
    cap.set(4, hCam)

    detector = htm.handDetector(detectionCon=0.85, )
    minVol = 0
    maxVol = 100
    vol = 0
    volBar = 400
    volPer = 0

    # target_volume = 50
    # vol = "set volume output volume " + str(target_volume)
    # osascript.osascript(vol)

    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmList = detector.findPosition(img, draw=False)
        if len(lmList) != 0:
            # print(lmList[4],lmList[8])

            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2
            cv.circle(img, (x1, y1), 10, (255, 0, 255), cv.FILLED)
            cv.circle(img, (x2, y2), 10, (255, 0, 255), cv.FILLED)
            cv.line(img, (x1, y1), (x2, y2), (255, 0, 255), 2)
            cv.circle(img, (cx, cy), 10, (255, 0, 255), cv.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)
            print(length)

            ## Hand Range is 15 250]
            ## VOlue range is 0 100

            vol = np.interp(length, [20, 250], [minVol, maxVol])
            volBar = np.interp(length, [20, 250], [450, 150])
            volPer = np.interp(length, [20, 250], [minVol, maxVol])

            print(vol, length)
            volume = "set volume output volume " + str(vol)
            osascript.osascript(volume)

            if length < 50:
                cv.circle(img, (x2, y2), 10, (0, 255, 0), cv.FILLED)

        cv.rectangle(img, (50, 150), (85, 400), (0, 0, 255), 3)
        cv.rectangle(img, (50, int(volBar)), (85, 400), (0, 0, 255), cv.FILLED)
        cv.putText(img, f'{int(volPer)} %', (40, 450), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv.putText(img, f'FPS:{int(fps)}', (30, 40), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv.imshow('Img', img)

        cv.waitKey(1)
else:
    print("Running on a different system (not Windows or macOS)")










