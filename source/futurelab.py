import requests
from lxml import etree

PLATFORM_NAME = 'AI FUTURELAB'


def get_data():
    """
    Returns a list of the html data

    Args:
    """
    url = 'https://ai.futurelab.tv/contest/all'

    response = requests.get(url=url)
    html = response.text
    html = etree.HTML(html)
    css_list = html.cssselect('#contest-ul1 > li')

    data = {'name': PLATFORM_NAME}
    cps = []
    for info in css_list:
        status = info.cssselect('span.contest-status')[0].text.strip()
        if status == '已结束':
            continue

        name = info.cssselect(
            'div.col-md-6.col-sm-5.col-xs-5.contest-li-1 > h3')[0].text.strip(
            )
        url = info.cssselect('div.contest-par > a')[0].attrib['href'].strip()
        description = name

        deadline = None
        start_time = None

        reward = info.cssselect(
            'div.col-md-2.col-sm-2.col-xs-3.text-center.contest-li > strong'
        )[0].text.strip()

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
