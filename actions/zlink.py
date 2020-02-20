def generate(datas):

    urls = []
    for data in datas:
        for c in data['competitions']:
            url = c['url'] + '\n'
            urls.append(url)

    with open('urls.txt', 'w') as f:
        f.writelines(urls)
