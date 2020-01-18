from source import kaggle, turingtopia

text = ''

text += kaggle.update()
text += turingtopia.update()

# 写入到文件
with open('README.md', 'w') as f:
    f.write(text)
