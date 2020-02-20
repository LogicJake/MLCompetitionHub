from datetime import datetime, timedelta

import requests
from lxml import etree

PLATFORM_NAME = 'biendata'


def get_data():
    url = 'https://www.biendata.com/competition/'

    response = requests.get(url=url)
    html = response.text

    html = etree.HTML(html)
    css_list = html.cssselect('div.active ul.list li')
    data = {'name': PLATFORM_NAME}
    cps = []
    for info in css_list:
        reward = info.cssselect('div.end > span')[0].text.strip()
        if reward == "":
            continue

        name = info.cssselect('span.des_text.p0')[0].text.strip()
        url = 'https://www.biendata.com' + info.cssselect(
            'div.content h4 a')[0].attrib['href'].strip()

        time = info.cssselect('dl dd:nth-child(2) > span')[0].text.strip()
        start_time = time.split('~')[0].strip()
        deadline = time.split('~')[1].strip()
        start_time = start_time.split(':')[1]

        FORMAT = "%Y-%m-%d"
        deadline = datetime.strptime(deadline, FORMAT) + timedelta(hours=8)
        start_time = datetime.strptime(start_time, FORMAT) + timedelta(hours=8)

        cp = {
            'name': name,
            'url': url,
            'description': name,
            'deadline': deadline,
            'reward': reward,
            'start_time': start_time,
        }

        cps.append(cp)

    data['competitions'] = cps

    return data
