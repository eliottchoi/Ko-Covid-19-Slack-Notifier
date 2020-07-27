import json
from slacker import Slacker
from main import today_total_cases, today_increased_cases, today_performing_tests, today_increased_performing_tests, today_recovered, today_increased_recovered, today_deaths, today_increased_deaths, date_last_report

with open('config.json', 'r') as f:
    config = json.load(f)

slack_token = config['SLACK']['API_TOKEN']
slack = Slacker(slack_token)


def increasement(increasement_number):
    up = "🔺"
    down = "🔻"
    if increasement_number > 0:
        return up, abs(increasement_number)
    elif increasement_number < 0:
        return down, abs(increasement_number)


today_total_cases_string = ("*확진 : {}명* ({}{})".format(today_total_cases, increasement(today_increased_cases)[0], increasement(today_increased_cases)[1]))
today_performing_tests_string = ("*검사 진행 : {}명* ({}{})".format(today_performing_tests, increasement(today_increased_performing_tests)[0], increasement(today_increased_performing_tests)[1]))
today_recovered_string = ("*완치자 : {}명* ({}{})".format(today_recovered, increasement(today_increased_recovered)[0], increasement(today_increased_recovered)[1]))
today_deaths_string = ("*사망자 : {}명* ({}{})".format(today_deaths, increasement(today_increased_deaths)[0], increasement(today_increased_deaths)[1]))
new_line = "\n"


slack.chat.post_message('#team', date_last_report + ' 발표')
slack.chat.post_message('#team', today_total_cases_string)
slack.chat.post_message('#team', today_performing_tests_string)
slack.chat.post_message('#team', today_recovered_string)
slack.chat.post_message('#team', today_deaths_string)