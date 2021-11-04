from datetime import datetime, timedelta

import requests

PLATFORM_NAME = 'Nishika'


def get_data():
    url = 'https://api.nishika.com/competitions?format=json'

    response = requests.get(url)
    content = response.json()
    competitions = content['competitions']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['status'] == 'CLOSED':
            continue
        # 必须字段
        name = competition['name']
        url = 'https://www.nishika.com/competitions/' + str(competition['id'])
        description = competition['description']

        if description is None:
            description = name

        deadline = competition['closingAt']
        start_time = competition['startAt']

        FORMAT1 = "%Y-%m-%dT%H:%M:%S+09:00"
        FORMAT2 = "%Y-%m-%dT%H:%M:%S.%f+09:00"

        try:
            deadline = datetime.strptime(deadline,
                                         FORMAT1) - timedelta(hours=1)
        except Exception:
            deadline = datetime.strptime(deadline,
                                         FORMAT2) - timedelta(hours=1)
        try:
            start_time = datetime.strptime(start_time,
                                           FORMAT1) - timedelta(hours=1)
        except Exception:
            start_time = datetime.strptime(start_time,
                                           FORMAT2) - timedelta(hours=1)

        reward = competition['totalPrize']

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
