from datetime import datetime, timedelta

from requests import request

from .utils import STANDARD_TIME_FORMAT, MAX_INTERVAL_DAY

PLATFORM_NAME = 'Kaggle'


def get_data():
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
        deadline = deadline.strftime(STANDARD_TIME_FORMAT)

        start_time = competition['enabledDate']
        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
        start_time = datetime.strptime(start_time, FORMAT) + timedelta(hours=8)
        now_time = datetime.utcnow() + timedelta(hours=8)
        interval = now_time - start_time
        if interval.days < MAX_INTERVAL_DAY:
            new_flag = True
        else:
            new_flag = False

        reward = str(competition['rewardQuantity']
                     ) + ' ' + competition['rewardTypeName']

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
