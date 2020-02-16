from datetime import datetime, timedelta

from requests import request

from .utils import STANDARD_TIME_FORMAT

PLATFORM_NAME = 'Kaggle'


def get_data():
    url = 'https://www.kaggle.com/competitions.json?sortBy=grouped&group=general&page=1&pageSize=20'

    response = request(method='GET', url=url)
    content = response.json()
    competitions = content['fullCompetitionGroups'][1]['competitions']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        # 必须字段
        name = competition['competitionTitle']
        url = 'https://www.kaggle.com' + competition['competitionUrl']
        description = competition['competitionDescription']
        deadline = competition['deadline']
        FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)
        deadline = deadline.strftime(STANDARD_TIME_FORMAT)
        if competition['rewardTypeName'] != 'USD':
            continue

        reward = str(competition['rewardQuantity']
                     ) + ' ' + competition['rewardTypeName']

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
