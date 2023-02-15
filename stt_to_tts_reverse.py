from gtts import gTTS # gtts 라이브러리의 gTTS 클래스 import
from playsound import playsound # playsound 모듈의 playsound 함수 import
import speech_recognition as sr # SpeechRecognition 라이브러리 import하고 sr이라는 별칭으로 사용

r = sr.Recognizer() # Recognizer 객체 생성
with sr.Microphone() as source: # 마이크를 source로 사용
    print("녹음 시작")
    audio = r.listen(source, phrase_time_limit=5) # 마이크를 사용하여 녹음
    print("녹음 끝")

try:
    text = r.recognize_google(audio, language='ko') # 오디오 데이터를 텍스트로 변환
    print(text) # 결과 출력
    reverse = text[::-1] # text를 뒤집음
    print(reverse) # 결과 출력

    speech = "reverse.mp3" # 오디오를 저장할 파일 이름
    tts = gTTS(reverse, lang="ko") # 텍스트를 오디오로 변환
    tts.save(speech) # 파일로 저장
    playsound(speech) # 오디오 파일 재생

except sr.UnknownValueError: # 음성 인식이 실패한 경우
    print("인식 실패")

except sr.RequestError as e: # 요청이 실패한 경우
    print(f"요청 실패 : {e}")
