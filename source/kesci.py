from datetime import datetime, timedelta

import requests

from .utils import STANDARD_TIME_FORMAT, MAX_INTERVAL_DAY

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
        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        if deadline is not None:
            deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)
            deadline = deadline.strftime(STANDARD_TIME_FORMAT)
        else:
            deadline = '无截止日期'

        start_time = competition['StartDate']
        start_time = datetime.strptime(start_time, FORMAT) + timedelta(hours=8)
        now_time = datetime.utcnow() + timedelta(hours=8)
        interval = now_time - start_time
        if interval.days < MAX_INTERVAL_DAY:
            new_flag = True
        else:
            new_flag = False

        reward = competition['DisplayLabel']

        cp = {
            'name': name,
            'url': url,
            'description': description,
            'deadline': deadline,
            'reward': reward,
            'start_time': start_time,
            'new_flag': new_flag
        }

        cps.append(cp)
    data['competitions'] = cps

    return data
