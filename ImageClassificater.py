import cv2
import os
path = 'ImageQuery'
orb = cv2.ORB_create(nfeatures=1000)


# 이미지 분석 현재 있는 데이터파일 분석
def findDes(images):
    desList = []
    for img in images:
        kp, des = orb.detectAndCompute(img, None)
        desList.append(des)
    return desList


# 원본 데이터와 비교
def findID(img, desList, thres=30):
    kp2, des2, = orb.detectAndCompute(img, None)
    bf = cv2.BFMatcher()
    matchList = []
    finalVal = -1
    try:
        for des in desList:
            matches = bf.knnMatch(des, des2, k=2)
            good = []
            for m, n in matches:
                if m.distance < 0.75 * n.distance:
                    good.append([m])
            matchList.append(len(good))
    except:
        pass
    if len(matchList) != 0:
        if max(matchList) > thres:
            finalVal = matchList.index(max(matchList))

    return finalVal




def setting():

    #### Import Images
    images = []
    classNames = []

    # os.listdir : 현재 디렉토리내 파일과 디렉토리 리스트를 리턴한다.
    myList = os.listdir(path)
    print('Total Classes Detected', len(myList))

    # 디렉토리 리스트를 위에서 정의한 배열들에 삽입한다.
    for cl in myList:
        imgCur = cv2.imread(f'{path}/{cl}', 0)
        images.append(imgCur)
        classNames.append(os.path.splitext(cl)[0])
    print(classNames)

    desList = findDes(images)
    print(len(desList))

    return desList, classNames

    #비디오 받아오기
    #cap = cv2.VideoCapture(0)


#무한반복
def img_detect(frame,desList, classNames):
    #success, img2 = cap.read()
    imgOriginal = frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    id = findID(frame, desList)
    if id != -1:

        cv2.putText(imgOriginal, classNames[id], (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 1)
        return 1

    return 0

    cv2.imshow('img2', imgOriginal)
    cv2.waitKey(1)


