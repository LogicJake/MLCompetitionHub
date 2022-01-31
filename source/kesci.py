from datetime import datetime, timedelta

import requests

PLATFORM_NAME = 'heywhale和鲸（Kesci）'


def get_data():
    url = 'https://www.heywhale.com/v2/api/competitionsCommunity?perPage=12&page=1&excludeDetailType=WORKSHOP,TRAINING_CAMP,EXERCISE_DATA_ANALYSIS,EXERCISE_ALGORITHM,OTHER&Status=1'

    response = requests.get(url=url)
    content = response.json()
    competitions = content['data']

    data = {'name': PLATFORM_NAME}
    cps = []
    for competition in competitions:
        FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"

        if 'IsSeriesCompetition' in competition:
            childrenCompetitions = competition['childrenCompetitions']
            parent_name = competition['Name']

            for competition in childrenCompetitions:
                if competition['DetailType'] != 'ALGORITHM':
                    continue

                name = parent_name + '——' + competition['Name']
                url = 'https://www.kesci.com/home/competition/' + competition[
                    '_id']
                description = name

                deadline = competition['EndDate']
                if deadline is not None:
                    deadline = datetime.strptime(deadline,
                                                 FORMAT) + timedelta(hours=8)
                else:
                    deadline = None

                start_time = competition['StartDate']
                start_time = datetime.strptime(start_time,
                                               FORMAT) + timedelta(hours=8)

                if competition['DisplayLabel'] == '':
                    reward = competition['Award']
                else:
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
        else:
            if competition['DetailType'] != 'ALGORITHM':
                continue

            # 必须字段
            name = competition['Name']
            url = 'https://www.kesci.com/home/competition/' + competition['_id']
            description = name

            deadline = competition['EndDate']
            if deadline is not None:
                deadline = datetime.strptime(deadline,
                                             FORMAT) + timedelta(hours=8)
            else:
                deadline = None

            start_time = competition['StartDate']
            start_time = datetime.strptime(start_time,
                                           FORMAT) + timedelta(hours=8)

            if competition['DisplayLabel'] == '':
                reward = competition['Award']
            else:
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
