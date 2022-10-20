# -*- coding: utf-8 -*-
import os
import sys
import random
import time
import word_similarity
import mode
import speech
import web
#import youtube

#drive = webdriver.ChromeDriverManager(ChromeDriverManager().install())
#path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"


PROMPT_LIMIT = 2
MODE = "init"

# 부팅 파트
print("아이코가 일어나고 있어요.")
speech.speak_response("아이코가 일어나고 있어요.")

while True:
    print("호출어 '오케이 아이코'를 불러서 아이코를 깨워주세요.")
    speech.speak_response("호출어 '오케이 아이코'를 불러서 아이코를 깨워주세요.")
    speech_input = speech.speech_recognize_session(PROMPT_LIMIT)
    #호출어 유사도 연산
    if speech_input['error']:
        similarity_num = 0.0
    else:
        similarity_num = word_similarity.similarity_con('오케이 아이코', speech_input['transcription'])

    print(speech_input['transcription'])
    if similarity_num >= 0.1:
    # 아이코의 인식률이 많아 가장 많이 오인하는 용어를 추려 감도를 높힘
        print("네, 부르셨나요. 사용하고 싶은 모드를 말씀해주세요.")
        speech.speak_response("네, 부르셨나요. 사용하고 싶은 모드를 말씀해주세요.")
        #XX모드라 말하면 XX만 추출해서 이용
        MODE = mode.mode_selection(speech_input)
         
        
        # 사용자 말에 따라 해당 모드로 이동
        if "독서" in MODE :
            mode.mode_read()
        elif "종료" in MODE:
            break
        #새로운 모드 함수를 넣게 된다면 여기에!!
        else:
            print("아직 구현되지 않은 모드입니다.")


print("시스템을 종료합니다.")
speech.speak_response("시스템을 종료합니다.")

