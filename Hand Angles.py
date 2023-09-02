import mediapipe as mp
import cv2 as cv
import numpy as np
import uuid
import os
from matplotlib import pyplot as plt
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
joint_list = [[6,7,8],[12,11,10],[4,3,2]]
cap = cv.VideoCapture(0)

hands= mp_hands.Hands(min_detection_confidence=0.8,min_tracking_confidence=0.5)
def get_labels(index,hand,results):
    output = None
    for idx,classification in enumerate(results.multi_handedness):
        if classification.classification[0].index == index:
            label = classification.classification[0].label
            score = classification.classification[0].score
            text = '{} {}'.format(label,round(score,2))

            coords = tuple(np.multiply(
                np.array((hand.landmark[mp_hands.HandLandmark.WRIST].x,
                           hand.landmark[mp_hands.HandLandmark.WRIST].y)),
                         [640,480]).astype(int))
            output = text,coords
    return output

def draw_finger_angle(image,results,joint_list):
    for hand in results.multi_hand_landmarks:
        for joint in joint_list:
            a = np.array([hand.landmark[joint[0]].x,hand.landmark[joint[0]].y])
            b = np.array([hand.landmark[joint[1]].x, hand.landmark[joint[2]].y])
            c = np.array([hand.landmark[joint[2]].x, hand.landmark[joint[2]].y])
            radians = np.arctan2(c[1]-b[1],c[0]-b[0]) - np.arctan2(a[1]-b[1],a[0]-b[0])
            angle = np.abs(radians*180.0/np.pi)
            # if angle>180.0:
            #     angle = 360-angle
            cv.putText(image,str(round(angle,2)),tuple(np.multiply(b,[640,480]).astype(int)),
                                                       cv.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2,cv.LINE_AA)
    return image



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


            if get_labels(num,hand,results):
                text,coord = get_labels(num,hand,results)
                cv.putText(image,text,coord,cv.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2,cv.LINE_AA)

        draw_finger_angle(image,results,joint_list)

    # cv.imwrite(os.path.join('Output Images','{}.jpg'.format(uuid.uuid1())),image)
    cv.imshow('Hand Tracking',image)
    cv.imshow('Hand Tracking ',image)
    if cv.waitKey(10) & 0xFF == ord('q'):
        break
cap.release()
cv.destroyAllWindows()

