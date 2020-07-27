import requests
import json
import xmltodict
import time


url = 'http://openapi.data.go.kr/openapi/service/rest/Covid19/getCovid19InfStateJson'
with open('config.json', 'r') as f:
    config = json.load(f)

apiKey = config['DEFAULT']['API_KEY']

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

full_url = requests.get(url, params=payload)

covid_string = json.dumps(xmltodict.parse(full_url.text), indent=4, sort_keys=True)
covid_json = json.loads(covid_string)

response_result = covid_json["response"]

result_code = int(response_result["header"]["resultCode"])
result_days = int(response_result["body"]["totalCount"])

covid_items = response_result["body"]["items"]["item"]

today_covid_info = None
yesterday_covid_info = None


if 1 < len(covid_items) < 10:
    today_covid_info = covid_items[0]
    yesterday_covid_info = covid_items[1]
elif len(covid_json) == 0 or result_code != 0:
    error_message = "서버와 통신하지 못했습니다."
    print(error_message)
    exit()
elif result_days < 2:
    error_message = "아직 오늘 확진자가 발표되지 않았습니다. 오전 11시에 다시 시도해주세요!"
    print(error_message)
    exit()

today_total_cases = int(today_covid_info["decideCnt"])
yesterday_total_cases = int(yesterday_covid_info["decideCnt"])

today_performing_tests = int(today_covid_info["examCnt"])
yesterday_performed_tests = int(yesterday_covid_info["examCnt"])

today_recovered = int(today_covid_info["clearCnt"])
yesterday_recovered = int(yesterday_covid_info["clearCnt"])

today_deaths = int(today_covid_info["deathCnt"])
yesterday_deaths = int(yesterday_covid_info["deathCnt"])

date_last_report = today_covid_info["createDt"]

def get_increasement(today, yesterday):
    increasement = today - yesterday
    return increasement


today_increased_cases = get_increasement(today_total_cases, yesterday_total_cases)
today_increased_performing_tests = get_increasement(today_performing_tests, yesterday_performed_tests)
today_increased_recovered = get_increasement(today_recovered, yesterday_recovered)
today_increased_deaths = get_increasement(today_deaths, yesterday_deaths)