import cv2  # OpenCV 라이브러리 import
import sys  # sys 모듈 import
import mediapipe as mp  # MediaPipe 패키지 import하고 mp라는 별칭으로 사용하겠다는 뜻.
import math  # math 모듈 import

# 거리 계산 함수 선언
def distance(p1, p2):
    return math.dist((p1.x, p1.y), (p2.x, p2.y))  # 두 점 p1, p2의 x, y 좌표로 거리를 계산한다.


# MediaPipe 패키지에서 사용할 기능들.
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands  # 손 인식을 위한 객체

cap = cv2.VideoCapture(0)  # 비디오 캡처 객체 생성

if not cap.isOpened():  # 연결 확인
    print("Camera is not opened")
    sys.exit(1)  # 프로그램 종료

hands = mp_hands.Hands()  # 손 인식 객체 생성

while True:  # 무한 반복
    res, frame = cap.read()  # 카메라 데이터 읽기

    if not res:  # 프레임 읽었는지 확인
        print("Camera error")
        break  # 반복문 종료

    frame = cv2.flip(frame, 1)  # 셀프 카메라처럼 좌우 반전
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 미디어파이프에서 인식 가능한 색공간으로 변경
    results = hands.process(image)  # 이미지에서 손을 찾고 결과를 반환

    if results.multi_hand_landmarks:  # 손이 인식되었는지 확인
        for hand_landmarks in results.multi_hand_landmarks:  # 반복문을 활용해 인식된 손의 주요 부분을 그림으로 그려 표현
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style(),
            )

            points = hand_landmarks.landmark  #  landmark 좌표 정보들을 points라는 변수로 활용

            # 엄지손가락부터 새끼손가락까지 손가락이 펴졌는지 확인한다.
            fingers = 0  # 편 손가락의 숫자를 세기 위한 변수

            # 엄지손가락 확인하기
            if distance(points[4], points[9]) > distance(points[3], points[9]):
                fingers += 1  # 폈으면 fingers에 1을 더한다.

            # 나머지 손가락 확인하기
            for i in range(8, 21, 4):
                if distance(points[i], points[0]) > distance(points[i - 1], points[0]):
                    fingers += 1  # 폈으면 fingers에 1을 더한다.

            # 펴진 손가락의 개수에 따라 모양을 인식하고 이미지에 출력한다.
            if fingers == 0:  # 손가락이 모두 접힌 경우
                hand_shape = "rock"  # 바위
            elif fingers == 2:  # 손가락이 2개 펴진 경우
                hand_shape = "scissors"  # 가위
            elif fingers == 5:  # 손가락이 5개 모두 펴진 경우
                hand_shape = "paper"  # 보
            else:  # 가위바위보 모양이 아닌 경우
                hand_shape = ""  # 내용을 출력하지 않음
            cv2.putText(  # 인식된 내용을 이미지에 출력한다.
                frame,
                hand_shape,
                (int(points[12].x * frame.shape[1]), int(points[12].y * frame.shape[0])),
                cv2.FONT_HERSHEY_COMPLEX,
                3,
                (0, 255, 0),
                5,
            )

    cv2.imshow("MediaPipe Hands", frame)  # 영상을 화면에 출력.

    key = cv2.waitKey(5) & 0xFF  # 키보드 입력받기
    if key == 27:  # ESC를 눌렀을 경우
        break  # 반복문 종료

cv2.destroyAllWindows()  # 영상 창 닫기
cap.release()  # 비디오 캡처 객체 해제
