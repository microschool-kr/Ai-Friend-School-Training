import speech_recognition as sr # SpeechRecognition 라이브러리 import하고 sr이라는 별칭으로 사용
from playsound import playsound # playsound 모듈의 playsound 함수 import

r = sr.Recognizer() # Recognizer 객체 생성
with sr.Microphone() as source: # 마이크를 source로 사용
    print("녹음 시작")
    audio = r.record(source, duration=5) # 5초 동안 마이크를 사용하여 녹음
    print("녹음 끝")

file_name = "voice.wav" # 저장할 오디오 파일의 이름
with open(file_name, "wb") as f:
    f.write(audio.get_wav_data()) # 녹음한 데이터를 저장

playsound(file_name) # 오디오 파일 재생
