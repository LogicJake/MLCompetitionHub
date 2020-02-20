from datetime import datetime, timedelta

import requests

from .utils import STANDARD_TIME_FORMAT, MAX_INTERVAL_DAY

PLATFORM_NAME = '华为云大赛（人工智能赛）'


def get_data():
    url = 'https://competition.huaweicloud.com/competition/v1/categoryId/10001/competions?trackId=107&page_index=1&page_size=10&status=all'

    response = requests.get(url=url)
    content = response.json()
    competitions = content['result']['results']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        if competition['status'] != 'started':
            continue
        # 必须字段
        name = competition['title']
        url = 'https://competition.huaweicloud.com/information/' + str(
            competition['competitionId']) + '/introduction'
        description = competition['brief']

        deadline = competition['endTime']
        FORMAT = "%Y-%m-%d %H:%M:%S"
        deadline = datetime.strptime(deadline, FORMAT)
        deadline = deadline.strftime(STANDARD_TIME_FORMAT)

        start_time = competition['startTime']
        start_time = datetime.strptime(start_time, FORMAT)
        now_time = datetime.utcnow() + timedelta(hours=8)
        interval = now_time - start_time
        if interval.days < MAX_INTERVAL_DAY:
            new_flag = True
        else:
            new_flag = False

        reward = '￥' + competition['bonus']

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
