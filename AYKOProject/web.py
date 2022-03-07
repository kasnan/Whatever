# -*- coding: utf-8 -*-

#웹용
from ssl import Options
import selenium
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import webbrowser as web
from webdriver_manager.chrome import ChromeDriverManager 
import requests
import chromedriver_autoinstaller
from bs4 import BeautifulSoup


#from main import PROMPT_LIMIT
PROMPT_LIMIT = 2

from selenium.webdriver.chrome.options import Options

import speech
import random
import time
import urllib.request
import speech

chrome_ver = chromedriver_autoinstaller.get_chrome_version().split('.')[0]





yesword_list = ['네', '응', '그래', '맞아', '예', '어']

def find_book_title(title) :                                # 기능 : 제목(사실 저자도 가능 짜잔~)을 입력하면 도서 후보군에 대한 html 정보를 모은다. 출력은 2차원 배열이며 최대 3개의 도서에 대한 제목, 저자, 링크 리스트이다. 
    url = 'https://search.kyobobook.co.kr/web/search?vPstrKeyWord='+ title 
    # + '&searchPcondition=1&searchCategory=%EA%B5%AD%EB%82%B4%EB%8F%84%EC%84%9C@KORBOOK&collName=KORBOOK&from_CollName=%EA%B5%AD%EB%82%B4%EB%8F%84%EC%84%9C@KORBOOK&searchOrder=0&vPstrTab=PRODUCT&from_coll=KORBOOK&currentPage=1&orderClick=LAH'
    # 교보문고 검색창을 활용하는데 논문과 블루레이 디스크 등이 섞이는 경우가 있는데 이게 싫다면 위의 코드를 url에 붙히면 된다. 단 국내도서로 한정된다.
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    details = soup.find_all('td',{'class' : 'detail'}) # 책들의 상세정보 class를 호출한다. 너무 포괄적인데서부터 가져와져와서 필터링 과정이 길어지는데 어쩔수 없다.
                                                       # detail는 각 책의 디테일 정보가 담긴 (저자, 출판사, 링크 등등) 1차원 리스트의 형태인데 우리는 여기서 제목, 저자, 링크를 추출할 것이다.

    i = 0
    title_list = ['','','']
    author_list = ['','','']
    link_list = ['','','']
    # 함수를 호출할 때마다 리스트와 카운터를 초기화시킨다. 사실 append 함수를 쓸수있었는데 까먹었다 ㅈㅅ ㅎㅎ;;
    
    print("도서 후보군을 생성합니다.")
    while  i < 3 and i<len(details) :      # 후보 3개만 만들겠습니다. 검색창에 세개 이상없으면 있는만큼만 만듬
        print( str(i+1) +'번 째 후보 생성중입니다.')
                                                                        #원리 : details 변수를 출력해보면 제목과 링크, 저자의 항목 앞 뒤에 특정 문자열이 붙는다(css 구문의 태그)
                                                                        #       이 태그들을 지우고 제목, 링크, 저자만을 필터링한다.
        title_start = str(details[i]).find('검색결과')                    
        title_end = str(details[i]).find(';GA_Ecommerce_Click') 
        title_list[i] = str(details[i])[title_start+ 7 : title_end- 2]  # 제목 추출

        link_start = str(details[i]).find('a href="')
        link_end = str(details[i]).find('onclick')
        link_list[i] = str(details[i])[link_start+8 : link_end-2]       # 링크 추출
        link_list[i] = link_list[i].replace("amp;",'')                  # 웹상에서 &가 amp; 로 바뀌는 문제가 생겨 이를 삭제

        author_start = str(details[i]).find('searchPcondition')        
        author_list[i] = str(details[i])[author_start +20:]             # keywords 변수의 앞부분을 지움으로써 똑같은 키워드 (</a>가 흔한 태그이므로)를 다시 찾아내는걸 방지한다.       
        author_end = author_list[i].find("</a>")                        # 앞부분을 지워줬기 때문에 흔한태그의 위치로도 저자 text의 정확한 끝을 찾을수 있다.
        if str(details[i]).find('searchPcondition') == -1 :             # 가끔 저자를 기재하지 않는 경우가 있어 author가 존재하지 않는다면 작가 미상으로 설정한다.
            author_list[i] = "미상"
        else :
            author_list[i] = author_list[i][:author_end]                #저자 추출
        i += 1 
    book_list = [title_list, author_list,link_list]                     # 리스트 작성 완료
    #print(details[0:2])  #디버그시 활용
    #print(book_list[1][0])
    print(book_list)
    
    return book_list



def check_book (book_list) : # 기능 : find_book_title로 도출된 후보 리스트을 입력하면 상위 후보부터 차례로 일치여부를 묻는다. 일치하면 url을 반환한다. 자꾸 헛소리하거나 아니라고 하면 짜증낸다.
    global url
    url = ""
    if book_list == [['','',''],['','',''],['','','']] :
        print('그런책은 찾을수 없었습니다.')
        speech.speak_response('그런책은 찾을수 없었습니다.')
    else :
        i = 0
        is_found = False 
        while i < 3 and i < len(book_list) : # 후보군은 최대 3개 
            print("읽고계신 책이 " + book_list[1][i] + " 작가의 " + book_list[0][i]+ "입니까?")
            speech.speak_response("읽고계신 책이 " + book_list[1][i] + " 작가의 " + book_list[0][i]+ "입니까?")
            time.sleep(0.3)
            speech_input = speech.speech_recognize_session(PROMPT_LIMIT)            
            print (speech_input["transcription"])
            if (speech_input["transcription"]) in yesword_list :
                url = book_list[2][i]
                print ("url : " + url)
                is_found = True                 # 찾았다면 찾은 상태의 부울 변수가 True가 되고 더 이상 묻지 않는다.
                break
            i += 1
        if is_found == False :                  # 3회 질문했음에도 찾지 못했다면 짜증을 낸다.
            print("깐깐하누';;")
        return url

def keyword_check(url) :                        # 기능 : check_book으로 부터 URL을 받으면 이를 통해 장르를 추출한다.
    chrome_options = Options()
    chrome_options.add_argument('--headless') 
    # 크롬브라우져의 옵션 확인 : 크롤링은 실행하되 브라우져창을 띄우지 않는다.

    try:
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe',chrome_options=chrome_options)
    except:
        chromedriver_autoinstaller.install(True)
        driver = webdriver.Chrome(f'./{chrome_ver}/chromedriver.exe',chrome_options=chrome_options)
    driver.implicitly_wait(10)
    # 동적크롤링을 위한 브라우져 스타트. 뒤쪽에 옵션을 붙혀주어 브라우져가 켜지는 낭비를 막았다.


    if str(url) == "None" :                      # check_book에서 도서를 찾지 못했다면 그냥 종료한다.
        print("도서정보를 찾을 수 없습니다. 키워드 검색을 종료합니다.")
        speech.speak_response("도서정보를 찾을 수 없습니다. 키워드 검색을 종료합니다.")
    else :
        print("키워드 데이터에 액세스 합니다.")
        driver.get(url)                                                 # keyword pick 은 요청을 보내면 바로 호출해주지 않고 직접 접속해야 실행되는 자바스트립트이다(하 왜 내가 이걸 몰랐을까~~).
                                                                        # 따라서 셀레니움으로 직접 웹에 접속해서 자바스크립트를 따오는 과정이 필요하다.
        soup = BeautifulSoup(driver.page_source, 'html.parser')         # 실행한 웹사이트에서 파싱
        html_keywords = soup.select( '.book_keyword')
        keywords = str(html_keywords[0])
        #print(keywords)
        html_category =  soup.find('ul',{'class' : 'list_detail_category'})                         #마찬가지로 카테고리 추출
        categorys = str(html_category.text).replace("\t","").replace(">","").replace(" ","")        #쓸데 없는 문자 제거
        keyword_list = []


        print("카테고리 리스트를 추출합니다.")
        keyword_list = []
        while True :
            categorys = categorys.lstrip("\n")
            category_end = categorys.find("\n")
            if category_end == -1 :
                print("카테고리 추출 종료")
                break
            else : 
                category = categorys[:category_end]
                keyword_list.append(category)
                categorys = categorys [category_end + 2 :]
        
        print("키워드 리스트를 추출합니다.")
        while True : 
            keyword_start = keywords.find('popupOpenKey')      # find_book_title의 방식과 같은 필터링 방식 
            keyword_end = keywords.find('\'JA3\'')     
            if keyword_start == -1 or keyword_end == - 1 :      # 더이상의 키워드 태그를 찾지 못하면 종료하고 모아온 키워드를 출력한다.
                print(keyword_list)
                print("키워드 추출 종료")
                break
            else :
                keyword = keywords[keyword_start + 14 : keyword_end - 3 ]   # 키워드 추출
                #print(keyword)
                #print(str(keyword_start) + "   " + str(keyword_end))
                keyword_list.append(keyword)                    # 키워드가 얼마나 있는지 모르기 때문에 append 함수를 이용했다.
                keywords = keywords[keyword_end + 10 : ]        # keywords 변수의 앞부분을 지움으로써 똑같은 키워드를 다시 찾아내는걸 방지한다.

    return keyword_list
    
