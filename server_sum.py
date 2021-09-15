import socket
import cv2
import numpy as np

import ImageClassificater
import LaneDetectionModule

HOST = ''
PORT = 1120
# captu = cv2.VideoCapture(0)
# _, re = captu.read()
# 소켓의 객체 생성
# socket에서 수신한 버퍼를 반환하는 함수
# recvall : 로우 레벨 네트워킹 인터페이스
def recvall(sock, count):
    # 바이트 문자열을 정의한다. 사용법 : b 'text'
    # 바이트 자료형을 연속적으로 저장하는 시퀀스 형태의 자료형
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

# 서버 : 소켓만들기 -> 포트에 맵핑 -> 클라이언트 접속 대기

# 스트리밍 소켓 정의
# socket.AF_INET = ipv4 , socket.SOCK_STREAM = TCP 통신
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

# 포트 맵핑
# bind : 서버가 소켓을 포트에 맵핑하는 행위를 바인드라 한다.
# 서버의 아이피와 포트번호 지정
s.bind((HOST, PORT))
print('Socket bind complete')

# 클라이언트의 접속을 기다린다. (클라이언트 연결을 10개까지 받는다)
s.listen(10)
print('Socket now listening')

# 연결, conn에는 소켓 객체, addr은 소켓에 바인드 된 주소
conn, addr = s.accept()


#image_list, className = ImageClassificater.setting()


while True:

    # client에서 받은 stringData의 크기 (==(str(len(stringDa ta))).encode().ljust(16))
    length = recvall(conn, 16)
    stringData = recvall(conn, int(length))
    data = np.frombuffer(stringData, dtype='uint8')

    # data를 디코딩한다.
    frame = cv2.imdecode(data, cv2.IMREAD_COLOR)
    
    curve = LaneDetectionModule.line_trace(frame)
    #print(curve)
    #sign = ImageClassificater.img_detect(frame, image_list, className)
    curve *= -1
    curve = str(curve)
    curve = curve.encode('utf-8')
    
    #    소켓 보내기
    conn.sendall(curve)

    # 이미지를 출력한다
    #cv2.imshow('jebal',re)
    # 프레임 10이라는뜻
    if cv2.waitKey(1) == 27:
        break


