# -*- coding: utf-8 -*-

import os
import sys
import random
import time

import speech
from speech import speech_recognize_session
import youtube
import web

def mode_selection(speech_input): #문자열 추출 함수의 설정 : 3회 분석
    PROMPT_LIMIT_MODE = 3

    speech_input = speech_recognize_session(PROMPT_LIMIT_MODE)

    if speech_input['error']:
        return 1
    else:
        speech_input_data = speech_input["transcription"]
        print(speech_input_data)
        return speech_input_data

def find_major_genre (keyword_list) :

    cut_same_keyword = set(keyword_list)
    keywords = list(cut_same_keyword)
    #print(keywords)
    # 장르 지수
    romance = 0         # 로맨스 연애 멜로
    sci_fi = 0          # 공상과학
    orient = 0          # 동양판타지, 동양역사,무협 등등
    fantasy = 0         # 일반 판타지
    mystery = 0         # 추리, 미스터리, 수사, 등 호기심 자극
    thriller = 0        # 범죄, 공포, 스릴러 등 긴장감 자극
    

    # 각 키워드에 점수를 매겨야 한다.
    keyword_Romance = [{"keyword" : "로맨스" , "cnt" : 1} , {"keyword" : "연애" , "cnt" :  1}, { "keyword" : "사랑" , "cnt" :  1}, {"keyword" : "러브" , "cnt" :  1}, {"keyword" : "감정" , "cnt" :  1}]
    keyword_Sci_fi = [{"keyword" : "SF" , "cnt" : 2},{"keyword" : "과학" , "cnt" : 1}, {"keyword" : "로봇" , "cnt" : 1}, {"keyword" : "우주" , "cnt" : 1},{"keyword" : "미래" , "cnt" : 1}]
    keyword_Orient = [{"keyword" : "역사" , "cnt" : 2}, {"keyword" : "대하" , "cnt" : 2}, {"keyword" : "무협" , "cnt" : 1}, {"keyword" : "고전" , "cnt" : 1},  {"keyword" : "중국" , "cnt" : 1}]     #중국은 로맨스도 삼국지, 스릴러도 초한지다 ㄹㅇ   
    keyword_Fantasy = [{"keyword" : "판타지" , "cnt" : 2}, {"keyword" : "중세" , "cnt" : 1}, {"keyword" : "마법" , "cnt" : 1}, {"keyword" : "라이트노벨" , "cnt" : "1"}]         # 라노벨 엄;;
    keyword_Mystery =  [{"keyword" : "미스터리" , "cnt" : 2}, {"keyword" : "스릴러" , "cnt" : 1} , {"keyword" : "추리" , "cnt" : 2} , {"keyword" : "수사" , "cnt" : 1} , {"keyword" : "탐정" , "cnt" : 1}]
    keyword_Thriller = [{"keyword" : "스릴러" , "cnt" :2 }, {"keyword" : "공포" , "cnt" : 2} , {"keyword" : "호러" , "cnt" : 1} , {"keyword" : "범죄" , "cnt" : 1}, {"keyword" : "살인" , "cnt" : 1}, {"keyword" : "누아르" , "cnt" : 1}]
    # 기준 1 : 모두 1점 이하면 주제없음 처리한다.
    # 기준 2 : 2점 이상인 항목이 있으면 가장 많음 점수를 얻은 장르를 분위기로 추출한다.
    # 기준 3 : 기준 2에서 동점이 생길경우 테마가 확실한 (ex : Orient가 로맨스보다 테마성이 짙음) 순서대로 메인장르를 추출한다.
    
    for dic in keyword_Romance :
        for keyword in keywords :
            if dic["keyword"] in keyword :
                romance += dic["cnt"]
                break
    for dic in keyword_Sci_fi :
        for keyword in keywords :
            if dic["keyword"] in keyword :
                sci_fi += dic["cnt"]
                break
    for dic in keyword_Orient :
        for keyword in keywords :
            if dic["keyword"] in keyword :
                orient += dic["cnt"]
                break
    for dic in keyword_Fantasy :
        for keyword in keywords :
            if dic["keyword"] in keyword :
                fantasy += dic["cnt"]
                break
    for dic in keyword_Mystery :
        for keyword in keywords :
            if dic["keyword"] in keyword :
                mystery += dic["cnt"]
                break
    for dic in keyword_Thriller :
        for keyword in keywords :
            if dic["keyword"] in keyword :
                thriller += dic["cnt"]
                break
    print("장르 점수판 :", romance, sci_fi, orient, fantasy, mystery, thriller)
    cnt_board = [romance , sci_fi , orient, fantasy, mystery, thriller]
    major_genre = "None"
    tmp = max(cnt_board)
    major_idx = cnt_board.index(tmp)
    #print(major_idx)
   
    if cnt_board.count(tmp) > 1 :
        major_genre = "None"
    elif tmp < 2 :
        major_genre = "None"
    else :
        if major_idx == 0 :
            major_genre = "Rommance"
        elif major_idx == 1 :
            major_genre = "SF"
        elif major_idx == 2 :
            major_genre = "Orient"
        elif major_idx == 3 :
            major_genre = "Fantasy"
        elif major_idx == 4 :
            major_genre = "Mystery"
        elif major_idx == 5 :
            major_genre = "Thriller"
        
    print("장르 :" , major_genre)
    return major_genre



def mode_read() :
    print("독서 모드를 실행합니다. 읽고 계신 책의 제목을 말씀해 주세요.")
    speech.speak_response("독서 모드를 실행합니다. 읽고 계신 책의 제목을 말씀해 주세요.")
    prompt = 0
    while True : 
        while True :
            time.sleep(0.3)
            speech_input = speech_recognize_session(2)
            if str(type(speech_input["transcription"])) == "<class 'str'>" :
                print(speech_input["transcription"])
                title = speech_input["transcription"]
                break
            else : 
                print("잘 못알아 들었습니다.")
                speech.speak_response("잘 못알아 들었습니다.")
        book_list = web.find_book_title(title)
        if book_list == [['','',''], ['','',''], ['','','']] :
            if prompt > 2 :
                print("지속적인 오류로 인해 아이코를 종료합니다.")
                speech.speak_response("지속적인 오류로 인해 아이코를 종료합니다.")
                return 1
            else :
                prompt += 1
                print("도서목록을 만들수 없었습니다. 다시한번 말씀해 주세요. 시도 : " , prompt )
                speech.speak_response("도서목록을 만들수 없었습니다. 다시한번 말씀해 주세요.")
        else : 
            url = web.check_book (book_list)
            if url == "" :
                if prompt > 2 :
                    print("지속적인 오류로 인해 아이코를 종료합니다.")
                    speech.speak_response("지속적인 오류로 인해 아이코를 종료합니다.")
                    return 1
                else : 
                    print("도서찾기가 힘드네요~ 도서명과 저자를 나란히 말씀해 주세요. 시도 : ", prompt)
                    speech.speak_response("도서찾기가 힘드네요~ 도서명과 저자를 나란히 말씀해 주세요.")
                    prompt += 1
            else :
                break
            
    keyword_list = web.keyword_check(url)
    genre = find_major_genre (keyword_list)
    search = "None"
    if genre = "None":
        search = "멜론차트"
    else:
        search = genre + "bgm"


    print ("음악재생을 시작합니다.")
    speech.speak_response("음악재생을 시작합니다.")
    youtube.play_player(search)

def mode_sleep():
    print ("수면 모드를 시작합니다. 재생시간을 말씀해 주세요")
    """
    # 아래 음성 출력 코드 
    output2 = gTTS(text = dest + "를 검색합니다", lang='ko', slow=False)
    output2.save("output2.mp3")
    os.system("start output2.mp3")
    """

def mode_search():
    pass

def mode_tomain():
    print("하던 작업을 종료합니다.")
    speech.speak_response("하던 작업을 종료합니다.")


