import json
from datetime import datetime, timedelta

import requests

PLATFORM_NAME = '图灵联邦'


def get_data():
    url = 'https://api.turingtopia.com/tuling/newCompetition/competitionList/get/competitionList?guid='
    data = {
        "competitionGrade": 2,
        "currentPage": 1,
        "pageSize": 10,
        "search": "",
        "industryId": "",
        "sequence": "newest",
        "inside": "0"
    }

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url=url, data=json.dumps(data), headers=headers)
    content = response.json()
    competitions = content['data']['competitionList']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if int(competition['competitionStatus']) != 3:
            continue
        # 必须字段
        name = competition['competitionName']
        url = 'http://www.turingtopia.com/competitionnew/detail/' + competition[
            'competitionId'] + '/sketch'
        description = name

        deadline = competition['endTime']
        FORMAT = "%Y-%m-%dT%H:%M:%S.%f+0000"
        deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)

        start_time = competition['startTime']
        start_time = datetime.strptime(start_time, FORMAT) + timedelta(hours=8)

        reward = competition['awardMoney']

        cp = {
            'name': name,
            'url': url,
            'description': description,
            'deadline': deadline,
            'reward': reward,
            'start_time': start_time,
        }

        cps.append(cp)
    data['competitions'] = cps

    return data
