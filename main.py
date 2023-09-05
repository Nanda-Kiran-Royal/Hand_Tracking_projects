import mediapipe as mp
import cv2 as cv
import numpy as np
import uuid
import os
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv.VideoCapture(0)

hands= mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5)

while cap.isOpened():
    ref,frame = cap.read()

    ## Detection
    image = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    image = cv.flip(image,1)
    # Set flag
    image.flags.writeable = False
    #Detections
    results = hands.process(image)
    ## set flag to true
    image.flags.writeable = True
    # BGR 2 RgB
    image = cv.cvtColor(image,cv.COLOR_RGB2BGR)

    # print(results)

    ##
    if results.multi_hand_landmarks:
        for num,hand in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks((image),hand,mp_hands.HAND_CONNECTIONS,
                                      mp_drawing.DrawingSpec(color=(255,0,255),thickness=10,circle_radius=5),
                                      mp_drawing.DrawingSpec(color=(0,255,0),thickness=5,circle_radius=10))

    # cv.imwrite(os.path.join('Output Images','{}.jpg'.format(uuid.uuid1())),image)
    cv.imshow('Hand Tracking',image)
    cv.imshow('Hand Tracking ',image)
    if cv.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

