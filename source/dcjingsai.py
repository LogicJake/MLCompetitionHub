from datetime import datetime, timedelta
from urllib import parse

import requests

PLATFORM_NAME = 'DC竞赛'


def get_data():
    """
    Get a dict

    Args:
    """
    url = 'https://www.dcjingsai.com/common/getNewCmptList.json'
    data = {
        'page': 1,
        'pageSize': 10,
        'type': 'SUBMITRESULT',
        'state': 'active'
    }

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(url=url,
                             data=parse.urlencode(data),
                             headers=headers)
    content = response.json()
    competitions = content['data']['cmptList']['list']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['rewardType'] != '奖金':
            continue
        # 必须字段
        name = competition['name']
        url = 'https://www.dcjingsai.com/common/cmpt/{}_竞赛信息.html'.format(name)
        description = competition['introduction']

        deadline = datetime.utcfromtimestamp(int(competition['endTime'] /
                                                 1000))
        start_time = datetime.utcfromtimestamp(
            int(competition['startTime'] / 1000))

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
