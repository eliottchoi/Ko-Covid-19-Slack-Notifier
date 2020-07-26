import json
import time

import requests
import xmltodict

URL = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
apiKey = 'jFxpmC%2Bk9OAuwelQlbTO2FMrhk4OGi%2BxyCFujfUbU%2F%2Bn2qJLMPW02PtKKIxvgSMb6oADdw4BYOLBX4BEobUCog%3D%3D'
decodedApiKey = requests.utils.unquote(apiKey)
now = time.localtime()
now_ymd = time.strftime('%Y%m%d', now)

payload = {'ServiceKey': decodedApiKey, 'pageNo': '1', 'numOfRows': '10', 'startCreateDt': str(int(now_ymd)-1), 'endCreateDt': now_ymd}

r = requests.get(URL, params=payload)

covid_string = json.dumps(xmltodict.parse(r.text), indent=4, sort_keys=True)
covid_json = json.loads(covid_string)
covid_items = covid_json["response"]["body"]["items"]["item"]

today_decideCnt = int(covid_items[0]["decideCnt"])
yesterday_decideCnt = int(covid_items[1]["decideCnt"])

today_examCnt = int(covid_items[0]["examCnt"])
yesterday_examCnt = int(covid_items[1]["examCnt"])

today_clearCnt = int(covid_items[0]["clearCnt"])
yesterday_clearCnt = int(covid_items[1]["clearCnt"])

today_deathCnt = int(covid_items[0]["deathCnt"])
yesterday_deathCnt = int(covid_items[1]["deathCnt"])


def decidecount():
    if today_decideCnt > yesterday_decideCnt:
        plus = today_decideCnt - yesterday_decideCnt
        print("총 확진환자 수:", today_decideCnt, "명 | 🔺", plus)
    elif today_decideCnt < yesterday_decideCnt:
        minus = yesterday_decideCnt - today_decideCnt
        print("총 확진환자 수:", today_decideCnt, "명 | 🔻", minus)
    else:
        print("총 확진환자 수:", today_decideCnt, "명")

def examcount():
    if today_examCnt > yesterday_examCnt:
        plus = today_examCnt - yesterday_examCnt
        print("검사진행 수:", today_examCnt, "명 | 🔺", plus)
    elif today_examCnt < yesterday_examCnt:
        minus = yesterday_examCnt - today_examCnt
        print("검사진행 수:", today_examCnt, "명 | 🔻", minus)
    else:
        print("검사진행 수:", today_examCnt, "명")

def clearcount():
    if today_clearCnt > yesterday_clearCnt:
        plus = today_clearCnt - yesterday_clearCnt
        print("총 완치자 수:", today_clearCnt, "명 | 🔺", plus)
    elif today_clearCnt < yesterday_clearCnt:
        minus = yesterday_clearCnt - today_clearCnt
        print("총 완치자 수:", today_clearCnt, "명 | 🔻", minus)
    else:
        print("총 완치자 수:", today_clearCnt, "명")

def deathcount():
    if today_deathCnt > yesterday_deathCnt:
        plus = today_deathCnt - yesterday_deathCnt
        print("총 사망자 수:", today_deathCnt, "명 | 🔺", plus)
    elif today_deathCnt < yesterday_deathCnt:
        minus = yesterday_deathCnt - today_deathCnt
        print("총 사망자 수:", today_deathCnt, "명 | 🔻", minus)
    else:
        print("총 사망자 수:", today_deathCnt, "명")

print()
print("오늘의 코로나 현황을 알려드립니다.")
print()

decidecount()
examcount()
clearcount()
deathcount()