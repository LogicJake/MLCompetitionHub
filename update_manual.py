import importlib
import pkgutil
import traceback

from dotenv import load_dotenv

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
for _, module_name, _ in pkgutil.iter_modules(['actions_schedule']):
    if module_name not in ['utils', 'mail']:
        try:
            module = importlib.import_module('.' + module_name,
                                             'actions_schedule')
            func_generate = getattr(module, 'generate')
            func_generate(datas)

        except Exception:
            print(module_name)
            traceback.print_exc()
