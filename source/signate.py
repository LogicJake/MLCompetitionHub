import json
from datetime import datetime

import requests
from lxml import etree

PLATFORM_NAME = 'SIGNATE'


def get_data():
    url = 'https://signate.jp/competitions/with-prizes?per=20'

    response = requests.get(url=url)
    html = response.text

    html = etree.HTML(html)
    text = html.cssselect('#app component')[0]
    text = text.attrib['v-bind']
    text = text.encode('utf-8').decode('unicode_escape')

    data = {'name': PLATFORM_NAME}
    cps_raw = json.loads(text)['competitions']
    cps = []
    for info in cps_raw:
        is_active = info['is_active']
        if not is_active:
            break

        reward = info['translated_total_prize']
        if '社会貢献' in reward:
            continue

        name = info['translated_title']
        url = info['uri']
        description = info['translated_description']
        deadline = info['end_date']

        FORMAT = "%Y-%m-%d %H:%M:%S"
        deadline = datetime.strptime(deadline, FORMAT)

        cp = {
            'name': name,
            'url': url,
            'description': description,
            'deadline': deadline,
            'reward': reward,
            'start_time': None,
        }

        cps.append(cp)

    data['competitions'] = cps

    return data
