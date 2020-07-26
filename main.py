import requests
import json
import xmltodict
import time


URL = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
apiKey = 'jFxpmC%2Bk9OAuwelQlbTO2FMrhk4OGi%2BxyCFujfUbU%2F%2Bn2qJLMPW02PtKKIxvgSMb6oADdw4BYOLBX4BEobUCog%3D%3D'
decodedApiKey = requests.utils.unquote(apiKey)
now_raw = time.localtime()
now_year_month_date = int(time.strftime('%Y%m%d', now_raw))

payload = {
    'ServiceKey': decodedApiKey,
    'pageNo': '1',
    'numOfRows': '10',
    'startCreateDt': now_year_month_date-1,
    'endCreateDt': now_year_month_date
}

r = requests.get(URL, params=payload)

covid_string = json.dumps(xmltodict.parse(r.text), indent=4, sort_keys=True)
covid_json = json.loads(covid_string)

covid_items = covid_json["response"]["body"]["items"]["item"]
today_covid = covid_items[0]
yesterday_covid = covid_items[1]
result_code = int(covid_json["response"]["header"]["resultCode"])
total_count = int(covid_json["response"]["body"]["totalCount"])
last_notified = int(today_covid["stateDt"])

if len(covid_json) == 0:
    print("서버와 통신하지 못했습니다.")
    exit()
elif result_code != 0:
    print("받아오지 못했습니다.")
    exit()
elif total_count == 0:
    print("출력할 항목이 없습니다.")
    exit()
elif last_notified != now_year_month_date:
    print("아직 오늘 확진자가 발표되지 않았습니다. 조금 뒤 다시 시도해주세요!")
    exit()


today_decideCnt = int(today_covid["decideCnt"])
yesterday_decideCnt = int(yesterday_covid["decideCnt"])

today_examCnt = int(today_covid["examCnt"])
yesterday_examCnt = int(yesterday_covid["examCnt"])

today_clearCnt = int(today_covid["clearCnt"])
yesterday_clearCnt = int(yesterday_covid["clearCnt"])

today_deathCnt = int(today_covid["deathCnt"])
yesterday_deathCnt = int(yesterday_covid["deathCnt"])


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

decidecount()
examcount()
clearcount()
deathcount()