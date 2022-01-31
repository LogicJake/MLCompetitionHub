import json
from datetime import datetime

from requests import request

PLATFORM_NAME = '天池'


def get_data():
    url = 'https://tianchi.aliyun.com/mobile/api/proxy/competitionService/api/race/listBrief?pageNum=1&pageSize=10&state=1&userId=-1'

    headers = {
        "User-Agent":
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1.6) "
    }

    response = request(method='GET', url=url, headers=headers)
    content = response.json()
    competitions = content['data']['list']

    data = {'name': PLATFORM_NAME}
    cps = []

    with open('./source/tianchi_url_map.json', 'r') as f:
        url_map = json.load(f)

    for competition in competitions:
        if int(competition['state']) != 1 or int(competition['bonus']) == 0:
            continue

        # 必须字段
        season = competition['season']
        name = competition['raceName'] + '(赛季 {})'.format(season + 1)

        if str(competition['raceId']) in url_map:
            url = url_map[str(competition['raceId'])]
        else:
            url = 'https://tianchi.aliyun.com/competition/entrance/{}/introduction'.format(
                competition['raceId'])

        description = competition['brief']

        deadline = competition['currentSeasonEnd']
        start_time = competition['currentSeasonStart']

        FORMAT = "%Y-%m-%d %H:%M:%S"
        deadline = datetime.strptime(deadline, FORMAT)
        start_time = datetime.strptime(start_time, FORMAT)

        reward = competition['currencySymbol'] + str(competition['bonus'])

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
