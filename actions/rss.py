from datetime import datetime, timedelta

from jinja2 import Environment, PackageLoader


def generate(datas):
    env = Environment(loader=PackageLoader('actions'))

    update = datetime.utcnow() + timedelta(hours=8)
    update = update.strftime('%Y-%m-%dT%H:%M:%S+0800')

    # 生成 RSS
    template = env.get_template('rss.j2')
    content = template.render(datas=datas, update=update)

    with open('rss.atom', 'w') as f:
        f.write(content)
