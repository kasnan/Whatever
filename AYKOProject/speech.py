# -*- coding: utf-8 -*-

import speech_recognition as sr
import playsound
from gtts import gTTS  
import os
import mode

def recognize_speech_from_mic(recognizer, microphone):  #마이크에서 잡음 제거후 음성정보 반환 함수
    # 마이크 인시스턴스 에러 확인
    if not isinstance(recognizer,sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source,duration = 1)     # 잡음 제거 : 시간 소요와 함께 음질 완화
        audio = recognizer.listen(source)               # 위의 if 가 어찌 되었든 일단 듣는다.
    # 리스폰스
    response = {
        "error": None,
        "transcription": None
    }
    # 인식시도
    try:
        response["transcription"] = recognizer.recognize_google(audio, language="ko-KR")
    except sr.RequestError:
        response["error"] = "RequestError Occured"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "UnknownValueError Occured"

    return response

def speech_recognize_session(PROMPT_LIMIT): #받은 음성정보에서 입력값만큼 분석 시도 후 문자열 추출 / 실패시 알림(에러 사유와 재송요청) 함수

    # 마이크 설정
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    for i in range(PROMPT_LIMIT):
        speech_input = recognize_speech_from_mic(recognizer, microphone)
        if speech_input["transcription"]:
            break
        if speech_input["error"]:
            print("못알아들었어요. 다시 말씀해주시겠어요?\n")
            break
            
    if speech_input["error"]:
        print("ERROR : {}".format(speech_input["error"]))
    return speech_input

def speak_response(script):
    tts = gTTS(text=script, lang='ko')
    
    filename = script+".mp3"
    path = './'+script+'.mp3'

    if not os.path.isfile(path):
        tts.save(filename)
    playsound.playsound(filename)
    print("다음으로 진행")
