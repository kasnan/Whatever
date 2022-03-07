# -*- coding: utf-8 -*-

# importing vlc module
import vlc
# importing pafy module
import pafy
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from speech import speech_recognize_session
import mode
import word_similarity
import speech

DEVELOPER_KEY = 'AIzaSyAZ9fzJyfHaoaxkF7v22q5rGvBXXv-AM9I'
YOUTUBE_API_SERVICE_NAME="youtube"
YOUTUBE_API_VERSION="v3"

URL_base = "https://www.youtube.com/watch?v="

videos = []
playlists = []

def youtube_search(options, query):
  youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
    developerKey=DEVELOPER_KEY)

  # Call the search.list method to retrieve results matching the specified
  # query term.
  search_response = youtube.search().list(
    q= query,
    order = "relevance",
    part="snippet",
    maxResults=options.max_results
  ).execute()

  # Add each result to the appropriate list, and then display the lists of
  # matching videos, channels, and playlists.
  for search_result in search_response.get("items", []):
    if search_result["id"]["kind"] == "youtube#video":
      videos.append("%s (%s)" % (search_result["snippet"]["title"],
                                 search_result['id']['videoId']))
      playlists.append("%s" % (URL_base + search_result['id']['videoId']))

  print("Videos:\n", "\n".join(videos), "\n")
  #print("Channels:\n", "\n".join(channels), "\n")
  #print("Playlists:\n", "\n".join(playlists), "\n")
  print("VideoURLs:\n", "\n".join(playlists), "\n")


def my_call_back(event):
    print("콜백함수호출: 종료호출")
    global status 
    status = 1 

class VlcPlayer:
    '''
    args: VLC인스턴스 생성옵션
    '''
    
    #초기 세팅
    def __init__(self, *args, instance, media_player):
        self.Instance = instance
        self.media_player = media_player
        self.media = self.Instance.media_new("")
    #재생하고자 하는 음악 URL지정
    def set_media_url(self, url):
        media = self.Instance.media_new(url)
        self.media_player.set_media(media)
    #음악 재생
    def play(self, path=None):
        return self.media_player.play()
    #음악 일시정지
    def pause(self):
        self.media_player.pause()
    #음악 재개
    def resume(self):
        self.media_player.set_pause(0)
    #음악 정지
    def stop(self):
        self.media_player.stop()
    #음악을 세팅한 미디어 객체 삭제
    def release(self):
        return self.media_player.release()
    #음악 재생하는 지 확인
    def is_playing(self):
        return self.media_player.is_playing()
    
    def get_time(self):
        return self.media_player.get_time()
    #원하는 시간 위치로 이동
    def set_time(self, ms):
        return self.media_player.get_time(ms)
    #영상 길이 반환
    def get_length(self):
        return self.media_player.get_length()
    #현재 볼륨 반환(근데 잘 안되네;;)
    def get_volume(self):
        return self.media_player.audio_get_volume()
    #볼륨 설정
    def set_volume(self, volume):
        return self.media_player.audio_set_volume(volume)
    #음악 재생?일시정지?그외?
    def get_state(self):
        state = self.media_player.get_state()
        if state == vlc.State.Playing:
            return 1
        elif state == vlc.State.Paused:
            return 0
        else:
            return -1
    #이건 뭘까.. 근데 아마도 영상 위치 관련일듯
    def get_position(self):
        return self.media_player.get_position()
 
    def set_position(self, float_val):
        return self.media_player.set_position(float_val)
 
    def get_rate(self):
        return self.media_player.get_rate()
 
    def set_rate(self, rate):
        return self.media_player.set_rate(rate)
 
    def set_aspect_ratio(self, ratio):
        self.media_player.video_set_scale(0) 
        self.media_player.video_set_aspect_ratio(ratio)
 
    def add_callback(self, event_type, callback):
        self.media_player.event_manager().event_attach(event_type, callback)
 
    def remove_callback(self, event_type, callback):
        self.media.event_manager().event_detach(event_type, callback)
 


def play_player(search_keyword) :
    flag = 0
    argparser.add_argument("--q", help="Search term", default="Google")
    argparser.add_argument("--max-results", help="Max results", default=10)
    args = argparser.parse_args()
    
    youtube_search(args, search_keyword)
    i = vlc.Instance()
    p = i.media_player_new()
    player = VlcPlayer(instance=i,media_player=p)
    player.add_callback(vlc.EventType.MediaPlayerStopped, my_call_back)

    for idx in playlists:
        print(flag)
        if flag == 1:
          break
        video = pafy.new(idx)                                                                                                                       
        best = video.getbestaudio()                                                                                                                 
        playurl = best.url
        player.set_media_url(playurl)
        player.play()
        #player.set_position(0.99)
    
        time.sleep(2.5)
        print("play start")
        status = 0
        while True:
          print("호출어를 불러 음악 정지가능!")
          PROMPT_LIMIT_MODE = 3

          speech_input = speech_recognize_session(PROMPT_LIMIT_MODE)
          speech_input_data = speech_input["transcription"]

          #호출어 유사도 연산
          if speech_input['error']:
            similarity_num = 0.0
          else:
            similarity_num = word_similarity.similarity_con('오케이 아이코', speech_input['transcription'])

          print(speech_input['transcription'])
          if similarity_num >= 0.1:
            # 아이코의 인식률이 많아 가장 많이 오인하는 용어를 추려 감도를 높힘
            player.pause()
            print("네, 부르셨나요.")
            speech.speak_response("네, 부르셨나요.")
            MODE = mode.mode_selection(speech_input)
            end_word = ["노래 꺼", "노래 멈춰", "노래 종료"]
            if MODE in end_word:
              flag = 1
              break            
            if status == 1:
              break
            else:
              pass
        
    p.release()
    i.release()
    mode.mode_tomain()

