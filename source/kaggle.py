from datetime import datetime, timedelta

from requests import request

PLATFORM_NAME = 'Kaggle'


def get_data():
    """
    Get a list

    Args:
    """
    url = 'https://www.kaggle.com/competitions.json?sortBy=grouped&group=general&page=1&pageSize=20'

    response = request(method='GET', url=url)
    content = response.json()
    competitions = content['fullCompetitionGroups'][1]['competitions']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['rewardTypeName'] != 'USD':
            continue

        # 必须字段
        name = competition['competitionTitle']
        url = 'https://www.kaggle.com' + competition['competitionUrl']
        description = competition['competitionDescription']

        deadline = competition['deadline']
        FORMAT = "%Y-%m-%dT%H:%M:%SZ"
        deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)

        start_time = competition['enabledDate']
        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        start_time = datetime.strptime(start_time, FORMAT) + timedelta(hours=8)

        reward = str(competition['rewardQuantity']
                     ) + ' ' + competition['rewardTypeName']

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
