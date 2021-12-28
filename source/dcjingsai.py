from datetime import datetime

import requests

PLATFORM_NAME = 'DC竞赛'


def parse_competition(competition):
    if competition['rewardType'] != '奖金':
        return
    # 必须字段
    name = competition['cmptName']
    id = competition['id']
    url = 'https://challenge.datacastle.cn/v3/cmptDetail.html?id={}'.format(id)


    reward = competition['reward']

    return name, url, reward


def get_data():
    url = 'https://challenge.datacastle.cn/v3/api/common/cmpt/getCmptListES.json?keword=&orderType=&type=&state=&page=1&pageSize=10'

    response = requests.get(url=url)
    content = response.json()
    competitions = content['data']['map']['list']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        description = competition['introduction']
        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        deadline = datetime.strptime(competition['endTime'], FORMAT)
        start_time = datetime.strptime(competition['startTime'], FORMAT)
        
        if competition['ztsList']:
            for c in competition['ztsList']:
                name, url, reward = parse_competition(
                    c)
                cp = {
                    'name': name,
                    'url': url,
                    'description': description,
                    'deadline': deadline,
                    'reward': reward,
                    'start_time': start_time,
                }

                cps.append(cp)
        else:
            name, url, reward = parse_competition(
                competition)
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
