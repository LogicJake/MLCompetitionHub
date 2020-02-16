from datetime import datetime, timedelta

import requests

from .utils import STANDARD_TIME_FORMAT

PLATFORM_NAME = 'heywhale和鲸（Kesci）'


def get_data():
    url = 'https://www.kesci.com/api/competitions?perPage=12&page=1&Status=1'

    response = requests.get(url=url)
    content = response.json()
    competitions = content['data']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['DisplayLabel'] == '练习赛' or competition[
                'DisplayLabel'] == '训练营':
            continue
        # 必须字段
        name = competition['Name']
        url = 'https://www.kesci.com/home/competition/' + competition['_id']
        description = competition['ShortDescription']

        deadline = competition['EndDate']
        if deadline is not None:
            FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
            deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)
            deadline = deadline.strftime(STANDARD_TIME_FORMAT)
        else:
            deadline = '无截止日期'

        reward = competition['DisplayLabel']

        cp = {
            'name': name,
            'url': url,
            'description': description,
            'deadline': deadline,
            'reward': reward
        }

        cps.append(cp)
    data['competitions'] = cps

    return data
