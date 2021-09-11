# -*- coding: utf8 -*-
import cv2
import socket
import numpy as np
import MotorModule


## ipv4 , TCP 사용
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
## server ip, port
s.connect(('192.168.0.29', 8485))

## webcam 이미지 capture
cam = cv2.VideoCapture(0)

## 이미지 속성 변경 3 = width, 4 = height
cam.set(3, 640);
cam.set(4, 480);

## 0~100에서 90의 이미지 품질로 설정 (default = 95)
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    # 비디오의 한 프레임씩 읽는다.
    # 제대로 읽으면 ret = True, 실패면 ret = False, frame에는 읽은 프레임
    ret, frame = cam.read()

    # cv2. imencode(ext, img [, params])
    # encode_param의 형식으로 frame을 jpg로 이미지를 인코딩한다.
    result, frame = cv2.imencode('.jpg', frame, encode_param)

    # 인코딩 된 값을 넘파이 배열값에 삽입
    # .tostring() 문을 사용하여 문자열 반환 스트링 데이터 삽입
    Sdata = np.array(frame)
    stringData = Sdata.tostring()

    # 서버에 데이터 전송
    # 반환된 값을 적절한 규격의 소켓으로 변환해서 보내주는 코드
    # (str(len(stringData))).encode().ljust(16)
    s.sendall((str(len(stringData))).encode().ljust(16) + stringData)

    # 서버로 부터 데이터를 수신함 TPC 체계를 사용하기에 데이터[버퍼]의 크기를 미리 정해둬야함 1024로 사용 즉 1024 바이트 미만인것만 보낼수있다
    Rdata = s.recv(1024)

    # 데이터 디코딩을 해줘야함 아니면 인코딩 된 상태의 데이터라 비교를 못함
    direction = Rdata.decode()

    motor = MotorModule.Motor(2,3,4,17,22,27)

    motor.move(0.5 , direction)

cam.release()
