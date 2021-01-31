import copy
from datetime import datetime, timedelta

from jinja2 import Environment, PackageLoader

STANDARD_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+0800'
MAX_INTERVAL_DAY = 7


def generate(datas_):
    datas = copy.deepcopy(datas_)

    try:
        with open('urls.txt', 'r') as f:
            urls = f.readlines()
    except Exception:
        urls = []

    urls = [url.strip() for url in urls]
    new_competitions = []

    for data in datas:
        for c in data['competitions']:
            start_time = c['start_time']
            deadline = c['deadline']
            url = c['url']

            # 转为标准时间格式字符串
            if start_time is None:
                start_time = '未给出具体时间'
            else:
                start_time = start_time.strftime(STANDARD_TIME_FORMAT)

            if deadline is None:
                deadline = '未给出具体时间'
            else:
                deadline = deadline.strftime(STANDARD_TIME_FORMAT)

            c['start_time'] = start_time
            c['deadline'] = deadline

            if url not in urls:
                new_competitions.append(c)

    update = datetime.utcnow() + timedelta(hours=8)
    update = update.strftime(STANDARD_TIME_FORMAT)

    env = Environment(loader=PackageLoader('actions'))
    template = env.get_template('md_nc.j2')
    content = template.render(update=update, competitions=new_competitions)
    with open('docs/new_competition.md', 'w') as f:
        f.write(content)
