# OPENCV 컬러 피킹 작업용 (무한재생 적용)
#mov는 오류 발생 가능성 있음 반드시 구글에서 convert mov to mp4 사용하여 변환후 사용 할 것

import cv2
import numpy as np

def empty(a):
    pass

frameWidth = 640
frameHeight = 480
# 0은 내장 웹캠
cap = cv2.VideoCapture('http://192.168.137.153:8090/?action=stream')
cap.set(3, frameWidth)
cap.set(4, frameHeight)

# HSV Setting controller
cv2.namedWindow("HSV")
cv2.resizeWindow("HSV", 640, 240)
cv2.createTrackbar("HUE Min", "HSV", 0, 179, empty)
cv2.createTrackbar("HUE Max", "HSV", 179, 179, empty)
cv2.createTrackbar("SAT Min", "HSV", 0, 255, empty)
cv2.createTrackbar("SAT Max", "HSV", 255, 255, empty)
cv2.createTrackbar("VALUE Min", "HSV", 0, 255, empty)
cv2.createTrackbar("VALUE Max", "HSV", 255, 255, empty)

# valiable for loop
frameCounter = 0
while True:
    frameCounter += 1
    if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frameCounter = 0
    _, img = cap.read()
    imgHsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("HUE Min", "HSV")
    h_max = cv2.getTrackbarPos("HUE Max", "HSV")
    s_min = cv2.getTrackbarPos("SAT Min", "HSV")
    s_max = cv2.getTrackbarPos("SAT Max", "HSV")
    v_min = cv2.getTrackbarPos("VALUE Min", "HSV")
    v_max = cv2.getTrackbarPos("VALUE Max", "HSV")

    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHsv, lower, upper)
    result = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    hStack = np.hstack([img, mask, result])
    cv2.imshow('Horizontal Stacking', hStack)

    # 프레임 수정 하면 속도 빠르게 if put 1 in pharam is playing faster
    if cv2.waitKey(1) == 27:
        print(lower)
        print(upper)
        break

cap.release()
cv2.destroyAllWindows()