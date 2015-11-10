# encoding: utf-8

import urllib
import json
import sys

reload(sys)
sys.setdefaultencoding('utf8')


class PersonSearcher:

    def __init__(self):
        self.topic_list = [
            'Data Mining',
            'Machine Learning',
            'Social Network',
            'Computer Vision',
            'Deep Learning',
            'Database',
            'Graphitisation',
            'Signal Processing',
            'INTERACTION',
            'Parallel Computability'
        ]

    @classmethod
    def get_url_from_topic(cls, topic):
        return 'https://api.aminer.org/api/search/person?as_h_index=10-20&query=%s&size=100&sort=relevance' % str(topic).replace(' ', '+')

    @classmethod
    def get_name_list_from_topic(cls, topic):
        ans_list = []
        url = cls.get_url_from_topic(topic)
        content = urllib.urlopen(url).read()
        person_dict = json.loads(content)
        print len(person_dict['result'])
        for result in person_dict['result']:
            ans_list.append(result['name'])
        return ans_list


if __name__ == '__main__':
    searcher = PersonSearcher()
    name_list = []
    for topic in searcher.topic_list:
        name_list += searcher.get_name_list_from_topic(topic)
    name_list = list(set(name_list))
    with open('normal_name_list.txt', 'w') as normal_name_list_file:
        for name in name_list:
            normal_name_list_file.write(str(name) + '\n')