from datetime import datetime, timedelta

import requests

PLATFORM_NAME = 'ZINDI'


def get_data():
    """
    Get a list of the competition

    Args:
    """
    url = 'https://api.zindi.africa/v1/competitions?page=0&per_page=20&kind=competition&active=1&reward=prize'

    response = requests.get(url=url)
    content = response.json()
    competitions = content['data']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        # 必须字段
        name = competition['title']
        description = competition['subtitle']
        url = 'https://zindi.africa/competitions/' + str(competition['id'])

        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        deadline = competition['end_time']
        start_time = competition['start_time']

        deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)
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
