import importlib
import pkgutil
import traceback
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader

# 真机运行时加载环境变量
load_dotenv()

competitions = []

# 一、获取数据
datas = []

for _, module_name, _ in pkgutil.iter_modules(['source']):
    if module_name in ['futurelab']:
        continue

    try:
        module = importlib.import_module('.' + module_name, 'source')
        func_data = getattr(module, 'get_data')
        data = func_data()
        datas.append(data)

        if ' ' in data['name']:
            link = data['name'].replace(' ', '_')
        else:
            link = data['name']
        competitions.append({'name': data['name'], 'link': link})

    except Exception:
        print(module_name)
        traceback.print_exc()

# 二、数据渲染
for _, module_name, _ in pkgutil.iter_modules(['actions']):
    if module_name not in ['utils']:
        try:
            module = importlib.import_module('.' + module_name, 'actions')
            func_generate = getattr(module, 'generate')
            func_generate(datas)

        except Exception:
            print(module_name)
            traceback.print_exc()

# 三、页面配置
env = Environment(loader=PackageLoader('actions'))
template = env.get_template('sidebar.j2')
content = template.render(competitions=competitions)
content = content.replace('\n\n', '\n')
with open('docs/_sidebar.md', 'w') as f:
    f.write(content)

template = env.get_template('competition_rm.j2')
content = template.render(competitions=competitions)
content = content.replace('\n\n', '\n')
with open('docs/competition/README.md', 'w') as f:
    f.write(content)

STANDARD_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+0800'
update = datetime.utcnow() + timedelta(hours=8)
update = update.strftime(STANDARD_TIME_FORMAT)
template = env.get_template('cover.j2')
content = template.render(update=update)
with open('docs/_coverpage.md', 'w') as f:
    f.write(content)
