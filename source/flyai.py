from datetime import datetime

import requests
from lxml import etree

PLATFORM_NAME = 'FlyAI'


def get_data():
    """
    Parse html data.

    Args:
    """
    url = 'https://www.flyai.com/'

    response = requests.get(url=url)
    html = response.text
    html = etree.HTML(html)
    css_list = html.cssselect('div.pro_box a.project.challage_itemInfo')

    data = {'name': PLATFORM_NAME}
    cps = []
    for info in css_list:
        try:
            info.cssselect('p.noReg')[0].text.strip()
        except Exception:
            continue

        name = info.cssselect('div.name h2')[0].text.strip()
        url = info.attrib['href'].strip()
        description = info.cssselect('div.describe')[0].text.strip()

        response = requests.get(url=url)
        html = response.text
        html = etree.HTML(html)
        time = html.cssselect(
            'div.contest_info > div:nth-child(3) > p')[0].text.strip()

        if '-' in time:
            start_time = time.split('-')[0].strip()
            start_time = start_time.split('：')[1].strip()
            deadline = time.split('-')[1].strip()

            FORMAT = "%Y.%m.%d %H:%M:%S"
            deadline = datetime.strptime(deadline, FORMAT)
            start_time = datetime.strptime(start_time, FORMAT)
        else:
            deadline = None
            start_time = None

        try:
            reward = info.cssselect('div.bonus.flex div')[0].text.strip()
        except Exception:
            reward = info.cssselect('div.bonus.flex p')[0].text.strip()

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
