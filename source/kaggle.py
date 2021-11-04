import json
from datetime import datetime, timedelta

import requests

PLATFORM_NAME = 'Kaggle'


def get_data():
    session = requests.session()
    session.get('https://www.kaggle.com/competitions')
    token = session.cookies.get_dict()['XSRF-TOKEN']

    url = 'https://www.kaggle.com/requests/CompetitionService/ListCompetitions'
    data = {
        "selector": {
            "competitionIds": [],
            "listOption": "active",
            "sortOption": "newest",
            "hostSegmentIdFilter": 0,
            "searchQuery": "",
            "prestigeFilter": "unspecified",
            "tagIds": [],
            "requireSimulations": False
        },
        "pageToken": "",
        "pageSize": 50
    }

    headers = {'x-xsrf-token': token}

    response = session.post(url=url, data=json.dumps(data), headers=headers)
    content = response.json()
    competitions = content['result']['competitions']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['rewardTypeName'] != 'USD':
            continue

        # 必须字段
        name = competition['title']
        url = 'https://www.kaggle.com/c/' + competition['competitionName']
        description = competition['briefDescription']

        deadline = competition['deadline']
        FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)

        start_time = competition['dateEnabled']
        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        start_time = datetime.strptime(start_time, FORMAT) + timedelta(hours=8)

        reward = str(competition['rewardQuantity']
                     ) + ' ' + competition['rewardTypeName']

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
