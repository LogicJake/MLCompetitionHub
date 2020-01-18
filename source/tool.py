def data2md(data):
    text = '# {}  \n'.format(data['name'])

    for competition in data['competitions']:
        text += '## [{}]({})  \n'.format(competition['name'],
                                         competition['url'])
        text += '### Description  \n{}  \n'.format(competition['description'])
        text += '### Deadline: {}  \n'.format(competition['deadline'])
        text += '### Reward: {}  \n  \n'.format(competition['reward'])

    return text
