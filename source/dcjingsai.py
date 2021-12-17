from datetime import datetime

import requests

PLATFORM_NAME = 'DC竞赛'


def get_data():
    url = 'https://challenge.datacastle.cn/v3/api/common/cmpt/getCmptListES.json?keword=&orderType=&type=%E7%AE%97%E6%B3%95%E8%B5%9B&state=1&page=1&pageSize=10'

    response = requests.get(url=url)
    content = response.json()
    competitions = content['data']['map']['list']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['rewardType'] != '奖金':
            continue
        # 必须字段
        name = competition['cmptName']
        id = competition['id']
        url = 'https://challenge.datacastle.cn/v3/cmptDetail.html?id={}'.format(
            id)
        description = competition['introduction']

        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        deadline = datetime.strptime(competition['endTime'], FORMAT)
        start_time = datetime.strptime(competition['startTime'], FORMAT)

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
