import traceback

from source import kaggle, tianchi, turingtopia, dcjingsai

text = '一站式显示各大数据竞赛平台正在进行的比赛，每天 21:00 UTC（北京时间早上5点）更新。  \n'

try:
    text += kaggle.update()
except Exception:
    traceback.print_exc()

try:
    text += turingtopia.update()
except Exception:
    traceback.print_exc()

try:
    text += tianchi.update()
except Exception:
    traceback.print_exc()

try:
    text += dcjingsai.update()
except Exception:
    traceback.print_exc()

# 写入到文件
with open('README.md', 'w') as f:
    f.write(text)
