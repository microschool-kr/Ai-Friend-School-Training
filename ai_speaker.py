from gtts import gTTS # gtts 라이브러리의 gTTS 클래스 import
from playsound import playsound # playsound 모듈의 playsound 함수 import
import speech_recognition as sr # SpeechRecognition 라이브러리 import하고 sr이라는 별칭으로 사용
import requests # requests 패키지 import
from datetime import datetime # datetime 모듈의 datetime 클래스 import

API_KEY = ""

r = sr.Recognizer() # Recognizer 객체 생성
end = False
cnt = 1
while not end:
    with sr.Microphone() as source: # 마이크를 source로 사용
        print("녹음 시작")
        audio = r.listen(source) # 마이크를 사용하여 녹음
        print("녹음 끝")

    try:
        text = r.recognize_google(audio, language='ko') # 오디오 데이터를 텍스트로 변환
        print(text) # 결과 출력

        url = "https://machinelearningforkids.co.uk/api/scratch/"+ API_KEY + "/classify"

        response = requests.get(url, params={ "data" : text }) # 인공지능에 데이터 입력

        if response.ok:
            responseData = response.json()
            topMatch = responseData[0] # 인공지능 인식 결과
        else:
            response.raise_for_status()

        label = topMatch["class_name"]
        confidence = topMatch["confidence"]

        print(f"[인공지능 인식 결과]: {label} {confidence}%")
        if confidence < 60:
            answer = "잘 모르겠습니다."
        elif label == "hello":
            answer = "안녕하세요. 반갑습니다."
        elif label == "time":
            answer = f"지금은 {datetime.now().strftime('%H시 %M분')}입니다."
        elif label == "weather":
            answer = "날씨가 좋아요."
        elif label == "meal":
            answer = "맛있어요"
        elif label == "exit":
            answer = "네, 종료하겠습니다."
            end = True

        speech = f"answer{cnt}.mp3" # 오디오를 저장할 파일 이름
        tts = gTTS(answer, lang="ko") # 텍스트를 오디오로 변환
        tts.save(speech) # 파일로 저장
        playsound(speech) # 오디오 파일 재생
        cnt += 1

    except sr.UnknownValueError: # 음성 인식이 실패한 경우
        print("인식 실패")

    except sr.RequestError as e: # 요청이 실패한 경우
        print(f"요청 실패 : {e}")
