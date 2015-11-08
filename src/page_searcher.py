# encoding: utf-8

import os
import random
import time

from src.search_helper.search_helper import GoogleHelper
from my_test import MyTest


class PageSearcher:

    def __init__(self):
        self.names = []
        self.ok_name_list = []
        self.error_name_list = []

    def get_google_page_from(self, person_name, search_helper):
        name = person_name.replace('\n', '')
        print '******', name, '*******'
        personal_path = search_helper.__RESULT_DIR_PATH__ + name + '/'
        # 建立搜索引擎文件夹
        if not os.path.exists(search_helper.__RESULT_DIR_PATH__):
            os.mkdir(search_helper.__RESULT_DIR_PATH__)
        # 建立每个人的文件夹
        if not os.path.exists(personal_path):
            os.mkdir(personal_path)
        # 打开文件
        content_file = open(personal_path + 'content.txt', 'w')
        search_page_cache_file = open(personal_path + 'search_page.html', 'w')
        try:
            # 获取搜索主页，并保存在个人文件夹下
            search_page_content = search_helper.get_search_page_by_name(name + ' email')
            if search_page_content is None:
                self.error_name_list.append(name)
                print '[Error]@EmailSearcher.get_google_page_from(): search_page_content is None'
                with open('missing_name.txt', 'w') as missing_name_file:
                    for missing_name in searcher.error_name_list:
                        missing_name_file.write(str(missing_name) + '\n')
                return False
            search_page_cache_file.write(search_page_content)
            search_page_cache_file.close()
            self.ok_name_list.append(name)
            print name, 'OK...'
            with open('ok_name.txt', 'a') as ok_name_file:
                ok_name_file.write(str(name) + '\n')

        except Exception as e:
            print e
            self.error_name_list.append(name)
            with open('missing_name.txt', 'w') as missing_name_file:
                for missing_name in searcher.error_name_list:
                    missing_name_file.write(str(missing_name) + '\n')
            return False
        finally:
            content_file.close()
        return True

    def start_from(self, start_name):
        flag = False
        test_case = MyTest()
        people_list = test_case.get_test_people_list('citation_top_1000.json')
        try:
            for person in people_list:
                if person.name == start_name:
                    flag = True
                    print 'starting from', start_name
                if not flag:
                    continue
                searcher.get_google_page_from(str(person.name), GoogleHelper())
                time.sleep(random.randint(1, 4))
        except Exception as e:
            print e

    def refresh_empty_pages(self):
        google_result_path = '../google_result/'
        for person_name in os.listdir(google_result_path):
            try:
                with open(google_result_path + person_name + '/search_page.html') as search_page:
                    if len(search_page.read()) < 10:
                        self.get_google_page_from(person_name, GoogleHelper())
            except Exception as e:
                print e


if __name__ == '__main__':
    searcher = PageSearcher()
    # searcher.start_from('Warren Gish')
    searcher.refresh_empty_pages()
