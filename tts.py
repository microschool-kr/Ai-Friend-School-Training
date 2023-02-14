from gtts import gTTS # gtts 라이브러리의 gTTS 클래스 import
from playsound import playsound # playsound 모듈의 playsound 함수 import

text = "안녕하세요." # 오디오로 변환할 텍스트
speech = "tts.mp3" # 오디오를 저장할 파일 이름
tts = gTTS(text, lang="ko") # 텍스트를 오디오로 변환
tts.save(speech) # 파일로 저장
playsound(speech) # 오디오 파일 재생
