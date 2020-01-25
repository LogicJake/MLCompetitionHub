import json

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
        reward = competition['awardMoney']

        cp = {
            'name': name,
            'url': url,
            'description': description,
            'deadline': deadline,
            'reward': reward
        }

        cps.append(cp)
    data['competitions'] = cps

    return data
