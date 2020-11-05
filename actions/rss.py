import copy
from datetime import datetime, timedelta
from xml.sax.saxutils import escape

from jinja2 import Environment, PackageLoader

STANDARD_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+08:00'


def generate(datas_):
    """
    Generate the report

    Args:
        datas_: (str): write your description
    """
    datas = copy.deepcopy(datas_)

    for data in datas:
        for c in data['competitions']:
            start_time = c['start_time']
            deadline = c['deadline']
            description = c['description']
            reward = c['reward']

            # 转为标准时间格式字符串
            if start_time is None:
                start_time = '未给出具体时间'
            else:
                start_time = start_time.strftime(STANDARD_TIME_FORMAT)

            if deadline is None:
                deadline = '未给出具体时间'
            else:
                deadline = deadline.strftime(STANDARD_TIME_FORMAT)

            content = '<h3>Description</h3>{}<h3>Deadline: {}</h3><h3>Reward: {}</h3>'.format(
                escape(description), deadline, reward)
            c['start_time'] = start_time
            c['deadline'] = deadline
            c['content'] = content
            c['name'] = escape(c['name'])
            c['description'] = escape(c['description'])
            c['url'] = escape(c['url'])

    update = datetime.utcnow() + timedelta(hours=8)
    update = update.strftime(STANDARD_TIME_FORMAT)

    # 生成 RSS
    env = Environment(loader=PackageLoader('actions'))
    template = env.get_template('rss.j2')
    content = template.render(datas=datas, update=update)

    with open('docs/rss.xml', 'w') as f:
        f.write(content)
