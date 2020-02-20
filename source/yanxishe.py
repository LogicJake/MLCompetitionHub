from datetime import datetime, timedelta

import requests

PLATFORM_NAME = 'AI研习社'


def get_data():
    url = 'https://api.yanxishe.com/aihub/match/default/index?page=1&size=10&tag=0&match_type=bonus'

    response = requests.get(url)
    content = response.json()
    competitions = content['data']['items']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['match_status'] == 'over':
            continue
        # 必须字段
        name = competition['title']
        url = 'https://god.yanxishe.com/' + competition['id']
        description = competition['desc']

        deadline = datetime.utcfromtimestamp(int(competition['end_time']))
        deadline = deadline + timedelta(hours=8)

        start_time = datetime.utcfromtimestamp(int(competition['start_time']))
        start_time = start_time + timedelta(hours=8)

        reward = competition['bonus']

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
