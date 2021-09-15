import cv2
import numpy as np
from numpy.lib.function_base import disp
import utils


curveList = []
avgVal=10

def getLaneCurve(img, display=2):

    imgCopy = img.copy()
    imgResult = img.copy()
    #### STEP1
    imgThres = utils.thresholding(img)

    #### STEP2
    hT, wT, c = img.shape
    points = utils.valTrackbars()
    # img로 바꾸면 처리 전 영상
    imgWarp = utils.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = utils.drawPoints(imgCopy, points)

    #### STPE 3
    middlePoint = utils.getHistogram(imgWarp, minPer=0.5)
    curveAveragePoint, imgHist = utils.getHistogram(imgWarp, True, 0.9, 1)
    curveRaw = curveAveragePoint - middlePoint

    #### STEP 4
    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)
    curve = int(sum(curveList)/len(curveList))

    #### STEP 5
    if display != 0:
        imgInvWarp = utils.warpImg(imgWarp, points, wT, hT,inv = True)
        imgInvWarp = cv2.cvtColor(imgInvWarp,cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT//3,0:wT] = 0,0,0
        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult,1,imgLaneColor,1,0)
        midY = 450
        cv2.putText(imgResult,str(curve),(wT//2-80,85),cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),3)
        cv2.line(imgResult,(wT//2,midY),(wT//2+(curve*3),midY),(255,0,255),5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY-25), (wT // 2 + (curve * 3), midY+25), (0, 255, 0), 5)
        for x in range(-30, 30):
            w = wT//20
            cv2.line(imgResult, (w * x + int(curve//50), midY - 10),
                        (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)
        #fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        #cv2.putText(imgResult, 'FPS ', str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3)
    if display == 2:
        imgStacked = utils.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                            [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
    elif display == 1:
        cv2.imshow('Result', imgResult)

    #### nomalization
    curve = curve /100
    if curve > 1: curve == 1
    if curve < -1: curve == -1
    return curve

def line_trace(cap):
    #cap = cv2.VideoCapture('vid1.mp4')
    #!!! 값 적용을 위해 변경할 것!!!
    #widthTop, HeightTop, WidthBottom, HeightBottom
    intialTrackBarVals = [79, 144, 58, 240]
    utils.initializeTrackbars(intialTrackBarVals)

    while True:
        #success, img = cap.read()
        img = cv2.resize(cap, (480, 240))
        # 이걸로 라인 값 튜닝 0, 안뜸, 1, 하나 2 여러개
        curve = getLaneCurve(img, display=2)
        print(curve)
        return curve
        #cv2.imshow('Video', img)
        cv2.waitKey(1)
