import importlib
import pkgutil
import traceback

# 一、获取数据
datas = []

for _, module_name, _ in pkgutil.iter_modules(['source']):
    try:
        module = importlib.import_module('.' + module_name, 'source')
        func_data = getattr(module, 'get_data')
        datas.append(func_data())

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
