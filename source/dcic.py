from datetime import datetime, timedelta

import requests

PLATFORM_NAME = 'DCIC 数字中国创新大赛'


def get_data():

    data = {'name': PLATFORM_NAME}
    cps = []

    for raceId in range(10, 20):
        url = f'https://www.dcic-china.com/api/competitions?search=&type=0&tagCode=&indCode=&page=1&per_page=10&sort=default&raceId={raceId}'

        response = requests.get(url=url)
        content = response.json()
        competitions = content['cmpt']['competitions']

        for competition in competitions:
            if competition['typeLabel'] != '算法赛':
                continue
            # 必须字段
            name = competition['title']
            url = 'https://www.dcic-china.com/competitions/' + str(
                competition['id'])

            deadline = competition['endTime']
            FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
            deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)

            start_time = competition['startTime']
            start_time = datetime.strptime(start_time,
                                           FORMAT) + timedelta(hours=8)

            reward = competition['reward']

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
