# encoding: utf-8

import urllib2
import random
import urllib
import socket
import time

from src.search_helper.search_helper import *
from src.search_helper.web_helper import WebHelper


class PageSearcher:

    def __init__(self):
        self.names = []

    def get_google_page_from(self, person_name):
        pass

    def run(self, filename, search_helper):
        # 得到待搜索的名字列表
        self.names = open(filename).readlines()

        for name in self.names:
            name = name.replace('\n', '')
            print '******', name, '*******'
            personal_path = search_helper.__RESULT_DIR_PATH__ + name + '/'
            # 建立搜索引擎文件夹
            if not os.path.exists(search_helper.__RESULT_DIR_PATH__):
                os.mkdir(search_helper.__RESULT_DIR_PATH__)
            # 建立每个人的文件夹
            if not os.path.exists(personal_path):
                os.mkdir(personal_path)
            # 建立个人文件夹/结果页面文件夹
            personal_pages_path = personal_path + 'pages/'
            if not os.path.exists(personal_pages_path):
                os.mkdir(personal_pages_path)
            # 打开文件
            content_file = open(personal_path + 'content.txt', 'w')
            # search_page_cache_file = open(personal_path + 'search_page.html', 'w')
            try:
                # # 获取搜索主页，并保存在个人文件夹下
                # search_page_content = search_helper.get_search_page_by_name(name + ' email')
                # if search_page_content is None:
                #     print '[Error]@EmailSearcher.run(): search_page_content is None'
                #     continue
                # search_page_cache_file.write(search_page_content)
                # search_page_cache_file.close()

                # 获取搜索结果列表
                search_page_content = open(personal_path + 'search_page.html').read()
                title_url_dict = search_helper.get_items_from_search_page(search_page_content)
                print title_url_dict
                # 对每条搜索结果：保存html内容并分析
                for title, url in title_url_dict:
                    try:
                        # 获取页面html
                        page_content = WebHelper.get_page_content_from_url(url)
                        if page_content is None:
                            continue
                        # 保存页面html
                        page_file = open(personal_pages_path + title + '.html', 'w')
                        page_file.write(page_content)

                        # # 分析抽取email列表
                        # self.mailParser.feed(page_content)
                        # email_list = list(set(self.mailParser.get_email_list()))
                        # # 保存email列表
                        # for email in email_list:
                        #     content_file.write(email + '\n')
                    except urllib2.HTTPError:
                        print '[Error]@EmailSearcher.run():', url
                        continue
                    finally:
                        pass
            except Exception as e:
                print e
            finally:
                time.sleep(2)
                content_file.close()
                # search_page_cache_file.close()
                print name, 'OK...'


if __name__ == '__main__':
    searcher = PageSearcher()
    # searcher.run('../resource/names.list', GoogleHelper())
    searcher.get_google_page_from('wave')