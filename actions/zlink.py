def generate(datas):
    # 增量式更新
    try:
        with open('urls.txt', 'r') as f:
            urls = f.readlines()
    except Exception:
        urls = []

    urls = [url.strip() for url in urls]

    for data in datas:
        for c in data['competitions']:
            url = c['url']
            if url not in urls:
                urls.append(url)

    urls = [url + '\n' for url in urls]

    with open('urls.txt', 'w') as f:
        f.writelines(urls)
