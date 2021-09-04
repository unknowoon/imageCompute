import cv2

# 스트리밍 명령
# mjpg_streamer -i "input_uvc.so -d /dev/video0" -o "output_http.so -p 8090 -w /usr/local/share/mjpg-streamer/www/"
# https://webnautes.tistory.com/1261
# 위 주소에서 명령어 참고
#
# 아래 주소는 송출중인 라즈베리파이 주소 + 송출시 부여한 포트 번호와 /?action=stream 으로 구성됨
# 방어벽 문제로 송출이 안될 수 도 있음
cap = cv2.VideoCapture("http://172.30.1.17:8090/?action=stream")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
fps = cap.get(cv2.CAP_PROP_FPS)
print("Frames per second using video.get(cv2.CAP_PROP_FPS) : {0} ".format(fps))

while True:

    ret, image = cap.read()
    #image = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    cv2.imshow('Image', image)

    if cv2.waitKey(30) > 0:
        break

cv2.destroyAllWindows()