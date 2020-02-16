import requests

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
