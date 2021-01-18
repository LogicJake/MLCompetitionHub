from datetime import datetime, timedelta

import requests

PLATFORM_NAME = 'DC竞赛'


def get_data():
    url = 'https://js.dclab.run/v2/api/common/cmpt/getCmptList.json?cmptName=&order=desc&orderType=&page=1&pageSize=10&state=active&type=%E7%AE%97%E6%B3%95%E8%B5%9B'

    response = requests.get(url=url)
    content = response.json()
    competitions = content['data']['map']['list']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['reward_type'] != '奖金':
            continue
        # 必须字段
        name = competition['name']
        id = competition['id']
        url = 'https://js.dclab.run/v2/cmptDetail.html?id={}'.format(id)
        description = competition['introduction']

        deadline = datetime.utcfromtimestamp(
            int(competition['end_time'] / 1000))
        start_time = datetime.utcfromtimestamp(
            int(competition['start_time'] / 1000))

        deadline = deadline + timedelta(hours=8)
        start_time = start_time + timedelta(hours=8)

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
