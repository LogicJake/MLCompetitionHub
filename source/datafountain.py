from datetime import datetime, timedelta

import requests

PLATFORM_NAME = 'DataFountain'


def get_data():
    url = 'https://www.datafountain.cn/api/competitions?search=&state=in_service&type=1&page=1&per_page=30&sort=latest&raceid=all'

    response = requests.get(url=url)
    content = response.json()
    competitions = content['cmpt']['competitions']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['stateOrder'] == 1:
            continue
        # 必须字段
        name = competition['title']
        url = 'https://www.datafountain.cn/competitions/' + str(
            competition['id'])

        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        deadline = competition['endTime']
        start_time = competition['startTime']

        deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)
        start_time = datetime.strptime(start_time, FORMAT) + timedelta(hours=8)

        reward = '￥' + competition['reward']

        cp = {
            'name': name,
            'url': url,
            'description': name,
            'deadline': deadline,
            'reward': reward,
            'start_time': start_time,
        }

        cps.append(cp)
    data['competitions'] = cps

    return data
