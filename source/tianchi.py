from requests import request

from source.tool import data2md

PLATFORM_NAME = '天池'


def get_data():
    url = 'https://tianchi.aliyun.com/competition/proxy/api/competition/api/race/listBrief?pageNum=1&pageSize=10&type=1&userId=-1'

    response = request(method='GET', url=url)
    content = response.json()
    competitions = content['data']['list']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        # 必须字段
        name = competition['raceName']
        url = 'https://tianchi.aliyun.com/competition/entrance/{}/introduction'.format(
            competition['raceId'])
        description = competition['brief']
        deadline = competition['currentSeasonEnd']
        reward = competition['currencySymbol'] + str(competition['bonus'])

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


def update():
    data = get_data()
    md_text = data2md(data)

    return md_text
