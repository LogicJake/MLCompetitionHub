from datetime import datetime, timedelta
from urllib import parse

import requests

PLATFORM_NAME = 'AI Studio'


def get_data():
    """
    Get a dict of the data

    Args:
    """
    url = 'https://aistudio.baidu.com/studio/match/list'
    data = {
        "p": 1,
        "pageSize": 10,
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url=url,
                             data=parse.urlencode(data),
                             headers=headers)
    content = response.json()
    competitions = content['result']['data']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if int(competition['processCode']) == 4:
            continue
        # 必须字段
        name = competition['matchName']
        url = 'https://aistudio.baidu.com/aistudio/competition/detail/' + str(
            competition['id'])
        description = competition['matchAbs']

        deadline = competition['endTime']
        FORMAT = "%Y/%m/%d"
        deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)

        start_time = competition['startTime']
        start_time = datetime.strptime(start_time, FORMAT) + timedelta(hours=8)

        reward = competition['reward']

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
