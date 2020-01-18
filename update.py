from source import kaggle, turingtopia, tianchi

text = '一站式显示各大数据竞赛平台正在进行的比赛，每天 21:00 UTC（北京时间早上5点）更新。  \n'

text += kaggle.update()
text += turingtopia.update()
text += tianchi.update()

# 写入到文件
with open('README.md', 'w') as f:
    f.write(text)
