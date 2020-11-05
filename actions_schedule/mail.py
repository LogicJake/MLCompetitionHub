import copy
import os
import smtplib
from email.header import Header
from email.mime.text import MIMEText

from jinja2 import Environment, PackageLoader

STANDARD_TIME_FORMAT = '%Y-%m-%dT%H:%M:%S+08:00'


def generate(datas_):
    """
    Generate an ascii file

    Args:
        datas_: (str): write your description
    """
    datas = copy.deepcopy(datas_)

    try:
        with open('urls.txt', 'r') as f:
            urls = f.readlines()
    except Exception:
        urls = []

    urls = [url.strip() for url in urls]

    new_datas = []

    for data in datas:
        competitions = []

        for c in data['competitions']:
            start_time = c['start_time']
            deadline = c['deadline']
            url = c['url']

            # 加入到发送列表
            if url not in urls:
                # 转为标准时间格式字符串
                if start_time is None:
                    start_time = '未给出具体时间'
                else:
                    start_time = start_time.strftime(STANDARD_TIME_FORMAT)

                if deadline is None:
                    deadline = '未给出具体时间'
                else:
                    deadline = deadline.strftime(STANDARD_TIME_FORMAT)

                cp = {
                    'name': c['name'],
                    'url': url,
                    'description': c['description'],
                    'deadline': deadline,
                    'reward': c['reward'],
                    'start_time': start_time,
                }
                competitions.append(cp)

        if len(competitions) != 0:
            cp = {}
            cp['name'] = data['name']
            cp['competitions'] = competitions
            new_datas.append(cp)

    if len(new_datas) == 0:
        return

    env = Environment(loader=PackageLoader('actions_schedule'))
    template = env.get_template('mail.j2')
    content = template.render(datas=new_datas)
    content = content.strip()

    mail_server = os.environ.get('mail_server')
    mail_port = os.environ.get('mail_port')
    mail_username = os.environ.get('mail_username')
    mail_password = os.environ.get('mail_password')
    mail_sender = os.environ.get('mail_sender')

    with open('mails.txt', 'r') as f:
        receivers = f.readlines()
    receivers = [receiver.strip() for receiver in receivers]
    receivers = [mail_sender] + receivers

    message = MIMEText(content, 'html', 'utf-8')
    message['From'] = mail_sender
    message['To'] = ','.join(receivers)
    message['Subject'] = Header('MLCompetitionHub: 有新的比赛了！', 'utf-8')

    smtpObj = smtplib.SMTP_SSL(mail_server, mail_port)
    smtpObj.login(mail_username, mail_password)
    smtpObj.sendmail(mail_sender, receivers, message.as_string())
