import requests
import json
import pandas as pd

url = "https://dapi.kakao.com/v2/local/geo/coord2regioncode.json?x=127.06101374947465&y=37.58564565326407"
headers = {"Authorization": "KakaoAK 033c1a2c95d3e8e5e5930a53428f574d"}

api_test = requests.get(url,headers=headers)
url_text = json.loads(api_test.text)
print(url_text['documents'][0]['address_name'])