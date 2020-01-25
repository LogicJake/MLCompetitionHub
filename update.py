import traceback

from jinja2 import Environment, PackageLoader

from source import dcjingsai, kaggle, tianchi, turingtopia

# 获取数据
datas = []

try:
    datas.append(kaggle.get_data())
except Exception:
    traceback.print_exc()

try:
    datas.append(turingtopia.get_data())
except Exception:
    traceback.print_exc()

try:
    datas.append(tianchi.get_data())
except Exception:
    traceback.print_exc()

try:
    datas.append(dcjingsai.get_data())
except Exception:
    traceback.print_exc()

# 生成 README.md
env = Environment(loader=PackageLoader('source'))
template = env.get_template('main.j2')
content = template.render(datas=datas)

with open('README.md', 'w') as f:
    f.write(content)
