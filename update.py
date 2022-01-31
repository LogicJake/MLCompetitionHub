import importlib
import pkgutil
import sys
import traceback
from datetime import datetime, timedelta

from dotenv import load_dotenv
from jinja2 import Environment, PackageLoader

# 真机运行时加载环境变量
load_dotenv()

# 获取任务模式
args = sys.argv
if len(args) == 1:
    mode = 'update_code'
else:
    mode = sys.argv[1]
mode_actions = []

if mode not in ['schedule', 'update_code', 'manual']:
    print('mode 错误')
    exit()

# 定时更新，先更新主体，再更新新增，最后才能更新 urls.txt（zlink）
if mode == 'schedule':
    mode_actions = [
        'json_main', 'markdown_main', 'rss', 'json_new', 'markdown_new',
        'mail', 'zlink'
    ]
# 更新代码，只更新主体，不更新新上线，不发送邮件
elif mode == 'update_code':
    mode_actions = ['json_main', 'markdown_main', 'rss']
# 手动更新，需先删除 urls.txt 新增的比赛网址，不发送邮件
elif mode == 'manual':
    mode_actions = [
        'json_main', 'markdown_main', 'rss', 'json_new', 'markdown_new',
        'zlink'
    ]

# 获取数据
datas = []
competitions = []

for _, module_name, _ in pkgutil.iter_modules(['source']):
    # if module_name not in ['tianchi']:
    #     continue
    '''
    死亡时间:
    dianshi: 2021.12.17 点石竞赛平台error page
    turingtopia: 2022.1.31 图灵联邦无法访问此网站
    '''
    if module_name in [
            'futurelab', 'flyai', 'huaweicloud', 'dianshi', 'turingtopia'
    ]:
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

    except Exception as e:
        print(module_name)
        print(e)

# 数据渲染
for module_name in mode_actions:
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
