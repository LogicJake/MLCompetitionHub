from datetime import datetime, timedelta

import requests

PLATFORM_NAME = 'heywhale和鲸（Kesci）'


def get_data():
    url = 'https://www.kesci.com/v2/api/competitions?perPage=12&page=1&Status=1'

    response = requests.get(url=url)
    content = response.json()
    competitions = content['data']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['DisplayLabel'] == '练习赛' or competition[
                'DisplayLabel'] == '训练营' or competition[
                    'DisplayLabel'] == 'DATA TRAIN':
            continue
        # 必须字段
        name = competition['Name']
        url = 'https://www.kesci.com/home/competition/' + competition['_id']
        description = competition['ShortDescription']

        deadline = competition['EndDate']
        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        if deadline is not None:
            deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)
        else:
            deadline = None

        start_time = competition['StartDate']
        start_time = datetime.strptime(start_time, FORMAT) + timedelta(hours=8)

        reward = competition['DisplayLabel']

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
