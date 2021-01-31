import copy
import json

STANDARD_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+08:00'


def generate(datas_):
    datas = copy.deepcopy(datas_)

    try:
        with open('urls.txt', 'r') as f:
            urls = f.readlines()
    except Exception:
        urls = []

    urls = [url.strip() for url in urls]
    new_competitions = []

    # 信息汇总
    for data in datas:
        for c in data['competitions']:
            start_time = c['start_time']
            deadline = c['deadline']
            url = c['url']

            # 转为标准时间格式字符串
            if start_time is None:
                start_time = '未给出具体时间'
            else:
                start_time = start_time.strftime(STANDARD_TIME_FORMAT)

            if deadline is None:
                deadline = '未给出具体时间'
            else:
                deadline = deadline.strftime(STANDARD_TIME_FORMAT)

            c['start_time'] = start_time
            c['deadline'] = deadline

            if url not in urls:
                new_competitions.append(c)

    with open('docs/new.json', 'w') as f:
        f.write(json.dumps(new_competitions, ensure_ascii=False))
