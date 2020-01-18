from source import kaggle

text = ''

text += kaggle.update()

# 写入到文件
with open('README.md', 'w') as f:
    f.write(text)
