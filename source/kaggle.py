from requests import request
from .tool import data2md

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

        if competition['rewardTypeName'] == 'USD':
            reward = str(competition['rewardQuantity']
                         ) + ' ' + competition['rewardTypeName']
        elif competition['rewardTypeName'] == 'None':
            reward = 'Nothing'
        else:
            reward = competition['rewardTypeName']

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


if __name__ == "__main__":
    data = update()
    print(data)
